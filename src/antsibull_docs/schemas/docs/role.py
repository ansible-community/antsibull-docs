# Author: Toshio Kuratomi <tkuratom@redhat.com>
# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""Schemas for the role documentation data."""

import typing as t
from collections.abc import Mapping, Sequence

import pydantic as p

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
from .plugin import PluginExamplesSchema

_SENTINEL = object()


class _RoleOptionsSchema(OptionsSchema):
    options: dict[str, t.Any] = {}
    mutually_exclusive: list[list[str]] = []
    required_together: list[list[str]] = []
    required_one_of: list[list[str]] = []
    required_if: list[tuple[str, t.Any, list[str], bool]] = []
    required_by: dict[str, list[str]] = {}

    @p.field_validator("mutually_exclusive", mode="before")
    @classmethod
    def _massage_mutually_exclusive(cls, obj):
        # mutually_exclusive can also be a single list of strings
        if obj and isinstance(obj, Sequence) and not isinstance(obj, str):
            if all(isinstance(elt, str) for elt in obj):
                return [obj]
        return obj

    @p.field_validator("required_if", mode="before")
    @classmethod
    def _massage_required_if(cls, obj):
        if not isinstance(obj, Sequence) or isinstance(obj, str):
            return obj
        result = []
        for elt in obj:
            if not isinstance(elt, Sequence) or isinstance(elt, str) or len(elt) != 3:
                result.append(elt)
                continue
            result.append((elt[0], elt[1], elt[2], False))
        return result


class InnerRoleOptionsSchema(_RoleOptionsSchema):
    options: dict[str, "InnerRoleOptionsSchema"] = {}

    @p.model_validator(mode="before")
    @classmethod
    def allow_description_to_be_optional(cls, values):
        # Doing this in a validator so that the json-schema will still flag it as an error
        if isinstance(values, dict) and "description" not in values:
            values["description"] = []
        return values


InnerRoleOptionsSchema.model_rebuild()


class RoleOptionsSchema(_RoleOptionsSchema):
    options: dict[str, "InnerRoleOptionsSchema"] = {}


class RoleEntrypointSchema(PluginExamplesSchema, BaseModel):
    """Documentation for role entrypoints."""

    description: list[str]
    short_description: str
    author: list[str] = []
    deprecated: t.Optional[DeprecationSchema] = None
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

    @p.field_validator(
        "author",
        "description",
        "todo",
        mode="before",
    )
    @classmethod
    def list_from_scalars(cls, obj):
        return list_from_scalars(obj)


class RoleSchema(BaseModel):
    """Documentation for roles."""

    collection: str = COLLECTION_NAME_F
    entry_points: dict[str, RoleEntrypointSchema]
    path: str

    @p.model_validator(mode="before")
    @classmethod
    def add_entrypoint_deprecation_collection(cls, values):
        if isinstance(values, Mapping):
            entry_points = values.get("entry_points")
            collection = values.get("collection")
            if isinstance(entry_points, Mapping) and isinstance(collection, str):
                for data in entry_points.values():
                    if isinstance(data, Mapping) and isinstance(
                        deprecation := data.get("deprecated"), Mapping
                    ):
                        removed_from_collection = deprecation.get(
                            "removed_from_collection", _SENTINEL
                        )
                        if removed_from_collection is _SENTINEL:
                            deprecation["removed_from_collection"] = collection
        return values
