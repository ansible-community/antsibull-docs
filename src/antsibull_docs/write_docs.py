# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output documentation."""

import asyncio
import os
import os.path
import typing as t

import asyncio_pool  # type: ignore[import]

from jinja2 import Template
from packaging.specifiers import SpecifierSet

from antsibull_core import app_context
from antsibull_core.logging import log
from antsibull_core.utils.io import copy_file, write_file

from .jinja2.environment import doc_environment
from .collection_links import CollectionLinks
from .docs_parsing import AnsibleCollectionMetadata
from .env_variables import EnvironmentVariableInfo
from .extra_docs import CollectionExtraDocsInfoT
from .utils.collection_name_transformer import CollectionNameTransformer


mlog = log.fields(mod=__name__)

#: Mapping of plugins to nonfatal errors.  This is the type to use when accepting the plugin.
#: The mapping is of plugin_type: plugin_name: [error_msgs]
PluginErrorsT = t.Mapping[str, t.Mapping[str, t.Sequence[str]]]

#: Mapping to collections to plugins.
#: The mapping is collection_name: plugin_type: plugin_name: plugin_short_description
CollectionInfoT = t.Mapping[str, t.Mapping[str, t.Mapping[str, str]]]

#: Plugins grouped first by plugin type, then by collection
#: The mapping is plugin_type: collection_name: plugin_name: plugin_short_description
PluginCollectionInfoT = t.Mapping[str, t.Mapping[str, t.Mapping[str, str]]]


def _render_template(_template: Template, _name: str, **kwargs) -> str:
    try:
        return _template.render(**kwargs)
    except Exception as exc:
        raise Exception(f"Error while rendering {_name}") from exc


def follow_relative_links(path: str) -> str:
    """
    Resolve relative links for path.

    :arg path: Path to a file.
    """
    flog = mlog.fields(func='follow_relative_links')
    flog.fields(path=path).debug('Enter')

    original_path = path
    loop_detection: t.Set[str] = set()
    while True:
        if path in loop_detection:
            flog.fields(
                path=original_path,
                loop=loop_detection
            ).error(
                '{path} resulted in a loop when looking up relative symbolic links.',
                path=path,
            )
            flog.debug('Leave')
            return original_path
        loop_detection.add(path)
        if not os.path.islink(path):
            flog.fields(result=path).debug('Leave')
            return path
        flog.debug('Reading link {path}', path=path)
        link = os.readlink(path)
        if link.startswith('/'):
            flog.fields(
                original_path=original_path,
                path=path,
                link=link,
            ).error(
                'When looking up relative links for {original_path}, an absolute link'
                ' "{link}" was found for {path}.',
                original_path=original_path,
                path=path,
                link=link,
            )
            flog.debug('Leave')
            return original_path
        path = os.path.join(os.path.dirname(path), link)


def has_broken_docs(plugin_record: t.Mapping[str, t.Any], plugin_type: str) -> bool:
    """
    Determine whether the plugin record is completely broken or not.
    """
    expected_fields = ('entry_points',) if plugin_type == 'role' else ('doc', 'examples', 'return')
    return not plugin_record or not all(field in plugin_record for field in expected_fields)


def guess_relative_filename(plugin_record: t.Mapping[str, t.Any],
                            plugin_short_name: str,
                            plugin_type: str,
                            collection_name: str,
                            collection_meta: AnsibleCollectionMetadata) -> str:
    """
    Make an educated guess on the documentation source file.
    """
    if plugin_record and plugin_record.get('doc') and plugin_record['doc'].get('filename'):
        filename = follow_relative_links(plugin_record['doc']['filename'])
        return os.path.relpath(filename, collection_meta.path)
    if plugin_type == 'role':
        return f"roles/{plugin_short_name}/meta/argument_specs.yml"
    plugin_dir = (
        # Modules in ansible-core:
        'modules' if plugin_type == 'module' and collection_name == 'ansible.builtin' else
        # Modules in collections:
        'plugins/modules' if plugin_type == 'module' else
        # Plugins in ansible-core or collections:
        'plugins/' + plugin_type
    )
    # Guess path inside collection tree
    return f"{plugin_dir}/{plugin_short_name}.py"


