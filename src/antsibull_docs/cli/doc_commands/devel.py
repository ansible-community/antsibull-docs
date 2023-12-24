# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Build devel ansible(-core) docs."""

from __future__ import annotations

import asyncio
import os
import os.path
import tempfile

import aiohttp
import asyncio_pool  # type: ignore[import]
from antsibull_core.ansible_core import get_ansible_core
from antsibull_core.collections import install_together
from antsibull_core.dependency_files import parse_pieces_file
from antsibull_core.galaxy import CollectionDownloader, DownloadResults, GalaxyContext
from antsibull_core.logging import log
from antsibull_core.venv import FakeVenvRunner, VenvRunner

from ... import app_context
from ...jinja2.environment import OutputFormat
from ._build import generate_docs_for_all_collections

mlog = log.fields(mod=__name__)


async def retrieve(
    collections: list[str],
    tmp_dir: str,
    galaxy_server: str,
    ansible_core_source: str | None = None,
    collection_cache: str | None = None,
    use_installed_ansible_core: bool = False,
) -> dict[str, str]:
    """
    Download ansible-core and the latest versions of the collections.

    :arg collections: List of collection names to download.
    :arg tmp_dir: The directory to download into.
    :arg galaxy_server: URL to the galaxy server.
    :kwarg ansible_core_source: If given, a path to an ansible-core checkout or expanded sdist.
        This will be used instead of downloading an ansible-core package if the version matches
        with ``ansible_core_version``.
    :kwarg collection_cache: If given, a path to a directory containing collection tarballs.
        These tarballs will be used instead of downloading new tarballs provided that the
        versions match the criteria (latest compatible version known to galaxy).
    :kwarg use_installed_ansible_core: If ``True``, do not download ansible-core.
    :returns: Map of collection name to directory it is in.  ansible-core will
        use the special key, `_ansible_core`.
    """
    collection_dir = os.path.join(tmp_dir, "collections")
    os.mkdir(collection_dir, mode=0o700)

    requestors = {}

    lib_ctx = app_context.lib_ctx.get()
    async with aiohttp.ClientSession() as aio_session:
        context = await GalaxyContext.create(aio_session, galaxy_server=galaxy_server)
        async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
            if not use_installed_ansible_core:
                requestors["_ansible_core"] = await pool.spawn(
                    get_ansible_core(
                        aio_session,
                        "@devel",
                        tmp_dir,
                        ansible_core_source=ansible_core_source,
                    )
                )

            downloader = CollectionDownloader(
                aio_session,
                collection_dir,
                context=context,
                collection_cache=collection_cache,
            )
            for collection in collections:
                requestors[collection] = await pool.spawn(
                    downloader.download_latest_matching(collection, "*")
                )

            responses = await asyncio.gather(*requestors.values())

    responses = [
        data.download_path if isinstance(data, DownloadResults) else data
        for data in responses
    ]
    # Note: Python dicts have always had a stable order as long as you don't modify the dict.
    # So requestors (implicitly, the keys) and responses have a matching order here.
    return dict(zip(requestors, responses))


def generate_docs() -> int:
    """
    Create documentation for the devel subcommand.

    Devel documentation creates documentation for the current development version of Ansible.
    It uses the latest collection releases for the collections mentioned in the specified pieces
    file to generate rst files documenting those collections.

    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func="generate_docs")
    flog.notice("Begin generating docs")

    app_ctx = app_context.app_ctx.get()
    lib_ctx = app_context.lib_ctx.get()

    use_installed_ansible_core: bool = app_ctx.extra["use_installed_ansible_core"]

    # Parse the pieces file
    flog.fields(deps_file=app_ctx.extra["pieces_file"]).info("Parse pieces file")
    collections = parse_pieces_file(app_ctx.extra["pieces_file"])
    flog.debug("Finished parsing deps file")

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Retrieve ansible-core and the collections
        flog.fields(tmp_dir=tmp_dir).info("created tmpdir")
        collection_tarballs = asyncio.run(
            retrieve(
                collections,
                tmp_dir,
                galaxy_server=str(lib_ctx.galaxy_url),
                ansible_core_source=app_ctx.extra["ansible_core_source"],
                collection_cache=lib_ctx.collection_cache,
                use_installed_ansible_core=use_installed_ansible_core,
            )
        )
        flog.fields(tarballs=collection_tarballs).debug("Download complete")
        flog.notice("Finished retrieving tarballs")

        # Get the ansible-core location
        if use_installed_ansible_core:
            ansible_core_path = None
        else:
            try:
                ansible_core_path = collection_tarballs.pop("_ansible_core")
            except KeyError:
                print("ansible-core did not download successfully")
                return 3
            flog.fields(ansible_core_path=ansible_core_path).info(
                "ansible-core location"
            )

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

        # Create venv for ansible-core
        venv: FakeVenvRunner | VenvRunner
        if ansible_core_path is None:
            venv = FakeVenvRunner()
        else:
            venv = VenvRunner("ansible-core-venv", tmp_dir)
            venv.install_package(ansible_core_path)
            flog.fields(venv=venv).notice("Finished installing ansible-core")

        return generate_docs_for_all_collections(
            venv,
            collection_dir,
            app_ctx.extra["dest_dir"],
            OutputFormat.ANSIBLE_DOCSITE,
            breadcrumbs=app_ctx.breadcrumbs,
            use_html_blobs=app_ctx.use_html_blobs,
            fail_on_error=app_ctx.extra["fail_on_error"],
            for_official_docsite=True,
        )
