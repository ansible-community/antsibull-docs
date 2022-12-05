# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Parse documentation from ansible plugins using anible-doc."""

import typing as t

from packaging.version import Version as PypiVer

from antsibull_core import app_context
from antsibull_core.logging import log

from .ansible_doc import (
    get_ansible_plugin_info as ansible_doc_get_ansible_plugin_info,
    get_ansible_core_version,
)
from .ansible_internal import (
    get_ansible_plugin_info as ansible_internal_get_ansible_plugin_info,
)
from .ansible_doc_core_213 import (
    get_ansible_plugin_info as ansible_doc_core_213_get_ansible_plugin_info,
)
from . import AnsibleCollectionMetadata

if t.TYPE_CHECKING:
    from antsibull_core.venv import VenvRunner, FakeVenvRunner  # pylint:disable=unused-import


mlog = log.fields(mod=__name__)


async def get_ansible_plugin_info(venv: t.Union['VenvRunner', 'FakeVenvRunner'],
                                  collection_dir: t.Optional[str],
                                  collection_names: t.Optional[t.List[str]] = None
                                  ) -> t.Tuple[
                                    t.MutableMapping[str, t.MutableMapping[str, t.Any]],
                                    t.Mapping[str, AnsibleCollectionMetadata]]:
    """
    Retrieve information about all of the Ansible Plugins.

    :arg venv: A VenvRunner into which Ansible has been installed.
    :arg collection_dir: Directory in which the collections have been installed.
                         If ``None``, the collections are assumed to be in the current
                         search path for Ansible.
    :arg collection_names: Optional list of collections. If specified, will only collect
                           information for plugins in these collections.
    :returns: An tuple. The first component is a nested directory structure that looks like:

            plugin_type:
                plugin_name:  # Includes namespace and collection.
                    {information from ansible-doc --json.  See the ansible-doc documentation
                     for more info.}

        The second component is a Mapping of collection names to metadata. The second mapping
        always includes the metadata for ansible.builtin, even if it was not explicitly
        mentioned in ``collection_names``.
    """
    flog = mlog.fields(func='get_ansible_plugin_info')

    lib_ctx = app_context.lib_ctx.get()

    doc_parsing_backend = lib_ctx.doc_parsing_backend
    if doc_parsing_backend == 'auto':
        version = get_ansible_core_version(venv)
        flog.debug(f'Ansible-core version: {version}')
        if version < PypiVer('2.13.0.dev0'):
            doc_parsing_backend = 'ansible-internal'
        else:
            doc_parsing_backend = 'ansible-core-2.13'
        flog.debug(f'Auto-detected docs parsing backend: {doc_parsing_backend}')
    if doc_parsing_backend == 'ansible-internal':
        return await ansible_internal_get_ansible_plugin_info(
            venv, collection_dir, collection_names=collection_names)
    if doc_parsing_backend == 'ansible-doc':
        return await ansible_doc_get_ansible_plugin_info(
            venv, collection_dir, collection_names=collection_names)
    if doc_parsing_backend == 'ansible-core-2.13':
        return await ansible_doc_core_213_get_ansible_plugin_info(
            venv, collection_dir, collection_names=collection_names)

    raise Exception(f'Invalid value for doc_parsing_backend: {doc_parsing_backend}')
