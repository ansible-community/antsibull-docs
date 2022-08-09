# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project

import pytest

import typing as t

from antsibull_docs.jinja2.parser import Command, CommandSet, ParsingException, convert_text


class TestCommand0(Command):
    command = 'command0'
    parameter_count = 0
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        assert len(parameters) == 0
        return f'EMPTY'


class TestCommand1A(Command):
    command = 'command1a'
    parameter_count = 1
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        assert len(parameters) == 1
        return f'FOOA{parameters!r}'


class TestCommand1B(Command):
    command = 'command1b'
    parameter_count = 1
    escaped_content = True

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        assert len(parameters) == 1
        return f'FOOB{parameters!r}'


class TestCommand2A(Command):
    command = 'command2a'
    parameter_count = 2
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        assert len(parameters) == 2
        return f'FOOC{parameters!r}'


class TestCommand2B(Command):
    command = 'command2b'
    parameter_count = 2
    escaped_content = True

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        assert len(parameters) == 2
        return f'FOOD{parameters!r}'


COMMAND_SET = CommandSet([
    TestCommand0(),
    TestCommand1A(),
    TestCommand1B(),
    TestCommand2A(),
    TestCommand2B(),
])


def _escape_regular(text: str) -> str:
    return f'TEXT:{text!r}'


CONVERT_TEXT_DATA = {
    'nothing': "TEXT:'nothing'",
    'command0': "EMPTY",
    'a command0 b': "TEXT:'a 'EMPTYTEXT:' b'",
    'acommand0b': "TEXT:'acommand0b'",
    'command1a(foo)': "FOOA['foo']",
    'command1a( foo  )': "FOOA[' foo  ']",
    'command1a(foo, bar)': "FOOA['foo, bar']",
    'command1a(())': "FOOA['(']TEXT:')'",
    r'command1a(\(\))': r"FOOA['\\(\\']TEXT:')'",
    'a command1a()b': "TEXT:'a 'FOOA['']TEXT:'b'",
    'a command1a() b': "TEXT:'a 'FOOA['']TEXT:' b'",
    'acommand1a()b': "TEXT:'acommand1a()b'",
    'command1b(foo)': "FOOB['foo']",
    'command1b( foo  )': "FOOB[' foo  ']",
    'command1b(foo, bar)': "FOOB['foo, bar']",
    'command1b(())': "FOOB['(']TEXT:')'",
    r'command1b(\(\))': "FOOB['()']",
    'a command1b()b': "TEXT:'a 'FOOB['']TEXT:'b'",
    'acommand1b()b': "TEXT:'acommand1b()b'",
    'command2a(foo, bar)': "FOOC['foo', 'bar']",
    'command2a(foo,bar)': "FOOC['foo', 'bar']",
    'command2a( foo ,  bar  , baz )': "FOOC[' foo', 'bar  , baz ']",
    'command2a((,))': "FOOC['(', '']TEXT:')'",
    r'command2a(\(,\))': r"FOOC['\\(', '\\']TEXT:')'",
    'a command2a(,)b': "TEXT:'a 'FOOC['', '']TEXT:'b'",
    'acommand2a(,)b': "TEXT:'acommand2a(,)b'",
    'command2b(foo, bar)': "FOOD['foo', 'bar']",
    'command2b(foo,bar)': "FOOD['foo', 'bar']",
    'command2b( foo ,  bar  , baz )': "FOOD[' foo', 'bar  , baz ']",
    r'command2b( foo\ ,  bar  , baz )': "FOOD[' foo ', 'bar  , baz ']",
    'command2b((,))': "FOOD['(', '']TEXT:')'",
    r'command2b(\(,\))': "FOOD['(', ')']",
    'a command2b(,)b': "TEXT:'a 'FOOD['', '']TEXT:'b'",
    'acommand2b(,)b': "TEXT:'acommand2b(,)b'",
}


@pytest.mark.parametrize('text, expected', CONVERT_TEXT_DATA.items())
def test_convert_text(text, expected):
    commands = COMMAND_SET
    result = convert_text(text, commands, _escape_regular, None)
    assert result == expected


CONVERT_TEXT_FAIL_DATA = {
    'command1a(': """Cannot find ")" closing after the last parameter for command "command1a" starting at index 0 in 'command1a('""",
    'command2a(,': """Cannot find ")" closing after the last parameter for command "command2a" starting at index 0 in 'command2a(,'""",
    'command2a(': """Cannot find comma separating parameter 1 from the next one for command "command2a" starting at index 0 in 'command2a('""",
    'command1b(': """Cannot find ")" closing after the last parameter for command "command1b" starting at index 0 in 'command1b('""",
    'command2b(,': """Cannot find ")" closing after the last parameter for command "command2b" starting at index 0 in 'command2b(,'""",
    'command2b(': """Cannot find comma separating parameter 1 from the next one for command "command2b" starting at index 0 in 'command2b('""",
    r'command2b(\,)': r"""Cannot find comma separating parameter 1 from the next one for command "command2b" starting at index 0 in 'command2b(\\,)'""",
}


@pytest.mark.parametrize('text, expected_exc', CONVERT_TEXT_FAIL_DATA.items())
def test_convert_text_fail(text, expected_exc):
    commands = COMMAND_SET
    with pytest.raises(ParsingException) as exc:
        convert_text(text, commands, _escape_regular, None)
    assert str(exc.value) == expected_exc
