# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Entrypoint to the antsibull-docs script."""

from __future__ import annotations

import os
import textwrap

from antsibull_core.logging import log

from ... import app_context
from ...collection_config import lint_collection_config
from ...collection_links import lint_collection_links
from ...jinja2.environment import OutputFormat
from ...lint_extra_docs import lint_collection_extra_docs_files
from ...lint_plugin_docs import lint_collection_plugin_docs, lint_core_plugin_docs
from ...schemas.app_context import (
    DEFAULT_COLLECTION_INSTALL_CMD,
    DEFAULT_COLLECTION_URL_TRANSFORM,
)
from ...utils.collection_name_transformer import CollectionNameTransformer

mlog = log.fields(mod=__name__)


def lint_collection_docs() -> int:
    """
    Lint collection documentation for inclusion into the collection's docsite.

    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func="lint_collection_docs")
    flog.notice("Begin collection docs linting")

    app_ctx = app_context.app_ctx.get()

    collection_root = app_ctx.extra["collection_root_path"]
    plugin_docs = app_ctx.extra["plugin_docs"]
    validate_collections_refs = app_ctx.extra["validate_collections_refs"]
    disallow_unknown_collection_refs = app_ctx.extra["disallow_unknown_collection_refs"]
    skip_rstcheck = app_ctx.extra["skip_rstcheck"]
    disallow_semantic_markup = app_ctx.extra["disallow_semantic_markup"]
    output_format = OutputFormat.parse(app_ctx.extra["output_format"])

    flog.notice("Linting docs config file")
    errors = lint_collection_config(collection_root)

    flog.notice("Linting extra docs files")
    errors.extend(lint_collection_extra_docs_files(collection_root))

    flog.notice("Linting collection links")
    errors.extend(lint_collection_links(collection_root))

    if plugin_docs:
        flog.notice("Linting plugin docs")
        collection_url = CollectionNameTransformer(
            app_ctx.collection_url, DEFAULT_COLLECTION_URL_TRANSFORM
        )
        collection_install = CollectionNameTransformer(
            app_ctx.collection_install,
            DEFAULT_COLLECTION_INSTALL_CMD,
        )
        errors.extend(
            lint_collection_plugin_docs(
                collection_root,
                collection_url=collection_url,
                collection_install=collection_install,
                validate_collections_refs=validate_collections_refs,
                disallow_unknown_collection_refs=disallow_unknown_collection_refs,
                skip_rstcheck=skip_rstcheck,
                disallow_semantic_markup=disallow_semantic_markup,
                output_format=output_format,
            )
        )

    messages = sorted(
        (os.path.normpath(error[0]), error[1], error[2], error[3].lstrip())
        for error in errors
    )

    for file, row, col, message in messages:
        prefix = f"{file}:{row}:{col}: "
        print(
            prefix
            + textwrap.indent(message, " " * len(prefix), lambda line: True).lstrip()
        )

    return 3 if messages else 0


def lint_core_docs() -> int:
    """
    Lint collection documentation for inclusion into the collection's docsite.

    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func="lint_core_docs")
    flog.notice("Begin ansible-core docs linting")

    app_ctx = app_context.app_ctx.get()

    validate_collections_refs = app_ctx.extra["validate_collections_refs"]
    disallow_unknown_collection_refs = app_ctx.extra["disallow_unknown_collection_refs"]

    flog.notice("Linting plugin docs")
    collection_url = CollectionNameTransformer(
        app_ctx.collection_url, DEFAULT_COLLECTION_URL_TRANSFORM
    )
    collection_install = CollectionNameTransformer(
        app_ctx.collection_install,
        DEFAULT_COLLECTION_INSTALL_CMD,
    )
    errors = lint_core_plugin_docs(
        collection_url=collection_url,
        collection_install=collection_install,
        validate_collections_refs=validate_collections_refs,
        disallow_unknown_collection_refs=disallow_unknown_collection_refs,
    )

    messages = sorted(
        (os.path.normpath(error[0]), error[1], error[2], error[3].lstrip())
        for error in errors
    )

    for file, row, col, message in messages:
        prefix = f"{file}:{row}:{col}: "
        print(
            prefix
            + textwrap.indent(message, " " * len(prefix), lambda line: True).lstrip()
        )

    return 3 if messages else 0
