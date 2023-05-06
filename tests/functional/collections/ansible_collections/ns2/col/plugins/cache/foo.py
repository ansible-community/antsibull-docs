# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: foo
    short_description: Foo files O(bar)
    description:
        - Cache foo files.
    version_added: "1.9.0"
    author: Ansible Core (@ansible-core)
    options:
      _uri:
        required: true
        description:
          - Path in which the cache plugin will save the foo files.
        env:
          - name: ANSIBLE_CACHE_PLUGIN_CONNECTION
        ini:
          - key: fact_caching_connection
            section: defaults
        type: path
      bar:
        description: Nothing.
        type: str
"""

from ansible.plugins.cache import BaseFileCacheModule


class CacheModule(BaseFileCacheModule):
    pass
