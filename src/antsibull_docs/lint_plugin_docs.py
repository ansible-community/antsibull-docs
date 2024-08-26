# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Lint plugin docs."""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import tempfile
import typing as t
from collections.abc import Mapping, Sequence

from antsibull_core.subprocess_util import log_run
from antsibull_core.vendored.json_utils import _filter_non_json_lines
from antsibull_core.venv import FakeVenvRunner
from antsibull_docs_parser import dom
from antsibull_docs_parser.parser import Context as ParserContext
from antsibull_docs_parser.parser import parse as parse_markup
from jinja2 import Template

from sphinx_antsibull_ext import directives as antsibull_directives
from sphinx_antsibull_ext import roles as antsibull_roles

from .augment_docs import augment_docs
from .collection_links import load_collections_links
from .docs_parsing import AnsibleCollectionMetadata
from .docs_parsing.ansible_doc import parse_ansible_galaxy_collection_list
from .docs_parsing.parsing import get_ansible_plugin_info
from .docs_parsing.routing import (
    CollectionRoutingT,
    load_all_collection_routing,
    remove_redirect_duplicates,
)
from .jinja2.environment import OutputFormat, doc_environment
from .lint_helpers import load_collection_info
from .markup.semantic_helper import split_option_like_name
from .plugin_docs import walk_plugin_docs_texts
from .process_docs import (
    get_collection_contents,
    get_plugin_contents,
    normalize_all_plugin_info,
)
from .rstcheck import check_rst_content
from .schemas.collection_links import CollectionLinks
from .utils.collection_name_transformer import CollectionNameTransformer
from .write_docs import BasicPluginInfo, PluginErrorsT
from .write_docs.plugins import (
    create_plugin_rst,
    guess_relative_filename,
    has_broken_docs,
)

ValidCollectionRefs = t.Literal["self", "dependent", "all"]


class CollectionCopier:
    dir: str | None

    def __init__(self):
        self.dir = None

    def __enter__(self):
        if self.dir is not None:
            raise AssertionError("Collection copier already initialized")
        self.dir = os.path.realpath(tempfile.mkdtemp(prefix="antsibull-docs-"))
        return self

    def add_collection(
        self, collecion_source_path: str, namespace: str, name: str
    ) -> None:
        self_dir = self.dir
        if self_dir is None:
            raise AssertionError("Collection copier not initialized")
        collection_container_dir = os.path.join(
            self_dir, "ansible_collections", namespace
        )
        os.makedirs(collection_container_dir, exist_ok=True)

        collection_dir = os.path.join(collection_container_dir, name)
        shutil.copytree(collecion_source_path, collection_dir, symlinks=True)

    def __exit__(self, type_, value, traceback_):
        self_dir = self.dir
        if self_dir is None:
            raise AssertionError("Collection copier not initialized")
        shutil.rmtree(self_dir, ignore_errors=True)
        self.dir = None


def _call_ansible_galaxy_collection_list() -> t.Mapping[str, t.Any]:
    p = log_run(["ansible-galaxy", "collection", "list", "--format", "json"])
    return json.loads(_filter_non_json_lines(p.stdout)[0])


class CollectionFinder:
    def __init__(self):
        self.collections = {}
        data = _call_ansible_galaxy_collection_list()
        for namespace, name, path, _ in reversed(
            parse_ansible_galaxy_collection_list(data)
        ):
            self.collections[f"{namespace}.{name}"] = path

    def find(self, namespace, name):
        return self.collections.get(f"{namespace}.{name}")


_CLASSICAL_MARKUP = (
    dom.PartType.BOLD,
    dom.PartType.CODE,
    dom.PartType.ERROR,  # not really markup, but having it here makes code simpler
    dom.PartType.HORIZONTAL_LINE,
    dom.PartType.ITALIC,
    dom.PartType.LINK,
    dom.PartType.MODULE,
    dom.PartType.RST_REF,
    dom.PartType.URL,
    dom.PartType.TEXT,
)


_NAME_SEPARATOR = "/"
_ROLE_ENTRYPOINT_SEPARATOR = "###"


