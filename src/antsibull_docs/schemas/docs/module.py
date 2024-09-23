# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Schemas for the plugin DOCUMENTATION data."""


import pydantic as p

from .base import BaseModel, DocSchema, OptionsSchema
from .plugin import PluginExamplesSchema, PluginMetadataSchema, PluginReturnSchema


class InnerModuleOptionsSchema(OptionsSchema):
    suboptions: dict[str, "InnerModuleOptionsSchema"] = {}

    @p.model_validator(mode="before")
    @classmethod
    def allow_description_to_be_optional(cls, values):
        # Doing this in a validator so that the json-schema will still flag it as an error
        if isinstance(values, dict) and "description" not in values:
            values["description"] = []
        return values


InnerModuleOptionsSchema.model_rebuild()


class ModuleOptionsSchema(OptionsSchema):
    suboptions: dict[str, "InnerModuleOptionsSchema"] = {}


class OuterModuleDocSchema(DocSchema):
    options: dict[str, ModuleOptionsSchema] = {}
    has_action: bool = False


class ModuleDocSchema(BaseModel):
    doc: OuterModuleDocSchema


class ModuleSchema(
    ModuleDocSchema,
    PluginExamplesSchema,
    PluginMetadataSchema,
    PluginReturnSchema,
    BaseModel,
):
    """Documentation for modules."""
