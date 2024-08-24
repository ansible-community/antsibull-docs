# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

from __future__ import annotations

import pytest

from antsibull_docs.utils.text import count_leading_whitespace, sanitize_whitespace


@pytest.mark.parametrize(
    "line, max_count, expected",
    [
        (
            "",
            None,
            None,
        ),
        (
            " \t ",
            None,
            None,
        ),
        (
            " test ",
            None,
            1,
        ),
        (
            "none   ",
            None,
            0,
        ),
        (
            "none   ",
            1,
            0,
        ),
        (
            "    some ",
            2,
            2,
        ),
        (
            "    some ",
            10,
            4,
        ),
    ],
)
def test_count_leading_whitespace(line, max_count, expected):
    result = count_leading_whitespace(line, max_count=max_count)
    assert result == expected


@pytest.mark.parametrize(
    "content, trailing_newline, remove_common_leading_whitespace, expected",
    [
        (
            "",
            False,
            True,
            "",
        ),
        (
            "",
            True,
            True,
            "",
        ),
        (
            r"""
Test
  Test
""",
            False,
            True,
            r"""Test
  Test""",
        ),
        (
            r"""
Test
  Test
""",
            True,
            True,
            r"""Test
  Test
""",
        ),
        (
            r"""

      Test!
  Test  
    Test

""",
            False,
            True,
            r"""    Test!
Test
  Test""",
        ),
        (
            r"""

      Test!
  Test  
    Test

""",
            False,
            False,
            r"""      Test!
  Test
    Test""",
        ),
        (
            """
- name: Do some foo
  ns2.flatcol.foo2:
    bar: foo
""",
            False,
            True,
            """- name: Do some foo
  ns2.flatcol.foo2:
    bar: foo""",
        ),
    ],
)
def test_sanitize_whitespace(
    content, trailing_newline, remove_common_leading_whitespace, expected
):
    result = sanitize_whitespace(
        content,
        trailing_newline=trailing_newline,
        remove_common_leading_whitespace=remove_common_leading_whitespace,
    )
    assert result == expected
