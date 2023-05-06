# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""
Helpers for parsing semantic markup.
"""

from __future__ import annotations

import re

_ARRAY_STUB_RE = re.compile(r"\[([^\]]*)\]")
_FQCN_TYPE_PREFIX_RE = re.compile(r"^([^.]+\.[^.]+\.[^#]+)#([a-z]+):(.*)$")
_IGNORE_MARKER = "ignore:"


def _remove_array_stubs(text: str) -> str:
    return _ARRAY_STUB_RE.sub("", text)


def _parse(
    text: str,
    plugin_fqcn: str | None,
    plugin_type: str | None,
    what: str,
    require_plugin=False,
) -> tuple[str | None, str | None, str | None, str, str, str | None]:
    """
    Given the contents of O(...) / :ansopt:`...` with potential escaping removed,
    split it into plugin FQCN, plugin type, option link name, option name, and option value.
    """
    value = None
    if "=" in text:
        text, value = text.split("=", 1)
    m = _FQCN_TYPE_PREFIX_RE.match(text)
    if m:
        plugin_fqcn = m.group(1)
        plugin_type = m.group(2)
        text = m.group(3)
    elif require_plugin:
        raise ValueError("Cannot extract plugin name and type")
    elif text.startswith(_IGNORE_MARKER):
        plugin_fqcn = ""
        plugin_type = ""
        text = text[len(_IGNORE_MARKER) :]
    entrypoint: str | None = None
    if plugin_type == "role":
        idx = text.find(":")
        if idx < 0:
            raise ValueError("Role reference is missing entrypoint")
        entrypoint = text[:idx]
        text = text[idx + 1 :]
    if ":" in text or "#" in text:
        raise ValueError(f'Invalid {what} "{text}"')
    return plugin_fqcn, plugin_type, entrypoint, _remove_array_stubs(text), text, value


def parse_option(
    text: str, plugin_fqcn: str | None, plugin_type: str | None, require_plugin=False
) -> tuple[str | None, str | None, str | None, str, str, str | None]:
    """
    Given the contents of O(...) / :ansopt:`...` with potential escaping removed,
    split it into plugin FQCN, plugin type, entrypoint, option link name, option name, and option
    value.
    """
    return _parse(
        text, plugin_fqcn, plugin_type, "option name", require_plugin=require_plugin
    )


def parse_return_value(
    text: str, plugin_fqcn: str | None, plugin_type: str | None, require_plugin=False
) -> tuple[str | None, str | None, str | None, str, str, str | None]:
    """
    Given the contents of RV(...) / :ansretval:`...` with potential escaping removed,
    split it into plugin FQCN, plugin type, entrypoint, return value link name, return value name,
    and return value's value.
    """
    return _parse(
        text,
        plugin_fqcn,
        plugin_type,
        "return value name",
        require_plugin=require_plugin,
    )