def _get_fqcn_collection_name(fqcn: str) -> str:
    return ".".join(fqcn.split(".")[:2])


def _get_fqcn_collection_prefix(fqcn: str) -> str:
    return _get_fqcn_collection_name(fqcn) + "."


class _NameCollector:
    _plugins: set[tuple[str, str]]
    _option_names: dict[tuple[str, str, str], str]
    _return_value_names: dict[tuple[str, str, str], str]
    _collection_prefixes: set[str]
    _collection_routing: CollectionRoutingT
    _routing_table: dict[tuple[str, str], str]

    def _collect_role_option_names(
        self,
        plugin: tuple[str, str],
        options: dict[str, t.Any],
        entrypoint: str,
        path_prefixes: list[str],
    ) -> None:
        for opt, data in sorted(options.items()):
            names = [opt]
            if isinstance(data.get("aliases"), Sequence):
                names.extend(data["aliases"])
            paths = [
                f"{path_prefix}{name}"
                for name in names
                for path_prefix in path_prefixes
            ]
            for path in paths:
                self._option_names[
                    (*plugin, f"{entrypoint}{_ROLE_ENTRYPOINT_SEPARATOR}{path}")
                ] = data["type"]
            if "options" in data:
                self._collect_role_option_names(
                    plugin,
                    data["options"],
                    entrypoint,
                    [f"{path}{_NAME_SEPARATOR}" for path in paths],
                )

    def _collect_option_names(
        self,
        plugin: tuple[str, str],
        options: dict[str, t.Any],
        path_prefixes: list[str],
    ) -> None:
        for opt, data in sorted(options.items()):
            names = [opt]
            if isinstance(data.get("aliases"), Sequence):
                names.extend(data["aliases"])
            paths = [
                f"{path_prefix}{name}"
                for name in names
                for path_prefix in path_prefixes
            ]
            for path in paths:
                self._option_names[(*plugin, path)] = data["type"]
            if "suboptions" in data:
                self._collect_option_names(
                    plugin,
                    data["suboptions"],
                    [f"{path}{_NAME_SEPARATOR}" for path in paths],
                )

    def _collect_return_value_names(
        self, plugin: tuple[str, str], return_values: dict[str, t.Any], path_prefix: str
    ) -> None:
        for rv, data in sorted(return_values.items()):
            path = f"{path_prefix}{rv}"
            self._return_value_names[(*plugin, path)] = data["type"]
            if "contains" in data:
                self._collect_return_value_names(
                    plugin, data["contains"], f"{path}{_NAME_SEPARATOR}"
                )

    def __init__(self, collection_routing: CollectionRoutingT):
        self._plugins = set()
        self._collection_prefixes = set()
        self._option_names = {}
        self._return_value_names = {}
        self._collection_routing = collection_routing
        self._routing_table = {}

    def collect_collection(self, collection_name_or_fqcn: str):
        self._collection_prefixes.add(
            _get_fqcn_collection_prefix(collection_name_or_fqcn)
        )

    def collect_plugin(
        self, plugin_record: dict[str, t.Any], plugin_fqcn: str, plugin_type: str
    ):
        plugin = (plugin_fqcn, plugin_type)
        self._plugins.add(plugin)
        self._collection_prefixes.add(_get_fqcn_collection_prefix(plugin_fqcn))
        if "doc" in plugin_record and "options" in plugin_record["doc"]:
            self._collect_option_names(plugin, plugin_record["doc"]["options"], [""])
        if "return" in plugin_record:
            self._collect_return_value_names(plugin, plugin_record["return"], "")
        if "entry_points" in plugin_record:
            for entry_point, data in sorted(plugin_record["entry_points"].items()):
                if "options" in data:
                    self._collect_role_option_names(
                        plugin, data["options"], entry_point, [""]
                    )

    def _resolve_plugin_fqcn(self, plugin_fqcn: str, plugin_type: str) -> str:
        try:
            return self._routing_table[(plugin_fqcn, plugin_type)]
        except KeyError:
            pass
        tried_names = {plugin_fqcn}
        new_fqcn = plugin_fqcn
        while True:
            try:
                new_fqcn = self._collection_routing[plugin_type][new_fqcn]["redirect"]
            except KeyError:
                break
            if new_fqcn in tried_names:
                # Found infinite loop! Do not resolve name.
                new_fqcn = plugin_fqcn
                break
            tried_names.add(new_fqcn)
        self._routing_table[(plugin_fqcn, plugin_type)] = new_fqcn
        return new_fqcn

    def get_option_type(
        self, plugin_fqcn: str, plugin_type: str, option_name: str
    ) -> str | None:
        key = (
            self._resolve_plugin_fqcn(plugin_fqcn, plugin_type),
            plugin_type,
            option_name,
        )
        return self._option_names.get(key)

    def get_return_value_type(
        self, plugin_fqcn: str, plugin_type: str, return_value_name: str
    ) -> str | None:
        key = (
            self._resolve_plugin_fqcn(plugin_fqcn, plugin_type),
            plugin_type,
            return_value_name,
        )
        return self._return_value_names.get(key)

    def is_valid_collection(self, plugin_fqcn: str) -> bool:
        return any(
            plugin_fqcn.startswith(prefix) for prefix in self._collection_prefixes
        )

    def is_valid_plugin(self, plugin_fqcn: str, plugin_type: str) -> bool:
        return (
            self._resolve_plugin_fqcn(plugin_fqcn, plugin_type),
            plugin_type,
        ) in self._plugins

    def is_valid_option(
        self, plugin_fqcn: str, plugin_type: str, option_name: str
    ) -> bool:
        return self.get_option_type(plugin_fqcn, plugin_type, option_name) is not None

    def is_valid_return_value(
        self, plugin_fqcn: str, plugin_type: str, return_value_name: str
    ) -> bool:
        return (
            self.get_return_value_type(plugin_fqcn, plugin_type, return_value_name)
            is not None
        )


