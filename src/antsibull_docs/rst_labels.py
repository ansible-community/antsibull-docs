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


def get_collection_ref(collection_name: str, what: str = "collection") -> str:
    if what == "communication":
        return f"communication_for_{collection_name}"
    if what == "changelog":
        return f"changelog_for_{collection_name}"
    if what == "changelog-section":
        return f"changelog_section_for_{collection_name}"
    if what == "plugin-index":
        return f"plugin_index_for_{collection_name}"
    if what.startswith("plugins-"):
        plugin_type = what[len("plugins-") :]
        if plugin_type:
            return f"{plugin_type}_plugins_in_{collection_name}"
    # Last case: "collection", "plugins", and catch-all
    return f"plugins_in_{collection_name}"


def get_plugin_ref(
    plugin_fqcn: str, plugin_type: str, entrypoint: str | None = None
) -> str:
    label = f"ansible_collections.{plugin_fqcn}_{plugin_type}"
    if plugin_type == "role" and entrypoint is not None:
        label = f"{label}__entrypoint-{entrypoint}"
    return label


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
