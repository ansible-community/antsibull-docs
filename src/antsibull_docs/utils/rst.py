# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
ReStructured Text utils.
"""

from __future__ import annotations


def massage_rst_label(label: str) -> str:
    return " ".join(label.lower().split())
