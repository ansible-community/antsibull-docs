# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project

from __future__ import annotations

import pytest

from antsibull_docs.jinja2 import OutputFormat
from antsibull_docs.markup.rstify import (
    get_rst_formatter_link_provider,
    rst_escape,
    rst_ify,
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
    formatter, link_provider = get_rst_formatter_link_provider(
        OutputFormat.ANSIBLE_DOCSITE
    )
    assert (
        rst_ify(
            text,
            formatter,
            plugin_fqcn="foo.bar.baz",
            plugin_type="module",
            link_provider=link_provider,
        )[0]
        == expected
    )


RST_ESCAPE_DATA = {
    "": "",
    "no-op": "no-op",
    None: "None",
    1: "1",
    "*": "\\*",
    "_": "\\_",
    "<": "\\<",
    ">": "\\>",
    "`": "\\`",
    "\\": "\\\\",
    "\\*": "\\\\\\*",
    "*\\": "\\*\\\\",
    ":role:`test`": ":role:\\`test\\`",
}


@pytest.mark.parametrize("value, expected", RST_ESCAPE_DATA.items())
def test_escape_ify(value, expected):
    assert rst_escape(value) == expected