def create_plugin_rst(collection_name: str,
                      collection_meta: AnsibleCollectionMetadata,
                      collection_links: CollectionLinks,
                      plugin_short_name: str,
                      plugin_type: str,
                      plugin_record: t.Dict[str, t.Any],
                      nonfatal_errors: t.Sequence[str],
                      plugin_tmpl: Template, error_tmpl: Template,
                      use_html_blobs: bool = False,
                      for_official_docsite: bool = False,
                      log_errors: bool = True) -> str:
    """
    Create the rst page for one plugin.

    :arg collection_name: Dotted colection name.
    :arg collection_meta: Collection metadata object.
    :arg collection_links: Collection links object.
    :arg plugin_short_name: short name for the plugin.
    :arg plugin_type: The type of the plugin.  (module, inventory, etc)
    :arg plugin_record: The record for the plugin.  doc, examples, and return are the
        toplevel fields.
    :arg nonfatal_errors: Mapping of plugin to any nonfatal errors that will be displayed in place
        of some or all of the docs
    :arg plugin_tmpl: Template for the plugin.
    :arg error_tmpl: Template to use when there wasn't enough documentation for the plugin.
    :arg use_html_blobs: If set to ``True``, will use HTML blobs for parameter and return value
                         tables instead of using RST tables.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg log_errors: Default True.  Set to False to avoid errors to be logged.
    """
    flog = mlog.fields(func='create_plugin_rst')
    flog.debug('Enter')

    plugin_name = '.'.join((collection_name, plugin_short_name))

    edit_on_github_url = None
    eog = collection_links.edit_on_github
    if eog:
        # Compose Edit on GitHub URL
        gh_path = guess_relative_filename(
            plugin_record, plugin_short_name, plugin_type, collection_name, collection_meta)
        edit_on_github_url = (
            f"https://github.com/{eog.repository}/edit/{eog.branch}/{eog.path_prefix}{gh_path}"
        )

    if has_broken_docs(plugin_record, plugin_type):
        if log_errors:
            flog.fields(plugin_type=plugin_type,
                        plugin_name=plugin_name,
                        nonfatal_errors=nonfatal_errors
                        ).error('{plugin_name} did not return correct DOCUMENTATION.  An error'
                                ' page will be generated.', plugin_name=plugin_name)
        plugin_contents = _render_template(
            error_tmpl,
            plugin_name + '_' + plugin_type,
            plugin_type=plugin_type, plugin_name=plugin_name,
            collection=collection_name,
            collection_version=collection_meta.version,
            nonfatal_errors=nonfatal_errors,
            edit_on_github_url=edit_on_github_url,
            collection_links=collection_links.links,
            collection_communication=collection_links.communication,
            collection_issue_tracker=collection_links.issue_tracker,
            for_official_docsite=for_official_docsite,
        )
    else:
        if log_errors and nonfatal_errors:
            flog.fields(plugin_type=plugin_type,
                        plugin_name=plugin_name,
                        nonfatal_errors=nonfatal_errors
                        ).error('{plugin_name} did not return correct RETURN or EXAMPLES.',
                                plugin_name=plugin_name)
        if plugin_type == 'role':
            plugin_contents = _render_template(
                plugin_tmpl,
                plugin_name + '_' + plugin_type,
                use_html_blobs=use_html_blobs,
                collection=collection_name,
                collection_version=collection_meta.version,
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                entry_points=plugin_record['entry_points'],
                nonfatal_errors=nonfatal_errors,
                edit_on_github_url=edit_on_github_url,
                collection_links=collection_links.links,
                collection_communication=collection_links.communication,
                collection_issue_tracker=collection_links.issue_tracker,
                for_official_docsite=for_official_docsite,
            )
        else:
            plugin_contents = _render_template(
                plugin_tmpl,
                plugin_name + '_' + plugin_type,
                use_html_blobs=use_html_blobs,
                collection=collection_name,
                collection_version=collection_meta.version,
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                doc=plugin_record['doc'],
                examples=plugin_record['examples'],
                returndocs=plugin_record['return'],
                nonfatal_errors=nonfatal_errors,
                edit_on_github_url=edit_on_github_url,
                collection_links=collection_links.links,
                collection_communication=collection_links.communication,
                collection_issue_tracker=collection_links.issue_tracker,
                for_official_docsite=for_official_docsite,
            )

    flog.debug('Leave')
    return plugin_contents


