# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
Label helpers.
"""

from __future__ import annotations

from antsibull_docs.utils.rst import massage_rst_label


def get_plugin_ref(plugin_fqcn: str, plugin_type: str) -> str:
    return f"ansible_collections.{plugin_fqcn}_{plugin_type}"


def get_attribute_ref(
    plugin_fqcn: str,
    plugin_type: str,
    role_entrypoint: str | None,
    attribute: str,
) -> str:
    ref = massage_rst_label(attribute)
    ep = (
        f"{role_entrypoint}__"
        if role_entrypoint is not None and plugin_type == "role"
        else ""
    )
    return f"{get_plugin_ref(plugin_fqcn, plugin_type)}__attribute-{ep}{ref}"


def get_option_ref(
    plugin_fqcn: str,
    plugin_type: str,
    role_entrypoint: str | None,
    option: list[str],
) -> str:
    ref = "/".join(massage_rst_label(part) for part in option)
    ep = (
        f"{role_entrypoint}__"
        if role_entrypoint is not None and plugin_type == "role"
        else ""
    )
    return f"{get_plugin_ref(plugin_fqcn, plugin_type)}__parameter-{ep}{ref}"


def get_return_value_ref(
    plugin_fqcn: str,
    plugin_type: str,
    role_entrypoint: str | None,
    return_value: list[str],
) -> str:
    ref = "/".join(massage_rst_label(part) for part in return_value)
    ep = (
        f"{role_entrypoint}__"
        if role_entrypoint is not None and plugin_type == "role"
        else ""
    )
    return f"{get_plugin_ref(plugin_fqcn, plugin_type)}__return-{ep}{ref}"


def get_requirements_ref(
    plugin_fqcn: str,
    plugin_type: str,
    role_entrypoint: str | None = None,
) -> str:
    ep = (
        f"-{role_entrypoint}"
        if role_entrypoint is not None and plugin_type == "role"
        else ""
    )
    return f"{get_plugin_ref(plugin_fqcn, plugin_type)}_requirements{ep}"
