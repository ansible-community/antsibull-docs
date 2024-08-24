# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""Build documentation for one or more collections."""

from __future__ import annotations

import asyncio
import os
import os.path
import tempfile

from antsibull_core.collections import install_together
from antsibull_core.logging import log
from antsibull_core.venv import FakeVenvRunner

from ... import app_context
from ...jinja2.environment import OutputFormat
from ._build import generate_docs_for_all_collections
from .collection import retrieve

mlog = log.fields(mod=__name__)


def generate_collection_plugins_docs(
    collection_dir: str | None,
    output_format: OutputFormat,
    fqcn_plugin_names: bool,
) -> int:
    flog = mlog.fields(func="generate_collection_plugins_docs")
    flog.debug("Begin generating docs")

    app_ctx = app_context.app_ctx.get()

    venv = FakeVenvRunner()

    return generate_docs_for_all_collections(
        venv,
        collection_dir,
        app_ctx.extra["dest_dir"],
        output_format,
        collection_names=list(app_ctx.extra["collection"]),
        create_indexes=False,
        create_collection_indexes=False,
        add_extra_docs=False,
        add_redirect_stubs=False,
        squash_hierarchy=True,
        breadcrumbs=app_ctx.breadcrumbs,
        use_html_blobs=app_ctx.use_html_blobs,
        fail_on_error=app_ctx.extra["fail_on_error"],
        include_collection_name_in_plugins=fqcn_plugin_names,
        add_antsibull_docs_version=app_ctx.add_antsibull_docs_version,
        cleanup=app_ctx.extra["cleanup"],
    )


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

    output_format = OutputFormat.parse(app_ctx.extra["output_format"])
    fqcn_plugin_names: bool = app_ctx.extra["fqcn_plugin_names"]

    if app_ctx.extra["use_current"]:
        return generate_collection_plugins_docs(
            None, output_format, fqcn_plugin_names=fqcn_plugin_names
        )

    collection_version = app_ctx.extra["collection_version"]
    if collection_version == "@latest":
        collection_version = None

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Retrieve the collections
        flog.fields(tmp_dir=tmp_dir).info("created tmpdir")
        collection_tarballs = asyncio.run(
            retrieve(
                list(app_ctx.extra["collection"]),
                collection_version,
                tmp_dir,
                galaxy_server=str(lib_ctx.galaxy_url),
                collection_cache=lib_ctx.collection_cache,
            )
        )
        flog.fields(tarballs=collection_tarballs).debug("Download complete")
        flog.notice("Finished retrieving tarball")

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
        flog.notice("Finished installing collection")

        return generate_collection_plugins_docs(
            collection_dir, output_format, fqcn_plugin_names=fqcn_plugin_names
        )
