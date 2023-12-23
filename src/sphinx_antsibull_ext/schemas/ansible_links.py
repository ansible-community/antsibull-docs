# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""Schema for ansible-links directive."""

from __future__ import annotations

import typing as t

from antsibull_docs._pydantic_compat import v1 as p

# Ignore Unitialized attribute errors because BaseModel works some magic
# to initialize the attributes when data is loaded into them.
# pyre-ignore-all-errors[13]


class AnsibleLink(p.BaseModel):
    title: str
    url: t.Optional[str] = None
    ref: t.Optional[str] = None
    external: bool = False

    @p.root_validator()
    # pylint:disable=no-self-argument
    def one_of_url_and_ref(cls, values: dict[str, t.Any]) -> dict[str, t.Any]:
        has_url = values.get("url")
        has_ref = values.get("ref")
        if has_url == has_ref:
            raise ValueError("Exactly one of 'url' and 'ref' must be specified.")
        return values


class AnsibleLinks(p.BaseModel):
    data: list[AnsibleLink]
