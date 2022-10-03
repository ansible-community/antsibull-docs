# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
name: foo
short_description: Foo shell
version_added: 1.0.0
description:
  - This is for the foo shell.
extends_documentation_fragment:
  - shell_common
'''

from ansible.plugins.shell import ShellBase


class ShellModule(ShellBase):
    COMPATIBLE_SHELLS = frozenset(('foo'))
    SHELL_FAMILY = 'foo'
