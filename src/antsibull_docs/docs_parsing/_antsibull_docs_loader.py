# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026, Ansible Project
"""Parse documentation from ansible plugins using antsibull-docs-loader."""

from __future__ import annotations

import dataclasses
import datetime
import typing as t
from pathlib import Path

from antsibull_core.logging import get_module_logger as _get_module_logger
from antsibull_docs_loader.ansible import ALL_DOCUMENTABLE_PLUGIN_TYPES, PluginType
from antsibull_docs_loader.data import CollectionInfo, CollectionInfos
from antsibull_docs_loader.documentation import (
    Documentation,
    DocumentationFragment,
    DocumentationFragments,
)
from antsibull_docs_loader.loader import (
    load_docs,
    load_docs_from_python_doc_fragment_file,
    load_docs_from_role_argspec_file,
)
from antsibull_docs_loader.resolver import Resolved, resolve
from antsibull_docs_loader.routing import (
    CollectionRouting,
    File,
    PluginRouting,
    RemovalData,
    collect_routing_information,
    complete_redirects,
)

from ._utils import _should_flatmap
from .routing import MutableCollectionRoutingT

if t.TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Mapping, MutableMapping

    from . import AnsibleCollectionMetadata


mlog = _get_module_logger(__name__)


class DocFragmentCollector:
    def __init__(self, *, collection_routing: Mapping[str, CollectionRouting]) -> None:
        self.collection_routing = collection_routing
        self.cache: dict[str, tuple[str, str | None, DocumentationFragments | None]] = (
            {}
        )

    def _resolve(
        self, fqcn: str
    ) -> tuple[str, str | None, DocumentationFragments | None]:
        resolved = resolve(
            self.collection_routing, fqcn=fqcn, plugin_type="doc_fragments"
        )
        if resolved.status == Resolved.NOT_FOUND:
            return resolved.fqcn, None, None
        if resolved.status in (Resolved.REDIRECT_ERROR, Resolved.COLLECTION_MISSING):
            return resolved.fqcn, resolved.error, None
        if resolved.status == Resolved.TOMBSTONE:
            return (
                resolved.fqcn,
                f"Doc fragment {resolved.fqcn} no longer exists",
                None,
            )
        assert resolved.status == Resolved.FOUND
        assert resolved.resolved is not None
        if resolved.resolved.python_file is None:
            return (
                resolved.fqcn,
                f"Doc fragment {resolved.fqcn} does not exist as Python file",
                None,
            )
        entry = self.cache.get(resolved.fqcn)
        if entry is not None:
            return entry
        try:
            result = load_docs_from_python_doc_fragment_file(
                resolved.resolved.python_file
            )
            if result is None:
                return (
                    resolved.fqcn,
                    f"Cannot load doc fragment {resolved.resolved.python_file}:"
                    " no content found",
                    None,
                )
            parts = resolved.fqcn.split(".", 2)
            result.add_collection_name(collection_name=".".join(parts[:2]))
            return resolved.fqcn, None, result
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return (
                resolved.fqcn,
                f"Cannot load doc fragment {resolved.resolved.python_file}: {exc}",
                None,
            )

    def _load(self, fqcn: str) -> tuple[str, str | None, DocumentationFragments | None]:
        entry = self.cache.get(fqcn)
        if entry is not None:
            return entry
        entry = self._resolve(fqcn)
        self.cache[entry[0]] = entry
        self.cache[fqcn] = entry
        return entry

    def load(
        self, fqcn: str
    ) -> tuple[str, str | None, DocumentationFragments | None, str]:
        parts = fqcn.split(".")
        if len(parts) < 3:
            # This should be eventually deprecated...
            return self.load(f"ansible.builtin.{fqcn}")
        full_fqcn, error, result = self._load(fqcn)
        if error is not None or result is not None:
            return full_fqcn, error, result, "documentation"
        if len(parts) > 3:
            deref_fqcn = ".".join(parts[:-1])
            deref_full_fqcn, deref_error, deref_result = self._load(deref_fqcn)
            if deref_error is not None or deref_result is not None:
                return deref_full_fqcn, deref_error, deref_result, parts[-1]
        return full_fqcn, None, None, "documentation"

    def resolve(self, fqcn: str) -> str | DocumentationFragment:
        fqcn, error, fragments, name = self.load(fqcn)
        if error is not None:
            return error
        if fragments is None:
            return f"Cannot find doc fragment {fqcn}"
        for f_name, f_data in fragments.fragments.items():
            if f_name.lower() == name:
                return f_data
        return f"Cannot find {name!r} in doc fragment {fqcn}"


def _convert_removal_data(removal: RemovalData) -> dict[str, t.Any]:
    res: dict[str, t.Any] = {}
    if removal.warning_text is not None:
        res["warning_text"] = removal.warning_text
    if removal.removal_version is not None:
        res["removal_version"] = removal.removal_version
    if removal.removal_date is not None:
        if isinstance(removal.removal_date, datetime.datetime):
            res["removal_date"] = removal.removal_date.date()
        elif isinstance(removal.removal_date, datetime.date):
            res["removal_date"] = removal.removal_date.isoformat()
        elif isinstance(removal.removal_date, str):
            res["removal_date"] = removal.removal_date
    return res


