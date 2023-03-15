# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
rstify Jinja2 filter for use in Ansible documentation.
"""

import re
import typing as t
from urllib.parse import quote

from .semantic_helper import augment_plugin_name_type
from .parser import Command, CommandSet, convert_text

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
    plugin_fqcn: t.Optional[str]
    plugin_type: t.Optional[str]

    def __init__(self,
                 plugin_fqcn: t.Optional[str] = None,
                 plugin_type: t.Optional[str] = None):
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
        self.plugin_fqcn = plugin_fqcn
        self.plugin_type = plugin_type


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


class _OptionName(Command):
    command = 'O'
    parameter_count = 1
    escaped_content = True

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['option-name'] += 1
        if context.plugin_fqcn is None or context.plugin_type is None:
            raise Exception('The markup O(...) cannot be used outside a plugin or role')
        text = augment_plugin_name_type(parameters[0], context.plugin_fqcn, context.plugin_type)
        return f"\\ :ansopt:`{rst_escape(text, escape_ending_whitespace=True)}`\\ "


class _OptionValue(Command):
    command = 'V'
    parameter_count = 1
    escaped_content = True

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['option-value'] += 1
        return f"\\ :ansval:`{rst_escape(parameters[0], escape_ending_whitespace=True)}`\\ "


class _EnvVariable(Command):
    command = 'E'
    parameter_count = 1
    escaped_content = True

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['environment-var'] += 1
        return f"\\ :envvar:`{rst_escape(parameters[0], escape_ending_whitespace=True)}`\\ "


class _RetValue(Command):
    command = 'RV'
    parameter_count = 1
    escaped_content = True

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['return-value'] += 1
        if context.plugin_fqcn is None or context.plugin_type is None:
            raise Exception('The markup RV(...) cannot be used outside a plugin or role')
        text = augment_plugin_name_type(parameters[0], context.plugin_fqcn, context.plugin_type)
        return f"\\ :ansretval:`{rst_escape(text, escape_ending_whitespace=True)}`\\ "


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
    _OptionName(),
    _OptionValue(),
    _EnvVariable(),
    _RetValue(),
    _HorizontalLine(),
])


def rst_ify(text: str,
            *,
            plugin_fqcn: t.Optional[str] = None,
            plugin_type: t.Optional[str] = None) -> t.Tuple[str, t.Mapping[str, int]]:
    ''' convert symbols like I(this is in italics) to valid restructured text '''
    our_context = _Context(
        plugin_fqcn=plugin_fqcn,
        plugin_type=plugin_type,
    )

    try:
        text = convert_text(text, _COMMAND_SET, rst_escape, our_context)
    except Exception as exc:  # pylint:disable=broad-except
        text = _create_error(text, str(exc))

    return text, our_context.counts
