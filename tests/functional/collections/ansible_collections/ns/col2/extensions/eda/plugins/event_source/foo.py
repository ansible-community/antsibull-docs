#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import annotations

import asyncio
import datetime
import typing as t

DOCUMENTATION = r"""
---
short_description: Receive events from foo
description:
  - A dummy even source for documentation testing purposes.
options:
  foo:
    description:
      - The foo.
    type: str
    required: true
  bar:
    description:
      - Something optional.
    type: int
"""

EXAMPLES = r"""
- ns.col2.foo:
    foo: Some foo.
    bar: 3
"""


async def main(queue: asyncio.Queue[t.Any], args: dict[str, t.Any]) -> None:
    """Receive events via AWS CloudTrail."""
    delay = 10

    foo: str = args["foo"]
    bar: int = args.get("bar")

    start_time = datetime.datetime.now(tz=datetime.timezone.utc)
    event_id = 0
    while True:
        event_id += 1
        await queue.put(
            {
                "StartTime": start_time,
                "EventTime": datetime.datetime.now(tz=datetime.timezone.utc),
                "EventId": str(event_id),
            }
        )
        await asyncio.sleep(delay)


if __name__ == "__main__":
    # MockQueue if running directly.

    class MockQueue(asyncio.Queue[t.Any]):
        """A fake queue."""

        async def put(self: "MockQueue", event: dict[str, t.Any]) -> None:
            """Print the event."""
            print(event)

    asyncio.run(main(MockQueue(), {}))