async def write_plugin_rst(collection_name: str,
                           collection_meta: AnsibleCollectionMetadata,
                           collection_links: CollectionLinks,
                           plugin_short_name: str, plugin_type: str,
                           plugin_record: t.Dict[str, t.Any], nonfatal_errors: t.Sequence[str],
                           plugin_tmpl: Template, error_tmpl: Template, dest_dir: str,
                           path_override: t.Optional[str] = None,
                           squash_hierarchy: bool = False,
                           use_html_blobs: bool = False,
                           for_official_docsite: bool = False) -> None:
    """
    Write the rst page for one plugin.

    :arg collection_name: Dotted colection name.
    :arg collection_meta: Collection metadata object.
    :arg collection_links: Collection links object.
    :arg plugin_short_name: short name for the plugin.
    :arg plugin_type: The type of the plugin.  (module, inventory, etc)
    :arg plugin_record: The record for the plugin.  doc, examples, and return are the
        toplevel fields.
    :arg nonfatal_errors: Mapping of plugin to any nonfatal errors that will be displayed in place
        of some or all of the docs
    :arg plugin_tmpl: Template for the plugin.
    :arg error_tmpl: Template to use when there wasn't enough documentation for the plugin.
    :arg dest_dir: Destination directory for the plugin data.  For instance,
        :file:`ansible-checkout/docs/docsite/rst/`.  The directory structure underneath this
        directory will be created if needed.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    :arg use_html_blobs: If set to ``True``, will use HTML blobs for parameter and return value
                         tables instead of using RST tables.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    flog = mlog.fields(func='write_plugin_rst')
    flog.debug('Enter')

    namespace, collection = collection_name.split('.')

    plugin_contents = create_plugin_rst(
        collection_name=collection_name,
        collection_meta=collection_meta,
        collection_links=collection_links,
        plugin_short_name=plugin_short_name,
        plugin_type=plugin_type,
        plugin_record=plugin_record,
        nonfatal_errors=nonfatal_errors,
        plugin_tmpl=plugin_tmpl,
        error_tmpl=error_tmpl,
        use_html_blobs=use_html_blobs,
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


async def output_all_plugin_rst(collection_to_plugin_info: CollectionInfoT,
                                plugin_info: t.Dict[str, t.Any],
                                nonfatal_errors: PluginErrorsT,
                                dest_dir: str,
                                collection_url: CollectionNameTransformer,
                                collection_install: CollectionNameTransformer,
                                collection_metadata: t.Mapping[str, AnsibleCollectionMetadata],
                                link_data: t.Mapping[str, CollectionLinks],
                                squash_hierarchy: bool = False,
                                use_html_blobs: bool = False,
                                for_official_docsite: bool = False) -> None:
    """
    Output rst files for each plugin.

    :arg collection_to_plugin_info: Mapping of collection_name to Mapping of plugin_type to Mapping
        of plugin_name to short_description.
    :arg plugin_info: Documentation information for all of the plugins.
    :arg nonfatal_errors: Mapping of plugins to nonfatal errors.  Using this to note on the docs
        pages when documentation wasn't formatted such that we could use it.
    :arg dest_dir: The directory to place the documentation in.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :arg link_data: Dictionary mapping collection names to CollectionLinks.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    :arg use_html_blobs: If set to ``True``, will use HTML blobs for parameter and return value
                         tables instead of using RST tables.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    # Setup the jinja environment
    env = doc_environment(
        ('antsibull_docs.data', 'docsite'),
        collection_url=collection_url,
        collection_install=collection_install)
    # Get the templates
    plugin_tmpl = env.get_template('plugin.rst.j2')
    role_tmpl = env.get_template('role.rst.j2')
    error_tmpl = env.get_template('plugin-error.rst.j2')

    writers = []
    lib_ctx = app_context.lib_ctx.get()
    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name, plugins_by_type in collection_to_plugin_info.items():
            for plugin_type, plugins in plugins_by_type.items():
                plugin_type_tmpl = plugin_tmpl
                if plugin_type == 'role':
                    plugin_type_tmpl = role_tmpl
                for plugin_short_name, dummy_ in plugins.items():
                    plugin_name = '.'.join((collection_name, plugin_short_name))
                    writers.append(await pool.spawn(
                        write_plugin_rst(collection_name,
                                         collection_metadata[collection_name],
                                         link_data[collection_name],
                                         plugin_short_name, plugin_type,
                                         plugin_info[plugin_type].get(plugin_name),
                                         nonfatal_errors[plugin_type][plugin_name],
                                         plugin_type_tmpl, error_tmpl,
                                         dest_dir, squash_hierarchy=squash_hierarchy,
                                         use_html_blobs=use_html_blobs,
                                         for_official_docsite=for_official_docsite)))

        # Write docs for each plugin
        await asyncio.gather(*writers)


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


