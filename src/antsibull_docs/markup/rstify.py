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
from antsibull_docs_parser.format import Formatter, LinkProvider
from antsibull_docs_parser.parser import Context, parse
from antsibull_docs_parser.rst import AntsibullRSTFormatter as _AntsibullRSTFormatter
from antsibull_docs_parser.rst import PlainRSTFormatter as _PlainRSTFormatter
from antsibull_docs_parser.rst import rst_escape as _rst_escape
from antsibull_docs_parser.rst import to_rst

from ..jinja2 import OutputFormat
from ..utils.rst import massage_rst_label
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
    return f":code:`{_rst_escape(value, escape_ending_whitespace=True)}`"


class AnsibleDocsiteFormatter(_AntsibullRSTFormatter):
    def __init__(self, referable_envvars: set[str] | None = None):
        self._referable_envvars = referable_envvars or set()

    def format_env_variable(self, part: dom.EnvVariablePart) -> str:
        envvar = part.name.split("=", 1)[0].strip()
        if envvar in self._referable_envvars:
            return f"\\ :ansenvvarref:`{_rst_escape(part.name, True)}`\\ "
        return f"\\ :ansenvvar:`{_rst_escape(part.name, True)}`\\ "


class SimplifiedRSTLinkProvider(LinkProvider):
    def plugin_link(
        self,
        plugin: dom.PluginIdentifier,
    ) -> t.Optional[str]:
        # TODO: return None for other collections
        name = plugin.fqcn.split(".", 2)[2]
        return f"{name}_{plugin.type}.rst"

    def plugin_option_like_link(
        self,
        plugin: dom.PluginIdentifier,
        entrypoint: t.Optional[str],
        what: t.Literal["option", "retval"],
        name: t.List[str],
        current_plugin: bool,
    ) -> t.Optional[str]:
        if current_plugin:
            ref = massage_rst_label("/".join(name))
            ep = f"{entrypoint}__" if entrypoint is not None else ""
            prefix = "return" if what == "retval" else "parameter"
            return f"{prefix}-{ep}{ref}_"
        return self.plugin_link(plugin)


class SimplifiedRSTFormatter(_PlainRSTFormatter):
    @staticmethod
    def _custom_format_option_like(
        part: t.Union[dom.OptionNamePart, dom.ReturnValuePart],
        url: t.Optional[str],
    ) -> str:
        plugin = part.plugin
        if url and url.endswith("_"):
            plugin_text = f" (`link <{url}>`_)"
        elif plugin:
            plugin_result = [plugin.type]
            if plugin.type not in ("module", "role", "playbook"):
                plugin_result.append(" plugin")
            plugin_result.append(" ")
            if url:
                plugin_result.append(f"`{rst_escape(plugin.fqcn)} <{url}>`__")
            else:
                plugin_result.append(rst_escape(plugin.fqcn))
            entrypoint = part.entrypoint
            if entrypoint is not None:
                if plugin_result:
                    plugin_result.append(", ")
                plugin_result.append("entrypoint ")
                plugin_result.append(rst_escape(entrypoint, True))
            plugin_text = f" (of {''.join(plugin_result)})"
        else:
            plugin_text = ""
        value_text = part.name
        value = part.value
        if value is not None:
            value_text = f"{value_text}={value}"
        return f"\\ :literal:`{rst_escape(value_text, True)}`{plugin_text}\\ "

    def format_option_name(self, part: dom.OptionNamePart, url: t.Optional[str]) -> str:
        return self._custom_format_option_like(part, url)

    def format_return_value(
        self, part: dom.ReturnValuePart, url: t.Optional[str]
    ) -> str:
        return self._custom_format_option_like(part, url)

    def format_env_variable(self, part: dom.EnvVariablePart) -> str:
        return f"\\ :literal:`{rst_escape(part.name, True)}`\\ "

    def format_module(self, part: dom.ModulePart, url: t.Optional[str]) -> str:
        if url:
            return f"\\ `{rst_escape(part.fqcn)} <{url}>`__\\ "
        return f"\\ {rst_escape(part.fqcn)}\\ "

    def format_plugin(self, part: dom.PluginPart, url: t.Optional[str]) -> str:
        if url:
            return f"\\ `{rst_escape(part.plugin.fqcn)} <{url}>`__\\ "
        return f"\\ {rst_escape(part.plugin.fqcn)} \\ "


def rst_ify(
    text: str,
    formatter: Formatter,
    *,
    plugin_fqcn: str | None = None,
    plugin_type: str | None = None,
    role_entrypoint: str | None = None,
    doc_plugin_fqcn: str | None = None,
    doc_plugin_type: str | None = None,
    link_provider: LinkProvider | None = None,
) -> tuple[str, Mapping[str, int]]:
    """convert symbols like I(this is in italics) to valid restructured text"""
    current_plugin: dom.PluginIdentifier | None = None
    if plugin_fqcn and plugin_type:
        current_plugin = dom.PluginIdentifier(fqcn=plugin_fqcn, type=plugin_type)
    doc_current_plugin: dom.PluginIdentifier | None = None
    if doc_plugin_fqcn and doc_plugin_type:
        doc_current_plugin = dom.PluginIdentifier(
            fqcn=doc_plugin_fqcn, type=doc_plugin_type
        )
    context = Context(current_plugin=current_plugin, role_entrypoint=role_entrypoint)
    paragraphs = parse(text, context, errors="message")
    text = to_rst(
        paragraphs,
        current_plugin=doc_current_plugin,
        formatter=formatter,
        link_provider=link_provider,
    )
    counts = _count(paragraphs)
    return text, counts


def get_rst_formatter_link_provider(
    output_format: OutputFormat,
    referable_envvars: set[str] | None = None,
) -> tuple[Formatter, LinkProvider | None]:
    if output_format == OutputFormat.ANSIBLE_DOCSITE:
        return (AnsibleDocsiteFormatter(referable_envvars), None)
    if output_format == OutputFormat.SIMPLIFIED_RST:
        return (SimplifiedRSTFormatter(), SimplifiedRSTLinkProvider())
    raise ValueError(f"Unknown output format {output_format}")
