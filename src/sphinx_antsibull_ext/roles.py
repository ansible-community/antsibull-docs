# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""
Add roles for semantic markup and general formatting.
"""

from __future__ import annotations

import typing as t

from docutils import nodes
from docutils.utils import unescape  # pyre-ignore[21]
from sphinx import addnodes
from sphinx.util import logging

from antsibull_docs.markup.semantic_helper import (
    parse_option,
    parse_plugin_name,
    parse_return_value,
)
from antsibull_docs.utils.rst import massage_rst_label

from .sphinx_helper import extract_explicit_title

logger = logging.getLogger(__name__)


def _plugin_ref(plugin_fqcn: str, plugin_type: str) -> str:
    return f"ansible_collections.{plugin_fqcn}_{plugin_type}"


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
    return f"{_plugin_ref(plugin_fqcn, plugin_type)}__parameter-{ep}{ref}"


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
    return f"{_plugin_ref(plugin_fqcn, plugin_type)}__return-{ep}{ref}"


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


def _create_error(rawtext: str, text: str, error: str) -> tuple[list[t.Any], list[str]]:
    content = nodes.strong(text, error, classes=["error"])
    logger.error(
        f"while processing {rawtext}: {error}", location=content, type="semantic-markup"
    )
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
            unescape(text), "", "", require_plugin=False
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
            unescape(text), "", "", require_plugin=False
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
    ref = unescape(text).split("=", 1)[0].strip()

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


# pylint:disable-next=unused-argument,dangerous-default-value
def plugin_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible plugin.

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
    target, title = extract_explicit_title(text)

    try:
        plugin_fqcn, plugin_type = parse_plugin_name(target)
    except ValueError as exc:
        return _create_error(rawtext, text, str(exc))

    if title is None:
        title = plugin_fqcn

    options = {
        "reftype": "ref",
        "refdomain": "std",
        "refexplicit": True,
        "refwarn": True,
    }
    refnode = addnodes.pending_xref(
        plugin_fqcn, nodes.inline(rawtext, title), **options
    )
    refnode["reftarget"] = _plugin_ref(plugin_fqcn, plugin_type)

    return [refnode], []


def _create_extra_role(
    role_name,
    prepend_raw=None,
    append_raw=None,
    node=None,
    nested_node=None,
    css_class=None,
):
    """Create a simple role."""

    # pylint:disable-next=unused-argument,dangerous-default-value
    def extra_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        """No special format, except adding the role name as a class.

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
        result = []
        if prepend_raw:
            for format_value, value in prepend_raw.items():
                result.append(nodes.raw(value, value, format=format_value))
        nested = []
        if nested_node:
            nested.append(nested_node(rawtext, text))
            text = ""
        result.append(
            (node or nodes.inline)(
                rawtext, text, *nested, classes=[css_class or role_name]
            )
        )
        if append_raw:
            for format_value, value in append_raw.items():
                result.append(nodes.raw(value, value, format=format_value))
        return result, []

    return extra_role


ROLES = {
    "ansopt": option_role,
    "ansval": value_role,
    "ansretval": return_value_role,
    "ansenvvar": environment_variable,
    "ansenvvarref": environment_variable_reference,
    "ansplugin": plugin_role,
}


def _add_prepend_raw(destination, builder, value):
    if "prepend_raw" not in destination:
        destination["prepend_raw"] = {}
    if builder not in destination["prepend_raw"]:
        destination["prepend_raw"][builder] = ""
    destination["prepend_raw"][builder] = value + destination["prepend_raw"][builder]


def _add_append_raw(destination, builder, value):
    if "append_raw" not in destination:
        destination["append_raw"] = {}
    if builder not in destination["append_raw"]:
        destination["append_raw"][builder] = ""
    destination["append_raw"][builder] = destination["append_raw"][builder] + value


def _add_latex(before, after, existing):
    _add_prepend_raw(existing, "latex", before)
    _add_append_raw(existing, "latex", after)
    return existing


def _add_latex_color(color_name, existing):
    return _add_latex(f"{{\\color{{{color_name}}}", "}", existing)


_EXTRA_ROLES = {
    "ansible-attribute-support-label": _add_latex(
        "\\vphantom{", "}", {"node": nodes.strong}
    ),
    "ansible-attribute-support-property": {"node": nodes.strong},
    "ansible-attribute-support-full": _add_latex_color(
        "antsibull-green", {"node": nodes.strong}
    ),
    "ansible-attribute-support-partial": _add_latex_color(
        "antsibull-darkyellow", {"node": nodes.strong}
    ),
    "ansible-attribute-support-none": _add_latex_color(
        "antsibull-red", {"node": nodes.strong}
    ),
    "ansible-attribute-support-na": {},
    "ansible-option-aliases": _add_latex_color("antsibull-darkgreen", {}),
    "ansible-option-choices": {"node": nodes.strong},
    "ansible-option-choices-default-mark": _add_latex_color("antsibull-blue", {}),
    "ansible-option-choices-entry": {"node": nodes.literal},
    "ansible-option-choices-entry-default": _add_latex_color(
        "antsibull-blue",
        {
            "node": nodes.literal,
            "nested_node": nodes.strong,
            "css_class": "ansible-option-default-bold",
        },
    ),
    "ansible-option-configuration": {"node": nodes.strong},
    "ansible-option-default": _add_latex_color(
        "antsibull-blue", {"node": nodes.literal}
    ),
    "ansible-option-default-bold": _add_latex_color(
        "antsibull-blue", {"node": nodes.strong}
    ),
    "ansible-option-elements": _add_latex_color("antsibull-purple", {}),
    "ansible-option-required": _add_latex_color("antsibull-red", {}),
    "ansible-option-returned-bold": {"node": nodes.strong},
    "ansible-option-sample-bold": _add_latex_color("black", {"node": nodes.strong}),
    "ansible-option-type": _add_latex_color("antsibull-purple", {}),
    "ansible-option-versionadded": _add_latex(
        "{\\footnotesize",
        "}",
        _add_latex_color("antsibull-darkgreen", {"node": nodes.emphasis}),
    ),
    "ansible-rv-sample-value": _add_latex_color(
        "antsibull-blue", {"node": nodes.literal, "css_class": "ansible-option-sample"}
    ),
}


for _extra_role, _kwargs in _EXTRA_ROLES.items():
    ROLES[_extra_role] = _create_extra_role(_extra_role, **_kwargs)


def setup_roles(app):
    """
    Setup roles for a Sphinx app object.
    """
    for name, role in ROLES.items():
        app.add_role(name, role)
