# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
  name: foo
  author: Nobody
  short_description: Is something a foo O(bar)
  description:
    - Check whether the input dictionary is a foo.
  options:
    _input:
      description: Something to test.
      type: dictionary
      required: true
    bar:
      description: Foo bar.
      type: string
"""

EXAMPLES = r"""
some_var: "{{ {'a': 1} is ns2.col.foo }}"
"""

RETURN = r"""
  _value:
    description: Whether the input is a foo.
    type: boolean
"""


def foo(input):
    return True


class TestModule(object):
    def tests(self):
        return {
            "foo": foo,
        }