def _create_lookup(
    opt: dom.OptionNamePart | dom.ReturnValuePart, link: list[str]
) -> str:
    lookup = _NAME_SEPARATOR.join(link)
    if opt.entrypoint is not None:
        lookup = f"{opt.entrypoint}{_ROLE_ENTRYPOINT_SEPARATOR}{lookup}"
    return lookup


class _ValidationWalker(dom.NoopWalker):
    def __init__(self, markup_validator: "_MarkupValidator", key: str):
        self.markup_validator = markup_validator
        self.errors = markup_validator.errors
        self.key = key

    def _error(self, part: dom.AnyPart, message: str) -> None:
        self.errors.append(f"{self.key}: {part.source}: {message}")

    def process_error(self, part: dom.ErrorPart) -> None:
        self.errors.append(f"{self.key}: Markup error: {part.message}")

    def process_bold(self, part: dom.BoldPart) -> None:
        if not part.text:
            self._error(part, "empty markup parameter")

    def process_code(self, part: dom.CodePart) -> None:
        if not part.text:
            self._error(part, "empty markup parameter")

    def process_horizontal_line(self, part: dom.HorizontalLinePart) -> None:
        pass

    def process_italic(self, part: dom.ItalicPart) -> None:
        if not part.text:
            self._error(part, "empty markup parameter")

    def process_link(self, part: dom.LinkPart) -> None:
        if not part.text:
            self._error(part, "empty link title")
        if not part.url.strip():
            self._error(part, "empty URL")

    def process_module(self, part: dom.ModulePart) -> None:
        self.markup_validator._validate_module(  # pylint:disable=protected-access
            part, self.key
        )

    def process_rst_ref(self, part: dom.RSTRefPart) -> None:
        if not part.text:
            self._error(part, "empty reference title")
        if not part.ref.strip():
            self._error(part, "empty reference")

    def process_url(self, part: dom.URLPart) -> None:
        if not part.url.strip():
            self._error(part, "empty URL")

    def process_text(self, part: dom.TextPart) -> None:
        pass

    def process_env_variable(self, part: dom.EnvVariablePart) -> None:
        if not part.name.strip():
            self._error(part, "empty environment variable")

    def process_option_name(self, part: dom.OptionNamePart) -> None:
        if not part.name:
            self._error(part, "empty option name")
        self.markup_validator._validate_option_name(  # pylint:disable=protected-access
            part, self.key
        )

    def process_option_value(self, part: dom.OptionValuePart) -> None:
        if not part.value:
            self._error(part, "empty value")

    def process_plugin(self, part: dom.PluginPart) -> None:
        self.markup_validator._validate_plugin(  # pylint:disable=protected-access
            part, self.key
        )

    def process_return_value(self, part: dom.ReturnValuePart) -> None:
        if not part.name:
            self._error(part, "empty return value name")
        self.markup_validator._validate_return_value(  # pylint:disable=protected-access
            part, self.key
        )


