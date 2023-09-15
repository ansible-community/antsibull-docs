# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Parse documentation from ansible plugins using anible-doc."""

from __future__ import annotations

import typing as t
from collections.abc import Mapping, MutableMapping

from antsibull_core.logging import log
from packaging.version import Version as PypiVer

from .. import app_context
from . import AnsibleCollectionMetadata
from .ansible_doc import get_ansible_core_version
from .ansible_doc_core_213 import (
    get_ansible_plugin_info as ansible_doc_core_213_get_ansible_plugin_info,
)

if t.TYPE_CHECKING:
    from antsibull_core.venv import FakeVenvRunner, VenvRunner


mlog = log.fields(mod=__name__)


async def get_ansible_plugin_info(
    venv: VenvRunner | FakeVenvRunner,
    collection_dir: str | None,
    collection_names: list[str] | None = None,
    fetch_all_installed: bool = False,
) -> tuple[
    MutableMapping[str, MutableMapping[str, t.Any]],
    Mapping[str, AnsibleCollectionMetadata],
]:
    """
    Retrieve information about all of the Ansible Plugins.

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
                plugin_name:  # Includes namespace and collection.
                    {information from ansible-doc --json.  See the ansible-doc documentation
                     for more info.}

        The second component is a Mapping of collection names to metadata. The second mapping
        always includes the metadata for ansible.builtin, even if it was not explicitly
        mentioned in ``collection_names``.
    """
    flog = mlog.fields(func="get_ansible_plugin_info")

    app_ctx = app_context.app_ctx.get()

    doc_parsing_backend = app_ctx.doc_parsing_backend
    ansible_core_version = None
    if doc_parsing_backend == "auto":
        ansible_core_version = await get_ansible_core_version(venv)
        flog.debug(f"Ansible-core version: {ansible_core_version}")
        if ansible_core_version < PypiVer("2.13.0.dev0"):
            raise RuntimeError(
                f"Unsupported ansible-core version {ansible_core_version}. Need 2.13.0 or later."
            )
        doc_parsing_backend = "ansible-core-2.13"
        flog.debug(f"Auto-detected docs parsing backend: {doc_parsing_backend}")
    if doc_parsing_backend == "ansible-core-2.13":
        if ansible_core_version is None:
            ansible_core_version = await get_ansible_core_version(venv)
        return await ansible_doc_core_213_get_ansible_plugin_info(
            venv,
            ansible_core_version=ansible_core_version,
            collection_dir=collection_dir,
            collection_names=collection_names,
            fetch_all_installed=fetch_all_installed,
        )

    raise RuntimeError(f"Invalid value for doc_parsing_backend: {doc_parsing_backend}")
