# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: extra
    short_description: Use foo O(bar)
    extra: foo
    description:
        - This become plugin uses foo.
        - This is a second paragraph.
    author: Nobody (!UNKNOWN)
    version_added: historical
    deprecated:
        removed_in: 5.0.0
        extra: bar
        why: Boo.
        alternatives: Absolutely none.
    options:
        become_user:
            description: User you 'become' to execute the task.
            default: root
            extra: baz
            ini:
              - section: privilege_escalation
                key: become_user
                version_added: 0.1.0
                extra: bam
              - section: foo_become_plugin
                key: user
                deprecated:
                    extra: foobarbaz
                    why: No idea.
                    version: 4.0.0
                    alternatives: None.
            vars:
              - name: ansible_become_user
                extra: barbaz
              - name: ansible_foo_user
                version_added: 0.1.0
                deprecated:
                    extra: foobarbaz
                    why: No idea.
                    version: 4.0.0
                    alternatives: None.
            env:
              - name: ANSIBLE_BECOME_USER
                version_added: 0.1.0
                extra: foobam
              - name: ANSIBLE_FOO_USER
                deprecated:
                    extra: foobarbaz
                    why: No idea.
                    version: 4.0.0
                    alternatives: None.
            keyword:
              - name: become_user
                version_added: 0.1.0
                extra: foobar
                deprecated:
                    extra: foobarbaz
                    why: No idea.
                    version: 4.0.0
                    alternatives: None.
            deprecated:
                extra: foobaz
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
    name = "ns2.col.extra"
