# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Schemas for the plugin DOCUMENTATION data."""

import typing as t

from .base import BaseModel
from .plugin import (
    InnerDocSchema,
    PluginExamplesSchema,
    PluginMetadataSchema,
    PluginReturnSchema,
)


class InnerCallbackDocSchema(InnerDocSchema):
    """
    Schema describing the structure of callback documentation.

    Differs from other plugins because callbacks have subtypes documented in ``type`` rather than
    having separate types.
    """

    type: t.Literal["aggregate", "notification", "stdout"]


class CallbackDocSchema(BaseModel):
    doc: InnerCallbackDocSchema


class CallbackSchema(
    CallbackDocSchema,
    PluginExamplesSchema,
    PluginMetadataSchema,
    PluginReturnSchema,
    BaseModel,
):
    """Documentation of callback plugins."""