async def write_collection_list(collections: t.Iterable[str], namespaces: t.Iterable[str],
                                template: Template, dest_dir: str,
                                breadcrumbs: bool = True,
                                for_official_docsite: bool = False) -> None:
    """
    Write an index page listing all of the collections.

    Each collection will link to an index page listing all content in the collection.

    :arg collections: Iterable of all the collection names.
    :arg namespaces: Iterable of all namespace names.
    :arg template: A template to render the collection index.
    :arg dest_dir: The destination directory to output the index into.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    index_contents = _render_template(
        template,
        dest_dir,
        collections=collections,
        namespaces=namespaces,
        breadcrumbs=breadcrumbs,
        for_official_docsite=for_official_docsite,
    )
    index_file = os.path.join(dest_dir, 'index.rst')

    await write_file(index_file, index_contents)


async def write_collection_namespace_index(namespace: str, collections: t.Iterable[str],
                                           template: Template, dest_dir: str,
                                           breadcrumbs: bool = True,
                                           for_official_docsite: bool = False) -> None:
    """
    Write an index page listing all of the collections for this namespace.

    Each collection will link to an index page listing all content in the collection.

    :arg namespace: The namespace.
    :arg collections: Iterable of all the collection names.
    :arg template: A template to render the collection index.
    :arg dest_dir: The destination directory to output the index into.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should
        be disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    index_contents = _render_template(
        template,
        dest_dir,
        namespace=namespace,
        collections=collections,
        breadcrumbs=breadcrumbs,
        for_official_docsite=for_official_docsite,
    )
    index_file = os.path.join(dest_dir, 'index.rst')

    await write_file(index_file, index_contents)