class _MarkupValidator:
    errors: list[str]

    _name_collector: _NameCollector
    _current_plugin: dom.PluginIdentifier
    _collection_name_prefix: str
    _validate_collections_refs: ValidCollectionRefs
    _disallow_unknown_collection_refs: bool
    _disallow_semantic_markup: bool

    def _report_disallowed_collection(
        self, part: dom.AnyPart | None, plugin_fqcn: str, key: str
    ) -> None:
        if part:
            key = f"{key}: {part.source}"
        self.errors.append(
            f"{key}: a reference to the collection"
            f" {_get_fqcn_collection_name(plugin_fqcn)} is not allowed"
        )

    def _validate_plugin_fqcn(
        self, part: dom.AnyPart | None, plugin_fqcn: str, plugin_type: str, key: str
    ) -> bool:
        if self._validate_collections_refs == "self":
            if not plugin_fqcn.startswith(self._collection_name_prefix):
                if self._disallow_unknown_collection_refs:
                    self._report_disallowed_collection(part, plugin_fqcn, key)
                return False
        if self._name_collector.is_valid_plugin(plugin_fqcn, plugin_type):
            return True
        if self._name_collector.is_valid_collection(plugin_fqcn):
            prefix = "" if plugin_type in ("role", "module") else " plugin"
            key_prefix = f"{key}: {part.source}" if part else key
            self.errors.append(
                f"{key_prefix}: there is no {plugin_type}{prefix} {plugin_fqcn}"
            )
        elif self._disallow_unknown_collection_refs:
            self._report_disallowed_collection(part, plugin_fqcn, key)
        return False

    def _validate_option_like_name(
        self,
        key: str,
        opt: dom.OptionNamePart | dom.ReturnValuePart,
        what: t.Literal["option", "return value"],
    ):
        try:
            split_option_like_name(opt.name)
        except ValueError as exc:
            self.errors.append(
                f"{key}: {opt.source}: {what} name {opt.name!r} cannot be parsed: {exc}"
            )

    def _validate_link(
        self,
        key: str,
        opt: dom.OptionNamePart | dom.ReturnValuePart,
        what: t.Literal["option", "return value"],
        lookup: t.Callable[[str], str | None],
    ):
        try:
            name = split_option_like_name(opt.name)
        except ValueError:
            return
        link: list[str] = []
        for index, part in enumerate(name):
            link.append(part[0])
            lookup_value = _create_lookup(opt, link)
            part_type = lookup(lookup_value)
            if part_type == "list" and part[1] is None and index + 1 < len(name):
                self.errors.append(
                    f"{key}: {opt.source}: {what} name {opt.name!r} refers to"
                    f" list {'.'.join(link)} without `[]`"
                )
            if part_type not in ("list", "dict", "dictionary") and part[1] is not None:
                self.errors.append(
                    f"{key}: {opt.source}: {what} name {opt.name!r} refers to"
                    f" {'.'.join(link)} - which is neither list nor dictionary - with `[]`"
                )
            if (
                part_type in ("dict", "dictionary")
                and part[1] is not None
                and index + 1 < len(name)
            ):
                self.errors.append(
                    f"{key}: {opt.source}: {what} name {opt.name!r} refers to"
                    f" dictionary {'.'.join(link)} with `[]`, which is only allowed"
                    " for the last part"
                )

    def _validate_option_name(self, opt: dom.OptionNamePart, key: str) -> None:
        self._validate_option_like_name(key, opt, "option")
        plugin = opt.plugin
        if plugin is None:
            return
        if not self._validate_plugin_fqcn(opt, plugin.fqcn, plugin.type, key):
            return
        lookup = _create_lookup(opt, opt.link)
        if not self._name_collector.is_valid_option(plugin.fqcn, plugin.type, lookup):
            prefix = "" if plugin.type in ("role", "module") else " plugin"
            self.errors.append(
                f"{key}: {opt.source}: option name does not reference to an existing"
                f" option of the {plugin.type}{prefix} {plugin.fqcn}"
            )
            return
        self._validate_link(
            key,
            opt,
            "option",
            lambda lookup_: self._name_collector.get_option_type(
                plugin.fqcn, plugin.type, lookup_  # type: ignore[union-attr]
            ),
        )

    def _validate_return_value(self, rv: dom.ReturnValuePart, key: str) -> None:
        self._validate_option_like_name(key, rv, "return value")
        plugin = rv.plugin
        if plugin is None:
            return
        if not self._validate_plugin_fqcn(rv, plugin.fqcn, plugin.type, key):
            return
        lookup = _create_lookup(rv, rv.link)
        if not self._name_collector.is_valid_return_value(
            plugin.fqcn, plugin.type, lookup
        ):
            prefix = "" if plugin.type in ("role", "module") else " plugin"
            self.errors.append(
                f"{key}: {rv.source}: return value name does not reference to an"
                f" existing return value of the {plugin.type}{prefix} {plugin.fqcn}"
            )
            return
        self._validate_link(
            key,
            rv,
            "return value",
            lambda lookup_: self._name_collector.get_return_value_type(
                plugin.fqcn, plugin.type, lookup_  # type: ignore[union-attr]
            ),
        )

    def _validate_module(self, module: dom.ModulePart, key: str) -> None:
        self._validate_plugin_fqcn(module, module.fqcn, "module", key)

    def _validate_plugin(self, plugin: dom.PluginPart, key: str) -> None:
        self._validate_plugin_fqcn(plugin, plugin.plugin.fqcn, plugin.plugin.type, key)

    def _validate_markup_entry(
        self, entry: str, key: str, role_entrypoint: str | None = None
    ) -> None:
        context = ParserContext(
            current_plugin=self._current_plugin,
            role_entrypoint=role_entrypoint,
        )
        parsed_paragraphs = parse_markup(
            entry,
            context,
            errors="message",
            add_source=True,
            only_classic_markup=False,
        )
        for paragraph in parsed_paragraphs:
            dom.walk(paragraph, _ValidationWalker(self, key))
            if self._disallow_semantic_markup:
                for par_elem in paragraph:
                    if par_elem.type not in _CLASSICAL_MARKUP:
                        self.errors.append(
                            f"{key}: Found semantic markup: {par_elem.source}"
                        )

    def _check_seealso(self, seealso: list[t.Any], key: str):
        for index, entry in enumerate(seealso):
            if not isinstance(entry, Mapping):
                continue
            entry_key = f"{key}[{index + 1}]"
            if "module" in entry:
                self._validate_plugin_fqcn(None, entry["module"], "module", entry_key)
            if "plugin" in entry and "plugin_type" in entry:
                self._validate_plugin_fqcn(
                    None, entry["plugin"], entry["plugin_type"], entry_key
                )

    def __init__(
        self,
        name_collector: _NameCollector,
        plugin_record: dict[str, t.Any],
        plugin_fqcn: str,
        plugin_type: str,
        validate_collections_refs: ValidCollectionRefs = "self",
        disallow_unknown_collection_refs: bool = False,
        disallow_semantic_markup: bool = False,
    ):
        self.errors = []
        self._name_collector = name_collector
        self._collection_name_prefix = _get_fqcn_collection_prefix(plugin_fqcn)
        self._current_plugin = dom.PluginIdentifier(fqcn=plugin_fqcn, type=plugin_type)
        self._disallow_semantic_markup = disallow_semantic_markup
        self._validate_collections_refs = validate_collections_refs
        self._disallow_unknown_collection_refs = disallow_unknown_collection_refs

        def callback(entry: str, key: str, role_entrypoint: str | None = None) -> None:
            self._validate_markup_entry(entry, key, role_entrypoint)

        walk_plugin_docs_texts(plugin_record, callback)

        if isinstance(plugin_record.get("doc"), Mapping):
            if isinstance(plugin_record["doc"].get("seealso"), Sequence):
                self._check_seealso(
                    plugin_record["doc"]["seealso"], key="DOCUMENTATION -> seealso"
                )
        if isinstance(plugin_record.get("entry_points"), Mapping):
            for entry_point, data in sorted(plugin_record["entry_points"].items()):
                if isinstance(data.get("seealso"), Sequence):
                    self._check_seealso(
                        data["seealso"], key=f"entry_points -> {entry_point} -> seealso"
                    )


