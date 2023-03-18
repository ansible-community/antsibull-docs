# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
rstify Jinja2 filter for use in Ansible documentation.
"""

import typing as t

from . import dom
from .parser import parse, Context
from .rst import rst_escape as _rst_escape, rst_code as _rst_code, to_rst


def rst_escape(value: t.Any, escape_ending_whitespace=False) -> str:
    ''' make sure value is converted to a string, and RST special characters are escaped '''
    if not isinstance(value, str):
        value = str(value)

    return _rst_escape(value, escape_ending_whitespace=escape_ending_whitespace)


rst_code = _rst_code


class _Counter(dom.Walker):
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

    def process_error(self, part: dom.ErrorPart) -> None:
        pass

    def process_bold(self, part: dom.BoldPart) -> None:
        self.counts['bold'] += 1

    def process_code(self, part: dom.CodePart) -> None:
        self.counts['const'] += 1

    def process_horizontal_line(self, part: dom.HorizontalLinePart) -> None:
        self.counts['ruler'] += 1

    def process_italic(self, part: dom.ItalicPart) -> None:
        self.counts['italic'] += 1

    def process_link(self, part: dom.LinkPart) -> None:
        self.counts['link'] += 1

    def process_module(self, part: dom.ModulePart) -> None:
        self.counts['module'] += 1

    def process_rst_ref(self, part: dom.RSTRefPart) -> None:
        self.counts['ref'] += 1

    def process_url(self, part: dom.URLPart) -> None:
        self.counts['url'] += 1

    def process_text(self, part: dom.TextPart) -> None:
        pass

    def process_env_variable(self, part: dom.EnvVariablePart) -> None:
        self.counts['environment-var'] += 1

    def process_option_name(self, part: dom.OptionNamePart) -> None:
        self.counts['option-name'] += 1

    def process_option_value(self, part: dom.OptionValuePart) -> None:
        self.counts['option-value'] += 1

    def process_plugin(self, part: dom.PluginPart) -> None:
        self.counts['plugin'] += 1

    def process_return_value(self, part: dom.ReturnValuePart) -> None:
        self.counts['return-value'] += 1


def _count(paragraphs: t.Sequence[dom.Paragraph]) -> t.Dict[str, int]:
    counter = _Counter()
    for paragraph in paragraphs:
        dom.walk(paragraph, counter)
    return counter.counts


def rst_ify(text: str,
            *,
            plugin_fqcn: t.Optional[str] = None,
            plugin_type: t.Optional[str] = None) -> t.Tuple[str, t.Mapping[str, int]]:
    ''' convert symbols like I(this is in italics) to valid restructured text '''
    current_plugin: t.Optional[dom.PluginIdentifier] = None
    if plugin_fqcn and plugin_type:
        current_plugin = dom.PluginIdentifier(fqcn=plugin_fqcn, type=plugin_type)
    paragraphs = parse(text, Context(current_plugin=current_plugin), errors='message')
    text = to_rst(paragraphs, current_plugin=current_plugin)
    counts = _count(paragraphs)
    return text, counts
