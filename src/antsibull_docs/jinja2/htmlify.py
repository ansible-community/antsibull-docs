# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
htmlify Jinja2 filter for use in Ansible documentation.
"""

import re
from html import escape as html_escape
from urllib.parse import quote

import typing as t

from antsibull_core.logging import log

from .parser import Command, CommandSet, convert_text


mlog = log.fields(mod=__name__)

_MODULE = re.compile(r"^([^).]+)\.([^).]+)\.([^)]+)$")
_PLUGIN = re.compile(r"^([^).]+)\.([^).]+)\.([^)]+)#([a-z]+)$")


def _escape_url(url: str) -> str:
    # We include '<>[]{}' in safe to allow urls such as 'https://<HOST>:[PORT]/v{version}/' to
    # remain unmangled by percent encoding
    return quote(url, safe=':/#?%<>[]{}')


def _create_error(text: str, error: str) -> str:
    text = f'<code>{html_escape(text)}</code>'
    return f'<span class="error">ERROR while parsing {text}: {html_escape(error)}</span>'


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
        return f"<em>{html_escape(parameters[0])}</em>"


class _Bold(Command):
    command = 'B'
    parameter_count = 1
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['bold'] += 1
        return f"<b>{html_escape(parameters[0])}</b>"


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
        url = html_escape(f'../../{m.group(1)}/{m.group(2)}/{m.group(3)}_module.html')
        return f"<a href='{url}' class='module'>{html_escape(fqcn)}</a>"


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
        url = html_escape(f'../../{m.group(1)}/{m.group(2)}/{m.group(3)}_{plugin_type}.html')
        cssclass = f'plugin-{html_escape(plugin_type)}'
        return f"<a href='{url}' class='module {cssclass}'>{html_escape(fqcn)}</a>"


class _URL(Command):
    command = 'U'
    parameter_count = 1
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['url'] += 1
        url = parameters[0]
        return f"<a href='{html_escape(_escape_url(url))}'>{html_escape(_escape_url(url))}</a>"


class _Link(Command):
    command = 'L'
    parameter_count = 2
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['link'] += 1
        url = parameters[1]
        return f"<a href='{html_escape(_escape_url(url))}'>{html_escape(parameters[0])}</a>"


class _Ref(Command):
    command = 'R'
    parameter_count = 2
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['ref'] += 1
        return f"<span class='module'>{html_escape(parameters[0])}</span>"


class _Const(Command):
    command = 'C'
    parameter_count = 1
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['const'] += 1
        # Escaping does not work in double backticks, so we use the :literal: role instead
        return f"<code class='docutils literal notranslate'>{html_escape(parameters[0])}</code>"


class _HorizontalLine(Command):
    command = 'HORIZONTALLINE'
    parameter_count = 0
    escaped_content = False

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['ruler'] += 1
        return '<hr/>'


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


def html_ify(text: str) -> str:
    ''' convert symbols like I(this is in italics) to valid HTML '''
    flog = mlog.fields(func='html_ify')
    flog.fields(text=text).debug('Enter')

    our_context = _Context()

    try:
        text = convert_text(text, _COMMAND_SET, html_escape, our_context)
    except Exception as exc:  # pylint:disable=broad-except
        return _create_error(text, str(exc))

    flog.fields(counts=our_context.counts).info('Number of macros converted to html equivalents')
    flog.debug('Leave')
    return text