async def write_plugin_type_index(plugin_type: str,
                                  per_collection_plugins: t.Mapping[str, t.Mapping[str, str]],
                                  template: Template,
                                  dest_filename: str,
                                  for_official_docsite: bool = False) -> None:
    """
    Write an index page for each plugin type.

    :arg plugin_type: The plugin type to write the index for.
    :arg per_collection_plugins: Mapping of collection_name to Mapping of plugin_name to
        short_description.
    :arg template: A template to render the plugin index.
    :arg dest_filename: The destination filename.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    index_contents = _render_template(
        template,
        dest_filename,
        plugin_type=plugin_type,
        per_collection_plugins=per_collection_plugins,
        for_official_docsite=for_official_docsite,
    )

    await write_file(dest_filename, index_contents)


def _parse_required_ansible(requires_ansible: str) -> t.List[str]:
    result = []
    for specifier in reversed(sorted(
        SpecifierSet(requires_ansible),
        key=lambda specifier: (specifier.operator, specifier.version)
    )):
        if specifier.operator == '>=':
            result.append(f'{specifier.version} or newer')
        elif specifier.operator == '>':
            result.append(f'newer than {specifier.version}')
        elif specifier.operator == '<=':
            result.append(f'{specifier.version} or older')
        elif specifier.operator == '<':
            result.append(f'older than {specifier.version}')
        elif specifier.operator == '!=':
            result.append(f'version {specifier.version} is specifically not supported')
        elif specifier.operator == '==':
            result.append(f'version {specifier.version} is specifically supported')
        else:
            result.append(f'{specifier.operator} {specifier.version}')
    return result


async def write_plugin_lists(collection_name: str,
                             plugin_maps: t.Mapping[str, t.Mapping[str, str]],
                             template: Template,
                             dest_dir: str,
                             collection_meta: AnsibleCollectionMetadata,
                             extra_docs_data: CollectionExtraDocsInfoT,
                             link_data: CollectionLinks,
                             breadcrumbs: bool = True,
                             for_official_docsite: bool = False,
                             squash_hierarchy: bool = False) -> None:
    """
    Write an index page for each collection.

    The per-collection index page links to plugins for each collection.

    :arg plugin_maps: Mapping of plugin_type to Mapping of plugin_name to short_description.
    :arg template: A template to render the collection index.
    :arg dest_dir: The destination directory to output the index into.
    :arg collection_meta: Metadata for the collection.
    :arg extra_docs_data: Extra docs data for the collection.
    :arg link_data: Links for the collection.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
        Undefined behavior if documentation for multiple collections are created.
    """
    flog = mlog.fields(func='write_plugin_lists')
    flog.debug('Enter')

    requires_ansible = []
    if collection_name != 'ansible.builtin' and collection_meta.requires_ansible:
        try:
            requires_ansible = _parse_required_ansible(collection_meta.requires_ansible)
        except Exception as exc:  # pylint:disable=broad-except
            flog.fields(
                collection_name=collection_name,
                exception=exc,
            ).error(
                'Cannot parse required_ansible specifier set for {collection_name}',
                collection_name=collection_name,
            )
    index_contents = _render_template(
        template,
        dest_dir,
        collection_name=collection_name,
        plugin_maps=plugin_maps,
        collection_version=collection_meta.version,
        requires_ansible=requires_ansible,
        link_data=link_data,
        breadcrumbs=breadcrumbs,
        extra_docs_sections=extra_docs_data[0],
        collection_authors=link_data.authors,
        collection_description=link_data.description,
        collection_links=link_data.links,
        collection_communication=link_data.communication,
        for_official_docsite=for_official_docsite,
        squash_hierarchy=squash_hierarchy,
    )

    # This is only safe because we made sure that the top of the directory tree we're writing to
    # (docs/docsite/rst) is only writable by us.
    os.makedirs(dest_dir, mode=0o755, exist_ok=True)
    index_file = os.path.join(dest_dir, 'index.rst')

    await write_file(index_file, index_contents)

    flog.debug('Leave')


async def output_collection_index(collection_to_plugin_info: CollectionInfoT,
                                  collection_namespaces: t.Mapping[str, t.List[str]],
                                  dest_dir: str,
                                  collection_url: CollectionNameTransformer,
                                  collection_install: CollectionNameTransformer,
                                  breadcrumbs: bool = True,
                                  for_official_docsite: bool = False) -> None:
    """
    Generate top-level collection index page for the collections.

    :arg collection_to_plugin_info: Mapping of collection_name to Mapping of plugin_type to
        Mapping of plugin_name to short_description.
    :arg collection_namespaces: Mapping from collection namespaces to list of collection names.
    :arg dest_dir: The directory to place the documentation in.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    flog = mlog.fields(func='output_collection_index')
    flog.debug('Enter')

    env = doc_environment(
        ('antsibull_docs.data', 'docsite'),
        collection_url=collection_url,
        collection_install=collection_install)
    # Get the templates
    collection_list_tmpl = env.get_template('list_of_collections.rst.j2')

    collection_toplevel = os.path.join(dest_dir, 'collections')
    flog.fields(toplevel=collection_toplevel, exists=os.path.isdir(collection_toplevel)).debug(
        'collection_toplevel exists?')
    # This is only safe because we made sure that the top of the directory tree we're writing to
    # (docs/docsite/rst) is only writable by us.
    os.makedirs(collection_toplevel, mode=0o755, exist_ok=True)

    await write_collection_list(collection_to_plugin_info.keys(), collection_namespaces.keys(),
                                collection_list_tmpl, collection_toplevel, breadcrumbs=breadcrumbs,
                                for_official_docsite=for_official_docsite)

    flog.debug('Leave')


