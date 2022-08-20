# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
rstify Jinja2 filter for use in Ansible documentation.
"""

import re
from urllib.parse import quote

import typing as t

from antsibull_core.logging import log

from .parser import Command, CommandSet, convert_text


mlog = log.fields(mod=__name__)

_MODULE = re.compile(r"^([^).]+)\.([^).]+)\.([^)]+)$")
_PLUGIN = re.compile(r"^([^).]+)\.([^).]+)\.([^)]+)#([a-z]+)$")


def rst_escape(value: t.Any, escape_ending_whitespace=False) -> str:
    ''' make sure value is converted to a string, and RST special characters are escaped '''

    if not isinstance(value, str):
        value = str(value)

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


def rst_code(value: str) -> str:
    ''' Write value as :code:`...` RST construct. '''
    if not isinstance(value, str):
        value = str(value)
    return f':code:`{rst_escape(value, escape_ending_whitespace=True)}`'


def _escape_url(url: str) -> str:
    # We include '<>[]{}' in safe to allow urls such as 'https://<HOST>:[PORT]/v{version}/' to
    # remain unmangled by percent encoding
    return quote(url, safe=':/#?%<>[]{}')


def _create_error(text: str, error: str) -> str:
    text = f':literal:`{rst_escape(text, escape_ending_whitespace=True)}`'
    error_msg = f':strong:`{rst_escape(error, escape_ending_whitespace=True)}`'
    return f"\\ :strong:`ERROR while parsing` {text}\\ : {error_msg}\\ "


class _Context:
    counts: t.Dict[str, int]

    def __init__(self):
        self.counts = {
            'italic': 0,
            'bold': 0,
            'module': 0,
            'plugin': 0,
            'link': 0,
            'url': 0,
            'ref': 0,
            'const': 0,
            'option-name': 0,
            'option-value': 0,
            'environment-var': 0,
            'return-value': 0,
            'ruler': 0,
        }


# In the following, we make heavy use of escaped whitespace ("\ ") being removed from the output.
# See
# https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#character-level-inline-markup-1
# for further information.


class _Italic(Command):
    command = 'I'
    parameter_count = 1
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['italic'] += 1
        return f"\\ :emphasis:`{rst_escape(parameters[0], escape_ending_whitespace=True)}`\\ "


class _Bold(Command):
    command = 'B'
    parameter_count = 1
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['bold'] += 1
        return f"\\ :strong:`{rst_escape(parameters[0], escape_ending_whitespace=True)}`\\ "


class _Module(Command):
    command = 'M'
    parameter_count = 1
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['module'] += 1
        m = _MODULE.match(parameters[0])
        if m is None:
            return _create_error(
                f'M({parameters[0]!r})', f'parameter {parameters[0]!r} is not a FQCN')
        fqcn = f'{m.group(1)}.{m.group(2)}.{m.group(3)}'
        return f"\\ :ref:`{rst_escape(fqcn)} <ansible_collections.{fqcn}_module>`\\ "


class _Plugin(Command):
    command = 'P'
    parameter_count = 1
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['plugin'] += 1
        m = _PLUGIN.match(parameters[0])
        if m is None:
            return _create_error(
                f'P({parameters[0]!r})',
                f'parameter {parameters[0]!r} is not of the form FQCN#type')
        fqcn = f'{m.group(1)}.{m.group(2)}.{m.group(3)}'
        plugin_type = m.group(4)
        return f"\\ :ref:`{rst_escape(fqcn)} <ansible_collections.{fqcn}_{plugin_type}>`\\ "


class _URL(Command):
    command = 'U'
    parameter_count = 1
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['url'] += 1
        return f"\\ {_escape_url(parameters[0])}\\ "


class _Link(Command):
    command = 'L'
    parameter_count = 2
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['link'] += 1
        return f"\\ `{rst_escape(parameters[0])} <{_escape_url(parameters[1])}>`__\\ "


class _Ref(Command):
    command = 'R'
    parameter_count = 2
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['ref'] += 1
        return f"\\ :ref:`{rst_escape(parameters[0])} <{parameters[1]}>`\\ "


class _Const(Command):
    command = 'C'
    parameter_count = 1
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['const'] += 1
        # Escaping does not work in double backticks, so we use the :literal: role instead
        return f"\\ :literal:`{rst_escape(parameters[0], escape_ending_whitespace=True)}`\\ "


class _HorizontalLine(Command):
    command = 'HORIZONTALLINE'
    parameter_count = 0
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['ruler'] += 1
        return '\n\n.. raw:: html\n\n  <hr>\n\n'


_COMMAND_SET = CommandSet([
    _Italic(),
    _Bold(),
    _Module(),
    _Plugin(),
    _URL(),
    _Link(),
    _Ref(),
    _Const(),
    _HorizontalLine(),
])


def rst_ify(text: str) -> str:
    ''' convert symbols like I(this is in italics) to valid restructured text '''
    flog = mlog.fields(func='rst_ify')
    flog.fields(text=text).debug('Enter')

    our_context = _Context()

    try:
        text = convert_text(text, _COMMAND_SET, rst_escape, our_context)
    except Exception as exc:  # pylint:disable=broad-except
        return _create_error(text, str(exc))

    flog.fields(counts=our_context.counts).info('Number of macros converted to rst equivalents')
    flog.debug('Leave')
    return text
