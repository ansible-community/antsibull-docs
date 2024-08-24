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
from antsibull_changelog.changes import load_changes
from antsibull_changelog.config import ChangelogConfig, CollectionDetails, PathsConfig
from antsibull_changelog.rendering.changelog import (
    ChangelogGenerator,
    create_document_renderer,
)
from antsibull_core import app_context
from antsibull_core.logging import log

from ..docs_parsing import AnsibleCollectionMetadata
from ..jinja2 import OutputFormat
from . import CollectionInfoT, _get_collection_dir
from .io import Output

mlog = log.fields(mod=__name__)


async def write_changelog(
    output: Output,
    collection_name: str,
    collection_dir: str,
    collection_metadata: AnsibleCollectionMetadata,
    output_format: OutputFormat,
):
    """
    Write a changelog for each collection.

    :arg collection_name: The collection's full name.
    :arg collection_dir: The destination directory to output the changelog into.
    :arg collection_metadata: Metadata for the collection.
    :arg output_format: The output format to use.
    """
    flog = mlog.fields(func="write_changelog")
    flog.debug("Enter")

    try:
        paths = PathsConfig.force_collection(collection_metadata.path)

        collection_details = CollectionDetails(paths)
        collection_details.namespace, collection_details.name = collection_name.split(
            ".", 1
        )
        collection_details.version = collection_metadata.version
        collection_details.flatmap = collection_metadata.docs_config.flatmap

        config = ChangelogConfig.default(paths, collection_details)
        config.title = collection_name.title()
        config.use_fqcn = True
        config.mention_ancestor = True
        config.flatmap = collection_metadata.docs_config.flatmap

        changes = load_changes(config)

        if not changes.has_release:
            changelog_contents = f"The changelog of {collection_name} is empty."
        else:
            generator = ChangelogGenerator(config, changes)

            renderer = create_document_renderer(output_format.changelog_format)
            generator.generate(renderer)

            changelog_contents = renderer.render()
            for warning in renderer.get_warnings():
                flog.warning(warning)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        flog.warning(f"Error while processing changelog for {collection_name}: {exc}")
        changelog_contents = f"""
The changelog of {collection_name} could not be rendered:

.. code-block:: text

  {exc}
"""

    changelog_file = os.path.join(
        collection_dir, f"changelog{output_format.output_extension}"
    )
    await output.write_file(changelog_file, changelog_contents)

    flog.debug("Leave")


async def output_changelogs(
    collection_to_plugin_info: CollectionInfoT,
    output: Output,
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    output_format: OutputFormat,
    squash_hierarchy: bool = False,
) -> None:
    """
    Generate collection changelogs if requested.

    :arg collection_to_plugin_info: Mapping of collection_name to Mapping of plugin_type to
        Mapping of plugin_name to short_description.
    :arg output: Output helper for writing output.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :kwarg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
        Undefined behavior if documentation for multiple collections are created.
    :kwarg output_format: The output format to use.
    """
    flog = mlog.fields(func="output_changelogs")
    flog.debug("Enter")

    if collection_metadata is None:
        collection_metadata = {}

    writers = []
    lib_ctx = app_context.lib_ctx.get()

    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name in collection_to_plugin_info:
            metadata = collection_metadata[collection_name]
            if not metadata.docs_config.changelog.write_changelog:
                continue

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
                    write_changelog(
                        output,
                        collection_name,
                        collection_dir,
                        collection_metadata[collection_name],
                        output_format,
                    )
                )
            )

        await asyncio.gather(*writers)

    flog.debug("Leave")
