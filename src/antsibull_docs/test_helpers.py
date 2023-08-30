# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""Detect and setup for CI tests"""

from __future__ import annotations

import os

import antsibull_docs


# Use an environment variable with a special value as a CI marker
ANTSIBULL_DOCS_CI_ENV_MARKER_NAME = "_ANTSIBULL_DOCS_CI_MARKER"
ANTSIBULL_DOCS_CI_ENV_MARKER_VALUE = "Noo4oogongae"

# The version string to use when in CI
ANTSIBULL_DOCS_CI_VERSION = "<ANTSIBULL_DOCS_VERSION>"


def is_in_antsibull_ci():
    """
    Determine whether the code is running in CI.
    """
    return os.environ.get(ANTSIBULL_DOCS_CI_ENV_MARKER_NAME) == ANTSIBULL_DOCS_CI_ENV_MARKER_VALUE


def ci_setup():
    """
    Changes some behavior, such as the version, when running in CI.
    """
    if not is_in_antsibull_ci():
        return

    antsibull_docs.__version__ = ANTSIBULL_DOCS_CI_VERSION
