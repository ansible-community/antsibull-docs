# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: foo
    version_added: 0.9.0
    short_description: Load foo O(bar)
    requirements:
        - Enabled in Ansible's configuration.
    description:
        - Load some foo.
        - This is so glorious.
    options:
      _valid_extensions:
        default:
          - .foo
          - .foobar
        description:
          - All extensions to check.
        env:
          - name: ANSIBLE_FOO_FILENAME_EXT
        ini:
          - key: foo_valid_extensions
            section: defaults
        type: list
        elements: string
      bar:
        description: Foo bar.
        type: string
"""

from ansible.plugins.vars import BaseVarsPlugin


class VarsModule(BaseVarsPlugin):
    REQUIRES_ENABLED = True
