#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: foo
author:
    - "Ansible Core Team"
    - "Someone else (@ansible)"
version_added: "2.0.0"
short_description: Do some foo O(bar)
description:
    - Does some foo on the remote host.
    - Whether foo is magic or not has not yet been determined.
options:
    foo:
        description: The foo source.
        type: str
        required: true
    bar:
        description:
          - A bar.
          - Independent from O(foo).
          - Do not confuse with RV(bar).
        type: list
        elements: int
        aliases:
          - baz
    subfoo:
        description: Some recursive foo.
        version_added: 2.0.0
        type: dict
        aliases:
          - subbaz
        suboptions:
            foo:
                description:
                    - A sub foo.
                    - Whatever.
                    - Also required when O(subfoo) is specified when O(foo=bar) or V(baz).
                    - Note that O(subfoo.foo) is the same as O(subbaz.foo), O(subbaz.bam), and O(subfoo.bam).
                    - E(FOOBAR1), E(FOOBAR2), E(FOOBAR3), E(FOOBAR4).
                type: str
                required: true
                aliases:
                  - bam
"""

EXAMPLES = """
- name: Do some foo
  ns2.flatcol.foo:
    foo: '{{ foo }}'
    bar:
      - 1
      - 2
      - 3
    subfoo:
      foo: hoo!
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
            subfoo=dict(
                type="dict",
                aliases=["subbaz"],
                options=dict(
                    foo=dict(type="str", required=True, aliases=["bam"]),
                ),
            ),
        ),
        supports_check_mode=True,
    )
    module.exit_json(bar="baz")


if __name__ == "__main__":
    main()
