# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
Parser for formatted texts.
"""

import abc
import re
import typing as t

from . import dom
from ._parser_impl import parse_parameters_escaped, parse_parameters_unescaped


_IGNORE_MARKER = 'ignore:'
_ARRAY_STUB_RE = re.compile(r'\[([^\]]*)\]')
_FQCN_TYPE_PREFIX_RE = re.compile(r'^([^.]+\.[^.]+\.[^#]+)#([^:]+):(.*)$')
_FQCN = re.compile(r'^[a-z0-9_]+\.[a-z0-9_]+(?:\.[a-z0-9_]+)+$')
_PLUGIN_TYPE = re.compile(r'^[a-z_]+$')


def _is_fqcn(text: str) -> bool:
    return _FQCN.match(text) is not None


def _is_plugin_type(text: str) -> bool:
    # We do not want to hard-code a list of valid plugin types that might be inaccurate, so we
    # simply check whether this is a valid kind of Python identifier usually used for plugin
    # types. If ansible-core ever adds one with digits, we'll have to update this.
    return _PLUGIN_TYPE.match(text) is not None


class Context(t.NamedTuple):
    current_plugin: t.Optional[dom.PluginIdentifier] = None
    role_entrypoint: t.Optional[str] = None


class CommandParser(abc.ABC):
    command: str
    parameters: int
    escaped_arguments: bool

    def __init__(self, command: str, parameters: int, escaped_arguments: bool = False):
        self.command = command
        self.parameters = parameters
        self.escaped_arguments = escaped_arguments

    @abc.abstractmethod
    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        pass  # pragma: no cover


class CommandParserEx(CommandParser):
    old_markup: bool

    def __init__(self, command: str, parameters: int,
                 escaped_arguments: bool = False, old_markup: bool = False):
        super().__init__(command, parameters, escaped_arguments)
        self.old_markup = old_markup


# Classic Ansible docs markup:


class _Italics(CommandParserEx):
    def __init__(self):
        super().__init__('I', 1, old_markup=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        return dom.ItalicPart(text=parameters[0])


class _Bold(CommandParserEx):
    def __init__(self):
        super().__init__('B', 1, old_markup=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        return dom.BoldPart(text=parameters[0])


class _Module(CommandParserEx):
    def __init__(self):
        super().__init__('M', 1, old_markup=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        fqcn = parameters[0]
        if not _is_fqcn(fqcn):
            raise ValueError(f'Module name "{fqcn}" is not a FQCN')
        return dom.ModulePart(fqcn=fqcn)


class _URL(CommandParserEx):
    def __init__(self):
        super().__init__('U', 1, old_markup=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        return dom.URLPart(url=parameters[0])


class _Link(CommandParserEx):
    def __init__(self):
        super().__init__('L', 2, old_markup=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        text = parameters[0]
        url = parameters[1]
        return dom.LinkPart(text=text, url=url)


class _RSTRef(CommandParserEx):
    def __init__(self):
        super().__init__('R', 2, old_markup=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        text = parameters[0]
        ref = parameters[1]
        return dom.RSTRefPart(text=text, ref=ref)


class _Code(CommandParserEx):
    def __init__(self):
        super().__init__('C', 1, old_markup=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        return dom.CodePart(text=parameters[0])


class _HorizontalLine(CommandParserEx):
    def __init__(self):
        super().__init__('HORIZONTALLINE', 0, old_markup=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        return dom.HorizontalLinePart()


# Semantic Ansible docs markup:


def _parse_option_like(text: str,
                       context: Context,
                       ) -> t.Tuple[t.Optional[dom.PluginIdentifier],
                                    t.Optional[str], t.List[str], str, t.Optional[str]]:
    value = None
    if '=' in text:
        text, value = text.split('=', 1)
    m = _FQCN_TYPE_PREFIX_RE.match(text)
    if m:
        plugin_fqcn = m.group(1)
        plugin_type = m.group(2)
        if not _is_fqcn(plugin_fqcn):
            raise ValueError(f'Plugin name "{plugin_fqcn}" is not a FQCN')
        if not _is_plugin_type(plugin_type):
            raise ValueError(f'Plugin type "{plugin_type}" is not valid')
        plugin_identifier = dom.PluginIdentifier(fqcn=plugin_fqcn, type=plugin_type)
        text = m.group(3)
    elif text.startswith(_IGNORE_MARKER):
        plugin_identifier = None
        text = text[len(_IGNORE_MARKER):]
    else:
        plugin_identifier = context.current_plugin
    entrypoint: t.Optional[str] = context.role_entrypoint
    if plugin_identifier is not None and plugin_identifier.type == 'role':
        idx = text.find(':')
        if idx < 0:
            if entrypoint is None:
                raise ValueError('Role reference is missing entrypoint')
        else:
            entrypoint = text[:idx]
            text = text[idx + 1:]
    if ':' in text or '#' in text:
        raise ValueError(f'Invalid option/return value name "{text}"')
    return (
        plugin_identifier,
        entrypoint,
        _ARRAY_STUB_RE.sub('', text).split('.'),
        text,
        value,
    )


class _Plugin(CommandParserEx):
    def __init__(self):
        super().__init__('P', 1, escaped_arguments=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        name = parameters[0]
        if '#' not in name:
            raise ValueError(f'Parameter "{name}" is not of the form FQCN#type')
        fqcn, ptype = name.split('#', 1)
        if not _is_fqcn(fqcn):
            raise ValueError(f'Plugin name "{fqcn}" is not a FQCN')
        if not _is_plugin_type(ptype):
            raise ValueError(f'Plugin type "{ptype}" is not valid')
        return dom.PluginPart(plugin=dom.PluginIdentifier(fqcn=fqcn, type=ptype))


class _EnvVar(CommandParserEx):
    def __init__(self):
        super().__init__('E', 1, escaped_arguments=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        return dom.EnvVariablePart(name=parameters[0])


class _OptionValue(CommandParserEx):
    def __init__(self):
        super().__init__('V', 1, escaped_arguments=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        return dom.OptionValuePart(value=parameters[0])


class _OptionName(CommandParserEx):
    def __init__(self):
        super().__init__('O', 1, escaped_arguments=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        plugin, entrypoint, link, name, value = _parse_option_like(parameters[0], context)
        return dom.OptionNamePart(
            plugin=plugin, entrypoint=entrypoint, link=link, name=name, value=value)


class _ReturnValue(CommandParserEx):
    def __init__(self):
        super().__init__('RV', 1, escaped_arguments=True)

    def parse(self, parameters: t.List[str], context: Context) -> dom.AnyPart:
        plugin, entrypoint, link, name, value = _parse_option_like(parameters[0], context)
        return dom.ReturnValuePart(
            plugin=plugin, entrypoint=entrypoint, link=link, name=name, value=value)


_COMMANDS = [
    _Italics(),
    _Bold(),
    _Module(),
    _URL(),
    _Link(),
    _RSTRef(),
    _Code(),
    _HorizontalLine(),
    _Plugin(),
    _EnvVar(),
    _OptionValue(),
    _OptionName(),
    _ReturnValue(),
]


def _command_re(command: CommandParser) -> str:
    return r'\b' + re.escape(command.command) + (r'\b' if command.parameters == 0 else r'\(')


class Parser:
    _group_map: t.Mapping[str, CommandParser]
    _re: 're.Pattern'  # on Python 3.6 the type is called differently

    def __init__(self, commands: t.Sequence[CommandParser]):
        self._group_map = {cmd.command + ('(' if cmd.parameters else ''): cmd for cmd in commands}
        if commands:
            self._re = re.compile('(' + '|'.join([_command_re(cmd) for cmd in commands]) + ')')
        else:
            self._re = re.compile('x^')  # does not match anything

    @staticmethod
    def _parse_command(result: dom.Paragraph, text: str, cmd: CommandParser, index: int,
                       end_index: int, context: Context, errors: dom.ErrorType, where: str
                       ) -> int:
        args: t.List[str]
        error: t.Optional[str] = None
        if cmd.parameters == 0:
            args = []
        elif cmd.escaped_arguments:
            args, end_index, error = parse_parameters_escaped(text, end_index, cmd.parameters)
        else:
            args, end_index, error = parse_parameters_unescaped(
                text, end_index, cmd.parameters)
        if error is None:
            try:
                result.append(cmd.parse(args, context))
            except Exception as exc:  # pylint:disable=broad-except
                error = f'{exc}'
        if error is not None:
            error = (
                f'While parsing {cmd.command}{"()" if cmd.parameters else ""}'
                f' at index {index + 1}{where}: {error}'
            )
            if errors == 'message':
                result.append(dom.ErrorPart(message=error))
            elif errors == 'exception':
                raise ValueError(error)
        return end_index

    def parse_string(self, text: str, context: Context,
                     errors: dom.ErrorType = 'message', where: str = '') -> dom.Paragraph:
        result: dom.Paragraph = []
        length = len(text)
        index = 0
        while index < length:
            m = self._re.search(text, index)
            if m is None:
                result.append(dom.TextPart(text=text[index:]))
                break
            if m.start(1) > index:
                result.append(dom.TextPart(text=text[index:m.start(1)]))
            index = self._parse_command(
                result,
                text,
                self._group_map[m.group(1)],
                m.start(1),
                m.end(1),
                context,
                errors,
                where,
            )
        return result


_CLASSIC = Parser([cmd for cmd in _COMMANDS if cmd.old_markup])
_SEMANTIC_MARKUP = Parser(_COMMANDS)


def parse(text: t.Union[str, t.Sequence[str]],
          context: Context,
          errors: dom.ErrorType = 'message',
          only_classic_markup: bool = False
          ) -> t.List[dom.Paragraph]:
    has_paragraphs = True
    if isinstance(text, str):
        has_paragraphs = False
        text = [text] if text else []
    parser = _CLASSIC if only_classic_markup else _SEMANTIC_MARKUP
    return [
        parser.parse_string(
            par,
            context,
            errors=errors,
            where=f' of paragraph {index + 1}' if has_paragraphs else '',
        )
        for index, par in enumerate(text)
    ]
