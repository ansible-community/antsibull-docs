# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: extra
    version_added: 0.5.0
    short_description: The extra inventory
    description:
        - Loads inventory from foo.
    extra: Toplevel.
    options:
        bar:
            description: Foo bar.
            type: string
            extra: Option.
"""

EXAMPLES = """
foo:
    bar!
"""

from ansible.plugins.inventory import BaseFileInventoryPlugin


class InventoryModule(BaseFileInventoryPlugin):
    NAME = "ns2.col.extra"