async def output_collection_namespace_indexes(collection_namespaces: t.Mapping[str, t.List[str]],
                                              dest_dir: str,
                                              collection_url: CollectionNameTransformer,
                                              collection_install: CollectionNameTransformer,
                                              breadcrumbs: bool = True,
                                              for_official_docsite: bool = False) -> None:
    """
    Generate collection namespace index pages for the collections.

    :arg collection_namespaces: Mapping from collection namespaces to list of collection names.
    :arg dest_dir: The directory to place the documentation in.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    flog = mlog.fields(func='output_collection_namespace_indexes')
    flog.debug('Enter')

    env = doc_environment(
        ('antsibull_docs.data', 'docsite'),
        collection_url=collection_url,
        collection_install=collection_install)
    # Get the templates
    collection_list_tmpl = env.get_template('list_of_collections_by_namespace.rst.j2')

    writers = []
    lib_ctx = app_context.lib_ctx.get()
    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for namespace, collection_names in collection_namespaces.items():
            namespace_dir = os.path.join(dest_dir, 'collections', namespace)
            # This is only safe because we made sure that the top of the directory tree we're
            # writing to (docs/docsite/rst) is only writable by us.
            os.makedirs(namespace_dir, mode=0o755, exist_ok=True)

            writers.append(await pool.spawn(
                write_collection_namespace_index(
                    namespace, collection_names, collection_list_tmpl, namespace_dir,
                    breadcrumbs=breadcrumbs, for_official_docsite=for_official_docsite)))

        await asyncio.gather(*writers)

    flog.debug('Leave')


async def output_plugin_indexes(plugin_info: PluginCollectionInfoT,
                                dest_dir: str,
                                collection_url: CollectionNameTransformer,
                                collection_install: CollectionNameTransformer,
                                for_official_docsite: bool = False) -> None:
    """
    Generate top-level plugin index pages for all plugins of a type in all collections.

    :arg plugin_info: Mapping of plugin_type to Mapping of collection_name to Mapping of
        plugin_name to short_description.
    :arg dest_dir: The directory to place the documentation in.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    flog = mlog.fields(func='output_plugin_indexes')
    flog.debug('Enter')

    env = doc_environment(
        ('antsibull_docs.data', 'docsite'),
        collection_url=collection_url,
        collection_install=collection_install)
    # Get the templates
    plugin_list_tmpl = env.get_template('list_of_plugins.rst.j2')

    collection_toplevel = os.path.join(dest_dir, 'collections')
    flog.fields(toplevel=collection_toplevel, exists=os.path.isdir(collection_toplevel)).debug(
        'collection_toplevel exists?')
    # This is only safe because we made sure that the top of the directory tree we're writing to
    # (docs/docsite/rst) is only writable by us.
    os.makedirs(collection_toplevel, mode=0o755, exist_ok=True)

    writers = []
    lib_ctx = app_context.lib_ctx.get()
    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for plugin_type, per_collection_data in plugin_info.items():
            filename = os.path.join(collection_toplevel, f'index_{plugin_type}.rst')
            writers.append(await pool.spawn(
                write_plugin_type_index(
                    plugin_type, per_collection_data, plugin_list_tmpl, filename,
                    for_official_docsite=for_official_docsite)))

        await asyncio.gather(*writers)

    flog.debug('Leave')


