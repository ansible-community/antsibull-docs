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
import typing as t

from antsibull_docutils.utils import parse_document
from docutils import nodes
from docutils.parsers.rst import Directive as _DocutilsDirective
from docutils.utils import unescape as _docutils_unescape

from sphinx_antsibull_ext import directives as antsibull_directives
from sphinx_antsibull_ext import roles as antsibull_roles
from sphinx_antsibull_ext.sphinx_helper import extract_explicit_title

from .extra_docs import (
    ExtraDocsIndexError,
    find_extra_docs,
    lint_required_conditions,
    load_extra_docs_index,
)
from .lint_collection_names import CollectionNameLinter, Plugin
from .lint_helpers import load_collection_name
from .markup.semantic_helper import (
    parse_collection_name,
    parse_option,
    parse_plugin_name,
    parse_return_value,
)
from .rstcheck import check_rst_content

_RST_LABEL_DEFINITION = re.compile(r"""^\.\. _([^:]+):""")


def _validate_option(value: str, names_linter: CollectionNameLinter) -> None:
    plugin_fqcn, plugin_type, entrypoint, option_link, option, _ = parse_option(
        value, "", "", require_plugin=False
    )
    plugin = None
    if plugin_fqcn and plugin_type:
        plugin = Plugin(
            plugin_fqcn=plugin_fqcn,
            plugin_type=plugin_type,
            role_entrypoint=entrypoint,
        )
    for error in names_linter.validate_option_name(
        plugin, option, option_link.split(".")
    ):
        raise ValueError(error)


def _validate_return_value(value: str, names_linter: CollectionNameLinter) -> None:
    plugin_fqcn, plugin_type, entrypoint, rv_link, rv, _ = parse_return_value(
        value, "", "", require_plugin=False
    )
    plugin = None
    if plugin_fqcn and plugin_type:
        plugin = Plugin(
            plugin_fqcn=plugin_fqcn,
            plugin_type=plugin_type,
            role_entrypoint=entrypoint,
        )
    for error in names_linter.validate_return_value(plugin, rv, rv_link.split(".")):
        raise ValueError(error)


def _validate_plugin(value: str, names_linter: CollectionNameLinter) -> None:
    plugin_fqcn, plugin_type, entrypoint = parse_plugin_name(value)
    for error in names_linter.validate_plugin_fqcn(
        Plugin(
            plugin_fqcn=plugin_fqcn, plugin_type=plugin_type, role_entrypoint=entrypoint
        )
    ):
        raise ValueError(error)


def _validate_collection(value: str, names_linter: CollectionNameLinter) -> None:
    collection_name, what = parse_collection_name(value)
    for error in names_linter.validate_collection_name(collection_name):
        raise ValueError(error)
    if what.startswith("plugins-"):
        plugin_type = what[len("plugins-") :]
        if not names_linter.has_plugins_of_type(collection_name, plugin_type):
            raise ValueError(f"{collection_name} has no {plugin_type} plugins")


def get_names_linter_roles(
    names_linter: CollectionNameLinter, errors: list[tuple[int, int, str]]
) -> dict[str, t.Any]:
    def wrap(
        value: str,
        rawtext: str,
        lineno: int,
        validator: t.Callable[[str, CollectionNameLinter], None],
    ):
        try:
            validator(value, names_linter)
            return [], []
        except ValueError as exc:
            errors.append((lineno, 0, f"{rawtext}: {exc}"))
            return [], []

    # pylint:disable-next=unused-argument,dangerous-default-value
    def option_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        return wrap(_docutils_unescape(text), rawtext, lineno, _validate_option)

    # pylint:disable-next=unused-argument,dangerous-default-value
    def return_value_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        return wrap(_docutils_unescape(text), rawtext, lineno, _validate_return_value)

    # pylint:disable-next=unused-argument,dangerous-default-value
    def plugin_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        target, _ = extract_explicit_title(text)
        return wrap(target, rawtext, lineno, _validate_plugin)

    # pylint:disable-next=unused-argument,dangerous-default-value
    def collection_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        target, _ = extract_explicit_title(text)
        return wrap(target, rawtext, lineno, _validate_collection)

    return {
        "ansopt": option_role,
        "ansretval": return_value_role,
        "ansplugin": plugin_role,
        "anscollection": collection_role,
    }


