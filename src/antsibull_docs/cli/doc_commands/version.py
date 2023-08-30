# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""Show version."""

from __future__ import annotations

import antsibull_docs


def print_version() -> int:
    print(f"antsibull-docs {antsibull_docs.__version__}")
    return 0
