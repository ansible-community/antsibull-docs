# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project
"""Schema for ansible-output-data directive."""

from __future__ import annotations

import typing as t

import pydantic as p


class VariableSource(p.BaseModel):
    # Language of previous code block whose content to use
    previous_code_block: t.Optional[str] = None

    # Fixed value
    value: t.Optional[str] = None

    @p.model_validator(mode="after")
    def _verify_one_of(self) -> t.Self:
        keys = ("previous_code_block", "value")
        values = [getattr(self, key) for key in keys]
        no = sum(value is not None for value in values)
        if no == 0:
            raise ValueError(f"Exactly one of {keys} must be provided")
        if no > 1:
            raise ValueError(f"Exactly one of {keys} must be provided")
        return self


class AnsibleOutputData(p.BaseModel):
    playbook: str
    env: dict[str, str] = {}
    prepend_lines: str = ""
    language: str = "ansible-output"
    variables: dict[str, VariableSource] = {}
    skip_first_lines: int = 0
    skip_last_lines: int = 0

    @p.field_validator("env", mode="before")
    @classmethod
    def convert_dict_values(cls, obj):
        """
        Convert dictionary values to strings that have a unique string representation.
        Values without a unique string representation (floats, booleans, ...)
        are not converted.
        """
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, int):
                    obj[k] = str(v)
        return obj
