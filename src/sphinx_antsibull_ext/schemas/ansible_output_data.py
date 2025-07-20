# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project
"""Schema for ansible-output-data directive."""

from __future__ import annotations

import typing as t

import pydantic as p


class VariableSourceCodeBlock(p.BaseModel):
    model_config = p.ConfigDict(frozen=True, extra="forbid", validate_default=True)

    # Language of previous code block whose content to use
    previous_code_block: str
    # Given the list of previous code blocks of the specified lanugage,
    # take the one with this index.
    previous_code_block_index: int = -1


class VariableSourceValue(p.BaseModel):
    model_config = p.ConfigDict(frozen=True, extra="forbid", validate_default=True)

    # Fixed value
    value: str


VariableSource = t.Union[VariableSourceCodeBlock, VariableSourceValue]


class PostprocessorCLI(p.BaseModel):
    model_config = p.ConfigDict(frozen=True, extra="forbid", validate_default=True)

    # Pass input as stdin to command, and use stdout
    command: list[str]


class PostprocessorNameRef(p.BaseModel):
    model_config = p.ConfigDict(frozen=True, extra="forbid", validate_default=True)

    # Name of postprocessor in global config
    name: str


Postprocessor = t.Union[PostprocessorCLI, PostprocessorNameRef]
NonRefPostprocessor = t.Union[PostprocessorCLI]


InventoryVariables = p.RootModel[dict[str, t.Any]]


class InventoryGroup(p.BaseModel):
    model_config = p.ConfigDict(frozen=True, extra="forbid", validate_default=True)

    hosts: dict[str, t.Optional[InventoryVariables]] = {}
    children: dict[str, t.Optional[InventoryGroup]] = {}
    vars: InventoryVariables = InventoryVariables({})


YAMLInventory = p.RootModel[dict[str, InventoryGroup]]


class AnsibleOutputTemplate(p.BaseModel):
    playbook: t.Optional[str] = None
    env: dict[str, str] = {}
    prepend_lines: t.Optional[str] = None
    language: t.Optional[str] = None
    variables: dict[str, VariableSource] = {}
    skip_first_lines: t.Optional[int] = None
    skip_last_lines: t.Optional[int] = None
    postprocessors: t.Optional[list[Postprocessor]] = None
    inventory: t.Optional[YAMLInventory] = None

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


class AnsibleOutputData(AnsibleOutputTemplate):
    playbook: t.Optional[str]  # no default


_T = t.TypeVar("_T")


def _coalesce(*values: _T | None) -> _T | None:
    for value in values:
        if value is not None:
            return value
    return None


def combine(
    *, template: AnsibleOutputTemplate, data: AnsibleOutputData
) -> AnsibleOutputData:
    playbook = _coalesce(data.playbook, template.playbook)
    if playbook is None:
        raise ValueError("Cannot use template's playbook since that is not set")
    env = template.env.copy()
    env.update(data.env)
    variables = template.variables.copy()
    variables.update(data.variables)
    return AnsibleOutputData(
        playbook=playbook,
        env=env,
        prepend_lines=data.prepend_lines or template.prepend_lines,
        language=data.language or template.language or "ansible-output",
        variables=variables,
        skip_first_lines=_coalesce(data.skip_first_lines, template.skip_first_lines),
        skip_last_lines=_coalesce(data.skip_last_lines, template.skip_last_lines),
        postprocessors=_coalesce(data.postprocessors, template.postprocessors),
        inventory=_coalesce(data.inventory, template.inventory),
    )
