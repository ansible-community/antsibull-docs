# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: foo
    author: Felix Fontein (@felixfontein)
    version_added: "1.0.0"
    short_description: Look up some foo O(bar)
    description:
      - This looks up some foo.
      - Whatever that is.
    options:
      _terms:
        description: The stuff to look up.
        required: true
        type: list
        elements: str
      bar:
        description: Foo bar.
        type: string
"""

EXAMPLES = """
- name: Look up bar
  ansible.builtin.debug:
    msg: "{{ lookup('ns2.col.foo', 'bar') }}"
"""

RETURN = """
_raw:
    description:
      - The resulting stuff.
    type: list
    elements: str
"""

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        return terms
