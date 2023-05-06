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
from collections.abc import Sequence

from antsibull_core.subprocess_util import log_run
from antsibull_core.vendored.json_utils import _filter_non_json_lines
from antsibull_core.venv import FakeVenvRunner
from antsibull_docs_parser import dom
from antsibull_docs_parser.parser import Context as ParserContext
from antsibull_docs_parser.parser import parse as parse_markup

from sphinx_antsibull_ext import roles as antsibull_roles

from .augment_docs import augment_docs
from .collection_links import load_collections_links
from .docs_parsing.ansible_doc import parse_ansible_galaxy_collection_list
from .docs_parsing.parsing import get_ansible_plugin_info
from .docs_parsing.routing import (
    load_all_collection_routing,
    remove_redirect_duplicates,
)
from .jinja2.environment import doc_environment
from .lint_helpers import load_collection_info
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


class CollectionFinder:
    def __init__(self):
        self.collections = {}
        p = log_run(["ansible-galaxy", "collection", "list", "--format", "json"])
        data = json.loads(_filter_non_json_lines(p.stdout)[0])
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


class _MarkupValidator:
    errors: list[str]

    _current_plugin: dom.PluginIdentifier
    _disallow_semantic_markup: bool
    _option_names: dict[str, str]
    _return_value_names: dict[str, str]

    def _collect_role_option_names(
        self, options: dict[str, t.Any], entrypoint: str, path_prefix: str
    ) -> None:
        for opt, data in sorted(options.items()):
            path = f"{path_prefix}{opt}"
            self._option_names[
                f"{entrypoint}{_ROLE_ENTRYPOINT_SEPARATOR}{path}"
            ] = data["type"]
            if "options" in data:
                self._collect_role_option_names(
                    data["options"], entrypoint, f"{path}{_NAME_SEPARATOR}"
                )

    def _collect_option_names(
        self, options: dict[str, t.Any], path_prefix: str
    ) -> None:
        for opt, data in sorted(options.items()):
            path = f"{path_prefix}{opt}"
            self._option_names[path] = data["type"]
            if "suboptions" in data:
                self._collect_option_names(
                    data["suboptions"], f"{path}{_NAME_SEPARATOR}"
                )

    def _collect_return_value_names(
        self, return_values: dict[str, t.Any], path_prefix: str
    ) -> None:
        for rv, data in sorted(return_values.items()):
            path = f"{path_prefix}{rv}"
            self._return_value_names[path] = data["type"]
            if "contains" in data:
                self._collect_return_value_names(
                    data["contains"], f"{path}{_NAME_SEPARATOR}"
                )

    def _validate_option_name(self, opt: dom.OptionNamePart, key: str) -> None:
        plugin = opt.plugin
        if plugin is None:
            return
        if plugin == self._current_plugin:
            lookup = _NAME_SEPARATOR.join(opt.link)
            if opt.entrypoint is not None:
                lookup = f"{opt.entrypoint}{_ROLE_ENTRYPOINT_SEPARATOR}{lookup}"
            if lookup not in self._option_names:
                prefix = "" if plugin.type in ("role", "module") else " plugin"
                self.errors.append(
                    f'{key}: option name reference "{opt.name}" does not reference to an existing'
                    f" option of the {plugin.type}{prefix} {plugin.fqcn}"
                )

    def _validate_return_value(self, rv: dom.ReturnValuePart, key: str) -> None:
        plugin = rv.plugin
        if plugin is None:
            return
        if plugin == self._current_plugin:
            lookup = _NAME_SEPARATOR.join(rv.link)
            if rv.entrypoint is not None:
                lookup = f"{rv.entrypoint}{_ROLE_ENTRYPOINT_SEPARATOR}{lookup}"
            if lookup not in self._return_value_names:
                prefix = "" if plugin.type in ("role", "module") else " plugin"
                self.errors.append(
                    f'{key}: return value name reference "{rv.name}" does not reference to an'
                    f" existing return value of the {plugin.type}{prefix} {plugin.fqcn}"
                )

    def _validate_markup_entry(
        self, entry: str | t.Sequence[str], key: str, role_entrypoint: str | None = None
    ) -> None:
        context = ParserContext(
            current_plugin=self._current_plugin,
            role_entrypoint=role_entrypoint,
        )
        parsed_paragraphs = parse_markup(
            entry,
            context,
            errors="message",
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
                        f"{key}: Found semantic markup ({par_elem.type.name} element)"
                    )
                if par_elem.type == dom.PartType.OPTION_NAME:
                    self._validate_option_name(
                        t.cast(dom.OptionNamePart, par_elem), key
                    )
                if par_elem.type == dom.PartType.RETURN_VALUE:
                    self._validate_return_value(
                        t.cast(dom.ReturnValuePart, par_elem), key
                    )

    def _validate_markup_dict_entry(
        self,
        dictionary: dict[str, t.Any],
        key: str,
        key_path: str,
        role_entrypoint: str | None = None,
    ) -> None:
        value = dictionary.get(key)
        if value is None:
            return
        full_key = f"{key_path} -> {key}"
        if isinstance(value, str):
            self._validate_markup_entry(
                value, full_key, role_entrypoint=role_entrypoint
            )
        elif isinstance(value, Sequence):
            all_strings = True
            for index, entry in enumerate(value):
                if not isinstance(entry, str):
                    self.errors.append(
                        f"Expected {full_key} to be a list of strings; the {index + 1}-th"
                        f" entry is of type {type(value)} instead"
                    )
                    all_strings = False
            if all_strings:
                self._validate_markup_entry(
                    value, full_key, role_entrypoint=role_entrypoint
                )
        else:
            self.errors.append(
                f"Expected {full_key} to be a string or list of strings, but got {type(value)}"
            )

    def _validate_deprecation(
        self, owner: dict[str, t.Any], key_path: str, role_entrypoint: str | None = None
    ) -> None:
        if "deprecated" not in owner:
            return
        key_path = f"{key_path} -> deprecated"
        deprecated = owner["deprecated"]
        self._validate_markup_dict_entry(
            deprecated, "why", key_path, role_entrypoint=role_entrypoint
        )
        self._validate_markup_dict_entry(
            deprecated, "alternative", key_path, role_entrypoint=role_entrypoint
        )

    def _validate_options(
        self,
        options: dict[str, t.Any],
        key_path: str,
        role_entrypoint: str | None = None,
    ) -> None:
        for opt, data in sorted(options.items()):
            opt_key = f"{key_path} -> {opt}"
            self._validate_markup_dict_entry(
                data, "description", opt_key, role_entrypoint=role_entrypoint
            )
            self._validate_deprecation(data, opt_key, role_entrypoint=role_entrypoint)
            for sub in ("cli", "env", "ini", "vars", "keyword"):
                if sub in data:
                    for index, sub_data in enumerate(data[sub]):
                        sub_key = f"{opt_key} -> {sub}[{index + 1}]"
                        self._validate_deprecation(
                            sub_data, sub_key, role_entrypoint=role_entrypoint
                        )
            for sub_key in ("options", "suboptions"):
                if sub_key in data:
                    self._validate_options(
                        data[sub_key],
                        f"{opt_key} -> {sub_key}",
                        role_entrypoint=role_entrypoint,
                    )

    def _validate_return_values(
        self,
        return_values: dict[str, t.Any],
        key_path: str,
        role_entrypoint: str | None = None,
    ) -> None:
        for rv, data in sorted(return_values.items()):
            rv_key = f"{key_path} -> {rv}"
            self._validate_markup_dict_entry(
                data, "description", rv_key, role_entrypoint=role_entrypoint
            )
            self._validate_markup_dict_entry(
                data, "returned", rv_key, role_entrypoint=role_entrypoint
            )
            if "contains" in data:
                self._validate_return_values(
                    data["contains"],
                    f"{rv_key} -> contains",
                    role_entrypoint=role_entrypoint,
                )

    def _validate_seealso(
        self, owner: dict[str, t.Any], key_path: str, role_entrypoint: str | None = None
    ) -> None:
        if "seealso" not in owner:
            return
        key_path = f"{key_path} -> seealso"
        seealso = owner["seealso"]
        for index, entry in enumerate(seealso):
            entry_path = f"{key_path}[{index + 1}]"
            self._validate_markup_dict_entry(
                entry, "description", entry_path, role_entrypoint=role_entrypoint
            )
            self._validate_markup_dict_entry(
                entry, "name", entry_path, role_entrypoint=role_entrypoint
            )

    def _validate_attributes(
        self, owner: dict[str, t.Any], key_path: str, role_entrypoint: str | None = None
    ) -> None:
        if "attributes" not in owner:
            return
        key_path = f"{key_path} -> attributes"
        attributes = owner["attributes"]
        for attribute, data in sorted(attributes.items()):
            attribute_path = f"{key_path} -> {attribute}"
            self._validate_markup_dict_entry(
                data, "description", attribute_path, role_entrypoint=role_entrypoint
            )
            self._validate_markup_dict_entry(
                data, "details", attribute_path, role_entrypoint=role_entrypoint
            )

    def _validate_main(
        self, main: dict[str, t.Any], key_path: str, role_entrypoint: str | None = None
    ) -> None:
        self._validate_deprecation(main, key_path, role_entrypoint=role_entrypoint)
        self._validate_markup_dict_entry(
            main, "short_description", key_path, role_entrypoint=role_entrypoint
        )
        self._validate_markup_dict_entry(
            main, "author", key_path, role_entrypoint=role_entrypoint
        )
        self._validate_markup_dict_entry(
            main, "description", key_path, role_entrypoint=role_entrypoint
        )
        self._validate_markup_dict_entry(
            main, "notes", key_path, role_entrypoint=role_entrypoint
        )
        self._validate_markup_dict_entry(
            main, "requirements", key_path, role_entrypoint=role_entrypoint
        )
        self._validate_markup_dict_entry(
            main, "todo", key_path, role_entrypoint=role_entrypoint
        )
        self._validate_seealso(main, key_path, role_entrypoint=role_entrypoint)
        self._validate_attributes(main, key_path, role_entrypoint=role_entrypoint)
        if "options" in main:
            self._validate_options(
                main["options"],
                f"{key_path} -> options",
                role_entrypoint=role_entrypoint,
            )

    def __init__(
        self,
        plugin_record: dict[str, t.Any],
        plugin_fqcn: str,
        plugin_type: str,
        disallow_semantic_markup: bool = False,
    ):
        self._current_plugin = dom.PluginIdentifier(fqcn=plugin_fqcn, type=plugin_type)
        self._disallow_semantic_markup = disallow_semantic_markup

        # Collect option and return value names
        self._option_names = {}
        self._return_value_names = {}
        if "doc" in plugin_record and "options" in plugin_record["doc"]:
            self._collect_option_names(plugin_record["doc"]["options"], "")
        if "return" in plugin_record:
            self._collect_return_value_names(plugin_record["return"], "")
        if "entry_points" in plugin_record:
            for entry_point, data in sorted(plugin_record["entry_points"].items()):
                if "options" in data:
                    self._collect_role_option_names(data["options"], entry_point, "")

        # Validate names
        self.errors = []
        if "doc" in plugin_record:
            self._validate_main(plugin_record["doc"], "DOCUMENTATION")
        if "return" in plugin_record:
            self._validate_return_values(plugin_record["return"], "RETURN")
        if "entry_points" in plugin_record:
            for entry_point, data in sorted(plugin_record["entry_points"].items()):
                self._validate_main(
                    data,
                    f"argument_specs -> {entry_point}",
                    role_entrypoint=entry_point,
                )


