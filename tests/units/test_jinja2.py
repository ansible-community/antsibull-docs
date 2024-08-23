# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project

from __future__ import annotations

import pytest

from antsibull_docs.jinja2 import OutputFormat
from antsibull_docs.jinja2.filters import (
    make_rst_ify,
    massage_author_name,
    move_first,
    to_ini_value,
    to_json,
)

RST_IFY_DATA = {
    # No substitutions
    "no-op": "no-op",
    "no-op Z(test)": "no-op Z(test)",
    # Simple cases of all substitutions
    "I(italic)": r":emphasis:`italic`",
    "B(bold)": r":strong:`bold`",
    "M(ansible.builtin.yum)": r":ref:`ansible.builtin.yum"
    r" <ansible_collections.ansible.builtin.yum_module>`",
    "U(https://docs.ansible.com)": r"`https://docs.ansible.com <https://docs.ansible.com>`__",
    "L(the user guide,https://docs.ansible.com/user-guide.html)": r"`the user guide"
    r" <https://docs.ansible.com/user-guide.html>`__",
    "R(the user guide,user-guide)": r":ref:`the user guide <user-guide>`",
    "C(/usr/bin/file)": r":literal:`/usr/bin/file`",
    "HORIZONTALLINE": ".. raw:: html\n\n  <hr>",
    # Multiple substitutions
    "The M(ansible.builtin.yum) module B(MUST) be given the C(package) parameter.  See the R(looping docs,using-loops) for more info": r"The :ref:`ansible.builtin.yum <ansible_collections.ansible.builtin.yum_module>` module :strong:`MUST` be given the :literal:`package` parameter. See the :ref:`looping docs <using-loops>` for more info",
    # Problem cases
    "IBM(International Business Machines)": "IBM(International Business Machines)",
    "L(the user guide, https://docs.ansible.com/)": r"`the user guide <https://docs.ansible.com/>`__",
    "R(the user guide, user-guide)": r":ref:`the user guide <user-guide>`",
}


@pytest.mark.parametrize("text, expected", RST_IFY_DATA.items())
def test_rst_ify(text, expected):
    context = {
        "plugin_name": "foo.bar.baz",
        "plugin_type": "module",
    }
    rst_ify = make_rst_ify(OutputFormat.ANSIBLE_DOCSITE)
    assert rst_ify(context, text) == expected


MOVE_FIRST_DATA = [
    ([], [], []),
    (["a", "b", "c"], ["d"], ["a", "b", "c"]),
    (["a", "b", "c"], ["b"], ["b", "a", "c"]),
    (["a", "b", "b", "c"], ["b"], ["b", "a", "b", "c"]),
    (["a", "b", "c"], ["b", "c"], ["b", "c", "a"]),
    (["a", "b", "c"], ["c", "b"], ["c", "b", "a"]),
]


@pytest.mark.parametrize("input, move_to_beginning, expected", MOVE_FIRST_DATA)
def test_move_first(input, move_to_beginning, expected):
    assert move_first(input, *move_to_beginning) == expected


MASSAGE_AUTHOR_NAME = [
    ("", ""),
    ("John Doe (@johndoe) <john.doe@gmail.com>", "John Doe (@johndoe)"),
    ("John Doe (@johndoe) john+doe@gmail.com", "John Doe (@johndoe)"),
    ("John Doe (@johndoe) (john-doe@gmail.com)", "John Doe (@johndoe)"),
    ("John Doe (@johndoe, john.doe@gmail.com)", "John Doe (@johndoe, )"),
]


@pytest.mark.parametrize("input, expected", MASSAGE_AUTHOR_NAME)
def test_massage_author_name(input, expected):
    assert massage_author_name(input) == expected


TO_JSON = [
    ("", '""'),
    ("<foo>", '"<foo>"'),
    (True, "true"),
    ({"b": False, "a": 1}, '{"a": 1, "b": false}'),
]


@pytest.mark.parametrize("input, expected", TO_JSON)
def test_to_json(input, expected):
    assert to_json(input) == expected


TO_INI_VALUE = [
    ("", '""'),
    ("<foo>", "<foo>"),
    (1, "1"),
    (True, "true"),
    (["a", "b", "c", 2, False], "a, b, c, 2, false"),
]


@pytest.mark.parametrize("input, expected", TO_INI_VALUE)
def test_to_ini_value(input, expected):
    assert to_ini_value(input) == expected
