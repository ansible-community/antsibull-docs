# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
rstify Jinja2 filter for use in Ansible documentation.
"""

from __future__ import annotations

import typing as t
from collections.abc import Mapping

from antsibull_docs_parser import dom
from antsibull_docs_parser.parser import Context, parse
from antsibull_docs_parser.rst import rst_escape as _rst_escape
from antsibull_docs_parser.rst import to_rst

from ._counter import count as _count


def rst_escape(value: t.Any, escape_ending_whitespace=False) -> str:
    """make sure value is converted to a string, and RST special characters are escaped"""
    if not isinstance(value, str):
        value = str(value)

    return _rst_escape(value, escape_ending_whitespace=escape_ending_whitespace)


def rst_code(value: str) -> str:
    """Write value as :code:`...` RST construct."""
    if not isinstance(value, str):
        value = str(value)
    return f":code:`{rst_escape(value, escape_ending_whitespace=True)}`"


def rst_ify(
    text: str,
    *,
    plugin_fqcn: str | None = None,
    plugin_type: str | None = None,
    role_entrypoint: str | None = None,
) -> tuple[str, Mapping[str, int]]:
    """convert symbols like I(this is in italics) to valid restructured text"""
    current_plugin: dom.PluginIdentifier | None = None
    if plugin_fqcn and plugin_type:
        current_plugin = dom.PluginIdentifier(fqcn=plugin_fqcn, type=plugin_type)
    context = Context(current_plugin=current_plugin, role_entrypoint=role_entrypoint)
    paragraphs = parse(text, context, errors="message")
    text = to_rst(paragraphs, current_plugin=current_plugin)
    counts = _count(paragraphs)
    return text, counts
