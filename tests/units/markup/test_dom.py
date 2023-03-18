# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project

import typing as t

import pytest

from antsibull_docs.markup import dom


class _TestWalker(dom.Walker):
    result: t.List[dom.AnyPart]

    def __init__(self):
        self.result = []

    def process_error(self, part: dom.ErrorPart) -> None:
        assert part.type == dom.PartType.ERROR
        self.result.append(part)

    def process_bold(self, part: dom.BoldPart) -> None:
        assert part.type == dom.PartType.BOLD
        self.result.append(part)

    def process_code(self, part: dom.CodePart) -> None:
        assert part.type == dom.PartType.CODE
        self.result.append(part)

    def process_horizontal_line(self, part: dom.HorizontalLinePart) -> None:
        assert part.type == dom.PartType.HORIZONTAL_LINE
        self.result.append(part)

    def process_italic(self, part: dom.ItalicPart) -> None:
        assert part.type == dom.PartType.ITALIC
        self.result.append(part)

    def process_link(self, part: dom.LinkPart) -> None:
        assert part.type == dom.PartType.LINK
        self.result.append(part)

    def process_module(self, part: dom.ModulePart) -> None:
        assert part.type == dom.PartType.MODULE
        self.result.append(part)

    def process_rst_ref(self, part: dom.RSTRefPart) -> None:
        assert part.type == dom.PartType.RST_REF
        self.result.append(part)

    def process_url(self, part: dom.URLPart) -> None:
        assert part.type == dom.PartType.URL
        self.result.append(part)

    def process_text(self, part: dom.TextPart) -> None:
        assert part.type == dom.PartType.TEXT
        self.result.append(part)

    def process_env_variable(self, part: dom.EnvVariablePart) -> None:
        assert part.type == dom.PartType.ENV_VARIABLE
        self.result.append(part)

    def process_option_name(self, part: dom.OptionNamePart) -> None:
        assert part.type == dom.PartType.OPTION_NAME
        self.result.append(part)

    def process_option_value(self, part: dom.OptionValuePart) -> None:
        assert part.type == dom.PartType.OPTION_VALUE
        self.result.append(part)

    def process_plugin(self, part: dom.PluginPart) -> None:
        assert part.type == dom.PartType.PLUGIN
        self.result.append(part)

    def process_return_value(self, part: dom.ReturnValuePart) -> None:
        assert part.type == dom.PartType.RETURN_VALUE
        self.result.append(part)


TEST_WALKER = [
    [],
    [dom.ErrorPart(message='foo')],
    [
        dom.TextPart(text='foo '),
        dom.ItalicPart(text='bar'),
        dom.TextPart(text=' baz '),
        dom.CodePart(text=' bam '),
        dom.TextPart(text=' '),
        dom.BoldPart(text=' ( boo '),
        dom.TextPart(text=' ) '),
        dom.URLPart(url='https://example.com/?foo=bar'),
        dom.HorizontalLinePart(),
        dom.TextPart(text=' '),
        dom.LinkPart(text='foo', url='https://bar.com'),
        dom.TextPart(text=' '),
        dom.RSTRefPart(text=' a', ref='b '),
        dom.ModulePart(fqcn='foo.bar.baz'),
        dom.TextPart(text='HORIZONTALLINEx '),
        dom.ModulePart(fqcn='foo.bar.baz.bam'),
    ],
    [
        dom.TextPart(text='foo '),
        dom.EnvVariablePart(name='a),b'),
        dom.TextPart(text=' '),
        dom.PluginPart(plugin=dom.PluginIdentifier(fqcn='foo.bar.baz', type='bam')),
        dom.TextPart(text=' baz '),
        dom.OptionValuePart(value=' b,na)\\m, '),
        dom.TextPart(text=' '),
        dom.OptionNamePart(plugin=None, link=['foo'], name='foo', value=None),
        dom.TextPart(text=' '),
    ],
]


@pytest.mark.parametrize('data', TEST_WALKER)
def test_walk(data: dom.Paragraph) -> None:
    walker = _TestWalker()
    dom.walk(data, walker)
    assert walker.result == data

