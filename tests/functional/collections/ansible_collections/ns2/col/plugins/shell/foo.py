# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
name: foo
short_description: Foo shell O(bar)
version_added: 1.0.0
description:
  - This is for the foo shell.
options:
  remote_tmp:
    description:
      - Temporary directory to use on targets when executing tasks.
    default: '~/.ansible/tmp'
    env:
      - name: ANSIBLE_REMOTE_TEMP
      - name: ANSIBLE_REMOTE_TMP
    ini:
      - section: defaults
        key: remote_tmp
    vars:
      - name: ansible_remote_tmp
    version_added: '2.10'
    version_added_collection: ansible.builtin
  bar:
    description: Foo bar.
    type: string
"""

from ansible.plugins.shell import ShellBase


class ShellModule(ShellBase):
    COMPATIBLE_SHELLS = frozenset(("foo"))
    SHELL_FAMILY = "foo"
