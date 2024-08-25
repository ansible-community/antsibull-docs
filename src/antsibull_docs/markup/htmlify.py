# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
htmlify Jinja2 filter for use in Ansible documentation.
"""

from __future__ import annotations

import typing as t
from collections.abc import Mapping
from urllib.parse import quote

from antsibull_docs_parser import dom
from antsibull_docs_parser.format import LinkProvider
from antsibull_docs_parser.html import to_html
from antsibull_docs_parser.parser import Context, Whitespace, parse

from ._counter import count as _count


class _HTMLLinkProvider(LinkProvider):
    def plugin_link(self, plugin: dom.PluginIdentifier) -> str | None:
        name = "/".join(plugin.fqcn.split(".", 2))
        return f"../../{name}_{plugin.type}.html"

    def plugin_option_like_link(
        self,
        plugin: dom.PluginIdentifier,
        entrypoint: str | None,
        what: t.Literal["option"] | t.Literal["retval"],
        name: list[str],
        current_plugin: bool,
    ) -> str | None:
        base = "" if current_plugin else self.plugin_link(plugin)
        w = "parameter" if what == "option" else "return"
        slug = quote("/".join(name))
        if entrypoint is not None:
            slug = f"{entrypoint}--{slug}"
        return f"{base}#{w}-{slug}"


def html_ify(
    text: str,
    *,
    plugin_fqcn: str | None = None,
    plugin_type: str | None = None,
    role_entrypoint: str | None = None,
    doc_plugin_fqcn: str | None = None,
    doc_plugin_type: str | None = None,
) -> tuple[str, Mapping[str, int]]:
    """convert symbols like I(this is in italics) to valid HTML"""
    current_plugin: dom.PluginIdentifier | None = None
    if plugin_fqcn and plugin_type:
        current_plugin = dom.PluginIdentifier(fqcn=plugin_fqcn, type=plugin_type)
    doc_current_plugin: dom.PluginIdentifier | None = None
    if doc_plugin_fqcn and doc_plugin_type:
        doc_current_plugin = dom.PluginIdentifier(
            fqcn=doc_plugin_fqcn, type=doc_plugin_type
        )
    context = Context(current_plugin=current_plugin, role_entrypoint=role_entrypoint)
    paragraphs = parse(
        text, context, errors="message", whitespace=Whitespace.KEEP_SINGLE_NEWLINES
    )
    link_provider = _HTMLLinkProvider()
    text = to_html(
        paragraphs,
        link_provider=link_provider,
        current_plugin=doc_current_plugin,
        par_start="",
        par_end="",
    )
    counts = _count(paragraphs)
    return text, counts
