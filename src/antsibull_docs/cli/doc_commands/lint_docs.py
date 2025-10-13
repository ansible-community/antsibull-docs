# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Entrypoint to the antsibull-docs script."""

from __future__ import annotations

import os
import textwrap

from antsibull_core.logging import get_module_logger

from ... import app_context
from ...collection_config import lint_collection_config
from ...collection_links import lint_collection_links
from ...jinja2.environment import OutputFormat
from ...lint_collection_names import CollectionNameLinter
from ...lint_extra_docs import lint_collection_extra_docs_files
from ...lint_plugin_docs import lint_plugin_docs
from ...schemas.app_context import (
    DEFAULT_COLLECTION_INSTALL_CMD,
    DEFAULT_COLLECTION_URL_TRANSFORM,
)
from ...utils.collection_copier import (
    CollectionLoadError,
    load_collection_infos,
)
from ...utils.collection_name_transformer import CollectionNameTransformer
from ...utils.collection_names import (
    ValidCollectionRefs,
    collect_names,
)

mlog = get_module_logger(__name__)


def lint_collection_docs() -> int:
    """
    Lint collection documentation for inclusion into the collection's docsite.

    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func="lint_collection_docs")
    flog.notice("Begin collection docs linting")

    app_ctx = app_context.app_ctx.get()

    collection_root: str = app_ctx.extra["collection_root_path"]
    plugin_docs: bool = app_ctx.extra["plugin_docs"]
    validate_collections_refs: ValidCollectionRefs = app_ctx.extra[
        "validate_collections_refs"
    ]
    validate_refs_in_extra_docs: bool = app_ctx.extra["check_extra_docs_refs"]
    disallow_unknown_collection_refs: bool = app_ctx.extra[
        "disallow_unknown_collection_refs"
    ]
    skip_rstcheck: bool = app_ctx.extra["skip_rstcheck"]
    disallow_semantic_markup: bool = app_ctx.extra["disallow_semantic_markup"]
    output_format = OutputFormat.parse(app_ctx.extra["output_format"])

    flog.notice("Linting docs config file")
    errors = lint_collection_config(collection_root)

    flog.notice("Linting collection links")
    errors.extend(lint_collection_links(collection_root))

    if validate_refs_in_extra_docs or plugin_docs:
        collection_url = CollectionNameTransformer(
            app_ctx.collection_url, DEFAULT_COLLECTION_URL_TRANSFORM
        )
        collection_install = CollectionNameTransformer(
            app_ctx.collection_install,
            DEFAULT_COLLECTION_INSTALL_CMD,
        )
        try:
            flog.notice("Loading collection information")
            with load_collection_infos(
                path_to_collection=collection_root,
                copy_dependencies=validate_collections_refs != "all",
            ) as (
                collection_name,
                collections_dir,
                dependencies,
                load_errors,
            ):
                for error in load_errors:
                    errors.append((error.path, 0, 0, error.error))

                flog.notice("Collecting names of collection objects")
                (
                    name_collection,
                    new_plugin_info,
                    nonfatal_errors,
                    collection_to_plugin_info,
                    collection_metadata,
                ) = collect_names(
                    collection_name=collection_name,
                    collections_dir=collections_dir,
                    dependencies=dependencies,
                    validate_collections_refs=validate_collections_refs,
                )

                if plugin_docs:
                    flog.notice("Linting plugin docs")
                    lint_errors = lint_plugin_docs(
                        name_collection=name_collection,
                        new_plugin_info=new_plugin_info,
                        nonfatal_errors=nonfatal_errors,
                        collection_to_plugin_info=collection_to_plugin_info,
                        collection_metadata=collection_metadata,
                        collection_name=collection_name,
                        original_path_to_collection=collection_root,
                        collection_url=collection_url,
                        collection_install=collection_install,
                        validate_collections_refs=validate_collections_refs,
                        disallow_unknown_collection_refs=disallow_unknown_collection_refs,
                        skip_rstcheck=skip_rstcheck,
                        disallow_semantic_markup=disallow_semantic_markup,
                        output_format=output_format,
                    )
                    errors.extend(lint_errors)

                flog.notice("Linting extra docs files")
                names_linter = None
                if validate_refs_in_extra_docs:
                    names_linter = CollectionNameLinter(
                        collection_name=collection_name,
                        name_collection=name_collection,
                        validate_collections_refs=validate_collections_refs,
                        disallow_unknown_collection_refs=disallow_unknown_collection_refs,
                    )
                errors.extend(
                    lint_collection_extra_docs_files(
                        collection_root,
                        collection_name=collection_name,
                        names_linter=names_linter,
                    )
                )

        except CollectionLoadError as exc:
            errors.append((exc.path, 0, 0, exc.error))
    else:
        flog.notice("Linting extra docs files")
        errors.extend(lint_collection_extra_docs_files(collection_root))

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

    validate_collections_refs: ValidCollectionRefs = app_ctx.extra[
        "validate_collections_refs"
    ]
    disallow_unknown_collection_refs: bool = app_ctx.extra[
        "disallow_unknown_collection_refs"
    ]

    flog.notice("Linting plugin docs")
    collection_url = CollectionNameTransformer(
        app_ctx.collection_url, DEFAULT_COLLECTION_URL_TRANSFORM
    )
    collection_install = CollectionNameTransformer(
        app_ctx.collection_install,
        DEFAULT_COLLECTION_INSTALL_CMD,
    )

    (
        name_collection,
        new_plugin_info,
        nonfatal_errors,
        collection_to_plugin_info,
        collection_metadata,
    ) = collect_names(
        collection_name="ansible.builtin",
        collections_dir=None,
        dependencies=["ansible.builtin"],
        validate_collections_refs=validate_collections_refs,
    )
    errors = lint_plugin_docs(
        name_collection=name_collection,
        new_plugin_info=new_plugin_info,
        nonfatal_errors=nonfatal_errors,
        collection_to_plugin_info=collection_to_plugin_info,
        collection_metadata=collection_metadata,
        collection_name="ansible.builtin",
        original_path_to_collection=None,
        collection_url=collection_url,
        collection_install=collection_install,
        validate_collections_refs=validate_collections_refs,
        disallow_unknown_collection_refs=disallow_unknown_collection_refs,
        skip_rstcheck=True,
        disallow_semantic_markup=False,
        output_format=OutputFormat.ANSIBLE_DOCSITE,
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
