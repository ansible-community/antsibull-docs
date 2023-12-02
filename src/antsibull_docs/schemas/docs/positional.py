# Author: Toshio Kuratomi <tkuratom@redhat.com>
# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Schemas for the plugin DOCUMENTATION data."""


from antsibull_docs._pydantic_compat import v1 as p

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

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument
    def add_default_positional(cls, values):
        """
        Remove example in favor of sample.

        Having both sample and example is redundant.  Many more plugins are using sample so
        standardize on that.
        """
        positional = values.get("positional", [])

        if isinstance(positional, str):
            positional = (
                [part.strip() for part in positional.split(",")] if positional else []
            )

        values["positional"] = positional
        return values


# Ignore Uninitialized attribute error as BaseModel works some magic to initialize the
# attributes when data is loaded into them.
# pyre-ignore[13]
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
