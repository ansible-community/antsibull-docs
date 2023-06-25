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
from antsibull_docs.utils.rst import massage_rst_label


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
    ref = massage_rst_label(option.replace(".", "/"))
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
    ref = massage_rst_label(return_value.replace(".", "/"))
    ep = f"{entrypoint}__" if entrypoint is not None else ""
    return f"ansible_collections.{plugin_fqcn}_{plugin_type}__return-{ep}{ref}"


def _create_ref_or_not(
    create_ref: t.Callable[[str | None, str | None, str | None, str], str | None],
    plugin_fqcn: str | None,
    plugin_type: str | None,
    entrypoint: str | None,
    ref_parameter: str,
    text: str,
) -> t.Any:
    # When successfully resolving *internal* references, Sphinx does **NOT**
    # use the node we provide, but simply extracts the text and creates a new
    # node. Thus we use nodes.inline so that the result is the same no matter
    # whether the reference was internal, not resolved, or external
    # (intersphinx).
    content = nodes.inline(text, text)
    ref = create_ref(plugin_fqcn, plugin_type, entrypoint, ref_parameter)
    if ref is None:
        return content

    options = {
        "reftype": "ref",
        "refdomain": "std",
        "refexplicit": True,
        "refwarn": True,
    }
    refnode = addnodes.pending_xref(text, content, **options)
    refnode["reftarget"] = ref
    return refnode


# pylint:disable-next=unused-argument
def _create_error(rawtext: str, text: str, error: str) -> tuple[list[t.Any], list[str]]:
    content = nodes.strong(text, error, classes=["error"])
    return [content], []


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
    content = _create_ref_or_not(
        _create_option_reference,
        plugin_fqcn,
        plugin_type,
        entrypoint,
        option_link,
        text,
    )
    if value is None:
        content = nodes.strong(rawtext, "", content)
    return [nodes.literal(rawtext, "", content, classes=classes)], []


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
    content = _create_ref_or_not(
        _create_return_value_reference,
        plugin_fqcn,
        plugin_type,
        entrypoint,
        rv_link,
        text,
    )
    return [nodes.literal(rawtext, "", content, classes=classes)], []


# pylint:disable-next=unused-argument,dangerous-default-value
def environment_variable(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format environment variable with possible assignment, without reference.

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
    classes = ["xref", "std", "std-envvar"]
    return [nodes.literal(rawtext, text, classes=classes)], []


# pylint:disable-next=dangerous-default-value
def environment_variable_reference(
    name,  # pylint:disable=unused-argument
    rawtext,
    text,
    lineno,  # pylint:disable=unused-argument
    inliner,  # pylint:disable=unused-argument
    options={},
    content=[],
):
    # Extract the name of the environment variable
    ref = text.replace("\x00", "").split("=", 1)[0].strip()

    classes = ["xref", "std", "std-envvar"]
    content = nodes.literal(rawtext, text, classes=classes)

    options = {
        "reftype": "envvar",
        "refdomain": "std",
        "refexplicit": True,
        "refwarn": True,
    }
    refnode = addnodes.pending_xref(text, content, **options)
    refnode["reftarget"] = ref

    return [refnode], []


ROLES = {
    "ansible-option-choices-entry": option_choice,
    "ansible-option-choices-entry-default": option_choice_default,
    "ansible-option-default": option_default,
    "ansible-rv-sample-value": return_value_sample,
    "ansopt": option_role,
    "ansval": value_role,
    "ansretval": return_value_role,
    "ansenvvar": environment_variable,
    "ansenvvarref": environment_variable_reference,
}


def setup_roles(app):
    """
    Setup roles for a Sphinx app object.
    """
    for name, role in ROLES.items():
        app.add_role(name, role)