class _IgnoredDirective(_DocutilsDirective):
    has_content = True

    def run(self):
        return []


# pylint:disable-next=unused-argument,dangerous-default-value
def _ignored_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    return [], []


def load_document_and_optionally_check_antsibull_roles(
    *,
    content: str,
    path: str,
    names_linter: CollectionNameLinter | None,
) -> tuple[list[tuple[int, int, str]], nodes.document | None]:
    errors: list[tuple[int, int, str]] = []

    roles = {}
    for role_name in antsibull_roles.ROLES:
        roles[role_name] = _ignored_role
    if names_linter:
        for role_name, role in get_names_linter_roles(names_linter, errors).items():
            roles[role_name] = role

    directives = {}
    for directive_name in antsibull_directives.DIRECTIVES:
        directives[directive_name] = _IgnoredDirective

    try:
        doc = parse_document(
            content,
            path=path,
            root_prefix=".",
            rst_directives=directives,
            rst_local_roles=roles,
            parser_name="restructuredtext",
        )
        return errors, doc
    except ValueError as exc:
        return [(0, 0, f"{exc}")], None


def lint_optional_conditions(
    *,
    content: str,
    path: str,
    # pylint:disable-next=unused-argument
    collection_name: str,
) -> list[tuple[int, int, str]]:
    """Check a extra docs RST file's content for whether it satisfied the required conditions.

    Return a list of errors.
    """
    ignore_roles = list(antsibull_roles.ROLES)
    ignore_directives = list(antsibull_directives.DIRECTIVES)
    return check_rst_content(
        content,
        filename=path,
        ignore_directives=ignore_directives,
        ignore_roles=ignore_roles,
    )


def _check_file(
    path: str,
    collection_name: str,
    names_linter: CollectionNameLinter | None,
    result: list[tuple[str, int, int, str]],
) -> list[str]:
    try:
        # Load content
        with open(path, encoding="utf-8") as f:
            content = f.read()
        # Rstcheck
        errors = lint_optional_conditions(
            content=content,
            path=path,
            collection_name=collection_name,
        )
        result.extend((path, line, col, msg) for (line, col, msg) in errors)
        # Check Ansible names
        errors, _ = load_document_and_optionally_check_antsibull_roles(
            content=content,
            path=path,
            names_linter=names_linter,
        )
        result.extend((path, line, col, msg) for (line, col, msg) in errors)
        # Lint labels
        labels, errors = lint_required_conditions(
            content=content, collection_name=collection_name
        )
        result.extend((path, line, col, msg) for (line, col, msg) in errors)
        return labels
    except Exception as e:  # pylint:disable=broad-except
        result.append((path, 0, 0, str(e)))
        return []


def lint_collection_extra_docs_files(
    path_to_collection: str,
    *,
    collection_name: str | None = None,
    names_linter: CollectionNameLinter | None = None,
) -> list[tuple[str, int, int, str]]:
    if collection_name is None:
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
    all_labels: set[str] = set()
    docs = find_extra_docs(path_to_collection)
    for doc in docs:
        all_labels.update(_check_file(doc[0], collection_name, names_linter, result))
    index_path = os.path.join(path_to_collection, "docs", "docsite", "extra-docs.yml")
    try:
        _, index_errors = load_extra_docs_index(index_path)
        result.extend((index_path, 0, 0, error) for error in index_errors)
    except ExtraDocsIndexError as exc:
        if len(docs) > 0:
            # Only report the missing index_path as an error if we found documents
            result.append((index_path, 0, 0, str(exc)))
    return result
