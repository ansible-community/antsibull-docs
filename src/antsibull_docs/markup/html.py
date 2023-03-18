# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
HTML serialization.
"""

import typing as t

from html import escape as _html_escape
from urllib.parse import quote

from . import dom
from .format import Formatter, LinkProvider, format_paragraphs as _format_paragraphs


def html_escape(text: str) -> str:
    return _html_escape(text).replace('&quot;', '"')


def _url_escape(url: str) -> str:
    # We include '<>[]{}' in safe to allow urls such as 'https://<HOST>:[PORT]/v{version}/' to
    # remain unmangled by percent encoding
    return quote(url, safe=':/#?%<>[]{}')


class HTMLFormatter(Formatter):
    @staticmethod
    def _format_option_like(part: t.Union[dom.OptionNamePart, dom.ReturnValuePart],
                            url: t.Optional[str]) -> str:
        link_start = ''
        link_end = ''
        if url:
            link_start = (
                f'<a class="reference internal" href="{_html_escape(_url_escape(url))}">'
                '<span class="std std-ref"><span class="pre">'
            )
            link_end = '</span></span></a>'
        strong_start = ''
        strong_end = ''
        if part.type == dom.PartType.OPTION_NAME:
            if part.value is None:
                cls = 'ansible-option'
                strong_start = '<strong>'
                strong_end = '</strong>'
            else:
                cls = 'ansible-option-value'
        else:
            cls = 'ansible-return-value'
        if part.value is None:
            text = part.name
        else:
            text = f'{part.name}={part.value}'
        return (
            f'<code class="{cls} literal notranslate">{strong_start}{link_start}'
            f'{html_escape(text)}{link_end}{strong_end}</code>'
        )

    def format_error(self, part: dom.ErrorPart) -> str:
        return f'<span class="error">ERROR while parsing: {html_escape(part.message)}</span>'

    def format_bold(self, part: dom.BoldPart) -> str:
        return f'<b>{html_escape(part.text)}</b>'

    def format_code(self, part: dom.CodePart) -> str:
        return f"<code class='docutils literal notranslate'>{html_escape(part.text)}</code>"

    def format_horizontal_line(self, part: dom.HorizontalLinePart) -> str:
        return '<hr/>'

    def format_italic(self, part: dom.ItalicPart) -> str:
        return f'<em>{html_escape(part.text)}</em>'

    def format_link(self, part: dom.LinkPart) -> str:
        return f"<a href='{_html_escape(_url_escape(part.url))}'>{html_escape(part.text)}</a>"

    def format_module(self, part: dom.ModulePart, url: t.Optional[str]) -> str:
        if not url:
            return f"<span class='module'>{html_escape(part.fqcn)}</span>"
        return (
            f"<a href='{_html_escape(_url_escape(url))}' class='module'>"
            f'{html_escape(part.fqcn)}</a>'
        )

    def format_rst_ref(self, part: dom.RSTRefPart) -> str:
        return f"<span class='module'>{html_escape(part.text)}</span>"

    def format_url(self, part: dom.URLPart) -> str:
        return (
            f"<a href='{_html_escape(_url_escape(part.url))}'>"
            f'{html_escape(_url_escape(part.url))}</a>'
        )

    def format_text(self, part: dom.TextPart) -> str:
        return html_escape(part.text)

    def format_env_variable(self, part: dom.EnvVariablePart) -> str:
        return (
            '<code class="xref std std-envvar literal notranslate">'
            f'{html_escape(part.name)}</code>'
        )

    def format_option_name(self, part: dom.OptionNamePart, url: t.Optional[str]) -> str:
        return self._format_option_like(part, url)

    def format_option_value(self, part: dom.OptionValuePart) -> str:
        return f'<code class="ansible-value literal notranslate">{html_escape(part.value)}</code>'

    def format_plugin(self, part: dom.PluginPart, url: t.Optional[str]) -> str:
        if not url:
            return f"<span class='module'>{html_escape(part.plugin.fqcn)}</span>"
        return (
            f"<a href='{_html_escape(_url_escape(url))}' class='module'>"
            f'{html_escape(part.plugin.fqcn)}</a>'
        )

    def format_return_value(self, part: dom.ReturnValuePart, url: t.Optional[str]) -> str:
        return self._format_option_like(part, url)


DEFAULT_FORMATTER = HTMLFormatter()


def to_html(paragraphs: t.Sequence[dom.Paragraph],
            formatter: Formatter = DEFAULT_FORMATTER,
            link_provider: t.Optional[LinkProvider] = None,
            par_start: str = '<p>',
            par_end: str = '</p>',
            par_sep: str = '',
            current_plugin: t.Optional[dom.PluginIdentifier] = None) -> str:
    return _format_paragraphs(
        paragraphs,
        formatter=formatter,
        link_provider=link_provider,
        par_start=par_start,
        par_end=par_end,
        par_sep=par_sep,
        current_plugin=current_plugin,
    )
