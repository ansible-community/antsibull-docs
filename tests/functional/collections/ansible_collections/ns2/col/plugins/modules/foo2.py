#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: foo2
author:
    - "Another one (@ansible-community)"
short_description: Another foo
description:
    - Foo bar.
    - See O(ns2.col.foo#role:main:foo_param_1) for a random role parameter reference. And
      O(ns2.col.foo#role:main:foo_param_2=42) for one with a value.
    - Reference using alias - O(ns2.col.foo_redirect#module:bar) and O(ns2.col.foo_redirect#module:baz).
options:
    bar:
        description:
          - Some bar.
          - See O(ns2.col.foo#role:main:foo_param_1) for a random role parameter reference. And
            O(ns2.col.foo#role:main:foo_param_2=42) for one with a value.
        type: str

attributes:
    check_mode:
        description: Can run in check_mode and return changed status prediction without modifying target
        support: full
    diff_mode:
        description: Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode
        support: N/A
    platform:
        description: Target OS/families that can be operated against
        support: partial
        platforms: posix
    action_group:
        description: Use C(group/ns2.col.foo_group) or C(group/ns2.col.bar_group) in C(module_defaults) to set defaults for this module.
        support: full
        membership:
          - ns2.col.bar_group
          - ns2.col.foo_group
"""

EXAMPLES = """
- name: Do some foo
  ns2.col.foo2:
    bar: foo
"""

RETURN = """
bar:
    description:
      - Some bar.
      - Referencing myself as RV(bar).
      - Do not confuse with O(bar).
    returned: success
    type: str
    sample: baz
"""

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            foo=dict(type="str", required=True),
            bar=dict(type="list", elements="int", aliases=["baz"]),
            subfoo=dict(type="dict", options=dict(foo=dict(type="str", required=True))),
        ),
        supports_check_mode=True,
    )
    module.exit_json(bar="baz")


if __name__ == "__main__":
    main()
