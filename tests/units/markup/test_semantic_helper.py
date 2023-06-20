# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project

from __future__ import annotations

import pytest

from antsibull_docs.markup.semantic_helper import split_option_like_name

SPLIT_OPTION_LIKE_DATA = {
    "": [],
    "foo": [("foo", None)],
    "foo.bar": [("foo", None), ("bar", None)],
    "foo[].bar": [("foo", "[]"), ("bar", None)],
    "foo.bar[]": [("foo", None), ("bar", "[]")],
    "foo[].bar[]": [("foo", "[]"), ("bar", "[]")],
    "foo[baz.bam].bar[.boom.]": [("foo", "[baz.bam]"), ("bar", "[.boom.]")],
    "foo..bar[..]": [("foo", None), ("", None), ("bar", "[..]")],
}


@pytest.mark.parametrize("value, expected", SPLIT_OPTION_LIKE_DATA.items())
def test_split_option_like_name(value: str, expected: list[tuple[str, str]]):
    assert split_option_like_name(value) == expected


SPLIT_OPTION_LIKE_FAILURE_DATA = {
    "[": 'Found "[" without closing "]" at position 1 of \'[\'',
    "[][]": "Expecting separator \".\", but got \"'['\" at position 3 of '[][]'",
    "[]f": "Expecting separator \".\", but got \"'f'\" at position 3 of '[]f'",
    "bar[foo[]]": "Expecting separator \".\", but got \"']'\" at position 10 of 'bar[foo[]]'",
}


@pytest.mark.parametrize("value, expected", SPLIT_OPTION_LIKE_FAILURE_DATA.items())
def test_split_option_like_name(value: str, expected: str):
    with pytest.raises(ValueError) as exc:
        split_option_like_name(value)
    assert str(exc.value) == expected
