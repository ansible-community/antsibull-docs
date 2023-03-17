# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
DOM classes used by parser.
"""

import abc
import sys

from enum import Enum
from typing import NamedTuple

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


class Walker(abc.ABC):
    @abc.abstractmethod
    def process_error(self, part: ErrorPart) -> None:
        pass

    @abc.abstractmethod
    def process_bold(self, part: BoldPart) -> None:
        pass

    @abc.abstractmethod
    def process_code(self, part: CodePart) -> None:
        pass

    @abc.abstractmethod
    def process_horizontal_line(self, part: HorizontalLinePart) -> None:
        pass

    @abc.abstractmethod
    def process_italic(self, part: ItalicPart) -> None:
        pass

    @abc.abstractmethod
    def process_link(self, part: LinkPart) -> None:
        pass

    @abc.abstractmethod
    def process_module(self, part: ModulePart) -> None:
        pass

    @abc.abstractmethod
    def process_rst_ref(self, part: RSTRefPart) -> None:
        pass

    @abc.abstractmethod
    def process_url(self, part: URLPart) -> None:
        pass

    @abc.abstractmethod
    def process_text(self, part: TextPart) -> None:
        pass

    @abc.abstractmethod
    def process_env_variable(self, part: EnvVariablePart) -> None:
        pass

    @abc.abstractmethod
    def process_option_name(self, part: OptionNamePart) -> None:
        pass

    @abc.abstractmethod
    def process_option_value(self, part: OptionValuePart) -> None:
        pass

    @abc.abstractmethod
    def process_plugin(self, part: PluginPart) -> None:
        pass

    @abc.abstractmethod
    def process_return_value(self, part: ReturnValuePart) -> None:
        pass


class NoopWalker(Walker):
    def process_error(self, part: ErrorPart) -> None:
        pass

    def process_bold(self, part: BoldPart) -> None:
        pass

    def process_code(self, part: CodePart) -> None:
        pass

    def process_horizontal_line(self, part: HorizontalLinePart) -> None:
        pass

    def process_italic(self, part: ItalicPart) -> None:
        pass

    def process_link(self, part: LinkPart) -> None:
        pass

    def process_module(self, part: ModulePart) -> None:
        pass

    def process_rst_ref(self, part: RSTRefPart) -> None:
        pass

    def process_url(self, part: URLPart) -> None:
        pass

    def process_text(self, part: TextPart) -> None:
        pass

    def process_env_variable(self, part: EnvVariablePart) -> None:
        pass

    def process_option_name(self, part: OptionNamePart) -> None:
        pass

    def process_option_value(self, part: OptionValuePart) -> None:
        pass

    def process_plugin(self, part: PluginPart) -> None:
        pass

    def process_return_value(self, part: ReturnValuePart) -> None:
        pass


def walk(paragraph: Paragraph, walker: Walker) -> None:  # noqa: C901, pylint:disable=too-many-branches
    for part in paragraph:
        if part.type == PartType.ERROR:
            walker.process_error(t.cast(ErrorPart, part))
        elif part.type == PartType.BOLD:
            walker.process_bold(t.cast(BoldPart, part))
        elif part.type == PartType.CODE:
            walker.process_code(t.cast(CodePart, part))
        elif part.type == PartType.HORIZONTAL_LINE:
            walker.process_horizontal_line(t.cast(HorizontalLinePart, part))
        elif part.type == PartType.ITALIC:
            walker.process_italic(t.cast(ItalicPart, part))
        elif part.type == PartType.LINK:
            walker.process_link(t.cast(LinkPart, part))
        elif part.type == PartType.MODULE:
            walker.process_module(t.cast(ModulePart, part))
        elif part.type == PartType.RST_REF:
            walker.process_rst_ref(t.cast(RSTRefPart, part))
        elif part.type == PartType.URL:
            walker.process_url(t.cast(URLPart, part))
        elif part.type == PartType.TEXT:
            walker.process_text(t.cast(TextPart, part))
        elif part.type == PartType.ENV_VARIABLE:
            walker.process_env_variable(t.cast(EnvVariablePart, part))
        elif part.type == PartType.OPTION_NAME:
            walker.process_option_name(t.cast(OptionNamePart, part))
        elif part.type == PartType.OPTION_VALUE:
            walker.process_option_value(t.cast(OptionValuePart, part))
        elif part.type == PartType.PLUGIN:
            walker.process_plugin(t.cast(PluginPart, part))
        elif part.type == PartType.RETURN_VALUE:
            walker.process_return_value(t.cast(ReturnValuePart, part))
