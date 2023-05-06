# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: foo
    short_description: Executes tasks in foo
    description:
        - This is something funny. Or at least I think so from its name.
    version_added: 1.1.0
    author: Ansible Core Team
"""

from ansible.plugins.strategy import StrategyBase


class StrategyModule(StrategyBase):
    ALLOW_BASE_THROTTLING = False
