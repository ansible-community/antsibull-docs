#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: foo
author:
    - "Nobody (@ansible)"
short_description: A test module
description:
  - Some foo bar.
options:
    foo:
        description: Foo.
        type: list
        elements: dict
        suboptions:
            bar:
                description:
                  - Bar.
                type: str
                required: true
"""

RETURN = """
baz:
    description:
      - Some baz.
      - Indeed.
    returned: success
    type: list
    elements: string
    sample:
      - foo
"""

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            foo=dict(
                type="list",
                elements="dict",
                options=dict(
                    bar=dict(type="str", required=True),
                ),
            ),
        ),
        supports_check_mode=True,
    )
    module.exit_json(baz="bam")


if __name__ == "__main__":
    main()
