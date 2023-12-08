# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Schemas for the plugin DOCUMENTATION data."""

# Ignore Unitialized attribute errors because BaseModel works some magic
# to initialize the attributes when data is loaded into them.
# pyre-ignore-all-errors[13]

import re
import typing as t

import pydantic as p

from .base import (
    COLLECTION_NAME_F,
    REQUIRED_CLI_F,
    REQUIRED_ENV_VAR_F,
    RETURN_TYPE_F,
    BaseModel,
    DeprecationSchema,
    DocSchema,
    LocalConfig,
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
    deprecated: DeprecationSchema = p.Field({})
    option: str = ""
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument
    def add_option(cls, values):
        """
        Add option if not present
        """
        option = values.get("option", _SENTINEL)

        if option is _SENTINEL:
            values["option"] = f'--{values["name"].replace("_", "-")}'

        return values


class OptionEnvSchema(BaseModel):
    name: str = REQUIRED_ENV_VAR_F
    deprecated: DeprecationSchema = p.Field({})
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F


class OptionIniSchema(BaseModel):
    key: str
    section: str
    deprecated: DeprecationSchema = p.Field({})
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F


class OptionVarsSchema(BaseModel):
    name: str
    deprecated: DeprecationSchema = p.Field({})
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F


class OptionKeywordSchema(BaseModel):
    name: str
    deprecated: DeprecationSchema = p.Field({})
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F


class ReturnSchema(BaseModel):
    """Schema of plugin return data docs."""

    description: list[str]
    choices: t.Union[list[t.Any], dict[t.Any, list[str]]] = []
    elements: str = RETURN_TYPE_F
    returned: str = "success"
    sample: t.Any = None  # JSON value
    type: str = RETURN_TYPE_F
    version_added: str = "historical"
    version_added_collection: str = COLLECTION_NAME_F

    @p.validator("description", pre=True)
    # pylint:disable=no-self-argument
    def list_from_scalars(cls, obj):
        return list_from_scalars(obj)

    @p.validator("sample", pre=True)
    # pylint:disable=no-self-argument
    def is_json_value(cls, obj):
        if not is_json_value(obj):
            raise ValueError("`sample` must be a JSON value")
        return obj

    @p.validator("type", "elements", pre=True)
    # pylint:disable=no-self-argument
    def normalize_types(cls, obj):
        return normalize_return_type_names(obj)

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument
    def remove_example(cls, values):
        """
        Remove example in favor of sample.

        Having both sample and example is redundant.  Many more plugins are using sample so
        standardize on that.
        """
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

        return values

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument
    def normalize_sample(cls, values):
        try:
            normalize_value(values, "sample")
        except ValueError:
            pass
        return values

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument
    def normalize_choices(cls, values):
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

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument
    def allow_description_to_be_optional(cls, values):
        # Doing this in a validator so that the json-schema will still flag it as an error
        if "description" not in values:
            values["description"] = []
        return values


InnerReturnSchema.update_forward_refs()


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
    deprecated: DeprecationSchema = p.Field({})


PluginOptionsSchema.update_forward_refs()


class InnerDocSchema(DocSchema):
    options: dict[str, PluginOptionsSchema] = {}


class PluginDocSchema(BaseModel):
    doc: InnerDocSchema


class PluginExamplesSchema(BaseModel):
    examples: str = ""
    examples_format: str = "yaml"

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument
    def extract_examples_format(cls, values):
        if isinstance(values.get("examples"), str):
            fmt_match = _EXAMPLES_FMT_RE.match(values["examples"].lstrip())
            if fmt_match:
                values["examples_format"] = fmt_match.group(1)
        return values

    @p.validator("examples", pre=True)
    # pylint:disable=no-self-argument
    def normalize_examples(cls, value):
        if value is None:
            value = ""
        return value


class PluginMetadataSchema(BaseModel):
    metadata: t.Optional[dict[str, t.Any]] = None


class PluginReturnSchema(BaseModel):
    class Config(LocalConfig):
        fields = {
            "return_": "return",
        }

    return_: dict[str, OuterReturnSchema] = {}

    @p.validator("return_", pre=True)
    # pylint:disable=no-self-argument
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
