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
    - E(FOOBAR1), E(FOOBAR2), E(FOOBAR3), E(FOOBAR4).
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
        suboptions:
            foo:
                description:
                    - A sub foo.
                    - Whatever.
                    - Also required when O(subfoo) is specified when O(foo=bar) or V(baz).
                type: str
                required: true

    manager:
        description:
          - The package manager(s) used by the system so we can query the package information.
            This is a list and can support multiple package managers per system, since version 2.8.
          - The 'portage' and 'pkg' options were added in version 2.8.
          - The 'apk' option was added in version 2.11.
          - The 'pkg_info' option was added in version 2.13.
          - Aliases were added in 2.18, to support using C(auto={{ansible_facts['pkg_mgr']}})
        default: ['auto']
        choices:
            auto: Depending on O(strategy), will match the first or all package managers provided, in order
            rpm: For RPM based distros, requires RPM Python bindings, not installed by default on Suse (python3-rpm)
            yum: Alias to rpm
            dnf: Alias to rpm
            dnf5: Alias to rpm
            zypper: Alias to rpm
            apt: For DEB based distros, C(python-apt) package must be installed on targeted hosts
            portage: Handles ebuild packages, it requires the C(qlist) utility, which is part of 'app-portage/portage-utils'
            pkg: libpkg front end (FreeBSD)
            pkg5: Alias to pkg
            pkgng: Alias to pkg
            pacman: Archlinux package manager/builder
            apk: Alpine Linux package manager
            pkg_info: OpenBSD package manager
            openbsd_pkg: Alias to pkg_info
        type: list
        elements: str

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
    action_group:
        description: Use C(group/ns2.col.foo_group) in C(module_defaults) to set defaults for this module.
        support: full
        membership:
          - ns2.col.foo_group

seealso:
    - module: ns2.col.foo2
    - plugin: ns2.col.foo
      plugin_type: lookup
    - module: ansible.builtin.service
      description: The service module.
    - plugin: ansible.builtin.ssh
      plugin_type: connection
      description: The ssh connection plugin.
"""

EXAMPLES = """
- name: Do some foo
  ns2.col.foo:
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
            subfoo=dict(type="dict", options=dict(foo=dict(type="str", required=True))),
        ),
        supports_check_mode=True,
    )
    module.exit_json(bar="baz")


if __name__ == "__main__":
    main()
