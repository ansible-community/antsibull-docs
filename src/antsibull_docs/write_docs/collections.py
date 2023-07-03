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
from antsibull_core.utils.io import copy_file, write_file
from jinja2 import Template
from packaging.specifiers import SpecifierSet

from ..collection_links import CollectionLinks
from ..docs_parsing import AnsibleCollectionMetadata
from ..extra_docs import CollectionExtraDocsInfoT
from ..jinja2 import FilenameGenerator, OutputFormat
from ..jinja2.environment import doc_environment, get_template_filename
from ..utils.collection_name_transformer import CollectionNameTransformer
from . import CollectionInfoT, _render_template

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


async def write_plugin_lists(
    collection_name: str,
    plugin_maps: Mapping[str, Mapping[str, str]],
    template: Template,
    dest_dir: str,
    collection_meta: AnsibleCollectionMetadata,
    extra_docs_data: CollectionExtraDocsInfoT,
    link_data: CollectionLinks,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,  # pylint: disable=unused-argument
    breadcrumbs: bool = True,
    for_official_docsite: bool = False,
    squash_hierarchy: bool = False,
) -> None:
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
    flog = mlog.fields(func="write_plugin_lists")
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
    index_file = os.path.join(dest_dir, f"index{output_format.output_extension}")

    await write_file(index_file, index_contents)

    flog.debug("Leave")


async def output_indexes(
    collection_to_plugin_info: CollectionInfoT,
    dest_dir: str,
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
) -> None:
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
    :kwarg referable_envvars: Optional set of environment variables that can be referenced.
    :kwarg output_format: The output format to use.
    """
    flog = mlog.fields(func="output_indexes")
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

    if not squash_hierarchy:
        collection_toplevel = os.path.join(dest_dir, "collections")
        flog.fields(
            toplevel=collection_toplevel, exists=os.path.isdir(collection_toplevel)
        ).debug("collection_toplevel exists?")
        # This is only safe because we made sure that the top of the directory tree we're writing to
        # (docs/docsite/rst) is only writable by us.
        os.makedirs(collection_toplevel, mode=0o755, exist_ok=True)
    else:
        collection_toplevel = dest_dir

    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name, plugin_maps in collection_to_plugin_info.items():
            if not squash_hierarchy:
                collection_dir = os.path.join(
                    collection_toplevel, *(collection_name.split("."))
                )
            else:
                collection_dir = collection_toplevel
            writers.append(
                await pool.spawn(
                    write_plugin_lists(
                        collection_name,
                        plugin_maps,
                        collection_plugins_tmpl,
                        collection_dir,
                        collection_metadata[collection_name],
                        extra_docs_data[collection_name],
                        link_data[collection_name],
                        output_format,
                        filename_generator,
                        breadcrumbs=breadcrumbs,
                        for_official_docsite=for_official_docsite,
                        squash_hierarchy=squash_hierarchy,
                    )
                )
            )

        await asyncio.gather(*writers)

    flog.debug("Leave")


async def output_extra_docs(
    dest_dir: str,
    extra_docs_data: Mapping[str, CollectionExtraDocsInfoT],
    squash_hierarchy: bool = False,
) -> None:
    """
    Write extra docs pages for the collections.

    :arg dest_dir: The directory to place the documentation in.
    :arg extra_docs_data: Dictionary mapping collection names to CollectionExtraDocsInfoT.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    """
    flog = mlog.fields(func="output_extra_docs")
    flog.debug("Enter")

    writers = []
    lib_ctx = app_context.lib_ctx.get()

    if not squash_hierarchy:
        collection_toplevel = os.path.join(dest_dir, "collections")
    else:
        collection_toplevel = dest_dir

    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name, (dummy, documents) in extra_docs_data.items():
            if not squash_hierarchy:
                collection_dir = os.path.join(
                    collection_toplevel, *(collection_name.split("."))
                )
            else:
                collection_dir = collection_toplevel
            for source_path, rel_path in documents:
                full_path = os.path.join(collection_dir, rel_path)
                os.makedirs(os.path.dirname(full_path), mode=0o755, exist_ok=True)
                writers.append(await pool.spawn(copy_file(source_path, full_path)))

        await asyncio.gather(*writers)

    flog.debug("Leave")
