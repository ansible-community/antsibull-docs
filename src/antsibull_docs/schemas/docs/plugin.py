# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Schemas for the plugin DOCUMENTATION data."""

import re
import typing as t

import pydantic as p

from .base import (
    COLLECTION_NAME_F,
    REQUIRED_CLI_F,
    REQUIRED_ENV_VAR_F,
    RETURN_TYPE,
    BaseModel,
    DeprecationSchema,
    DocSchema,
    OptionsSchema,
    is_json_value,
    list_from_scalars,
    normalize_return_type_names,
    normalize_value,
    transform_return_docs,
)

_SENTINEL = object()

_EXAMPLES_FMT_RE = re.compile(r"^# fmt:\s+(\S+)")


class OptionCliSchema(BaseModel):
    name: str = REQUIRED_CLI_F
    deprecated: t.Optional[DeprecationSchema] = None
    option: str = ""
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F

    @p.model_validator(mode="before")
    @classmethod
    def add_option(cls, values):
        """
        Add option if not present
        """
        if isinstance(values, dict):
            option = values.get("option", _SENTINEL)

            if option is _SENTINEL:
                values["option"] = f'--{values["name"].replace("_", "-")}'

        return values


class OptionEnvSchema(BaseModel):
    name: str = REQUIRED_ENV_VAR_F
    deprecated: t.Optional[DeprecationSchema] = None
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F


class OptionIniSchema(BaseModel):
    key: str
    section: str
    deprecated: t.Optional[DeprecationSchema] = None
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F


class OptionVarsSchema(BaseModel):
    name: str
    deprecated: t.Optional[DeprecationSchema] = None
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F


class OptionKeywordSchema(BaseModel):
    name: str
    deprecated: t.Optional[DeprecationSchema] = None
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F


class ReturnSchema(BaseModel):
    """Schema of plugin return data docs."""

    description: list[str]
    choices: t.Union[list[t.Any], dict[t.Any, list[str]]] = []
    elements: RETURN_TYPE = "str"
    returned: str = "success"
    sample: t.Any = None  # JSON value
    type: RETURN_TYPE = "str"
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F

    @p.field_validator("description", mode="before")
    @classmethod
    def list_from_scalars(cls, obj):
        return list_from_scalars(obj)

    @p.field_validator("sample", mode="before")
    @classmethod
    def is_json_value(cls, obj):
        if not is_json_value(obj):
            raise ValueError("`sample` must be a JSON value")
        return obj

    @p.field_validator("type", "elements", mode="before")
    @classmethod
    def normalize_types(cls, obj):
        return normalize_return_type_names(obj)

    @p.model_validator(mode="before")
    @classmethod
    def remove_example_normalize_sample(cls, values):
        """
        Remove example in favor of sample, and normalize sample.

        Having both sample and example is redundant.  Many more plugins are using sample so
        standardize on that.
        """
        if isinstance(values, dict):
            example = values.get("example", _SENTINEL)

            if example is not _SENTINEL:
                if values.get("sample"):
                    raise ValueError(
                        "Cannot specify `example` if `sample` has been specified."
                    )

                if not is_json_value(example):
                    raise ValueError("`example` must be a JSON value")

                values["sample"] = example
                del values["example"]

            try:
                normalize_value(values, "sample")
            except ValueError:
                pass

        return values

    @p.model_validator(mode="before")
    @classmethod
    def normalize_choices(cls, values):
        if isinstance(values, dict):
            if isinstance(values.get("choices"), dict):
                for k, v in values["choices"].items():
                    values["choices"][k] = list_from_scalars(v)
            normalize_value(
                values,
                "choices",
                is_list_of_values=values.get("type") != "list",
                accept_dict=True,
            )
        return values


class InnerReturnSchema(ReturnSchema):
    """Nested return schema which allows leaving out description."""

    contains: dict[str, "InnerReturnSchema"] = {}

    @p.model_validator(mode="before")
    @classmethod
    def allow_description_to_be_optional(cls, values):
        # Doing this in a validator so that the json-schema will still flag it as an error
        if isinstance(values, dict) and "description" not in values:
            values["description"] = []
        return values


InnerReturnSchema.model_rebuild()


class OuterReturnSchema(ReturnSchema):
    """Toplevel return schema."""

    contains: dict[str, InnerReturnSchema] = {}


class PluginOptionsSchema(OptionsSchema):
    cli: list[OptionCliSchema] = []
    env: list[OptionEnvSchema] = []
    ini: list[OptionIniSchema] = []
    suboptions: dict[str, "PluginOptionsSchema"] = {}
    vars: list[OptionVarsSchema] = []
    keyword: list[OptionKeywordSchema] = []
    deprecated: t.Optional[DeprecationSchema] = None


PluginOptionsSchema.model_rebuild()


class InnerDocSchema(DocSchema):
    options: dict[str, PluginOptionsSchema] = {}


class PluginDocSchema(BaseModel):
    doc: InnerDocSchema


class PluginExamplesSchema(BaseModel):
    examples: str = ""
    examples_format: str = "yaml"

    @p.model_validator(mode="before")
    @classmethod
    def extract_examples_format(cls, values):
        if isinstance(values, dict):
            if isinstance(examples := values.get("examples"), str):
                if fmt_match := _EXAMPLES_FMT_RE.match(examples.lstrip()):
                    values["examples_format"] = fmt_match.group(1)
        return values

    @p.field_validator("examples", mode="before")
    @classmethod
    def normalize_examples(cls, value):
        if value is None:
            value = ""
        return value


class PluginMetadataSchema(BaseModel):
    metadata: t.Optional[dict[str, t.Any]] = None


class PluginReturnSchema(BaseModel):
    return_: t.Annotated[dict[str, OuterReturnSchema], p.Field(alias="return")] = {}

    @p.field_validator("return_", mode="before")
    @classmethod
    def transform_return(cls, obj):
        return transform_return_docs(obj)


class PluginSchema(
    PluginDocSchema,
    PluginExamplesSchema,
    PluginMetadataSchema,
    PluginReturnSchema,
    BaseModel,
):
    """Documentation of an Ansible plugin."""
