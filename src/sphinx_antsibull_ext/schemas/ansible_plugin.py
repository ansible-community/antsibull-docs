# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""Schema for ansible-plugin and ansible-role-entrypoint directives."""

from __future__ import annotations

import typing as t

import pydantic as p

# Ignore Unitialized attribute errors because BaseModel works some magic
# to initialize the attributes when data is loaded into them.
# pyre-ignore-all-errors[13]


class AnsiblePlugin(p.BaseModel):
    fqcn: str
    plugin_type: str
    short_description: t.Optional[str] = None


class AnsibleRoleEntrypoint(p.BaseModel):
    fqcn: str
    entrypoint: str
    short_description: t.Optional[str] = None


class AnsibleRequirementsAnchor(p.BaseModel):
    fqcn: str
    plugin_type: str
    role_entrypoint: t.Optional[str] = None


class AnsibleAttribute(p.BaseModel):
    fqcn: str
    plugin_type: str
    role_entrypoint: t.Optional[str] = None
    name: str


class AnsibleOption(p.BaseModel):
    fqcn: str
    plugin_type: str
    role_entrypoint: t.Optional[str] = None
    name: str
    full_keys: list[list[str]]


class AnsibleReturnValue(p.BaseModel):
    fqcn: str
    plugin_type: str
    role_entrypoint: t.Optional[str] = None
    name: str
    full_keys: list[list[str]]