def _convert_plugin_routing(data: PluginRouting) -> dict[str, t.Any]:
    result: dict[str, t.Any] = {}
    if data.redirect is not None and data.redirect is not ...:
        result["redirect"] = data.redirect
        result["redirect_is_symlink"] = data.redirect_by_symlink
    if data.tombstone is not None:
        result["tombstone"] = _convert_removal_data(data.tombstone)
    if data.deprecation is not None:
        result["deprecation"] = _convert_removal_data(data.deprecation)
    return result


def _extract_collection_routing(
    adl_collection_routing: Mapping[str, CollectionRouting],
) -> MutableCollectionRoutingT:
    result: dict[str, MutableMapping[str, MutableMapping[str, t.Any]]] = {}
    for collection_name, collection_routing in adl_collection_routing.items():
        for plugin_type, plugin_type_data in collection_routing.plugin_data.items():
            plugin_type_result = result.get(plugin_type)
            if plugin_type_result is None:
                plugin_type_result = {}
                result[plugin_type] = plugin_type_result
            for plugin_name, plugin_data in plugin_type_data.items():
                fqcn = f"{collection_name}.{plugin_name}"
                plugin_type_result[fqcn] = _convert_plugin_routing(plugin_data)
    return result


def _get_collection_info(
    name: str, *, meta: AnsibleCollectionMetadata, is_core: bool = False
) -> CollectionInfo:
    namespace, name = name.split(".", 1)
    return CollectionInfo(
        path=Path(meta.path),
        namespace=namespace,
        name=name,
        full_name=f"{namespace}.{name}",
        version=meta.version,
        is_ansible_core=is_core,
    )


def _get_collection_infos(
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
) -> CollectionInfos:
    ansible_core = collection_metadata.get("ansible.builtin")
    if ansible_core is None:
        raise RuntimeError(
            f"Expected ansible.builtin to be present, but only got {sorted(collection_metadata)}"
        )
    return CollectionInfos(
        ansible_core=_get_collection_info(
            "ansible.builtin", meta=ansible_core, is_core=True
        ),
        collections={
            name: _get_collection_info(name, meta=meta)
            for name, meta in collection_metadata.items()
        },
    )


def _merge(action: PluginRouting, module: PluginRouting) -> PluginRouting:
    replace: dict[str, t.Any] = {}
    if action.redirect is not None:
        replace["redirect"] = action.redirect
        replace["redirect_by_symlink"] = action.redirect_by_symlink
    if action.deprecation is not None:
        replace["deprecation"] = action.deprecation
    if action.tombstone is not None:
        replace["tombstone"] = action.tombstone
    return dataclasses.replace(module, **replace)


def load_collection_routing(
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
) -> tuple[Mapping[str, CollectionRouting], MutableCollectionRoutingT]:
    """
    Loads collection routing information in two formats,
    and populates collection metadata with ``requires_ansible``.
    """
    collection_infos = _get_collection_infos(collection_metadata)
    collection_routing = collect_routing_information(collection_infos)

    for a_collection_name, a_collection_routing in collection_routing.items():
        # Merge action into module routing
        action_routing = a_collection_routing.plugin_data.pop("action", None)
        if action_routing:
            module_routing = a_collection_routing.plugin_data.get("module")
            if module_routing is None:
                module_routing = {}
                a_collection_routing.plugin_data["module"] = module_routing
            for plugin_name, plugin_data in action_routing.items():
                if plugin_name not in module_routing:
                    module_routing[plugin_name] = plugin_data
                else:
                    module_routing[plugin_name] = _merge(
                        plugin_data, module_routing[plugin_name]
                    )

        # Populate requires_ansible
        a_meta = collection_metadata.get(a_collection_name)
        if (
            a_meta is not None
            and a_collection_name != "ansible.builtin"
            and a_collection_routing.requires_ansible is not None
        ):
            a_meta.requires_ansible = a_collection_routing.requires_ansible

    complete_redirects(collection_routing)
    return collection_routing, _extract_collection_routing(collection_routing)


def _collect_role_doc(*, fqcn: str, collection_name: str, file: File) -> t.Any:
    path = file.docs_candidates[0]
    role_docs = load_docs_from_role_argspec_file(path)
    if role_docs is None:
        raise ValueError(f"Cannot load documentation for role {fqcn}")
    role_docs.add_collection_name(collection_name=collection_name)
    result = {}
    for name, entrypoint in role_docs.entrypoints.items():
        ep_result = {}
        ep_result.update(entrypoint.documentation)
        if entrypoint.examples is not None:
            ep_result["examples"] = entrypoint.examples
        result[name] = ep_result
    return {"entry_points": result, "collection": collection_name, "path": str(path)}


