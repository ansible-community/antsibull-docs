# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""Lint extra collection documentation in docs/docsite/."""

from __future__ import annotations

import os
import os.path
import re

from sphinx_antsibull_ext import directives as antsibull_directives
from sphinx_antsibull_ext import roles as antsibull_roles

from .extra_docs import (
    ExtraDocsIndexError,
    find_extra_docs,
    lint_required_conditions,
    load_extra_docs_index,
)
from .lint_helpers import load_collection_name
from .rstcheck import check_rst_content

_RST_LABEL_DEFINITION = re.compile(r"""^\.\. _([^:]+):""")


def lint_optional_conditions(
    content: str,
    path: str,
    # pylint:disable-next=unused-argument
    collection_name: str,
) -> list[tuple[int, int, str]]:
    """Check a extra docs RST file's content for whether it satisfied the required conditions.

    Return a list of errors.
    """
    return check_rst_content(
        content,
        filename=path,
        ignore_directives=list(antsibull_directives.DIRECTIVES),
        ignore_roles=list(antsibull_roles.ROLES),
    )


def lint_collection_extra_docs_files(
    path_to_collection: str,
) -> list[tuple[str, int, int, str]]:
    try:
        collection_name = load_collection_name(path_to_collection)
    except Exception:  # pylint:disable=broad-except
        return [
            (
                path_to_collection,
                0,
                0,
                "Cannot identify collection with galaxy.yml or MANIFEST.json at this path",
            )
        ]
    result: list[tuple[str, int, int, str]] = []
    all_labels = set()
    docs = find_extra_docs(path_to_collection)
    for doc in docs:
        try:
            # Load content
            with open(doc[0], encoding="utf-8") as f:
                content = f.read()
            # Rstcheck
            errors = lint_optional_conditions(content, doc[0], collection_name)
            result.extend((doc[0], line, col, msg) for (line, col, msg) in errors)
            # Lint labels
            labels, errors = lint_required_conditions(content, collection_name)
            all_labels.update(labels)
            result.extend((doc[0], line, col, msg) for (line, col, msg) in errors)
        except Exception as e:  # pylint:disable=broad-except
            result.append((doc[0], 0, 0, str(e)))
    index_path = os.path.join(path_to_collection, "docs", "docsite", "extra-docs.yml")
    try:
        _, index_errors = load_extra_docs_index(index_path)
        result.extend((index_path, 0, 0, error) for error in index_errors)
    except ExtraDocsIndexError as exc:
        if len(docs) > 0:
            # Only report the missing index_path as an error if we found documents
            result.append((index_path, 0, 0, str(exc)))
    return result
