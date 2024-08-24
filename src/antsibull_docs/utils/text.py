# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project
"""
Text utils.
"""

import typing as t


def count_leading_whitespace(
    line: str, *, max_count: t.Optional[int] = None
) -> t.Optional[int]:
    """
    Count the number of leading whitespace for the given line.

    If ``max_count`` is given, will not return numbers greater than ``max_count``.
    If the line completely consists out of whitespace, ``None`` is returned.
    """
    length = len(line)
    to_check = length
    if max_count is not None and max_count < to_check:
        to_check = max_count
    count = 0
    while count < to_check and line[count] in " \t":
        count += 1
    if count == length:
        return None
    return count


def sanitize_whitespace(
    content: str,
    /,
    *,
    trailing_newline: bool = True,
    remove_common_leading_whitespace: bool = True,
) -> str:
    # Split into lines and remove trailing whitespace
    lines = [line.rstrip(" \t") for line in content.splitlines()]

    # Remove starting and trailing empty lines
    start = 0
    end = len(lines)
    while start < end and lines[start] == "":
        start += 1
    while start < end and lines[end - 1] == "":
        end -= 1
    lines = lines[start:end]

    # Remove common leading whitespace
    if remove_common_leading_whitespace:
        common_whitespace = None
        for line in lines:
            whitespace = count_leading_whitespace(line, max_count=common_whitespace)
            if whitespace is not None:
                if common_whitespace is None or common_whitespace > whitespace:
                    common_whitespace = whitespace
                    if common_whitespace == 0:
                        break
        if common_whitespace is not None and common_whitespace > 0:
            lines = [line[common_whitespace:] for line in lines]

    if trailing_newline and lines:
        lines.append("")

    # Re-combine the result
    return "\n".join(lines)
