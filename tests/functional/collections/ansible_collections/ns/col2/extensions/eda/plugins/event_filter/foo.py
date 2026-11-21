# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import annotations

import multiprocessing as mp
import typing as t

DOCUMENTATION = r"""
---
short_description: Do fancy stuff
description:
  - This is some fancy filter.
options:
  foobar:
    description:
      - Something.
    type: bool
    default: true
"""

EXAMPLES = r"""
- ns.col2.bar:
  filters:
    - ns.col2.foo:
        overwrite: false
"""


def main(
    event: dict[str, t.Any],
    overwrite: bool = True,
) -> dict[str, t.Any]:
    """Fancy stuff."""
    logger = mp.get_logger()
    logger.info("foo")
    if overwrite:
        event["Overridden"] = "YES!"
    return event
