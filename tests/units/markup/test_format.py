# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project

import typing as t

from antsibull_docs.markup import dom
from antsibull_docs.markup.format import Formatter, format_paragraphs


class _TestFormatter(Formatter):
    def format_error(self, part: dom.ErrorPart) -> str:
        return 'format_error'

    def format_bold(self, part: dom.BoldPart) -> str:
        return 'format_bold'

    def format_code(self, part: dom.CodePart) -> str:
        return 'format_code'

    def format_horizontal_line(self, part: dom.HorizontalLinePart) -> str:
        return 'format_horizontal_line'

    def format_italic(self, part: dom.ItalicPart) -> str:
        return 'format_italic'

    def format_link(self, part: dom.LinkPart) -> str:
        return 'format_link'

    def format_module(self, part: dom.ModulePart, url: t.Optional[str]) -> str:
        return 'format_module'

    def format_rst_ref(self, part: dom.RSTRefPart) -> str:
        return 'format_rst_ref'

    def format_url(self, part: dom.URLPart) -> str:
        return 'format_url'

    def format_text(self, part: dom.TextPart) -> str:
        return 'format_text'

    def format_env_variable(self, part: dom.EnvVariablePart) -> str:
        return 'format_env_variable'

    def format_option_name(self, part: dom.OptionNamePart, url: t.Optional[str]) -> str:
        return 'format_option_name'

    def format_option_value(self, part: dom.OptionValuePart) -> str:
        return 'format_option_value'

    def format_plugin(self, part: dom.PluginPart, url: t.Optional[str]) -> str:
        return 'format_plugin'

    def format_return_value(self, part: dom.ReturnValuePart, url: t.Optional[str]) -> str:
        return 'format_return_value'


def test_format_paragraphs():
    assert format_paragraphs([], formatter=_TestFormatter()) == ''
    assert format_paragraphs(
        [[dom.HorizontalLinePart(), dom.TextPart(text='foo')]],
        formatter=_TestFormatter()
    ) == 'format_horizontal_lineformat_text'
