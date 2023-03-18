# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
ReStructured Text serialization.
"""

import typing as t

from . import dom
from .format import Formatter, LinkProvider, format_paragraphs as _format_paragraphs
from .html import _url_escape


def rst_escape(value: str, escape_ending_whitespace=False) -> str:
    '''Escape RST specific constructs.'''
    value = value.replace('\\', '\\\\')
    value = value.replace('<', '\\<')
    value = value.replace('>', '\\>')
    value = value.replace('_', '\\_')
    value = value.replace('*', '\\*')
    value = value.replace('`', '\\`')

    if escape_ending_whitespace and value.endswith(' '):
        value = value + '\\ '
    if escape_ending_whitespace and value.startswith(' '):
        value = '\\ ' + value

    return value


class RSTFormatter(Formatter):
    @staticmethod
    def _format_option_like(part: t.Union[dom.OptionNamePart, dom.ReturnValuePart],
                            role: str) -> str:
        result: t.List[str] = []
        plugin = part.plugin
        if plugin:
            result.append(plugin.fqcn)
            result.append('#')
            result.append(plugin.type)
            result.append(':')
        result.append(part.name)
        value = part.value
        if value is not None:
            result.append('=')
            result.append(value)
        return f'\\ :{role}:`{rst_escape("".join(result), True)}`\\ '

    def format_error(self, part: dom.ErrorPart) -> str:
        return f'\\ :strong:`ERROR while parsing`\\ : {rst_escape(part.message, True)}\\ '

    def format_bold(self, part: dom.BoldPart) -> str:
        return f'\\ :strong:`{rst_escape(part.text, True)}`\\ '

    def format_code(self, part: dom.CodePart) -> str:
        return f'\\ :literal:`{rst_escape(part.text, True)}`\\ '

    def format_horizontal_line(self, part: dom.HorizontalLinePart) -> str:
        return '\n\n.. raw:: html\n\n  <hr>\n\n'

    def format_italic(self, part: dom.ItalicPart) -> str:
        return f'\\ :emphasis:`{rst_escape(part.text, True)}`\\ '

    def format_link(self, part: dom.LinkPart) -> str:
        return f'\\ `{rst_escape(part.text)} <{_url_escape(part.url)}>`__\\ '

    def format_module(self, part: dom.ModulePart, url: t.Optional[str]) -> str:
        return f'\\ :ref:`{rst_escape(part.fqcn)} <ansible_collections.{part.fqcn}_module>`\\ '

    def format_rst_ref(self, part: dom.RSTRefPart) -> str:
        return f'\\ :ref:`{rst_escape(part.text)} <{part.ref}>`\\ '

    def format_url(self, part: dom.URLPart) -> str:
        return f'\\ {_url_escape(part.url)}\\ '

    def format_text(self, part: dom.TextPart) -> str:
        return rst_escape(part.text)

    def format_env_variable(self, part: dom.EnvVariablePart) -> str:
        return f'\\ :envvar:`{rst_escape(part.name, True)}`\\ '

    def format_option_name(self, part: dom.OptionNamePart, url: t.Optional[str]) -> str:
        return self._format_option_like(part, 'ansopt')

    def format_option_value(self, part: dom.OptionValuePart) -> str:
        return f'\\ :ansval:`{rst_escape(part.value, True)}`\\ '

    def format_plugin(self, part: dom.PluginPart, url: t.Optional[str]) -> str:
        return (
            f'\\ :ref:`{rst_escape(part.plugin.fqcn)} '
            f'<ansible_collections.{part.plugin.fqcn}_{part.plugin.type}>`\\ '
        )

    def format_return_value(self, part: dom.ReturnValuePart, url: t.Optional[str]) -> str:
        return self._format_option_like(part, 'ansretval')


DEFAULT_FORMATTER = RSTFormatter()


def to_rst(paragraphs: t.Sequence[dom.Paragraph],
           formatter: Formatter = DEFAULT_FORMATTER,
           link_provider: t.Optional[LinkProvider] = None,
           par_start: str = '',
           par_end: str = '',
           par_sep: str = '\n\n',
           par_empty: str = r'\ ',
           current_plugin: t.Optional[dom.PluginIdentifier] = None) -> str:
    return _format_paragraphs(
        paragraphs,
        formatter=formatter,
        link_provider=link_provider,
        par_start=par_start,
        par_end=par_end,
        par_sep=par_sep,
        par_empty=par_empty,
        current_plugin=current_plugin,
    )
