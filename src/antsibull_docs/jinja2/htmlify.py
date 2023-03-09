# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
htmlify Jinja2 filter for use in Ansible documentation.
"""

import re
import typing as t
from html import escape as html_escape
from urllib.parse import quote

from antsibull_core.logging import log
from jinja2.runtime import Context
from jinja2.utils import pass_context

from ..semantic_helper import parse_option, parse_return_value
from .filters import extract_plugin_data
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
    j2_context: Context
    counts: t.Dict[str, int]
    plugin_fqcn: t.Optional[str]
    plugin_type: t.Optional[str]

    def __init__(self, j2_context: Context,
                 plugin_fqcn: t.Optional[str] = None,
                 plugin_type: t.Optional[str] = None):
        self.j2_context = j2_context
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
        self.plugin_fqcn, self.plugin_type = extract_plugin_data(
            j2_context, plugin_fqcn=plugin_fqcn, plugin_type=plugin_type)


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


class _OptionName(Command):
    command = 'O'
    parameter_count = 1
    escaped_content = True

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['option-name'] += 1
        if context.plugin_fqcn is None or context.plugin_type is None:
            raise Exception('The markup O(...) cannot be used outside a plugin or role')
        text = parameters[0]
        try:
            plugin_fqcn, plugin_type, option_link, option, value = parse_option(
                text, context.plugin_fqcn, context.plugin_type, require_plugin=False)
        except ValueError as exc:
            return _create_error(f'O({text})', str(exc))
        if value is None:
            cls = 'ansible-option'
            text = f'{option}'
            strong_start = '<strong>'
            strong_end = '</strong>'
        else:
            cls = 'ansible-option-value'
            text = f'{option}={value}'
            strong_start = ''
            strong_end = ''
        if plugin_fqcn and plugin_type and plugin_fqcn.count('.') >= 2:
            # TODO: handle role arguments (entrypoint!)
            namespace, name, plugin = plugin_fqcn.split('.', 2)
            url = f'../../{namespace}/{name}/{plugin}_{plugin_type}.html'
            fragment = f'parameter-{quote(option_link.replace(".", "/"))}'
            link_start = (
                f'<a class="reference internal" href="{url}#{fragment}">'
                '<span class="std std-ref"><span class="pre">'
            )
            link_end = '</span></span></a>'
        else:
            link_start = ''
            link_end = ''
        return (
            f'<code class="{cls} literal notranslate">'
            f'{strong_start}{link_start}{text}{link_end}{strong_end}</code>'
        )


class _OptionValue(Command):
    command = 'V'
    parameter_count = 1
    escaped_content = True

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['option-value'] += 1
        text = parameters[0]
        return f'<code class="ansible-value literal notranslate">{html_escape(text)}</code>'


class _EnvVariable(Command):
    command = 'E'
    parameter_count = 1
    escaped_content = True

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['environment-var'] += 1
        text = parameters[0]
        return f'<code class="xref std std-envvar literal notranslate">{html_escape(text)}</code>'


class _RetValue(Command):
    command = 'RV'
    parameter_count = 1
    escaped_content = True

    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        context.counts['return-value'] += 1
        if context.plugin_fqcn is None or context.plugin_type is None:
            raise Exception('The markup RV(...) cannot be used outside a plugin or role')
        text = parameters[0]
        try:
            plugin_fqcn, plugin_type, rv_link, rv, value = parse_return_value(
                text, context.plugin_fqcn, context.plugin_type, require_plugin=False)
        except ValueError as exc:
            return _create_error(f'RV({text})', str(exc))
        cls = 'ansible-return-value'
        if value is None:
            text = f'{rv}'
        else:
            text = f'{rv}={value}'
        if plugin_fqcn and plugin_type and plugin_fqcn.count('.') >= 2:
            namespace, name, plugin = plugin_fqcn.split('.', 2)
            url = f'../../{namespace}/{name}/{plugin}_{plugin_type}.html'
            fragment = f'return-{quote(rv_link.replace(".", "/"))}'
            link_start = (
                f'<a class="reference internal" href="{url}#{fragment}">'
                '<span class="std std-ref"><span class="pre">'
            )
            link_end = '</span></span></a>'
        else:
            link_start = ''
            link_end = ''
        return f'<code class="{cls} literal notranslate">{link_start}{text}{link_end}</code>'


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
    _OptionName(),
    _OptionValue(),
    _EnvVariable(),
    _RetValue(),
    _HorizontalLine(),
])


@pass_context
def html_ify(context: Context, text: str,
             *,
             plugin_fqcn: t.Optional[str] = None,
             plugin_type: t.Optional[str] = None) -> str:
    ''' convert symbols like I(this is in italics) to valid HTML '''
    flog = mlog.fields(func='html_ify')
    flog.fields(text=text).debug('Enter')

    our_context = _Context(
        context,
        plugin_fqcn=plugin_fqcn,
        plugin_type=plugin_type,
    )

    try:
        text = convert_text(text, _COMMAND_SET, html_escape, our_context)
    except Exception as exc:  # pylint:disable=broad-except
        return _create_error(text, str(exc))

    flog.fields(counts=our_context.counts).info('Number of macros converted to html equivalents')
    flog.debug('Leave')
    return text
