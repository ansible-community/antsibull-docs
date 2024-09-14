# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output collection hierarchy."""

from __future__ import annotations

import asyncio
import os
import os.path
from collections.abc import Iterable, Mapping

import asyncio_pool  # type: ignore[import]
from antsibull_core import app_context
from antsibull_core.logging import log
from jinja2 import Template

from ..docs_parsing import AnsibleCollectionMetadata
from ..jinja2 import FilenameGenerator, OutputFormat
from ..jinja2.environment import doc_environment, get_template_filename
from ..utils.collection_name_transformer import CollectionNameTransformer
from . import CollectionInfoT, _render_template
from .io import Output

mlog = log.fields(mod=__name__)


async def write_collection_list(
    collections: Iterable[str],
    namespaces: Iterable[str],
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    template: Template,
    output: Output,
    directory: str,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,  # pylint: disable=unused-argument
    breadcrumbs: bool = True,
    for_official_docsite: bool = False,
    add_version: bool = True,
) -> None:
    """
    Write an index page listing all of the collections.

    Each collection will link to an index page listing all content in the collection.

    :arg collections: Iterable of all the collection names.
    :arg namespaces: Iterable of all namespace names.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :arg template: A template to render the collection index.
    :arg output: Output helper for writing output.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg add_version: If set to ``False``, will not insert antsibull-docs' version into
        the generated files.
    """
    index_file = os.path.join(directory, f"index{output_format.output_extension}")
    index_contents = _render_template(
        template,
        index_file,
        collections=collections,
        namespaces=namespaces,
        breadcrumbs=breadcrumbs,
        for_official_docsite=for_official_docsite,
        add_version=add_version,
        collection_metadata=collection_metadata,
    )

    await output.write_file(index_file, index_contents)


async def write_collection_namespace_index(
    namespace: str,
    collections: Iterable[str],
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    template: Template,
    output: Output,
    directory: str,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,  # pylint: disable=unused-argument
    breadcrumbs: bool = True,
    for_official_docsite: bool = False,
    add_version: bool = True,
) -> None:
    """
    Write an index page listing all of the collections for this namespace.

    Each collection will link to an index page listing all content in the collection.

    :arg namespace: The namespace.
    :arg collections: Iterable of all the collection names.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :arg template: A template to render the collection index.
    :arg output: Output helper for writing output.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should
        be disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg add_version: If set to ``False``, will not insert antsibull-docs' version into
        the generated files.
    """
    index_file = os.path.join(directory, f"index{output_format.output_extension}")
    index_contents = _render_template(
        template,
        index_file,
        namespace=namespace,
        collections=collections,
        breadcrumbs=breadcrumbs,
        for_official_docsite=for_official_docsite,
        add_version=add_version,
        collection_metadata=collection_metadata,
    )

    await output.write_file(index_file, index_contents)


async def output_collection_index(
    collection_to_plugin_info: CollectionInfoT,
    collection_namespaces: Mapping[str, list[str]],
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    output: Output,
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,
    breadcrumbs: bool = True,
    for_official_docsite: bool = False,
    referable_envvars: set[str] | None = None,
    add_version: bool = True,
) -> None:
    """
    Generate top-level collection index page for the collections.

    :arg collection_to_plugin_info: Mapping of collection_name to Mapping of plugin_type to
        Mapping of plugin_name to short_description.
    :arg collection_namespaces: Mapping from collection namespaces to list of collection names.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :arg output: Output helper for writing output.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg referable_envvars: Optional set of environment variables that can be referenced.
    :kwarg output_format: The output format to use.
    :kwarg add_version: If set to ``False``, will not insert antsibull-docs' version into
        the generated files.
    """
    flog = mlog.fields(func="output_collection_index")
    flog.debug("Enter")

    env = doc_environment(
        collection_url=collection_url,
        collection_install=collection_install,
        referable_envvars=referable_envvars,
        output_format=output_format,
        filename_generator=filename_generator,
    )
    # Get the templates
    collection_list_tmpl = env.get_template(
        get_template_filename("list_of_collections", output_format)
    )

    collection_toplevel = "collections"
    output.ensure_directory(collection_toplevel)

    await write_collection_list(
        collection_to_plugin_info.keys(),
        collection_namespaces.keys(),
        collection_metadata,
        collection_list_tmpl,
        output,
        collection_toplevel,
        output_format,
        filename_generator,
        breadcrumbs=breadcrumbs,
        for_official_docsite=for_official_docsite,
        add_version=add_version,
    )

    flog.debug("Leave")


async def output_collection_namespace_indexes(
    collection_namespaces: Mapping[str, list[str]],
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    output: Output,
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,
    breadcrumbs: bool = True,
    for_official_docsite: bool = False,
    referable_envvars: set[str] | None = None,
    add_version: bool = True,
) -> None:
    """
    Generate collection namespace index pages for the collections.

    :arg collection_namespaces: Mapping from collection namespaces to list of collection names.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :arg output: Output helper for writing output.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg referable_envvars: Optional set of environment variables that can be referenced.
    :kwarg output_format: The output format to use.
    :kwarg add_version: If set to ``False``, will not insert antsibull-docs' version into
        the generated files.
    """
    flog = mlog.fields(func="output_collection_namespace_indexes")
    flog.debug("Enter")

    env = doc_environment(
        collection_url=collection_url,
        collection_install=collection_install,
        referable_envvars=referable_envvars,
        output_format=output_format,
        filename_generator=filename_generator,
    )
    # Get the templates
    collection_list_tmpl = env.get_template(
        get_template_filename("list_of_collections_by_namespace", output_format)
    )

    writers = []
    lib_ctx = app_context.lib_ctx.get()
    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for namespace, collection_names in collection_namespaces.items():
            namespace_dir = os.path.join("collections", namespace)
            output.ensure_directory(namespace_dir)

            writers.append(
                await pool.spawn(
                    write_collection_namespace_index(
                        namespace,
                        collection_names,
                        collection_metadata,
                        collection_list_tmpl,
                        output,
                        namespace_dir,
                        output_format,
                        filename_generator,
                        breadcrumbs=breadcrumbs,
                        for_official_docsite=for_official_docsite,
                        add_version=add_version,
                    )
                )
            )

        await asyncio.gather(*writers)

    flog.debug("Leave")
