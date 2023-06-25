# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""
Output format enum.
"""

from __future__ import annotations

from enum import Enum


class OutputFormat(Enum):
    def __init__(self, output_format: str, extension: str):
        self._output_format = output_format
        self._extension = extension

    ANSIBLE_DOCSITE = ("ansible-docsite", ".rst.j2")
    SIMPLIFIED_RST = ("simplified-rst", ".rst.j2")

    @property
    def output_format(self):
        return self._output_format

    @property
    def extension(self):
        return self._extension

    @classmethod
    def parse(cls, output_format: str) -> OutputFormat:
        for elt in cls:
            if elt.output_format == output_format:
                return elt
        output_formats = ", ".join(sorted(f"'{elt.output_format}'" for elt in cls))
        raise ValueError(
            f"Unknown output format '{output_format}'. Allowed values are {output_formats}"
        )
