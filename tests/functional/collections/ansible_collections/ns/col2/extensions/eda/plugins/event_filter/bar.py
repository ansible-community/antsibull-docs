# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import annotations

import typing as t

DOCUMENTATION = r"""
---
short_description: Something else
description:
  - Doesn't do anything.
authors:
  - Felix
deprecated:
    removed_in: 2.0.0
    why: It doesn't do anything, so don't use it.
    alternatives: Nothing.
"""

EXAMPLES = r"""
- ns.col2.foo:
    foo: foo!
  filters:
    - ns.col2.bar:
"""


def main(event: dict[str, t.Any]) -> dict[str, t.Any]:
    """Does nothing."""
    return event
