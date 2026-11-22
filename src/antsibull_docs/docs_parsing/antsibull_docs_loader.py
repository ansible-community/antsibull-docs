# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026, Ansible Project
"""Parse documentation from ansible plugins using antsibull-docs-loader."""

from __future__ import annotations

import typing as t

from antsibull_core.logging import get_module_logger as _get_module_logger

from . import _get_environment
from ._antsibull_docs_loader import collect_docs as _collect_docs
from ._antsibull_docs_loader import load_collection_routing as _load_collection_routing
from ._utils import call_ansible_doc as _call_ansible_doc
from ._utils import limit_by_wildcards as _limit_by_wildcards
from ._utils import process_ansible_doc_output as _process_ansible_doc_output
from .ansible_doc import get_collection_metadata as _get_collection_metadata
from .fqcn import is_collection_name as _is_collection_name
from .fqcn import is_wildcard_collection_name as _is_wildcard_collection_name
from .routing import (
    MutableCollectionRoutingT,
    _add_meta_redirect_for_aliases,
    _remove_other_duplicates,
)

if t.TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Mapping, MutableMapping

    from antsibull_core.venv import FakeVenvRunner, VenvRunner

    from . import AnsibleCollectionMetadata


mlog = _get_module_logger(__name__)


async def get_ansible_plugin_info(
    venv: VenvRunner | FakeVenvRunner,
    collection_dir: str | None,
    collection_names: list[str] | None = None,
    fetch_all_installed: bool = False,
) -> tuple[
    MutableMapping[str, MutableMapping[str, t.Any]],
    Mapping[str, AnsibleCollectionMetadata],
    MutableCollectionRoutingT,
]:
    """
    Retrieve information about all of the Ansible Plugins. Requires ansible-core 2.13+
    and antsibull-docs-loader.

    :arg venv: A VenvRunner into which Ansible has been installed.
    :arg collection_dir: Directory in which the collections have been installed.
                         If ``None``, the collections are assumed to be in the current
                         search path for Ansible.
    :arg collection_names: Optional list of collections. If specified, will only collect
                           information for plugins in these collections.
    :arg fetch_all_installed: If set to ``True``, will also retrieve plugins of installed
        collections outside ``collection_dir`` (if specified).
    :returns: An tuple. The first component is a nested directory structure that looks like:

            plugin_type:
                plugin_name:  # FQCN
                    {information from ansible-doc --json.  See the ansible-doc documentation
                     for more info.}

        The second component is a Mapping of collection names to metadata. The second mapping
        always includes the metadata for ansible.builtin, even if it was not explicitly
        mentioned in ``collection_names``.

        The third component contains routing information for the collections.
        It is a nested directory structure that looks like:

            plugin_type:
                plugin_name:  # FQCN
                    tombstone: t.Optional[{tombstone record}]
                    deprecation: t.Optional[{deprecation record}]
                    redirect: t.Optional[str]
                    redirect_is_symlink: t.Optional[bool]
    """
    flog = mlog.fields(func="get_ansible_plugin_info")
    flog.debug("Enter")

    env = _get_environment(
        collection_dir, keep_current_collections_path=fetch_all_installed, venv=venv
    )

    has_wildcards = collection_names is not None and any(
        _is_wildcard_collection_name(cn) and not _is_collection_name(cn)
        for cn in collection_names
    )

    flog.debug("Retrieving collection metadata")
    collection_metadata = await _get_collection_metadata(
        venv, env, None if has_wildcards else collection_names
    )

    if has_wildcards:
        flog.debug("Restricting collection list by wildcards")
        _, collection_names = _limit_by_wildcards(
            collection_metadata=collection_metadata,
            collection_names=collection_names or [],
        )

    flog.debug("Loading collection routing")
    adl_collection_routing, collection_routing = _load_collection_routing(
        collection_metadata
    )

    plugin_map: MutableMapping[str, MutableMapping[str, t.Any]]

    if collection_names is None or "ansible.builtin" in collection_names:
        env = _get_environment(
            "/dev/null", keep_current_collections_path=False, venv=venv
        )

        flog.debug("Retrieving and loading ansible-core plugin documentation")
        ansible_doc_output = await _call_ansible_doc(
            "ansible.builtin",
            env=env,
            venv=venv,
        )

        flog.debug("Processing plugin documentation")
        plugin_map = _process_ansible_doc_output(
            ansible_doc_output,
            collection_names=collection_names,
            collection_metadata=collection_metadata,
        )
        for plugin_type, plugin_type_map in plugin_map.items():
            if plugin_type not in collection_routing:
                continue
            plugin_routing = collection_routing[plugin_type]
            _add_meta_redirect_for_aliases(plugin_type_map, plugin_routing)
            _remove_other_duplicates(plugin_type, plugin_type_map, plugin_routing)
    else:
        plugin_map = {}

    if collection_names is None or collection_names != ["ansible.builtin"]:
        flog.debug("Load documentation of other collections")
        _collect_docs(
            plugin_map=plugin_map,
            collection_metadata=collection_metadata,
            collection_routing=adl_collection_routing,
            collection_names=collection_names,
        )

    flog.debug("Leave")
    return plugin_map, collection_metadata, collection_routing
