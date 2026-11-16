# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Parse documentation from ansible plugins using anible-doc from ansible-core 2.13+."""

from __future__ import annotations

import typing as t
from collections.abc import Mapping, MutableMapping

from antsibull_core.logging import get_module_logger
from packaging.version import Version as PypiVer

from . import AnsibleCollectionMetadata, _get_environment
from ._utils import call_ansible_doc as _call_ansible_doc
from ._utils import get_ansible_doc_filters as _get_ansible_doc_filters
from ._utils import limit_by_wildcards as _limit_by_wildcards
from ._utils import process_ansible_doc_output as _process_ansible_doc_output
from .ansible_doc import get_collection_metadata
from .fqcn import is_collection_name, is_wildcard_collection_name

if t.TYPE_CHECKING:
    from antsibull_core.venv import FakeVenvRunner, VenvRunner


mlog = get_module_logger(__name__)


async def get_ansible_plugin_info(
    venv: VenvRunner | FakeVenvRunner,
    ansible_core_version: PypiVer,
    collection_dir: str | None,
    collection_names: list[str] | None = None,
    fetch_all_installed: bool = False,
) -> tuple[
    MutableMapping[str, MutableMapping[str, t.Any]],
    Mapping[str, AnsibleCollectionMetadata],
]:
    """
    Retrieve information about all of the Ansible Plugins. Requires ansible-core 2.13+.

    :arg venv: A VenvRunner into which Ansible has been installed.
    :arg ansible_core_version: The version of ansible-core. Needed to figure out how
                               many filters can be provided to ansible-doc.
    :arg collection_dir: Directory in which the collections have been installed.
                         If ``None``, the collections are assumed to be in the current
                         search path for Ansible.
    :arg collection_names: Optional list of collections. If specified, will only collect
                           information for plugins in these collections.
    :arg fetch_all_installed: If set to ``True``, will also retrieve plugins of installed
        collections outside ``collection_dir`` (if specified).
    :returns: An tuple. The first component is a nested directory structure that looks like:

            plugin_type:
                plugin_name:  # Includes namespace and collection.
                    {information from ansible-doc --json.  See the ansible-doc documentation
                     for more info.}

        The second component is a Mapping of collection names to metadata.
    """
    flog = mlog.fields(func="get_ansible_plugin_info")
    flog.debug("Enter")

    env = _get_environment(
        collection_dir, keep_current_collections_path=fetch_all_installed, venv=venv
    )

    has_wildcards = collection_names is not None and any(
        is_wildcard_collection_name(cn) and not is_collection_name(cn)
        for cn in collection_names
    )

    flog.debug("Retrieving collection metadata")
    collection_metadata = await get_collection_metadata(
        venv, env, None if has_wildcards else collection_names
    )

    if has_wildcards:
        flog.debug("Restricting collection list by wildcards")
        collection_metadata, collection_names = _limit_by_wildcards(
            collection_metadata=collection_metadata,
            collection_names=collection_names or [],
        )

    flog.debug("Retrieving and loading plugin documentation")
    ansible_doc_output = await _call_ansible_doc(
        *_get_ansible_doc_filters(
            ansible_core_version, collection_names=collection_names
        ),
        env=env,
        venv=venv,
    )

    flog.debug("Processing plugin documentation")
    plugin_map = _process_ansible_doc_output(
        ansible_doc_output,
        collection_names=collection_names,
        collection_metadata=collection_metadata,
    )

    flog.debug("Leave")
    return (plugin_map, collection_metadata)
