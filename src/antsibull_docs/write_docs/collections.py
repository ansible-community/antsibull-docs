# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output collection documentation."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Mapping

import asyncio_pool  # type: ignore[import]
from antsibull_core import app_context
from antsibull_core.logging import log
from antsibull_core.schemas.collection_meta import (
    CollectionsMetadata,
    RemovedCollectionMetadata,
)
from jinja2 import Template
from packaging.specifiers import SpecifierSet

from ..collection_links import CollectionLinks
from ..docs_parsing import AnsibleCollectionMetadata
from ..extra_docs import CollectionExtraDocsInfoT
from ..jinja2 import FilenameGenerator, OutputFormat
from ..jinja2.environment import doc_environment, get_template_filename
from ..utils.collection_name_transformer import CollectionNameTransformer
from . import BasicPluginInfo, CollectionInfoT, _get_collection_dir, _render_template
from .io import Output

mlog = log.fields(mod=__name__)


def _parse_required_ansible(requires_ansible: str) -> list[str]:
    result = []
    for specifier in reversed(
        sorted(
            SpecifierSet(requires_ansible),
            key=lambda specifier: (specifier.operator, specifier.version),
        )
    ):
        if specifier.operator == ">=":
            result.append(f"{specifier.version} or newer")
        elif specifier.operator == ">":
            result.append(f"newer than {specifier.version}")
        elif specifier.operator == "<=":
            result.append(f"{specifier.version} or older")
        elif specifier.operator == "<":
            result.append(f"older than {specifier.version}")
        elif specifier.operator == "!=":
            result.append(f"version {specifier.version} is specifically not supported")
        elif specifier.operator == "==":
            result.append(f"version {specifier.version} is specifically supported")
        else:
            result.append(f"{specifier.operator} {specifier.version}")
    return result


async def write_collection_index(
    collection_name: str,
    plugin_maps: Mapping[str, Mapping[str, BasicPluginInfo]],
    template: Template,
    output: Output,
    collection_dir: str,
    collection_meta: AnsibleCollectionMetadata,
    extra_docs_data: CollectionExtraDocsInfoT,
    link_data: CollectionLinks,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,  # pylint: disable=unused-argument
    breadcrumbs: bool = True,
    for_official_docsite: bool = False,
    squash_hierarchy: bool = False,
    add_version: bool = True,
) -> None:
    """
    Write an index page for each collection.

    The per-collection index page links to plugins for each collection.

    :arg plugin_maps: Mapping of plugin_type to Mapping of plugin_name to short_description.
    :arg template: A template to render the collection index.
    :arg output: Output helper for writing output.
    :arg collection_meta: Metadata for the collection.
    :arg extra_docs_data: Extra docs data for the collection.
    :arg link_data: Links for the collection.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
        Undefined behavior if documentation for multiple collections are created.
    :kwarg add_version: If set to ``False``, will not insert antsibull-docs' version into
        the generated files.
    """
    flog = mlog.fields(func="write_collection_index")
    flog.debug("Enter")

    requires_ansible = []
    if collection_name != "ansible.builtin" and collection_meta.requires_ansible:
        try:
            requires_ansible = _parse_required_ansible(collection_meta.requires_ansible)
        except Exception as exc:  # pylint:disable=broad-except
            flog.fields(
                collection_name=collection_name,
                exception=exc,
            ).error(
                "Cannot parse required_ansible specifier set for {collection_name}",
                collection_name=collection_name,
            )
    index_file = os.path.join(collection_dir, f"index{output_format.output_extension}")
    index_contents = _render_template(
        template,
        index_file,
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
        has_changelog=collection_meta.docs_config.changelog.write_changelog,
        add_version=add_version,
        collection_deprecation_info=collection_meta.deprecation_info,
    )

    await output.write_file(index_file, index_contents)

    flog.debug("Leave")


async def write_collection_tombstone(
    collection_name: str,
    template: Template,
    output: Output,
    collection_dir: str,
    collection_metadata: RemovedCollectionMetadata,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,  # pylint: disable=unused-argument
    breadcrumbs: bool = True,
    for_official_docsite: bool = False,
    squash_hierarchy: bool = False,
    add_version: bool = True,
) -> None:
    """
    Write a tombstone page for a collection.

    :arg template: A template to render the collection tombstone.
    :arg output: Output helper for writing output.
    :arg collection_metadata: Removal metadata for the collection.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
        Undefined behavior if documentation for multiple collections are created.
    :kwarg add_version: If set to ``False``, will not insert antsibull-docs' version into
        the generated files.
    """
    flog = mlog.fields(func="write_collection_tombstone")
    flog.debug("Enter")

    index_file = os.path.join(collection_dir, f"index{output_format.output_extension}")
    index_contents = _render_template(
        template,
        index_file,
        collection_name=collection_name,
        collection_removal_version=collection_metadata.removal.version,
        breadcrumbs=breadcrumbs,
        for_official_docsite=for_official_docsite,
        squash_hierarchy=squash_hierarchy,
        add_version=add_version,
    )

    await output.write_file(index_file, index_contents)

    flog.debug("Leave")


