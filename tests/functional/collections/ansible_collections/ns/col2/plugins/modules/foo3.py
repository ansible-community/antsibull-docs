#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: foo3
author:
    - "Someone else (@ansible)"
short_description: Foo III
description:
    - Does some foo on the remote host.
options:
    foo:
        description: The foo source.
        type: str
    bar:
        description:
          - Bar.
        type: list
        elements: int
    subfoo:
        description: Some recursive foo.
        type: dict
        suboptions:
            foo:
                description:
                    - A sub foo.
                    - Whatever.
                    - Also required when I(subfoo) is specified when I(foo=bar) or C(baz).
                type: str
                required: true

requirements: Foo.

attributes:
    check_mode:
        description: Can run in check_mode and return changed status prediction without modifying target
        support: full
    diff_mode:
        description: Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode
        support: full
    platform:
        description: Target OS/families that can be operated against
        support: N/A
        platforms: posix
"""

EXAMPLES = """
This is not YAML.
"""

RETURN = """
bar:
    description: Some bar.
    returned: success
    type: string or so
    sample: baz
baz:
    baz!
"""

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )
    module.exit_json(bar="baz")


if __name__ == "__main__":
    main()
