# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: foo
    short_description: Use foo O(bar)
    description:
        - This become plugin uses foo.
        - This is a second paragraph.
    author: Nobody (!UNKNOWN)
    version_added: historical
    deprecated:
        removed_in: 5.0.0
        why: |
          Just some text.
          This one has more than one line.
          And one more.
        alternatives: |
          I don't know
          of any
          alternative.
    options:
        become_user:
            description: User you 'become' to execute the task.
            default: root
            ini:
              - section: privilege_escalation
                key: become_user
                version_added: 0.1.0
              - section: foo_become_plugin
                key: user
            vars:
              - name: ansible_become_user
              - name: ansible_foo_user
                version_added: 0.1.0
            env:
              - name: ANSIBLE_BECOME_USER
                version_added: 0.1.0
              - name: ANSIBLE_FOO_USER
            keyword:
              - name: become_user
                version_added: 0.1.0
        become_exe:
            description: Foo executable.
            default: foo
            version_added: 0.2.0
            ini:
              - section: privilege_escalation
                key: become_exe
              - section: foo_become_plugin
                key: executable
                deprecated:
                    why: Just some text.
                    version: 3.0.0
                    alternatives: nothing
            vars:
              - name: ansible_become_exe
              - name: ansible_foo_exe
                deprecated:
                    why: Just some text.
                    version: 3.0.0
                    alternatives: nothing
            env:
              - name: ANSIBLE_BECOME_EXE
              - name: ANSIBLE_FOO_EXE
                deprecated:
                    why: Just some text.
                    version: 3.0.0
                    alternatives: nothing
            keyword:
              - name: become_exe
        bar:
            description:
                - Bar. B(BAR!)
                - Totally unrelated to O(become_user). Even with O(become_user=foo).
                - Might not be compatible when O(become_user) is V(bar), though.
            type: str
            version_added: 1.2.0
            deprecated:
                why: |
                  Just some other text.
                  This one has more than one line though.
                  One more.
                version: 4.0.0
                alternatives: |
                  nothing
                  relevant
                  I know of
"""

from ansible.plugins.become import BecomeBase


class BecomeModule(BecomeBase):
    name = "ns2.col.foo"
