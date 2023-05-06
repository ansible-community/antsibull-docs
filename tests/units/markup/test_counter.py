# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project


from __future__ import annotations

import pytest
from antsibull_docs_parser import dom

from antsibull_docs.markup._counter import count

TEST_COUNTER = [
    (
        [],
        {
            "italic": 0,
            "bold": 0,
            "module": 0,
            "plugin": 0,
            "link": 0,
            "url": 0,
            "ref": 0,
            "const": 0,
            "option-name": 0,
            "option-value": 0,
            "environment-var": 0,
            "return-value": 0,
            "ruler": 0,
        },
    ),
    (
        [dom.ErrorPart(message="foo")],
        {
            "italic": 0,
            "bold": 0,
            "module": 0,
            "plugin": 0,
            "link": 0,
            "url": 0,
            "ref": 0,
            "const": 0,
            "option-name": 0,
            "option-value": 0,
            "environment-var": 0,
            "return-value": 0,
            "ruler": 0,
        },
    ),
    (
        [
            dom.TextPart(text="foo "),
            dom.ItalicPart(text="bar"),
            dom.TextPart(text=" baz "),
            dom.CodePart(text=" bam "),
            dom.TextPart(text=" "),
            dom.BoldPart(text=" ( boo "),
            dom.TextPart(text=" ) "),
            dom.URLPart(url="https://example.com/?foo=bar"),
            dom.HorizontalLinePart(),
            dom.TextPart(text=" "),
            dom.LinkPart(text="foo", url="https://bar.com"),
            dom.TextPart(text=" "),
            dom.RSTRefPart(text=" a", ref="b "),
            dom.ModulePart(fqcn="foo.bar.baz"),
            dom.TextPart(text="HORIZONTALLINEx "),
            dom.ModulePart(fqcn="foo.bar.baz.bam"),
        ],
        {
            "italic": 1,
            "bold": 1,
            "module": 2,
            "plugin": 0,
            "link": 1,
            "url": 1,
            "ref": 1,
            "const": 1,
            "option-name": 0,
            "option-value": 0,
            "environment-var": 0,
            "return-value": 0,
            "ruler": 1,
        },
    ),
    (
        [
            dom.TextPart(text="foo "),
            dom.EnvVariablePart(name="a),b"),
            dom.TextPart(text=" "),
            dom.PluginPart(plugin=dom.PluginIdentifier(fqcn="foo.bar.baz", type="bam")),
            dom.TextPart(text=" baz "),
            dom.OptionValuePart(value=" b,na)\\m, "),
            dom.TextPart(text=" "),
            dom.OptionNamePart(
                plugin=None, entrypoint=None, link=["foo"], name="foo", value=None
            ),
            dom.TextPart(text=" "),
            dom.ReturnValuePart(
                plugin=None,
                entrypoint=None,
                link=["bar", "baz"],
                name="bar.baz[1]",
                value=None,
            ),
        ],
        {
            "italic": 0,
            "bold": 0,
            "module": 0,
            "plugin": 1,
            "link": 0,
            "url": 0,
            "ref": 0,
            "const": 0,
            "option-name": 1,
            "option-value": 1,
            "environment-var": 1,
            "return-value": 1,
            "ruler": 0,
        },
    ),
]


@pytest.mark.parametrize("paragraph, counter", TEST_COUNTER)
def test_count(paragraph: dom.Paragraph, counter: dict[str, int]) -> None:
    result = count([paragraph])
    assert result == counter
