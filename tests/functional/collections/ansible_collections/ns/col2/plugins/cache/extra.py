# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: extra
    short_description: Some extra attributes
    description:
        - Cache foo files.
    extra: indeed
    version_added: "1.9.0"
    author: Ansible Core (@ansible-core)
    options:
      _uri:
        required: true
        extra: more
        description:
          - Path in which the cache plugin will save the foo files.
        env:
          - name: ANSIBLE_CACHE_PLUGIN_CONNECTION
            extra: More extra.
        ini:
          - key: fact_caching_connection
            section: defaults
            extra: Yes.
        type: path
"""

from ansible.plugins.cache import BaseFileCacheModule


class CacheModule(BaseFileCacheModule):
    pass
