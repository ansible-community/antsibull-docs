# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Lint plugin docs."""

from __future__ import annotations

import asyncio
import os
import typing as t
from collections.abc import Mapping, MutableMapping, Sequence

from antsibull_docs_parser import dom
from antsibull_docs_parser.parser import Context as ParserContext
from antsibull_docs_parser.parser import parse as parse_markup
from jinja2 import Template

from sphinx_antsibull_ext import directives as antsibull_directives
from sphinx_antsibull_ext import roles as antsibull_roles

from .collection_links import load_collections_links
from .docs_parsing import AnsibleCollectionMetadata
from .jinja2.environment import OutputFormat, doc_environment
from .lint_collection_names import CollectionNameLinter, Plugin
from .markup.semantic_helper import split_option_like_name
from .plugin_docs import walk_plugin_docs_texts
from .process_docs import PluginErrorsRT
from .rstcheck import check_rst_content
from .schemas.collection_links import CollectionLinks
from .utils.collection_name_transformer import CollectionNameTransformer
from .utils.collection_names import (
    NameCollection,
    ValidCollectionRefs,
)
from .write_docs import BasicPluginInfo, PluginErrorsT
from .write_docs.plugins import (
    create_plugin_rst,
    guess_relative_filename,
    has_broken_docs,
)

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
        self.markup_validator.validate_module(part, self.key)

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
        self.markup_validator.validate_option_name(part, self.key)

    def process_option_value(self, part: dom.OptionValuePart) -> None:
        if not part.value:
            self._error(part, "empty value")

    def process_plugin(self, part: dom.PluginPart) -> None:
        self.markup_validator.validate_plugin(part, self.key)

    def process_return_value(self, part: dom.ReturnValuePart) -> None:
        if not part.name:
            self._error(part, "empty return value name")
        self.markup_validator.validate_return_value(part, self.key)


class _MarkupValidator:
    errors: list[str]

    _name_collection: NameCollection
    _current_plugin: dom.PluginIdentifier
    _collection_name_prefix: str
    _validate_collections_refs: ValidCollectionRefs
    _disallow_unknown_collection_refs: bool
    _disallow_semantic_markup: bool

    def _validate_plugin_fqcn(
        self,
        part: dom.AnyPart | None,
        plugin_fqcn: str,
        plugin_type: str,
        role_entrypoint: str | None,
        key: str,
    ) -> None:
        for error in self._linter.validate_plugin_fqcn(
            Plugin(
                plugin_fqcn=plugin_fqcn,
                plugin_type=plugin_type,
                role_entrypoint=role_entrypoint,
            )
        ):
            key_prefix = f"{key}: {part.source}" if part else key
            self.errors.append(f"{key_prefix}: {error}")

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

    def validate_option_name(self, opt: dom.OptionNamePart, key: str) -> None:
        l_plugin = None
        plugin = opt.plugin
        if plugin is not None:
            l_plugin = Plugin(
                plugin_fqcn=plugin.fqcn,
                plugin_type=plugin.type,
                role_entrypoint=opt.entrypoint,
            )
        for error in self._linter.validate_option_name(
            plugin=l_plugin,
            name=opt.name,
            link=opt.link,
        ):
            self.errors.append(f"{key}: {opt.source}: {error}")

    def validate_return_value(self, rv: dom.ReturnValuePart, key: str) -> None:
        l_plugin = None
        plugin = rv.plugin
        if plugin is not None:
            l_plugin = Plugin(
                plugin_fqcn=plugin.fqcn,
                plugin_type=plugin.type,
                role_entrypoint=rv.entrypoint,
            )
        for error in self._linter.validate_return_value(
            plugin=l_plugin,
            name=rv.name,
            link=rv.link,
        ):
            self.errors.append(f"{key}: {rv.source}: {error}")

    def validate_module(self, module: dom.ModulePart, key: str) -> None:
        self._validate_plugin_fqcn(module, module.fqcn, "module", None, key)

    def validate_plugin(self, plugin: dom.PluginPart, key: str) -> None:
        self._validate_plugin_fqcn(
            plugin, plugin.plugin.fqcn, plugin.plugin.type, None, key
        )

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
                self._validate_plugin_fqcn(
                    None, entry["module"], "module", None, entry_key
                )
            if "plugin" in entry and "plugin_type" in entry:
                self._validate_plugin_fqcn(
                    None, entry["plugin"], entry["plugin_type"], None, entry_key
                )

    def __init__(
        self,
        name_collection: NameCollection,
        plugin_record: dict[str, t.Any],
        plugin_fqcn: str,
        plugin_type: str,
        validate_collections_refs: ValidCollectionRefs = "self",
        disallow_unknown_collection_refs: bool = False,
        disallow_semantic_markup: bool = False,
    ):
        self.errors = []
        self._linter = CollectionNameLinter(
            collection_name=_get_fqcn_collection_name(plugin_fqcn),
            name_collection=name_collection,
            validate_collections_refs=validate_collections_refs,
            disallow_unknown_collection_refs=disallow_unknown_collection_refs,
        )
        self._name_collection = name_collection
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
    *,
    name_collection: NameCollection,
    plugin_record: dict[str, t.Any],
    plugin_fqcn: str,
    plugin_type: str,
    path: str,
    validate_collections_refs: ValidCollectionRefs,
    disallow_unknown_collection_refs: bool,
    disallow_semantic_markup: bool,
) -> list[tuple[str, int, int, str]]:
    validator = _MarkupValidator(
        name_collection,
        plugin_record,
        plugin_fqcn,
        plugin_type,
        validate_collections_refs=validate_collections_refs,
        disallow_unknown_collection_refs=disallow_unknown_collection_refs,
        disallow_semantic_markup=disallow_semantic_markup,
    )
    return [(path, 0, 0, msg) for msg in validator.errors]


