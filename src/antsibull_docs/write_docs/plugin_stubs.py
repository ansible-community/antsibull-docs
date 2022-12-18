# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output plugin stubs."""

import asyncio
import os
import os.path
import typing as t

import asyncio_pool  # type: ignore[import]
from antsibull_core import app_context
from antsibull_core.logging import log
from antsibull_core.utils.io import write_file
from jinja2 import Template

from ..collection_links import CollectionLinks
from ..docs_parsing import AnsibleCollectionMetadata
from ..jinja2.environment import doc_environment
from ..utils.collection_name_transformer import CollectionNameTransformer
from . import _render_template

mlog = log.fields(mod=__name__)


async def write_stub_rst(collection_name: str, collection_meta: AnsibleCollectionMetadata,
                         collection_links: CollectionLinks,
                         plugin_short_name: str, plugin_type: str,
                         routing_data: t.Mapping[str, t.Any],
                         redirect_tmpl: Template,
                         tombstone_tmpl: Template,
                         dest_dir: str,
                         path_override: t.Optional[str] = None,
                         squash_hierarchy: bool = False,
                         for_official_docsite: bool = False) -> None:
    """
    Write the rst page for one plugin stub.

    :arg collection_name: Dotted colection name.
    :arg collection_meta: Collection metadata object.
    :arg collection_links: Collection links object.
    :arg plugin_short_name: short name for the plugin.
    :arg plugin_type: The type of the plugin.  (module, inventory, etc)
    :arg routing_data: The routing data record for the plugin stub.  tombstone, deprecation,
        redirect, redirect_is_symlink are the optional toplevel fields.
    :arg redirect_tmpl: Template for redirects.
    :arg tombstone_tmpl: Template for tombstones.
    :arg dest_dir: Destination directory for the plugin data.  For instance,
        :file:`ansible-checkout/docs/docsite/rst/`.  The directory structure underneath this
        directory will be created if needed.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    flog = mlog.fields(func='write_stub_rst')
    flog.debug('Enter')

    namespace, collection = collection_name.split('.')
    plugin_name = '.'.join((collection_name, plugin_short_name))

    if 'tombstone' in routing_data:
        plugin_contents = _render_template(
            tombstone_tmpl,
            plugin_name + '_' + plugin_type,
            plugin_type=plugin_type,
            plugin_name=plugin_name,
            collection=collection_name,
            collection_version=collection_meta.version,
            collection_links=collection_links.links,
            collection_communication=collection_links.communication,
            tombstone=routing_data['tombstone'],
            for_official_docsite=for_official_docsite,
        )
    else:  # 'redirect' in routing_data
        plugin_contents = _render_template(
            redirect_tmpl,
            plugin_name + '_' + plugin_type,
            collection=collection_name,
            collection_version=collection_meta.version,
            collection_links=collection_links.links,
            collection_communication=collection_links.communication,
            plugin_type=plugin_type,
            plugin_name=plugin_name,
            redirect=routing_data['redirect'],
            redirect_is_symlink=routing_data.get('redirect_is_symlink') or False,
            deprecation=routing_data.get('deprecation'),
            for_official_docsite=for_official_docsite,
        )

    if path_override is not None:
        plugin_file = path_override
    else:
        if squash_hierarchy:
            collection_dir = dest_dir
        else:
            collection_dir = os.path.join(dest_dir, 'collections', namespace, collection)
            # This is dangerous but the code that takes dest_dir from the user checks
            # permissions on it to make it as safe as possible.
            os.makedirs(collection_dir, mode=0o755, exist_ok=True)

        plugin_file = os.path.join(collection_dir, f'{plugin_short_name}_{plugin_type}.rst')

    await write_file(plugin_file, plugin_contents)

    flog.debug('Leave')


async def output_all_plugin_stub_rst(stubs_info: t.Mapping[
                                         str, t.Mapping[str, t.Mapping[str, t.Any]]],
                                     dest_dir: str,
                                     collection_url: CollectionNameTransformer,
                                     collection_install: CollectionNameTransformer,
                                     collection_metadata: t.Mapping[
                                         str, AnsibleCollectionMetadata],
                                     link_data: t.Mapping[str, CollectionLinks],
                                     squash_hierarchy: bool = False,
                                     for_official_docsite: bool = False) -> None:
    """
    Output rst files for each plugin stub.

    :arg stubs_info: Mapping of collection_name to Mapping of plugin_type to Mapping
        of plugin_name to routing information.
    :arg dest_dir: The directory to place the documentation in.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :arg link_data: Dictionary mapping collection names to CollectionLinks.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    # Setup the jinja environment
    env = doc_environment(
        ('antsibull_docs.data', 'docsite'),
        collection_url=collection_url,
        collection_install=collection_install)
    # Get the templates
    redirect_tmpl = env.get_template('plugin-redirect.rst.j2')
    tombstone_tmpl = env.get_template('plugin-tombstone.rst.j2')

    writers = []
    lib_ctx = app_context.lib_ctx.get()
    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name, plugins_by_type in stubs_info.items():
            for plugin_type, plugins in plugins_by_type.items():
                for plugin_short_name, routing_data in plugins.items():
                    writers.append(await pool.spawn(
                        write_stub_rst(collection_name,
                                       collection_metadata[collection_name],
                                       link_data[collection_name],
                                       plugin_short_name, plugin_type,
                                       routing_data, redirect_tmpl, tombstone_tmpl,
                                       dest_dir, squash_hierarchy=squash_hierarchy,
                                       for_official_docsite=for_official_docsite)))

        # Write docs for each plugin
        await asyncio.gather(*writers)
