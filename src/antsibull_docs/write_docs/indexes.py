# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output indexes."""

from __future__ import annotations

import asyncio
import os
import os.path
from collections.abc import Mapping

import asyncio_pool  # type: ignore[import]
from antsibull_core import app_context
from antsibull_core.logging import log
from antsibull_core.utils.io import write_file
from jinja2 import Template

from ..docs_parsing import AnsibleCollectionMetadata
from ..env_variables import EnvironmentVariableInfo
from ..jinja2 import FilenameGenerator, OutputFormat
from ..jinja2.environment import doc_environment, get_template_filename
from ..utils.collection_name_transformer import CollectionNameTransformer
from . import PluginCollectionInfoT, _render_template

mlog = log.fields(mod=__name__)


async def write_callback_type_index(
    callback_type: str,
    per_collection_plugins: Mapping[str, Mapping[str, str]],
    template: Template,
    dest_filename: str,
    for_official_docsite: bool = False,
) -> None:
    """
    Write an index page for each plugin type.

    :arg callback_type: The callback plugin type to write the index for.
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
        callback_type=callback_type,
        per_collection_plugins=per_collection_plugins,
        for_official_docsite=for_official_docsite,
    )

    await write_file(dest_filename, index_contents)


async def write_plugin_type_index(
    plugin_type: str,
    per_collection_plugins: Mapping[str, Mapping[str, str]],
    # pylint:disable-next=unused-argument
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    template: Template,
    dest_filename: str,
    for_official_docsite: bool = False,
) -> None:
    """
    Write an index page for each plugin type.

    :arg plugin_type: The plugin type to write the index for.
    :arg per_collection_plugins: Mapping of collection_name to Mapping of plugin_name to
        short_description.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
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


async def output_callback_indexes(
    plugin_info: PluginCollectionInfoT,
    dest_dir: str,
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,
    for_official_docsite: bool = False,
    referable_envvars: set[str] | None = None,
) -> None:
    """
    Generate top-level callback plugin index pages for all callback plugins of a type in all
    collections.

    :arg plugin_info: Mapping of callback_type to Mapping of collection_name to Mapping of
        plugin_name to short_description.
    :arg dest_dir: The directory to place the documentation in.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg referable_envvars: Optional set of environment variables that can be referenced.
    :kwarg output_format: The output format to use.
    """
    flog = mlog.fields(func="output_callback_indexes")
    flog.debug("Enter")

    env = doc_environment(
        collection_url=collection_url,
        collection_install=collection_install,
        referable_envvars=referable_envvars,
        output_format=output_format,
        filename_generator=filename_generator,
    )
    # Get the templates
    plugin_list_tmpl = env.get_template(
        get_template_filename("list_of_callback_plugins", output_format)
    )

    collection_toplevel = os.path.join(dest_dir, "collections")
    flog.fields(
        toplevel=collection_toplevel, exists=os.path.isdir(collection_toplevel)
    ).debug("collection_toplevel exists?")
    # This is only safe because we made sure that the top of the directory tree we're writing to
    # (docs/docsite/rst) is only writable by us.
    os.makedirs(collection_toplevel, mode=0o755, exist_ok=True)

    writers = []
    lib_ctx = app_context.lib_ctx.get()
    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for callback_type, per_collection_data in plugin_info.items():
            filename = os.path.join(
                collection_toplevel,
                f"callback_index_{callback_type}{output_format.output_extension}",
            )
            writers.append(
                await pool.spawn(
                    write_callback_type_index(
                        callback_type,
                        per_collection_data,
                        plugin_list_tmpl,
                        filename,
                        for_official_docsite=for_official_docsite,
                    )
                )
            )

        await asyncio.gather(*writers)

    flog.debug("Leave")


async def output_plugin_indexes(
    plugin_info: PluginCollectionInfoT,
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    dest_dir: str,
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,
    for_official_docsite: bool = False,
    referable_envvars: set[str] | None = None,
) -> None:
    """
    Generate top-level plugin index pages for all plugins of a type in all collections.

    :arg plugin_info: Mapping of plugin_type to Mapping of collection_name to Mapping of
        plugin_name to short_description.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :arg dest_dir: The directory to place the documentation in.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg referable_envvars: Optional set of environment variables that can be referenced.
    :kwarg output_format: The output format to use.
    """
    flog = mlog.fields(func="output_plugin_indexes")
    flog.debug("Enter")

    env = doc_environment(
        collection_url=collection_url,
        collection_install=collection_install,
        referable_envvars=referable_envvars,
        output_format=output_format,
        filename_generator=filename_generator,
    )
    # Get the templates
    plugin_list_tmpl = env.get_template(
        get_template_filename("list_of_plugins", output_format)
    )

    collection_toplevel = os.path.join(dest_dir, "collections")
    flog.fields(
        toplevel=collection_toplevel, exists=os.path.isdir(collection_toplevel)
    ).debug("collection_toplevel exists?")
    # This is only safe because we made sure that the top of the directory tree we're writing to
    # (docs/docsite/rst) is only writable by us.
    os.makedirs(collection_toplevel, mode=0o755, exist_ok=True)

    writers = []
    lib_ctx = app_context.lib_ctx.get()
    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for plugin_type, per_collection_data in plugin_info.items():
            filename = os.path.join(
                collection_toplevel,
                f"index_{plugin_type}{output_format.output_extension}",
            )
            writers.append(
                await pool.spawn(
                    write_plugin_type_index(
                        plugin_type,
                        per_collection_data,
                        collection_metadata,
                        plugin_list_tmpl,
                        filename,
                        for_official_docsite=for_official_docsite,
                    )
                )
            )

        await asyncio.gather(*writers)

    flog.debug("Leave")


async def output_environment_variables(
    dest_dir: str,
    env_variables: Mapping[str, EnvironmentVariableInfo],
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,
    squash_hierarchy: bool = False,
    referable_envvars: set[str] | None = None,
) -> None:
    """
    Write environment variable Generate collection-level index pages for the collections.

    :arg dest_dir: The directory to place the documentation in.
    :arg env_variables: Mapping of environment variable names to environment variable information.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    :kwarg referable_envvars: Optional set of environment variables that can be referenced.
    :kwarg output_format: The output format to use.
    """
    flog = mlog.fields(func="write_environment_variables")
    flog.debug("Enter")

    if not squash_hierarchy:
        collection_toplevel = os.path.join(dest_dir, "collections")
    else:
        collection_toplevel = dest_dir

    env = doc_environment(
        referable_envvars=referable_envvars,
        output_format=output_format,
        filename_generator=filename_generator,
    )
    # Get the templates
    env_var_list_tmpl = env.get_template(
        get_template_filename("list_of_env_variables", output_format)
    )

    flog.fields(
        toplevel=collection_toplevel, exists=os.path.isdir(collection_toplevel)
    ).debug("collection_toplevel exists?")
    # This is only safe because we made sure that the top of the directory tree we're writing to
    # (docs/docsite/rst) is only writable by us.
    os.makedirs(collection_toplevel, mode=0o755, exist_ok=True)

    index_file = os.path.join(
        collection_toplevel, f"environment_variables{output_format.output_extension}"
    )
    index_contents = _render_template(
        env_var_list_tmpl,
        index_file,
        env_variables=env_variables,
    )

    await write_file(index_file, index_contents)

    flog.debug("Leave")
