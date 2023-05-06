# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
Count markup instructions in parsed markup.
"""

from __future__ import annotations

from collections.abc import Sequence

from antsibull_docs_parser import dom


class _Counter(dom.Walker):
    counts: dict[str, int]

    def __init__(self):
        self.counts = {
            "italic": 0,
            "bold": 0,
            "module": 0,
            "plugin": 0,
            "link": 0,
            "url": 0,
            "ref": 0,
            "const": 0,
            "option-name": 0,
            "option-value": 0,
            "environment-var": 0,
            "return-value": 0,
            "ruler": 0,
        }

    def process_error(self, part: dom.ErrorPart) -> None:
        pass

    def process_bold(self, part: dom.BoldPart) -> None:
        self.counts["bold"] += 1

    def process_code(self, part: dom.CodePart) -> None:
        self.counts["const"] += 1

    def process_horizontal_line(self, part: dom.HorizontalLinePart) -> None:
        self.counts["ruler"] += 1

    def process_italic(self, part: dom.ItalicPart) -> None:
        self.counts["italic"] += 1

    def process_link(self, part: dom.LinkPart) -> None:
        self.counts["link"] += 1

    def process_module(self, part: dom.ModulePart) -> None:
        self.counts["module"] += 1

    def process_rst_ref(self, part: dom.RSTRefPart) -> None:
        self.counts["ref"] += 1

    def process_url(self, part: dom.URLPart) -> None:
        self.counts["url"] += 1

    def process_text(self, part: dom.TextPart) -> None:
        pass

    def process_env_variable(self, part: dom.EnvVariablePart) -> None:
        self.counts["environment-var"] += 1

    def process_option_name(self, part: dom.OptionNamePart) -> None:
        self.counts["option-name"] += 1

    def process_option_value(self, part: dom.OptionValuePart) -> None:
        self.counts["option-value"] += 1

    def process_plugin(self, part: dom.PluginPart) -> None:
        self.counts["plugin"] += 1

    def process_return_value(self, part: dom.ReturnValuePart) -> None:
        self.counts["return-value"] += 1


def count(paragraphs: Sequence[dom.Paragraph]) -> dict[str, int]:
    counter = _Counter()
    for paragraph in paragraphs:
        dom.walk(paragraph, counter)
    return counter.counts
