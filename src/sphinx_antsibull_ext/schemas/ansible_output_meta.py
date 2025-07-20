# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project
"""Schema for ansible-output-data directive."""

from __future__ import annotations

import typing as t

import pydantic as p

from .ansible_output_data import AnsibleOutputTemplate


class ActionResetPreviousBlocks(p.BaseModel):
    model_config = p.ConfigDict(frozen=True, extra="forbid", validate_default=True)

    name: t.Literal["reset-previous-blocks"]


class ActionSetTemplate(p.BaseModel):
    model_config = p.ConfigDict(frozen=True, extra="forbid", validate_default=True)

    name: t.Literal["set-template"]
    template: AnsibleOutputTemplate


AnsibleOutputAction = t.Union[ActionResetPreviousBlocks, ActionSetTemplate]


class AnsibleOutputMeta(p.BaseModel):
    model_config = p.ConfigDict(frozen=True, extra="forbid", validate_default=True)

    actions: list[AnsibleOutputAction]
