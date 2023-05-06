# Author: Toshio Kuratomi <tkuratom@redhat.com>
# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""Schemas for the role documentation data."""

# Ignore Unitialized attribute errors because BaseModel works some magic
# to initialize the attributes when data is loaded into them.
# pyre-ignore-all-errors[13]

import typing as t

import pydantic as p

from .base import (
    COLLECTION_NAME_F,
    AttributeSchema,
    AttributeSchemaActionGroup,
    AttributeSchemaPlatform,
    BaseModel,
    DeprecationSchema,
    OptionsSchema,
    SeeAlsoLinkSchema,
    SeeAlsoModSchema,
    SeeAlsoRefSchema,
)


class InnerRoleOptionsSchema(OptionsSchema):
    options: dict[str, "InnerRoleOptionsSchema"] = {}

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument
    def allow_description_to_be_optional(cls, values):
        # Doing this in a validator so that the json-schema will still flag it as an error
        if "description" not in values:
            values["description"] = []
        return values


InnerRoleOptionsSchema.update_forward_refs()


class RoleOptionsSchema(OptionsSchema):
    options: dict[str, "InnerRoleOptionsSchema"] = {}


class RoleEntrypointSchema(BaseModel):
    """Documentation for role entrypoints."""

    description: list[str]
    short_description: str
    author: list[str] = []
    deprecated: DeprecationSchema = p.Field({})
    notes: list[str] = []
    requirements: list[str] = []
    seealso: list[t.Union[SeeAlsoModSchema, SeeAlsoRefSchema, SeeAlsoLinkSchema]] = []
    todo: list[str] = []
    version_added: str = "historical"
    attributes: dict[
        str,
        t.Union[AttributeSchema, AttributeSchemaActionGroup, AttributeSchemaPlatform],
    ] = {}

    options: dict[str, RoleOptionsSchema] = {}


class RoleSchema(BaseModel):
    """Documentation for roles."""

    collection: str = COLLECTION_NAME_F
    entry_points: dict[str, RoleEntrypointSchema]
    path: str