def _validate_markup(
    name_collector: _NameCollector,
    plugin_record: dict[str, t.Any],
    plugin_fqcn: str,
    plugin_type: str,
    path: str,
    validate_collections_refs: ValidCollectionRefs,
    disallow_unknown_collection_refs: bool,
    disallow_semantic_markup: bool,
) -> list[tuple[str, int, int, str]]:
    validator = _MarkupValidator(
        name_collector,
        plugin_record,
        plugin_fqcn,
        plugin_type,
        validate_collections_refs=validate_collections_refs,
        disallow_unknown_collection_refs=disallow_unknown_collection_refs,
        disallow_semantic_markup=disallow_semantic_markup,
    )
    return [(path, 0, 0, msg) for msg in validator.errors]


def _collect_names(
    new_plugin_info: Mapping[str, Mapping[str, t.Any]],
    collection_to_plugin_info: Mapping[
        str, Mapping[str, Mapping[str, BasicPluginInfo]]
    ],
    collection_name: str,
    collections: list[str],
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    validate_collections_refs: ValidCollectionRefs,
    collection_routing: CollectionRoutingT,
) -> _NameCollector:
    name_collector = _NameCollector(collection_routing)
    name_collector.collect_collection(collection_name)
    for other_collection in collection_metadata.keys():
        if validate_collections_refs != "all" and other_collection not in collections:
            continue
    for collection_name_, plugins_by_type in collection_to_plugin_info.items():
        if validate_collections_refs != "all" and collection_name_ not in collections:
            continue
        for plugin_type, plugins_dict in plugins_by_type.items():
            for plugin_short_name in plugins_dict:
                plugin_name = ".".join((collection_name_, plugin_short_name))
                plugin_record = new_plugin_info[plugin_type].get(plugin_name) or {}
                if not has_broken_docs(plugin_record, plugin_type):
                    name_collector.collect_plugin(
                        plugin_record, plugin_name, plugin_type
                    )
    return name_collector


