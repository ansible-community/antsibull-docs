# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""The main antsibull-docs module. Contains versioning information."""

import os
import warnings

import pydantic

__version__ = "2.8.0"


def _filter_pydantic_v2_warnings() -> None:
    """
    Filter DeprecationWarnings from Pydantic v2. We cannot fix these without
    dropping support for v1 entirely, and we don't want to break setups with
    PYTHONWARNINGS=error.
    """

    typ: type[DeprecationWarning] | None
    if typ := getattr(pydantic, "PydanticDeprecatedSince20", None):
        warnings.simplefilter(action="ignore", category=typ)


if "_ANTSIBULL_SHOW_PYDANTIC_WARNINGS" not in os.environ:
    _filter_pydantic_v2_warnings()

__all__ = ("__version__",)
