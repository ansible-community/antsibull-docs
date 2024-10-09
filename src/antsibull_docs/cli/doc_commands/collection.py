# Author: Toshio Kuratomi <tkuratom@redhat.com>
# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Build documentation for one or more collections."""

from __future__ import annotations

import asyncio
import os
import os.path
import tempfile

import aiohttp
import asyncio_pool  # type: ignore[import]
from antsibull_core.collections import install_together
from antsibull_core.galaxy import CollectionDownloader, GalaxyContext
from antsibull_core.logging import log
from antsibull_core.venv import FakeVenvRunner

from ... import app_context
from ...jinja2.environment import OutputFormat
from ._build import generate_docs_for_all_collections

mlog = log.fields(mod=__name__)


def generate_collection_docs(
    collection_dir: str | None, output_format: OutputFormat, squash_hierarchy: bool
) -> int:
    flog = mlog.fields(func="generate_collection_docs")
    flog.debug("Begin generating docs")

    app_ctx = app_context.app_ctx.get()

    venv = FakeVenvRunner()

    return generate_docs_for_all_collections(
        venv,
        collection_dir,
        app_ctx.extra["dest_dir"],
        output_format,
        collection_names=app_ctx.extra["collections"],
        create_indexes=app_ctx.indexes and not squash_hierarchy,
        squash_hierarchy=squash_hierarchy,
        breadcrumbs=app_ctx.breadcrumbs,
        use_html_blobs=app_ctx.use_html_blobs,
        fail_on_error=app_ctx.extra["fail_on_error"],
        add_antsibull_docs_version=app_ctx.add_antsibull_docs_version,
        cleanup=app_ctx.extra["cleanup"],
    )


async def retrieve(
    collections: list[str],
    collection_version: str | None,
    tmp_dir: str,
    galaxy_server: str,
    collection_cache: str | None = None,
) -> dict[str, str]:
    """
    Download collections, with specified version if applicable.

    :arg collections: List of collection names.
    :arg collection_version: Collection version to download.
    :arg tmp_dir: The directory to download into.
    :arg galaxy_server: URL to the galaxy server.
    :kwarg collection_cache: If given, a path to a directory containing collection tarballs.
        These tarballs will be used instead of downloading new tarballs provided that the
        versions match the criteria (latest compatible version known to galaxy).
    :returns: Map of collection name to directory it is in.
    """
    collection_dir = os.path.join(tmp_dir, "collections")
    os.mkdir(collection_dir, mode=0o700)

    requestors = {}

    lib_ctx = app_context.lib_ctx.get()
    async with aiohttp.ClientSession(trust_env=True) as aio_session:
        context = await GalaxyContext.create(aio_session, galaxy_server=galaxy_server)
        async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
            downloader = CollectionDownloader(
                aio_session,
                collection_dir,
                context=context,
                collection_cache=collection_cache,
            )
            for collection in collections:
                if collection_version is None:
                    requestors[collection] = await pool.spawn(
                        downloader.download_latest_matching(collection, "*")
                    )
                else:
                    requestors[collection] = await pool.spawn(
                        downloader.download(collection, collection_version)
                    )

            responses = await asyncio.gather(*requestors.values())
            if collection_version is None:
                responses = [resp.download_path for resp in responses]

    # Note: Python dicts have always had a stable order as long as you don't modify the dict.
    # So requestors (implicitly, the keys) and responses have a matching order here.
    return dict(zip(requestors, responses))


def generate_docs() -> int:
    """
    Create documentation for the collection subcommand.

    Creates documentation for one or multiple (currently installed) collections.

    :arg args: The parsed comand line args.
    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func="generate_docs")
    flog.debug("Begin processing docs")

    app_ctx = app_context.app_ctx.get()
    lib_ctx = app_context.lib_ctx.get()

    squash_hierarchy: bool = app_ctx.extra["squash_hierarchy"]
    output_format = OutputFormat.parse(app_ctx.extra["output_format"])

    if app_ctx.extra["use_current"]:
        return generate_collection_docs(None, output_format, squash_hierarchy)

    collection_version = app_ctx.extra["collection_version"]
    if collection_version == "@latest":
        collection_version = None

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Retrieve the collections
        flog.fields(tmp_dir=tmp_dir).info("created tmpdir")
        collection_tarballs = asyncio.run(
            retrieve(
                app_ctx.extra["collections"],
                collection_version,
                tmp_dir,
                galaxy_server=str(lib_ctx.galaxy_url),
                collection_cache=lib_ctx.collection_cache,
            )
        )
        flog.fields(tarballs=collection_tarballs).debug("Download complete")
        flog.notice("Finished retrieving tarballs")

        # Install the collections to a directory

        # Directory that ansible needs to see
        collection_dir = os.path.join(tmp_dir, "installed")
        # Directory that the collections will be untarred inside of
        collection_install_dir = os.path.join(collection_dir, "ansible_collections")
        # Safe to recursively mkdir because we created the tmp_dir
        os.makedirs(collection_install_dir, mode=0o700)
        flog.fields(collection_install_dir=collection_install_dir).debug(
            "collection install dir"
        )

        # Install the collections
        asyncio.run(
            install_together(list(collection_tarballs.values()), collection_install_dir)
        )
        flog.notice("Finished installing collections")

        return generate_collection_docs(collection_dir, output_format, squash_hierarchy)
