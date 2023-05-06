# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""
Add roles for semantic markup.
"""

from __future__ import annotations

import typing as t

from docutils import nodes
from sphinx import addnodes

from antsibull_docs.markup.semantic_helper import parse_option, parse_return_value


# pylint:disable-next=unused-argument,dangerous-default-value
def option_choice(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible option choice entry.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return [nodes.literal(rawtext, text, classes=["ansible-option-choices-entry"])], []


# pylint:disable-next=unused-argument,dangerous-default-value
def option_choice_default(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible option choice entry that is the default.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return [nodes.literal(rawtext, text, classes=["ansible-option-default-bold"])], []


# pylint:disable-next=unused-argument,dangerous-default-value
def option_default(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible option default value.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return [nodes.literal(rawtext, text, classes=["ansible-option-default"])], []


# pylint:disable-next=unused-argument,dangerous-default-value
def return_value_sample(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible return value sample value.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return [nodes.literal(rawtext, text, classes=["ansible-option-sample"])], []


def _create_option_reference(
    plugin_fqcn: str | None,
    plugin_type: str | None,
    entrypoint: str | None,
    option: str,
) -> str | None:
    if not plugin_fqcn or not plugin_type:
        return None
    ref = option.replace(".", "/")
    ep = f"{entrypoint}__" if entrypoint is not None else ""
    return f"ansible_collections.{plugin_fqcn}_{plugin_type}__parameter-{ep}{ref}"


def _create_return_value_reference(
    plugin_fqcn: str | None,
    plugin_type: str | None,
    entrypoint: str | None,
    return_value: str,
) -> str | None:
    if not plugin_fqcn or not plugin_type:
        return None
    ref = return_value.replace(".", "/")
    ep = f"{entrypoint}__" if entrypoint is not None else ""
    return f"ansible_collections.{plugin_fqcn}_{plugin_type}__return-{ep}{ref}"


def _create_ref_or_not(
    create_ref: t.Callable[[str | None, str | None, str | None, str], str | None],
    plugin_fqcn: str | None,
    plugin_type: str | None,
    entrypoint: str | None,
    ref_parameter: str,
    text: str,
) -> tuple[str, list[t.Any]]:
    ref = create_ref(plugin_fqcn, plugin_type, entrypoint, ref_parameter)
    if ref is None:
        return text, []

    # The content node will be replaced by Sphinx anyway, so it doesn't matter what kind
    # of node we are using...
    content = nodes.literal(text, text)

    options = {
        "reftype": "ref",
        "refdomain": "std",
        "refexplicit": True,
        "refwarn": True,
    }
    refnode = addnodes.pending_xref(text, content, **options)
    refnode["reftarget"] = ref
    return "", [refnode]


# pylint:disable-next=unused-argument
def _create_error(rawtext: str, text: str, error: str) -> tuple[list[t.Any], list[str]]:
    node = ...  # FIXME
    return [node], []


# pylint:disable-next=unused-argument,dangerous-default-value
def option_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible option key, or option key-value.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    classes = []
    try:
        plugin_fqcn, plugin_type, entrypoint, option_link, option, value = parse_option(
            text.replace("\x00", ""), "", "", require_plugin=False
        )
    except ValueError as exc:
        return _create_error(rawtext, text, str(exc))
    if value is None:
        text = f"{option}"
        classes.append("ansible-option")
    else:
        text = f"{option}={value}"
        classes.append("ansible-option-value")
    text, subnodes = _create_ref_or_not(
        _create_option_reference,
        plugin_fqcn,
        plugin_type,
        entrypoint,
        option_link,
        text,
    )
    if value is None:
        content = nodes.strong(rawtext, text, *subnodes)
        content = nodes.literal(rawtext, "", content, classes=classes)
    else:
        content = nodes.literal(rawtext, text, *subnodes, classes=classes)
    return [content], []


# pylint:disable-next=unused-argument,dangerous-default-value
def value_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible option value.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return [nodes.literal(rawtext, text, classes=["ansible-value"])], []


# pylint:disable-next=unused-argument,dangerous-default-value
def return_value_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible option value.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    classes = ["ansible-return-value"]
    try:
        plugin_fqcn, plugin_type, entrypoint, rv_link, rv, value = parse_return_value(
            text.replace("\x00", ""), "", "", require_plugin=False
        )
    except ValueError as exc:
        return _create_error(rawtext, text, str(exc))
    if value is None:
        text = f"{rv}"
    else:
        text = f"{rv}={value}"
    text, subnodes = _create_ref_or_not(
        _create_return_value_reference,
        plugin_fqcn,
        plugin_type,
        entrypoint,
        rv_link,
        text,
    )
    return [nodes.literal(rawtext, text, *subnodes, classes=classes)], []


ROLES = {
    "ansible-option-choices-entry": option_choice,
    "ansible-option-choices-entry-default": option_choice_default,
    "ansible-option-default": option_default,
    "ansible-rv-sample-value": return_value_sample,
    "ansopt": option_role,
    "ansval": value_role,
    "ansretval": return_value_role,
}


def setup_roles(app):
    """
    Setup roles for a Sphinx app object.
    """
    for name, role in ROLES.items():
        app.add_role(name, role)