def _lint_plugin_docs(
    result: list[tuple[str, int, int, str]],
    original_path_to_collection: str,
    name_collector: _NameCollector,
    collection_name: str,
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    link_data: Mapping[str, CollectionLinks],
    plugin_name: str,
    plugin_type: str,
    plugin_short_name: str,
    filename: str,
    plugin_record: dict[str, t.Any],
    nonfatal_errors: PluginErrorsT,
    plugin_type_tmpl: Template,
    error_tmpl: Template,
    disallow_unknown_collection_refs: bool,
    disallow_semantic_markup: bool,
    skip_rstcheck: bool,
    validate_collections_refs: ValidCollectionRefs,
):
    if has_broken_docs(plugin_record, plugin_type):
        result.append((filename, 0, 0, "Did not return correct DOCUMENTATION"))
    else:
        result.extend(
            _validate_markup(
                name_collector,
                plugin_record,
                plugin_name,
                plugin_type,
                filename,
                validate_collections_refs,
                disallow_unknown_collection_refs,
                disallow_semantic_markup,
            )
        )
    for error in nonfatal_errors[plugin_type][plugin_name]:
        result.append((filename, 0, 0, error))
    rst_content = create_plugin_rst(
        collection_name,
        collection_metadata[collection_name],
        link_data[collection_name],
        plugin_short_name,
        plugin_type,
        plugin_record,
        nonfatal_errors[plugin_type][plugin_name],
        plugin_type_tmpl,
        error_tmpl,
        use_html_blobs=False,
        log_errors=False,
    )
    if not skip_rstcheck:
        path = os.path.join(
            original_path_to_collection,
            "plugins",
            plugin_type,
            f"{plugin_short_name}.rst",
        )
        rst_results = check_rst_content(
            rst_content,
            filename=path,
            ignore_directives=["rst-class"] + list(antsibull_directives.DIRECTIVES),
            ignore_roles=list(antsibull_roles.ROLES),
        )
        result.extend(
            [(path, result[0], result[1], result[2]) for result in rst_results]
        )


