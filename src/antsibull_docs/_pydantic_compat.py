# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Utilities to help maintain compatibility between Pydantic v1 and Pydantic v2
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import pydantic as p
from packaging.version import Version
from pydantic.version import VERSION as PYDANTIC_VERSION

pydantic_version = Version(PYDANTIC_VERSION)
HAS_PYDANTIC_V2 = pydantic_version.major == 2

if TYPE_CHECKING or HAS_PYDANTIC_V2:
    # These pragmas are only applicable when running linters with pydantic v1
    # installed. pylint and mypy will work correctly when run against pydantic
    # v2.

    # pylint: disable-next=no-name-in-module,useless-suppression
    from pydantic import v1  # type: ignore

else:
    v1 = p

_PYDANTIC_FIELD_RENAMES: dict[str, tuple[str, Callable | None]] = {
    "min_items": ("min_length", None),
    "max_items": ("max_length", None),
    "regex": ("pattern", None),
    "allow_mutation": ("frozen", lambda v: not v),
}


def Field(*args: Any, **kwargs: Any) -> Any:
    """
    Compatibility shim between pydantic v1 and pydantic v2's `Field`.
    """

    if HAS_PYDANTIC_V2:
        for key, value in tuple(kwargs.items()):
            if key in _PYDANTIC_FIELD_RENAMES:
                new_key, transform = _PYDANTIC_FIELD_RENAMES[key]
                if transform:
                    value = transform(value)
                kwargs[new_key] = value
                del kwargs[key]
    return p.Field(*args, **kwargs)


__all__ = ("pydantic_version", "HAS_PYDANTIC_V2", "Field", "v1")
