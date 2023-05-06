# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Constant values for use throughout the antsibull codebase."""


from __future__ import annotations

#: All the types of ansible plugins
PLUGIN_TYPES: frozenset[str] = frozenset(
    (
        "become",
        "cache",
        "callback",
        "cliconf",
        "connection",
        "httpapi",
        "inventory",
        "lookup",
        "shell",
        "strategy",
        "vars",
        "module",
        "module_utils",
        "role",
    )
)

#: The subset of PLUGINS which we build documentation for
DOCUMENTABLE_PLUGINS: frozenset[str] = frozenset(
    (
        "become",
        "cache",
        "callback",
        "cliconf",
        "connection",
        "httpapi",
        "inventory",
        "lookup",
        "netconf",
        "shell",
        "vars",
        "module",
        "strategy",
        "role",
        "filter",
        "test",
    )
)


DOCUMENTABLE_PLUGINS_MIN_VERSION: dict[str, str] = {
    "filter": "2.14.0",
    "role": "2.11.0",
    "test": "2.14.0",
}
