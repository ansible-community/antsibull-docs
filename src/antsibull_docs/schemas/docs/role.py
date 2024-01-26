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
from collections.abc import Mapping

from antsibull_docs._pydantic_compat import v1 as p

from .base import (
    COLLECTION_NAME_F,
    AttributeSchema,
    AttributeSchemaActionGroup,
    AttributeSchemaPlatform,
    BaseModel,
    DeprecationSchema,
    OptionsSchema,
    SeeAlsoSchemaT,
    list_from_scalars,
)

_SENTINEL = object()


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
    seealso: list[SeeAlsoSchemaT] = []
    todo: list[str] = []
    version_added: str = "historical"
    attributes: dict[
        str,
        t.Union[AttributeSchema, AttributeSchemaActionGroup, AttributeSchemaPlatform],
    ] = {}

    options: dict[str, RoleOptionsSchema] = {}

    @p.validator(
        "author",
        "description",
        "todo",
        pre=True,
    )
    # pylint:disable=no-self-argument
    def list_from_scalars(cls, obj):
        return list_from_scalars(obj)


class RoleSchema(BaseModel):
    """Documentation for roles."""

    collection: str = COLLECTION_NAME_F
    entry_points: dict[str, RoleEntrypointSchema]
    path: str

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument
    def add_entrypoint_deprecation_collection(cls, values):
        entry_points = values.get("entry_points")
        collection = values.get("collection")
        if isinstance(entry_points, Mapping) and isinstance(collection, str):
            for data in entry_points.values():
                if isinstance(data, Mapping):
                    deprecation = data.get("deprecated")
                    if isinstance(deprecation, Mapping):
                        removed_from_collection = deprecation.get(
                            "removed_from_collection", _SENTINEL
                        )
                        if removed_from_collection is _SENTINEL:
                            deprecation["removed_from_collection"] = collection
        return values
