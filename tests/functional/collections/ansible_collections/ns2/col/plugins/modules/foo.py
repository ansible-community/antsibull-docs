#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: foo
author:
    - "Ansible Core Team"
    - "Someone else (@ansible)"
version_added: "2.0.0"
short_description: Do some foo
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
          - Independent from I(foo).
        type: list
        elements: int
        aliases:
          - baz
    subfoo:
        description: Some recursive foo.
        version_added: 2.0.0
        type: dict
        suboptions:
            foo:
                description:
                    - A sub foo.
                    - Whatever.
                    - Also required when I(subfoo) is specified when I(foo=bar) or C(baz).
                type: str
                required: true

requirements:
    - Foo on remote.

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
'''

EXAMPLES = '''
- name: Do some foo
  ns2.col.foo:
    foo: '{{ foo }}'
    bar:
      - 1
      - 2
      - 3
    subfoo:
      foo: hoo!
'''

RETURN = '''
bar:
    description: Some bar.
    returned: success
    type: str
    sample: baz
'''

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            foo=dict(type='str', required=True),
            bar=dict(type='list', elements='int', aliases=['baz']),
            subfoo=dict(
                type='dict',
                options=dict(
                    foo=dict(type='str', required=True)
                )
            ),
        ),
        supports_check_mode=True,
    )
    module.exit_json(bar='baz')


if __name__ == '__main__':
    main()