def _resolve_fragments(
    *,
    docs: Documentation,
    fqcn: str,
    plugin_type: PluginType,
    doc_fragments: DocFragmentCollector,
) -> dict[str, t.Any]:
    for doc_fragment in docs.get_doc_fragments():
        fragment = doc_fragments.resolve(doc_fragment)
        if isinstance(fragment, str):
            return {
                "error": f"Error while resolving doc fragment {doc_fragment}: {fragment}"
            }
        try:
            docs.merge_doc_fragment(fragment=fragment)
        except ValueError as exc:
            return {
                "error": (
                    f"Error while merging doc fragment {doc_fragment}"
                    f" into {plugin_type} {fqcn}: {exc}"
                )
            }
    for doc_fragment in docs.get_return_fragments():
        fragment = doc_fragments.resolve(doc_fragment)
        if isinstance(fragment, str):
            return {
                "error": f"Error while resolving return fragment {doc_fragment}: {fragment}"
            }
        try:
            docs.merge_return_fragment(fragment=fragment)
        except ValueError as exc:
            return {
                "error": (
                    f"Error while merging return fragment {doc_fragment}"
                    f" into {plugin_type} {fqcn}: {exc}"
                )
            }
    return {
        "doc": docs.documentation,
        "examples": docs.examples,
        "return": docs.return_values,
    }


def _collect_doc(
    *,
    fqcn: str,
    collection_name: str,
    plugin_type: PluginType,
    file: File,
    doc_fragments: DocFragmentCollector,
    has_action: bool,
) -> dict[str, t.Any]:
    docs_path = load_docs(file.docs_candidates)
    if docs_path is None:
        raise ValueError(f"Cannot load documentation for {plugin_type} {fqcn}")
    docs, path = docs_path
    docs.documentation["filename"] = str(path)
    if plugin_type == "module":
        docs.documentation["has_action"] = has_action
    docs.add_collection_name(collection_name=collection_name, plugin_type=plugin_type)
    return _resolve_fragments(
        docs=docs,
        fqcn=fqcn,
        plugin_type=plugin_type,
        doc_fragments=doc_fragments,
    )


def _has_action(
    *, collection_routing: Mapping[str, CollectionRouting], fqcn: str
) -> bool:
    try:
        res = resolve(collection_routing, fqcn=fqcn, plugin_type="action")
        return res.status in (
            Resolved.FOUND,
            Resolved.TOMBSTONE,
            Resolved.COLLECTION_MISSING,
        )
    except ValueError:
        return False


def _collect_docs(
    *,
    plugin_map: MutableMapping[str, MutableMapping[str, t.Any]],
    collection_name: str,
    collection_routing: Mapping[str, CollectionRouting],
    doc_fragments: DocFragmentCollector,
    flatmap: bool,
) -> None:
    routing = collection_routing.get(collection_name)
    if routing is None:
        raise AssertionError(
            f"Could not find routing information for {collection_name}"
        )
    for plugin_type, plugin_files in routing.files.items():
        if plugin_type not in ALL_DOCUMENTABLE_PLUGIN_TYPES:
            continue
        plugin_type_map = plugin_map.get(plugin_type)
        if plugin_type_map is None:
            plugin_type_map = {}
            plugin_map[plugin_type] = plugin_type_map
        plugin_routing = routing.plugin_data.get(plugin_type) or {}
        for parts, file in plugin_files.items():
            name = ".".join(parts)
            fqcn = f"{collection_name}.{name}"
            dest_fqcn = f"{collection_name}.{parts[-1]}" if flatmap else fqcn
            r = plugin_routing.get(name)
            if r is not None and (r.redirect is not None or r.tombstone is not None):
                continue
            try:
                if plugin_type == "role":
                    plugin_type_map[dest_fqcn] = _collect_role_doc(
                        fqcn=fqcn, collection_name=collection_name, file=file
                    )
                else:
                    has_action = _has_action(
                        collection_routing=collection_routing, fqcn=fqcn
                    )
                    plugin_type_map[dest_fqcn] = _collect_doc(
                        fqcn=fqcn,
                        collection_name=collection_name,
                        plugin_type=plugin_type,
                        file=file,
                        doc_fragments=doc_fragments,
                        has_action=has_action,
                    )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                plugin_type_map[dest_fqcn] = {"error": str(exc)}


def _iterate_collections(
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    collection_names: list[str] | None,
) -> t.Generator[str]:
    if collection_names is not None:
        for collection_name in collection_names:
            if collection_name != "ansible.builtin":
                yield collection_name
        return
    for collection_name in collection_metadata:
        if collection_name != "ansible.builtin":
            yield collection_name


def collect_docs(
    *,
    plugin_map: MutableMapping[str, MutableMapping[str, t.Any]],
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    collection_routing: Mapping[str, CollectionRouting],
    collection_names: list[str] | None,
) -> None:
    flog = mlog.fields(func="collect_docs")
    flog.debug("Enter")

    doc_fragments = DocFragmentCollector(collection_routing=collection_routing)
    for collection_name in _iterate_collections(collection_metadata, collection_names):
        _collect_docs(
            plugin_map=plugin_map,
            collection_name=collection_name,
            collection_routing=collection_routing,
            doc_fragments=doc_fragments,
            flatmap=_should_flatmap(
                collection_name, collection_metadata=collection_metadata
            ),
        )

    flog.debug("Leave")
