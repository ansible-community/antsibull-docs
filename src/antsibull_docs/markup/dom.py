# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
DOM classes used by parser.
"""

from enum import Enum
from typing import NamedTuple
import sys

import typing as t


if sys.version_info >= (3, 8):
    ErrorType = t.Union[t.Literal['ignore'], t.Literal['message'], t.Literal['exception']]
else:
    # Python 3.6/3.7 do not have t.Literal
    ErrorType = str


class PluginIdentifier(NamedTuple):
    fqcn: str
    type: str


class PartType(Enum):
    ERROR = 0
    BOLD = 1
    CODE = 2
    HORIZONTAL_LINE = 3
    ITALIC = 4
    LINK = 5
    MODULE = 6
    RST_REF = 7
    URL = 8
    TEXT = 9
    ENV_VARIABLE = 10
    OPTION_NAME = 11
    OPTION_VALUE = 12
    PLUGIN = 13
    RETURN_VALUE = 14


class TextPart(NamedTuple):
    type: 't.Literal[PartType.TEXT]'
    text: str


class ItalicPart(NamedTuple):
    type: 't.Literal[PartType.ITALIC]'
    text: str


class BoldPart(NamedTuple):
    type: 't.Literal[PartType.BOLD]'
    text: str


class ModulePart(NamedTuple):
    type: 't.Literal[PartType.MODULE]'
    fqcn: str


class PluginPart(NamedTuple):
    type: 't.Literal[PartType.PLUGIN]'
    plugin: PluginIdentifier


class URLPart(NamedTuple):
    type: 't.Literal[PartType.URL]'
    url: str


class LinkPart(NamedTuple):
    type: 't.Literal[PartType.LINK]'
    text: str
    url: str


class RSTRefPart(NamedTuple):
    type: 't.Literal[PartType.RST_REF]'
    text: str
    ref: str


class CodePart(NamedTuple):
    type: 't.Literal[PartType.CODE]'
    text: str


class OptionNamePart(NamedTuple):
    type: 't.Literal[PartType.OPTION_NAME]'
    plugin: t.Optional[PluginIdentifier]
    link: t.List[str]
    name: str
    value: t.Optional[str]


class OptionValuePart(NamedTuple):
    type: 't.Literal[PartType.OPTION_VALUE]'
    value: str


class EnvVariablePart(NamedTuple):
    type: 't.Literal[PartType.ENV_VARIABLE]'
    name: str


class ReturnValuePart(NamedTuple):
    type: 't.Literal[PartType.RETURN_VALUE]'
    plugin: t.Optional[PluginIdentifier]
    link: t.List[str]
    name: str
    value: t.Optional[str]


class HorizontalLinePart(NamedTuple):
    type: 't.Literal[PartType.HORIZONTAL_LINE]'


class ErrorPart(NamedTuple):
    type: 't.Literal[PartType.ERROR]'
    message: str


AnyPart = t.Union[
    TextPart,
    ItalicPart,
    BoldPart,
    ModulePart,
    PluginPart,
    URLPart,
    LinkPart,
    RSTRefPart,
    CodePart,
    OptionNamePart,
    OptionValuePart,
    EnvVariablePart,
    ReturnValuePart,
    HorizontalLinePart,
    ErrorPart,
]


Paragraph = t.List[AnyPart]
