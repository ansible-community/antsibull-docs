# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026, Ansible Project
"""Schemas for the EDA plugin DOCUMENTATION data."""

from __future__ import annotations

import typing as t

import pydantic as p

from .base import BaseModel, DocSchema, OptionsSchema
from .plugin import PluginExamplesSchema


class InnerEDAOptionsSchema(OptionsSchema):
    suboptions: dict[str, "InnerEDAOptionsSchema"] = {}

    @p.model_validator(mode="before")
    @classmethod
    def allow_description_to_be_optional(cls, values):
        # Doing this in a validator so that the json-schema will still flag it as an error
        if isinstance(values, dict) and "description" not in values:
            values["description"] = []
        return values


InnerEDAOptionsSchema.model_rebuild()


class EDAOptionsSchema(OptionsSchema):
    suboptions: dict[str, "InnerEDAOptionsSchema"] = {}


class OuterEDADocSchema(DocSchema):
    name: str = ""  # EDA docs do not have name
    options: dict[str, EDAOptionsSchema] = {}


class EDADocSchema(BaseModel):
    doc: OuterEDADocSchema


class _Empty(BaseModel):
    pass


class EDAReturnSchema(BaseModel):
    return_: t.Annotated[_Empty, p.Field(alias="return")] = _Empty()

    @p.field_validator("return_", mode="before")
    @classmethod
    def accept_none(cls, obj):
        return {} if obj is None else obj


class EDASchema(
    EDADocSchema,
    PluginExamplesSchema,
    EDAReturnSchema,
    BaseModel,
):
    """Documentation for EDA plugins."""