def _lint_collection_plugin_docs(
    collections_dir: str | None,
    dependencies: list[str],
    collection_name: str,
    original_path_to_collection: str | None,
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    validate_collections_refs: ValidCollectionRefs,
    disallow_unknown_collection_refs: bool,
    skip_rstcheck: bool,
    disallow_semantic_markup: bool,
    output_format: OutputFormat,
) -> list[tuple[str, int, int, str]]:
    # Compile a list of collections that the collection depends on, and make
    # sure that ansible.builtin is on it
    collections = list(dependencies)
    collections.append(collection_name)
    collections.append("ansible.builtin")
    collections = sorted(set(collections))

    # Load collection docs
    venv = FakeVenvRunner()
    plugin_info, collection_metadata = asyncio.run(
        get_ansible_plugin_info(
            venv,
            collections_dir,
            collection_names=(
                [collection_name]
                if validate_collections_refs == "self"
                else collections if validate_collections_refs == "dependent" else None
            ),
            fetch_all_installed=validate_collections_refs == "all",
        )
    )
    if original_path_to_collection is None:
        original_path_to_collection = collection_metadata[collection_name].path

    # Load routing information
    collection_routing = asyncio.run(load_all_collection_routing(collection_metadata))
    # Process data
    remove_redirect_duplicates(plugin_info, collection_routing)
    new_plugin_info, nonfatal_errors = asyncio.run(
        normalize_all_plugin_info(plugin_info)
    )
    augment_docs(new_plugin_info, collection_routing)
    # Load link data
    link_data = asyncio.run(
        load_collections_links(
            {name: data.path for name, data in collection_metadata.items()}
        )
    )
    # More processing
    plugin_contents = get_plugin_contents(new_plugin_info, nonfatal_errors)
    collection_to_plugin_info = get_collection_contents(plugin_contents)
    for collection in collection_metadata:
        collection_to_plugin_info[collection]  # pylint:disable=pointless-statement
    # Compose RST files and check for errors
    # Setup the jinja environment
    env = doc_environment(
        collection_url=collection_url,
        collection_install=collection_install,
        referable_envvars=None,  # this shouldn't make a difference for validation
        output_format=output_format,
    )
    # Get the templates
    plugin_tmpl = env.get_template("plugin.rst.j2")
    role_tmpl = env.get_template("role.rst.j2")
    error_tmpl = env.get_template("plugin-error.rst.j2")
    # Collect all option and return value names
    name_collector = _collect_names(
        new_plugin_info,
        collection_to_plugin_info,
        collection_name,
        collections,
        collection_metadata,
        validate_collections_refs,
        collection_routing,
    )

    result: list[tuple[str, int, int, str]] = []
    for collection_name_, plugins_by_type in collection_to_plugin_info.items():
        if collection_name_ != collection_name:
            continue
        for plugin_type, plugins_dict in plugins_by_type.items():
            plugin_type_tmpl = plugin_tmpl
            if plugin_type == "role":
                plugin_type_tmpl = role_tmpl
            for plugin_short_name, dummy_ in plugins_dict.items():
                plugin_name = ".".join((collection_name_, plugin_short_name))
                plugin_record = new_plugin_info[plugin_type].get(plugin_name) or {}
                filename = os.path.join(
                    original_path_to_collection,
                    guess_relative_filename(
                        plugin_record,
                        plugin_short_name,
                        plugin_type,
                        collection_name_,
                        collection_metadata[collection_name_],
                    ),
                )
                _lint_plugin_docs(
                    result,
                    original_path_to_collection,
                    name_collector,
                    collection_name_,
                    collection_metadata,
                    link_data,
                    plugin_name,
                    plugin_type,
                    plugin_short_name,
                    filename,
                    plugin_record,
                    nonfatal_errors,
                    plugin_type_tmpl,
                    error_tmpl,
                    disallow_unknown_collection_refs,
                    disallow_semantic_markup,
                    skip_rstcheck,
                    validate_collections_refs,
                )
    return result


