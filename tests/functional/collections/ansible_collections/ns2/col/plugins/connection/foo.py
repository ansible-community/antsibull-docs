# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: foo
    short_description: Foo connection O(bar)
    version_added: 1.2.0
    description:
        - This is for the C(foo) connection.
    author: ansible (@core)
    notes:
        - "Some note. B(Something in bold). C(And in code). I(And in italics). An URL: U(https://example.org)."
        - "And another one. L(A link, https://example.com)."
    options:
      host:
          description: Hostname to connect to.
          default: inventory_hostname
          vars:
               - name: inventory_hostname
               - name: ansible_host
               - name: ansible_ssh_host
               - name: delegated_vars['ansible_host']
               - name: delegated_vars['ansible_ssh_host']
      bar:
          description: Foo bar.
          type: int
"""

from ansible.plugins.connection import ConnectionBase


class Connection(ConnectionBase):
    """ssh based connections"""

    transport = "ns2.col.foo"
    has_pipelining = False