def _validate_markup(
    plugin_record: dict[str, t.Any],
    plugin_fqcn: str,
    plugin_type: str,
    path: str,
    disallow_semantic_markup: bool,
) -> list[tuple[str, int, int, str]]:
    validator = _MarkupValidator(
        plugin_record,
        plugin_fqcn,
        plugin_type,
        disallow_semantic_markup=disallow_semantic_markup,
    )
    return [(path, 0, 0, msg) for msg in validator.errors]


def _lint_collection_plugin_docs(
    collections_dir: str,
    collection_name: str,
    original_path_to_collection: str,
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    skip_rstcheck: bool,
    disallow_semantic_markup: bool,
) -> list[tuple[str, int, int, str]]:
    # Load collection docs
    venv = FakeVenvRunner()
    plugin_info, collection_metadata = asyncio.run(
        get_ansible_plugin_info(
            venv, collections_dir, collection_names=[collection_name]
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
    )
    # Get the templates
    plugin_tmpl = env.get_template("plugin.rst.j2")
    role_tmpl = env.get_template("role.rst.j2")
    error_tmpl = env.get_template("plugin-error.rst.j2")

    result = []
    for collection_name_, plugins_by_type in collection_to_plugin_info.items():
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
                            plugin_record,
                            plugin_name,
                            plugin_type,
                            filename,
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
        if dependencies:
            collection_finder = CollectionFinder()
            while dependencies:
                dependency = dependencies.pop(0)
                if dependency in done_dependencies:
                    continue
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
                collection_name,
                path_to_collection,
                collection_url=collection_url,
                collection_install=collection_install,
                skip_rstcheck=skip_rstcheck,
                disallow_semantic_markup=disallow_semantic_markup,
            )
        )
    return result
