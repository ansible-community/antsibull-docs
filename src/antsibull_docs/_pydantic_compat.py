# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-3.0-or-later
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Utilities to help maintain compatibility between Pydantic v1 and Pydantic v2
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pydantic as p

# pylint: disable-next=no-name-in-module,useless-suppression
from pydantic import v1  # type: ignore

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

    for key, value in tuple(kwargs.items()):
        if key in _PYDANTIC_FIELD_RENAMES:
            new_key, transform = _PYDANTIC_FIELD_RENAMES[key]
            if transform:
                value = transform(value)
            kwargs[new_key] = value
            del kwargs[key]
    return p.Field(*args, **kwargs)


__all__ = ("Field", "v1")