async def output_indexes(collection_to_plugin_info: CollectionInfoT,
                         dest_dir: str,
                         collection_metadata: t.Mapping[str, AnsibleCollectionMetadata],
                         extra_docs_data: t.Mapping[str, CollectionExtraDocsInfoT],
                         link_data: t.Mapping[str, CollectionLinks],
                         collection_url: CollectionNameTransformer,
                         collection_install: CollectionNameTransformer,
                         squash_hierarchy: bool = False,
                         breadcrumbs: bool = True,
                         for_official_docsite: bool = False) -> None:
    """
    Generate collection-level index pages for the collections.

    :arg collection_to_plugin_info: Mapping of collection_name to Mapping of plugin_type to
        Mapping of plugin_name to short_description.
    :arg dest_dir: The directory to place the documentation in.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :arg extra_docs_data: Dictionary mapping collection names to CollectionExtraDocsInfoT.
    :arg link_data: Dictionary mapping collection names to CollectionLinks.
    :kwarg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
        Undefined behavior if documentation for multiple collections are created.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    flog = mlog.fields(func='output_indexes')
    flog.debug('Enter')

    if collection_metadata is None:
        collection_metadata = {}

    env = doc_environment(
        ('antsibull_docs.data', 'docsite'),
        collection_url=collection_url,
        collection_install=collection_install)
    # Get the templates
    collection_plugins_tmpl = env.get_template('plugins_by_collection.rst.j2')

    writers = []
    lib_ctx = app_context.lib_ctx.get()

    if not squash_hierarchy:
        collection_toplevel = os.path.join(dest_dir, 'collections')
        flog.fields(toplevel=collection_toplevel, exists=os.path.isdir(collection_toplevel)).debug(
            'collection_toplevel exists?')
        # This is only safe because we made sure that the top of the directory tree we're writing to
        # (docs/docsite/rst) is only writable by us.
        os.makedirs(collection_toplevel, mode=0o755, exist_ok=True)
    else:
        collection_toplevel = dest_dir

    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name, plugin_maps in collection_to_plugin_info.items():
            if not squash_hierarchy:
                collection_dir = os.path.join(collection_toplevel, *(collection_name.split('.')))
            else:
                collection_dir = collection_toplevel
            writers.append(await pool.spawn(
                write_plugin_lists(collection_name, plugin_maps, collection_plugins_tmpl,
                                   collection_dir, collection_metadata[collection_name],
                                   extra_docs_data[collection_name],
                                   link_data[collection_name],
                                   breadcrumbs=breadcrumbs,
                                   for_official_docsite=for_official_docsite,
                                   squash_hierarchy=squash_hierarchy)))

        await asyncio.gather(*writers)

    flog.debug('Leave')


async def output_extra_docs(dest_dir: str,
                            extra_docs_data: t.Mapping[str, CollectionExtraDocsInfoT],
                            squash_hierarchy: bool = False) -> None:
    """
    Write extra docs pages for the collections.

    :arg dest_dir: The directory to place the documentation in.
    :arg extra_docs_data: Dictionary mapping collection names to CollectionExtraDocsInfoT.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    """
    flog = mlog.fields(func='output_extra_docs')
    flog.debug('Enter')

    writers = []
    lib_ctx = app_context.lib_ctx.get()

    if not squash_hierarchy:
        collection_toplevel = os.path.join(dest_dir, 'collections')
    else:
        collection_toplevel = dest_dir

    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name, (dummy, documents) in extra_docs_data.items():
            if not squash_hierarchy:
                collection_dir = os.path.join(collection_toplevel, *(collection_name.split('.')))
            else:
                collection_dir = collection_toplevel
            for source_path, rel_path in documents:
                full_path = os.path.join(collection_dir, rel_path)
                os.makedirs(os.path.dirname(full_path), mode=0o755, exist_ok=True)
                writers.append(await pool.spawn(copy_file(source_path, full_path)))

        await asyncio.gather(*writers)

    flog.debug('Leave')


async def output_environment_variables(dest_dir: str,
                                       env_variables: t.Mapping[str, EnvironmentVariableInfo],
                                       squash_hierarchy: bool = False
                                       ) -> None:
    """
    Write environment variable Generate collection-level index pages for the collections.

    :arg dest_dir: The directory to place the documentation in.
    :arg env_variables: Mapping of environment variable names to environment variable information.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    """
    flog = mlog.fields(func='write_environment_variables')
    flog.debug('Enter')

    if not squash_hierarchy:
        collection_toplevel = os.path.join(dest_dir, 'collections')
    else:
        collection_toplevel = dest_dir

    env = doc_environment(('antsibull_docs.data', 'docsite'))
    # Get the templates
    env_var_list_tmpl = env.get_template('list_of_env_variables.rst.j2')

    flog.fields(toplevel=collection_toplevel, exists=os.path.isdir(collection_toplevel)).debug(
        'collection_toplevel exists?')
    # This is only safe because we made sure that the top of the directory tree we're writing to
    # (docs/docsite/rst) is only writable by us.
    os.makedirs(collection_toplevel, mode=0o755, exist_ok=True)

    index_file = os.path.join(collection_toplevel, 'environment_variables.rst')
    index_contents = _render_template(
        env_var_list_tmpl,
        index_file,
        env_variables=env_variables,
    )

    await write_file(index_file, index_contents)

    flog.debug('Leave')
