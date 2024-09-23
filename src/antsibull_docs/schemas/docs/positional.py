# Author: Toshio Kuratomi <tkuratom@redhat.com>
# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Schemas for the plugin DOCUMENTATION data."""


import pydantic as p

from .base import BaseModel
from .plugin import (
    InnerDocSchema,
    PluginExamplesSchema,
    PluginMetadataSchema,
    PluginReturnSchema,
)


class InnerPositionalDocSchema(InnerDocSchema):
    """
    Schema describing the structure of documentation for plugins with positional parameters.
    """

    positional: list[str] = []

    @p.model_validator(mode="before")
    @classmethod
    def add_default_positional(cls, values):
        """
        Remove example in favor of sample.

        Having both sample and example is redundant.  Many more plugins are using sample so
        standardize on that.
        """
        if isinstance(values, dict):
            positional = values.get("positional", [])

            if isinstance(positional, str):
                positional = (
                    [part.strip() for part in positional.split(",")]
                    if positional
                    else []
                )

            values["positional"] = positional
        return values


class PositionalDocSchema(BaseModel):
    doc: InnerPositionalDocSchema


class PositionalSchema(
    PositionalDocSchema,
    PluginExamplesSchema,
    PluginMetadataSchema,
    PluginReturnSchema,
    BaseModel,
):
    """Documentation of plugins with positional parameters."""
