# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: bar
    author: Felix Fontein (@felixfontein)
    version_added: "1.0.0"
    short_description: Look up some bar
    description:
      - This one is private.
    options:
      _terms:
        description: Something
        required: true
        type: list
        elements: dict
"""

EXAMPLES = """
- name: Look up!
  ansible.builtin.debug:
    msg: "{{ lookup('ns2.col.bar', {}) }}"
"""

RETURN = """
_raw:
    description:
      - The resulting stuff.
    type: list
    elements: dict
"""

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        return terms