def lint_collection_plugin_docs(
    path_to_collection: str,
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    validate_collections_refs: ValidCollectionRefs = "self",
    disallow_unknown_collection_refs: bool = False,
    skip_rstcheck: bool = False,
    disallow_semantic_markup: bool = False,
    output_format: OutputFormat = OutputFormat.ANSIBLE_DOCSITE,
) -> list[tuple[str, int, int, str]]:
    try:
        info = load_collection_info(path_to_collection)
        namespace = info["namespace"]
        name = info["name"]
        dependencies = info.get("dependencies") or {}
    except Exception:  # pylint:disable=broad-except
        return [
            (
                path_to_collection,
                0,
                0,
                "Cannot identify collection with galaxy.yml or MANIFEST.json at this path",
            )
        ]
    result = []
    collection_name = f"{namespace}.{name}"
    done_dependencies = {collection_name}
    dependencies = sorted(dependencies)
    with CollectionCopier() as copier:
        # Copy collection
        copier.add_collection(path_to_collection, namespace, name)
        # Copy all dependencies
        if dependencies and validate_collections_refs != "all":
            collection_finder = CollectionFinder()
            while dependencies:
                dependency = dependencies.pop(0)
                if dependency in done_dependencies:
                    continue
                done_dependencies.add(dependency)
                dep_namespace, dep_name = dependency.split(".", 2)
                dep_collection_path = collection_finder.find(dep_namespace, dep_name)
                if dep_collection_path:
                    copier.add_collection(dep_collection_path, dep_namespace, dep_name)
                    try:
                        info = load_collection_info(dep_collection_path)
                        dependencies.extend(sorted(info.get("dependencies") or {}))
                    except Exception:  # pylint:disable=broad-except
                        result.append(
                            (
                                dep_collection_path,
                                0,
                                0,
                                "Cannot identify collection with galaxy.yml or MANIFEST.json"
                                " at this path",
                            )
                        )
        # Load docs
        result.extend(
            _lint_collection_plugin_docs(
                copier.dir,
                sorted(done_dependencies),
                collection_name,
                path_to_collection,
                collection_url=collection_url,
                collection_install=collection_install,
                validate_collections_refs=validate_collections_refs,
                disallow_unknown_collection_refs=disallow_unknown_collection_refs,
                skip_rstcheck=skip_rstcheck,
                disallow_semantic_markup=disallow_semantic_markup,
                output_format=output_format,
            )
        )
    return result


def lint_core_plugin_docs(
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    validate_collections_refs: ValidCollectionRefs = "self",
    disallow_unknown_collection_refs: bool = False,
) -> list[tuple[str, int, int, str]]:
    result = _lint_collection_plugin_docs(
        None,
        ["ansible.builtin"],
        "ansible.builtin",
        None,
        collection_url=collection_url,
        collection_install=collection_install,
        validate_collections_refs=validate_collections_refs,
        disallow_unknown_collection_refs=disallow_unknown_collection_refs,
        skip_rstcheck=True,
        disallow_semantic_markup=False,
        output_format=OutputFormat.ANSIBLE_DOCSITE,
    )
    return result
