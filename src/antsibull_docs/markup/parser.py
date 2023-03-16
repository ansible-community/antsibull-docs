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

from ._parser_impl import parse_parameters_escaped, parse_parameters_unescaped


class ParsingException(Exception):
    pass


class Command(abc.ABC):
    command: str
    parameter_count: int
    escaped_content: bool

    @abc.abstractmethod
    def handle(self, parameters: t.List[str], context: t.Any) -> str:
        pass


class CommandSet:
    _command_map: t.Mapping[str, Command]
    _group_map: t.Mapping[str, Command]
    _re: 're.Pattern'  # on Python 3.6 the type is called differently

    def __init__(self, commands: t.List[Command]):
        group_map = {}
        command_map = {}
        command_names = []
        for command in commands:
            if command.command in command_map:
                raise Exception(
                    f'Command "{command.command}" appears multiple times in parameter list')
            command_map[command.command] = command
            if command.parameter_count == 0:
                command_names.append(fr'{re.escape(command.command)}\b')
                group_map[command.command] = command
            else:
                command_names.append(fr'{re.escape(command.command)}\(')
                group_map[f'{command.command}('] = command
        self._command_map = command_map
        self._group_map = group_map
        if command_names:
            command_re = '|'.join(command_names)
            self._re = re.compile(fr'\b({command_re})')
        else:
            self._re = re.compile(r' ^')  # never matches

    def find_next_command(self, text: str, start_index: int) -> t.Optional[t.Tuple[int, Command]]:
        match = self._re.search(text, pos=start_index)
        if not match:
            return None
        return match.start(1), self._group_map[match.group(1)]


class CommandData(t.NamedTuple):
    command: Command
    parameters: t.List[str]


Part = t.Union[str, CommandData]


def parse_text(text: str, commands: CommandSet) -> t.List[Part]:
    result: t.List[Part] = []
    index = 0
    length = len(text)
    while index < length:
        next_command = commands.find_next_command(text, index)
        if next_command is None:
            result.append(text[index:])
            break
        command_start, command = next_command
        if command_start > index:
            result.append(text[index:command_start])
        index = command_start + len(command.command)
        if command.parameter_count == 0:
            result.append(CommandData(command=command, parameters=[]))
            continue
        index += 1
        if command.escaped_content:
            parameters, index, error = parse_parameters_escaped(
                text, index, command.parameter_count)
        else:
            parameters, index, error = parse_parameters_unescaped(
                text, index, command.parameter_count)
        if error is not None:
            raise ParsingException(
                error +
                f' for command "{command.command}" starting at index {command_start} in {text!r}'
            )
        result.append(CommandData(command=command, parameters=parameters))
    return result


def convert_text(text: str, commands: CommandSet, process_other_text: t.Callable[[str], str],
                 context: t.Any,) -> str:
    parts = parse_text(text, commands)
    result = []
    for part in parts:
        if isinstance(part, str):
            result.append(process_other_text(part))
        else:
            result.append(part.command.handle(part.parameters, context))
    return ''.join(result)
