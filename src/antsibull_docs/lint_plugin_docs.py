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

from sphinx_antsibull_ext import roles as antsibull_roles

from .augment_docs import augment_docs
from .collection_links import load_collections_links
from .docs_parsing import AnsibleCollectionMetadata
from .docs_parsing.ansible_doc import parse_ansible_galaxy_collection_list
from .docs_parsing.parsing import get_ansible_plugin_info
from .docs_parsing.routing import (
    load_all_collection_routing,
    remove_redirect_duplicates,
)
from .jinja2.environment import doc_environment
from .lint_helpers import load_collection_info
from .plugin_docs import walk_plugin_docs_texts
from .process_docs import (
    get_collection_contents,
    get_plugin_contents,
    normalize_all_plugin_info,
)
from .rstcheck import check_rst_content
from .utils.collection_name_transformer import CollectionNameTransformer
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

    def __init__(self):
        self._plugins = set()
        self._collection_prefixes = set()
        self._option_names = {}
        self._return_value_names = {}

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

    def get_option_type(
        self, plugin_fqcn: str, plugin_type: str, option_name: str
    ) -> str | None:
        key = (plugin_fqcn, plugin_type, option_name)
        return self._option_names.get(key)

    def get_return_value_type(
        self, plugin_fqcn: str, plugin_type: str, return_value_name: str
    ) -> str | None:
        key = (plugin_fqcn, plugin_type, return_value_name)
        return self._return_value_names.get(key)

    def is_valid_collection(self, plugin_fqcn: str) -> bool:
        return any(
            plugin_fqcn.startswith(prefix) for prefix in self._collection_prefixes
        )

    def is_valid_plugin(self, plugin_fqcn: str, plugin_type: str) -> bool:
        return (plugin_fqcn, plugin_type) in self._plugins

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


