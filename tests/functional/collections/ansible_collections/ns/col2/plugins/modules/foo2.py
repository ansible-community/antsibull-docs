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
    - "Someone else (@ansible)"
short_description: Foo two
description:
    - Does some foo on the remote host.
    - A broken reference R(asdfasdfoobarTHISDOESNOTEXIST,asdfasdfoobarTHISDOESNOTEXIST).
    - The option O(foo) exists, but O(foobar) does not.
    - The return value RV(bar) exists, but RV(barbaz) does not.
    - "Again existing: O(ns.col2.foo#module:foo=1), RV(ns.col2.foo#module:bar=2)"
    - "Again not existing: O(ns.col2.foo#module:foobar=1), RV(ns.col2.foo#module:barbaz=2)"
options:
    foo:
        description: The foo source.
        type: str
    bar:
        description:
          - Bar.
          - Some O(broken markup).
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
                    - RV(foobarbaz) does not exist.
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
        details:
          - The module M(boo) is not using an FQCN.
          - Sometimes our markup is B(broken.
        support: N/A
        platforms: posix
"""

EXAMPLES = """
name: This is YAML.
"""

RETURN = """
bar:
    description: Some bar.
    returned: success
    type: string
    sample: baz
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
