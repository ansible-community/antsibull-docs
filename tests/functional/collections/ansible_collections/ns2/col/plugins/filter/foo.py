# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
  name: foo
  version_added: 1.3.0
  short_description: The foo filter O(bar)
  description:
    - Do some fooing.
  options:
    _input:
      description: The main input.
      type: str
      required: true
    foo:
      description: Some foo.
      type: list
      elements: dictionary
      required: true
    bar:
      description: Some bar.
      type: string
"""

EXAMPLES = r"""
some_var: "{{ 'foo' | ns2.col.foo }}"
"""

RETURN = r"""
  _value:
    description: The result.
    type: str
"""


def foo(input, foo):
    return "FOO:{0}:BAR".format(input)


class FilterModule(object):
    def filters(self):
        return {
            "foo": foo,
        }