class _MarkupValidator:
    errors: list[str]

    _name_collector: _NameCollector
    _current_plugin: dom.PluginIdentifier
    _collection_name_prefix: str
    _validate_collections_refs: ValidCollectionRefs
    _disallow_unknown_collection_refs: bool
    _disallow_semantic_markup: bool

    def _report_disallowed_collection(
        self, part: dom.AnyPart, plugin_fqcn: str, key: str
    ) -> None:
        self.errors.append(
            f"{key}: {part.source}: a reference to the collection"
            f" {_get_fqcn_collection_name(plugin_fqcn)} is not allowed"
        )

    def _validate_plugin_fqcn(
        self, part: dom.AnyPart, plugin_fqcn: str, plugin_type: str, key: str
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
            self.errors.append(
                f"{key}: {part.source}: there is no {plugin_type}{prefix} {plugin_fqcn}"
            )
        elif self._disallow_unknown_collection_refs:
            self._report_disallowed_collection(part, plugin_fqcn, key)
        return False

    def _validate_option_name(self, opt: dom.OptionNamePart, key: str) -> None:
        plugin = opt.plugin
        if plugin is None:
            return
        if not self._validate_plugin_fqcn(opt, plugin.fqcn, plugin.type, key):
            return
        lookup = _NAME_SEPARATOR.join(opt.link)
        if opt.entrypoint is not None:
            lookup = f"{opt.entrypoint}{_ROLE_ENTRYPOINT_SEPARATOR}{lookup}"
        if not self._name_collector.is_valid_option(plugin.fqcn, plugin.type, lookup):
            prefix = "" if plugin.type in ("role", "module") else " plugin"
            self.errors.append(
                f"{key}: {opt.source}: option name does not reference to an existing"
                f" option of the {plugin.type}{prefix} {plugin.fqcn}"
            )

    def _validate_return_value(self, rv: dom.ReturnValuePart, key: str) -> None:
        plugin = rv.plugin
        if plugin is None:
            return
        if not self._validate_plugin_fqcn(rv, plugin.fqcn, plugin.type, key):
            return
        lookup = _NAME_SEPARATOR.join(rv.link)
        if rv.entrypoint is not None:
            lookup = f"{rv.entrypoint}{_ROLE_ENTRYPOINT_SEPARATOR}{lookup}"
        if not self._name_collector.is_valid_return_value(
            plugin.fqcn, plugin.type, lookup
        ):
            prefix = "" if plugin.type in ("role", "module") else " plugin"
            self.errors.append(
                f"{key}: {rv.source}: return value name does not reference to an"
                f" existing return value of the {plugin.type}{prefix} {plugin.fqcn}"
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
            for par_elem in paragraph:
                if par_elem.type == dom.PartType.ERROR:
                    error_elem = t.cast(dom.ErrorPart, par_elem)
                    self.errors.append(f"{key}: Markup error: {error_elem.message}")
                if (
                    self._disallow_semantic_markup
                    and par_elem.type not in _CLASSICAL_MARKUP
                ):
                    self.errors.append(
                        f"{key}: Found semantic markup: {par_elem.source}"
                    )
                if par_elem.type == dom.PartType.OPTION_NAME:
                    self._validate_option_name(
                        t.cast(dom.OptionNamePart, par_elem), key
                    )
                if par_elem.type == dom.PartType.RETURN_VALUE:
                    self._validate_return_value(
                        t.cast(dom.ReturnValuePart, par_elem), key
                    )
                if par_elem.type == dom.PartType.MODULE:
                    self._validate_module(t.cast(dom.ModulePart, par_elem), key)
                if par_elem.type == dom.PartType.PLUGIN:
                    self._validate_plugin(t.cast(dom.PluginPart, par_elem), key)

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
    collection_to_plugin_info: Mapping[str, Mapping[str, Mapping[str, str]]],
    collection_name: str,
    collections: list[str],
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    validate_collections_refs: ValidCollectionRefs,
) -> _NameCollector:
    name_collector = _NameCollector()
    name_collector.collect_collection(collection_name)
    for other_collection in collection_metadata.keys():
        if validate_collections_refs != "all" and other_collection not in collections:
            continue
    for collection_name_, plugins_by_type in collection_to_plugin_info.items():
        if validate_collections_refs != "all" and collection_name_ not in collections:
            continue
        for plugin_type, plugins_dict in plugins_by_type.items():
            for plugin_short_name, dummy_ in plugins_dict.items():
                plugin_name = ".".join((collection_name_, plugin_short_name))
                plugin_record = new_plugin_info[plugin_type].get(plugin_name) or {}
                if not has_broken_docs(plugin_record, plugin_type):
                    name_collector.collect_plugin(
                        plugin_record, plugin_name, plugin_type
                    )
    return name_collector


def _lint_collection_plugin_docs(
    collections_dir: str,
    dependencies: list[str],
    collection_name: str,
    original_path_to_collection: str,
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    validate_collections_refs: ValidCollectionRefs,
    disallow_unknown_collection_refs: bool,
    skip_rstcheck: bool,
    disallow_semantic_markup: bool,
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
            collection_names=[collection_name]
            if validate_collections_refs == "self"
            else collections
            if validate_collections_refs == "dependent"
            else None,
            fetch_all_installed=validate_collections_refs == "all",
        )
    )
    # Load routing information
    collection_routing = asyncio.run(load_all_collection_routing(collection_metadata))
    # Process data
    remove_redirect_duplicates(plugin_info, collection_routing)
    new_plugin_info, nonfatal_errors = asyncio.run(
        normalize_all_plugin_info(plugin_info)
    )
    augment_docs(new_plugin_info)
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
        ("antsibull_docs.data", "docsite"),
        collection_url=collection_url,
        collection_install=collection_install,
        referable_envvars=None,  # this shouldn't make a difference for validation
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
    )

    result = []
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
                if has_broken_docs(plugin_record, plugin_type):
                    result.append(
                        (filename, 0, 0, "Did not return correct DOCUMENTATION")
                    )
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
                    collection_name_,
                    collection_metadata[collection_name_],
                    link_data[collection_name_],
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
                        ignore_directives=["rst-class"],
                        ignore_roles=list(antsibull_roles.ROLES),
                    )
                    result.extend(
                        [
                            (path, result[0], result[1], result[2])
                            for result in rst_results
                        ]
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
            )
        )
    return result
