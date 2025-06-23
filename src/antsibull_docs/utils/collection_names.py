# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Tools for collecting names."""

from __future__ import annotations

import asyncio
import contextlib
import typing as t
from collections.abc import Mapping, MutableMapping, Sequence

from antsibull_core.venv import FakeVenvRunner

from ..augment_docs import augment_docs
from ..docs_parsing import AnsibleCollectionMetadata
from ..docs_parsing.parsing import get_ansible_plugin_info
from ..docs_parsing.routing import (
    CollectionRoutingT,
    load_all_collection_routing,
    remove_redirect_duplicates,
)
from ..process_docs import (
    PluginErrorsRT,
    get_collection_contents,
    get_plugin_contents,
    normalize_all_plugin_info,
)
from ..write_docs import BasicPluginInfo
from ..write_docs.plugins import (
    has_broken_docs,
)
from .collection_copier import CollectionLoadError, load_collection_infos

ValidCollectionRefs = t.Literal["self", "dependent", "all"]


_NAME_SEPARATOR = "/"
_ROLE_ENTRYPOINT_SEPARATOR = "###"


def _get_fqcn_collection_name(fqcn: str) -> str:
    return ".".join(fqcn.split(".")[:2])


def _get_fqcn_collection_prefix(fqcn: str) -> str:
    return _get_fqcn_collection_name(fqcn) + "."


class NameCollection:
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

    def _collect_collection(self, collection_name_or_fqcn: str):
        self._collection_prefixes.add(
            _get_fqcn_collection_prefix(collection_name_or_fqcn)
        )

    def _collect_plugin(
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
                self._role_entrypoints.add((plugin_fqcn, entry_point))
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

    def __init__(self, collection_routing: CollectionRoutingT):
        self._plugins: set[tuple[str, str]] = set()
        self._role_entrypoints: set[tuple[str, str]] = set()
        self._collection_prefixes: set[str] = set()
        self._option_names: dict[tuple[str, str, str], str] = {}
        self._return_value_names: dict[tuple[str, str, str], str] = {}
        self._collection_routing: CollectionRoutingT = collection_routing
        self._routing_table: dict[tuple[str, str], str] = {}

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

    def has_plugins(self, collection_name: str, plugin_type: str) -> bool:
        collection_prefix = f"{collection_name}."
        return any(
            a_plugin_type == plugin_type and a_plugin_fqcn.startswith(collection_prefix)
            for a_plugin_fqcn, a_plugin_type in self._plugins
        )

    def is_valid_plugin(self, plugin_fqcn: str, plugin_type: str) -> bool:
        return (
            self._resolve_plugin_fqcn(plugin_fqcn, plugin_type),
            plugin_type,
        ) in self._plugins

    def is_valid_role_entrypoint(self, plugin_fqcn: str, entrypoint: str) -> bool:
        return (
            self._resolve_plugin_fqcn(plugin_fqcn, "role"),
            entrypoint,
        ) in self._role_entrypoints

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


def _collect_names_impl(
    new_plugin_info: Mapping[str, Mapping[str, t.Any]],
    collection_to_plugin_info: Mapping[
        str, Mapping[str, Mapping[str, BasicPluginInfo]]
    ],
    collection_name: str,
    collections: list[str],
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    validate_collections_refs: ValidCollectionRefs,
    collection_routing: CollectionRoutingT,
) -> NameCollection:
    name_collection = NameCollection(collection_routing)
    name_collection._collect_collection(  # pylint: disable=protected-access
        collection_name
    )
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
                    name_collection._collect_plugin(  # pylint: disable=protected-access
                        plugin_record, plugin_name, plugin_type
                    )
    return name_collection


def collect_names(
    *,
    collection_name: str,
    collections_dir: str | None,
    dependencies: list[str],
    validate_collections_refs: ValidCollectionRefs = "self",
) -> tuple[
    NameCollection,
    Mapping[str, MutableMapping[str, t.Any]],
    PluginErrorsRT,
    Mapping[str, dict[str, Mapping[str, BasicPluginInfo]]],
    Mapping[str, AnsibleCollectionMetadata],
]:
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

    # Load routing information
    collection_routing = asyncio.run(load_all_collection_routing(collection_metadata))
    # Process data
    remove_redirect_duplicates(plugin_info, collection_routing)
    new_plugin_info, nonfatal_errors = asyncio.run(
        normalize_all_plugin_info(plugin_info)
    )
    augment_docs(new_plugin_info, collection_routing)
    # More processing
    plugin_contents = get_plugin_contents(new_plugin_info, nonfatal_errors)
    collection_to_plugin_info = get_collection_contents(plugin_contents)
    for collection in collection_metadata:
        collection_to_plugin_info[collection]  # pylint:disable=pointless-statement
    # Collect all option and return value names
    return (
        _collect_names_impl(
            new_plugin_info,
            collection_to_plugin_info,
            collection_name,
            collections,
            collection_metadata,
            validate_collections_refs,
            collection_routing,
        ),
        new_plugin_info,
        nonfatal_errors,
        collection_to_plugin_info,
        collection_metadata,
    )


@contextlib.contextmanager
def load_name_collection(
    *,
    path_to_collection: str,
    validate_collections_refs: ValidCollectionRefs = "self",
) -> t.Generator[tuple[NameCollection, list[CollectionLoadError]]]:
    with load_collection_infos(
        path_to_collection=path_to_collection,
        copy_dependencies=validate_collections_refs != "all",
    ) as (
        collection_name,
        collections_dir,
        dependencies,
        errors,
    ):
        name_collection, _, __, ___, ____ = collect_names(
            collection_name=collection_name,
            collections_dir=collections_dir,
            dependencies=dependencies,
            validate_collections_refs=validate_collections_refs,
        )

        yield name_collection, errors


__all__ = (
    "NameCollection",
    "ValidCollectionRefs",
    "collect_names",
    "load_name_collection",
)