async def output_collection_indexes(
    collection_to_plugin_info: CollectionInfoT,
    output: Output,
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    extra_docs_data: Mapping[str, CollectionExtraDocsInfoT],
    link_data: Mapping[str, CollectionLinks],
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,
    squash_hierarchy: bool = False,
    breadcrumbs: bool = True,
    for_official_docsite: bool = False,
    referable_envvars: set[str] | None = None,
    add_version: bool = True,
) -> None:
    """
    Generate collection-level index pages for the collections.

    :arg collection_to_plugin_info: Mapping of collection_name to Mapping of plugin_type to
        Mapping of plugin_name to short_description.
    :arg output: Output helper for writing output.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :arg extra_docs_data: Dictionary mapping collection names to CollectionExtraDocsInfoT.
    :arg link_data: Dictionary mapping collection names to CollectionLinks.
    :kwarg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
        Undefined behavior if documentation for multiple collections are created.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg referable_envvars: Optional set of environment variables that can be referenced.
    :kwarg output_format: The output format to use.
    :kwarg add_version: If set to ``False``, will not insert antsibull-docs' version into
        the generated files.
    """
    flog = mlog.fields(func="output_collection_indexes")
    flog.debug("Enter")

    if collection_metadata is None:
        collection_metadata = {}

    env = doc_environment(
        collection_url=collection_url,
        collection_install=collection_install,
        referable_envvars=referable_envvars,
        output_format=output_format,
        filename_generator=filename_generator,
    )
    # Get the templates
    collection_plugins_tmpl = env.get_template(
        get_template_filename("plugins_by_collection", output_format)
    )

    writers = []
    lib_ctx = app_context.lib_ctx.get()

    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name, plugin_maps in collection_to_plugin_info.items():
            namespace, collection = collection_name.split(".", 1)
            collection_dir = _get_collection_dir(
                output,
                namespace,
                collection,
                squash_hierarchy=squash_hierarchy,
                create_if_not_exists=True,
            )
            writers.append(
                await pool.spawn(
                    write_collection_index(
                        collection_name,
                        plugin_maps,
                        collection_plugins_tmpl,
                        output,
                        collection_dir,
                        collection_metadata[collection_name],
                        extra_docs_data[collection_name],
                        link_data[collection_name],
                        output_format,
                        filename_generator,
                        breadcrumbs=breadcrumbs,
                        for_official_docsite=for_official_docsite,
                        squash_hierarchy=squash_hierarchy,
                        add_version=add_version,
                    )
                )
            )

        await asyncio.gather(*writers)

    flog.debug("Leave")


async def output_collection_tombstones(
    collections_metadata: CollectionsMetadata | None,
    output: Output,
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,
    squash_hierarchy: bool = False,
    breadcrumbs: bool = True,
    for_official_docsite: bool = False,
    add_version: bool = True,
) -> None:
    """
    Generate collection-level index pages for the collections.

    :arg collections_metadata: Metadata on collections.
    :arg output: Output helper for writing output.
    :kwarg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
        Undefined behavior if documentation for multiple collections are created.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg output_format: The output format to use.
    :kwarg add_version: If set to ``False``, will not insert antsibull-docs' version into
        the generated files.
    """
    flog = mlog.fields(func="output_collection_tombstones")
    flog.debug("Enter")

    if collections_metadata is None:
        return

    env = doc_environment(
        collection_url=collection_url,
        collection_install=collection_install,
        referable_envvars=None,
        output_format=output_format,
        filename_generator=filename_generator,
    )
    # Get the templates
    collection_tombstone_tmpl = env.get_template(
        get_template_filename("collection-tombstone", output_format)
    )

    writers = []
    lib_ctx = app_context.lib_ctx.get()

    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for (
            collection_name,
            collection_meta,
        ) in collections_metadata.removed_collections.items():
            namespace, collection = collection_name.split(".", 1)
            collection_dir = _get_collection_dir(
                output,
                namespace,
                collection,
                squash_hierarchy=squash_hierarchy,
                create_if_not_exists=True,
            )
            writers.append(
                await pool.spawn(
                    write_collection_tombstone(
                        collection_name,
                        collection_tombstone_tmpl,
                        output,
                        collection_dir,
                        collection_meta,
                        output_format,
                        filename_generator,
                        breadcrumbs=breadcrumbs,
                        for_official_docsite=for_official_docsite,
                        squash_hierarchy=squash_hierarchy,
                        add_version=add_version,
                    )
                )
            )

        await asyncio.gather(*writers)

    flog.debug("Leave")


async def output_extra_docs(
    output: Output,
    extra_docs_data: Mapping[str, CollectionExtraDocsInfoT],
    squash_hierarchy: bool = False,
) -> None:
    """
    Write extra docs pages for the collections.

    :arg output: Output helper for writing output.
    :arg extra_docs_data: Dictionary mapping collection names to CollectionExtraDocsInfoT.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    """
    flog = mlog.fields(func="output_extra_docs")
    flog.debug("Enter")

    writers = []
    lib_ctx = app_context.lib_ctx.get()

    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name, (dummy, documents) in extra_docs_data.items():
            namespace, collection = collection_name.split(".", 1)
            collection_dir = _get_collection_dir(
                output,
                namespace,
                collection,
                squash_hierarchy=squash_hierarchy,
                create_if_not_exists=True,
            )
            for source_path, rel_path in documents:
                dest_path = os.path.join(collection_dir, rel_path)
                output.ensure_directory(os.path.dirname(dest_path))
                writers.append(
                    await pool.spawn(output.copy_file(source_path, dest_path))
                )

        await asyncio.gather(*writers)

    flog.debug("Leave")
