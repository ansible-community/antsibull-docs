# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""
Output format enum.
"""

from __future__ import annotations

from enum import Enum


class OutputFormatObj:
    def __init__(self, value: str, extension: str):
        self._value_ = value
        self._value = value
        self._extension = extension

    @property
    def value(self):
        return self._value

    @property
    def extension(self):
        return self._extension

    def __str__(self):
        return self._value


class OutputFormat(OutputFormatObj, Enum):
    def __new__(cls, value: str, extension: str):
        return OutputFormatObj(value, extension)

    ANSIBLE_DOCSITE = ("ansible-docsite", ".rst.j2")