def _lint_plugin_docs(
    *,
    result: list[tuple[str, int, int, str]],
    original_path_to_collection: str,
    name_collection: NameCollection,
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
                name_collection=name_collection,
                plugin_record=plugin_record,
                plugin_fqcn=plugin_name,
                plugin_type=plugin_type,
                path=filename,
                validate_collections_refs=validate_collections_refs,
                disallow_unknown_collection_refs=disallow_unknown_collection_refs,
                disallow_semantic_markup=disallow_semantic_markup,
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


def lint_plugin_docs(
    *,
    name_collection: NameCollection,
    new_plugin_info: Mapping[str, MutableMapping[str, t.Any]],
    nonfatal_errors: PluginErrorsRT,
    collection_to_plugin_info: Mapping[str, dict[str, Mapping[str, BasicPluginInfo]]],
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
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
    if original_path_to_collection is None:
        original_path_to_collection = collection_metadata[collection_name].path
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
    # Load link data
    link_data = asyncio.run(
        load_collections_links(
            {name: data.path for name, data in collection_metadata.items()}
        )
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
                    result=result,
                    original_path_to_collection=original_path_to_collection,
                    name_collection=name_collection,
                    collection_name=collection_name_,
                    collection_metadata=collection_metadata,
                    link_data=link_data,
                    plugin_name=plugin_name,
                    plugin_type=plugin_type,
                    plugin_short_name=plugin_short_name,
                    filename=filename,
                    plugin_record=plugin_record,
                    nonfatal_errors=nonfatal_errors,
                    plugin_type_tmpl=plugin_type_tmpl,
                    error_tmpl=error_tmpl,
                    disallow_unknown_collection_refs=disallow_unknown_collection_refs,
                    disallow_semantic_markup=disallow_semantic_markup,
                    skip_rstcheck=skip_rstcheck,
                    validate_collections_refs=validate_collections_refs,
                )
    return result
