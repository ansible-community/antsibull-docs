# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""Schema for ansible-links directive."""

from __future__ import annotations

import typing as t

import pydantic as p


class AnsibleLink(p.BaseModel):
    title: str
    url: t.Optional[str] = None
    ref: t.Optional[str] = None
    external: bool = False

    @p.model_validator(mode="before")
    @classmethod
    def one_of_url_and_ref(cls, values: t.Any) -> t.Any:
        if isinstance(values, dict):
            has_url = values.get("url")
            has_ref = values.get("ref")
            if has_url == has_ref:
                raise ValueError("Exactly one of 'url' and 'ref' must be specified.")
        return values


class AnsibleLinks(p.BaseModel):
    data: list[AnsibleLink]
