# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""Compatibility package."""

from __future__ import annotations

import warnings

# This module is just a backwards compatible location for ansible_doc so the wildcard
# import is just putting all the symbols from docs.ansible_doc into this namespace.
# pylint: disable=wildcard-import,unused-wildcard-import
from .docs.ansible_doc import *  # noqa: F403,F401

warnings.warn(
    "antsibull.schemas.ansible_doc is deprecated."
    " Use antsibull_docs.schemas.docs.ansible_doc instead.",
    DeprecationWarning,
    stacklevel=2,
)
