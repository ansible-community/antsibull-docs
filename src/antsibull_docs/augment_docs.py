# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Augment data from plugin documenation with additional values."""

from __future__ import annotations

import typing as t
from collections import defaultdict
from collections.abc import Mapping, MutableMapping

from .docs_parsing.routing import CollectionRoutingT
from .utils.rst import massage_rst_label


def add_full_key(
    options_data: Mapping[str, t.Any],
    suboption_entry: str,
    _full_key: list[str] | None = None,
    _full_keys: list[list[str]] | None = None,
) -> None:
    """
    Add information on the strucfture of a dict value in options or returns.

    suboptions and contains are used for nested information (an option taking a dict which has
    a deeply nested structure, for instance.)  They describe each entry into the dict.  When
    constructing documentation which uses that, it can be useful to know the hierarchy leads to
    that entry (for instance, to make a target for an html href).  This function adds that
    information to a ``full_key`` field on the suboptions' entry.

    :arg options_data: The documentation data which is going to be analyzed and updated.
    :arg suboption_entry: The name of the suboptions key in the data.  For options data, this is
        ``suboptions``.  For returndocs, it is ``contains``.
    :kwarg _full_key: This is a recursive function.  After we pass the first level of nesting,
        ``_full_key`` is set to record the names of the upper levels of the hierarchy.
    :kwarg _full_keys: This is a recursive function.  After we pass the first level of nesting,
        ``_full_keys`` is a list of sets to record the names of the upper levels of the hierarchy,
        including all aliases for all names involved.

    .. warning:: This function operates by side-effect.  The options_data dictionay is modified
        directly.
    """
    if _full_key is None:
        _full_key = []
    if _full_keys is None:
        _full_keys = [[]]

    for key, entry in options_data.items():
        # Make sure that "full key" is contained
        full_key_k = _full_key + [key]
        full_keys_k = [fk + [key] for fk in _full_keys]
        if "aliases" in entry:
            for alias in entry["aliases"]:
                full_keys_k.extend([fk + [alias] for fk in _full_keys])
        entry["full_key"] = full_key_k
        entry["full_keys"] = full_keys_k
        entry["full_keys_rst"] = sorted(
            {tuple(massage_rst_label(p) for p in fk) for fk in full_keys_k}
        )

        # Process suboptions
        suboptions = entry.get(suboption_entry)
        if suboptions:
            add_full_key(
                suboptions,
                suboption_entry=suboption_entry,
                _full_key=full_key_k,
                _full_keys=full_keys_k,
            )


def _add_seealso(
    seealso: list[MutableMapping[str, t.Any]],
    plugin_info: Mapping[str, Mapping[str, t.Any]],
) -> None:
    for entry in seealso:
        if entry.get("description"):
            continue
        plugin = ""
        plugin_type = "module"
        if entry.get("module"):
            plugin = entry["module"]
        elif entry.get("plugin") and entry.get("plugin_type"):
            plugin = entry["plugin"]
            plugin_type = entry["plugin_type"]
        else:
            continue
        if plugin_type not in plugin_info or plugin not in plugin_info[plugin_type]:
            # We cannot use KeyError in the following try/except since plugin_info could
            # be a defaultdict, which effectively creates new entries.
            continue
        try:
            desc = plugin_info[plugin_type][plugin]["doc"]["short_description"]
        except (KeyError, TypeError):
            desc = None
        if desc:
            if not desc.endswith((".", "!", "?")):
                desc += "."
            entry["description"] = desc


def _add_aliases(
    plugin_name: str,
    plugin_record: MutableMapping[str, t.Any],
    routing_sources: list[str],
) -> None:
    collection_prefix = ".".join(plugin_name.split(".", 2)[:2]) + "."
    for redirect in routing_sources:
        if redirect.startswith(collection_prefix):
            alias = redirect[len(collection_prefix) :]
            if "aliases" not in plugin_record:
                plugin_record["aliases"] = []
            if alias not in plugin_record["aliases"]:
                plugin_record["aliases"].append(alias)


def augment_docs(
    plugin_info: MutableMapping[str, MutableMapping[str, t.Any]],
    collection_routing: CollectionRoutingT,
) -> None:
    """
    Add additional data to the data extracted from the plugins.

    The additional data is calculated from the existing data and then added to the data.
    Current Augmentations:

    * ``full_key`` allows displaying nested suboptions and return dicts.
    * In see-alsos that reference to modules or plugins but that have no description,
      automatically insert the destination's short_description (if available)

    :arg plugin_info: The plugin_info that will be analyzed and augmented.

    .. warning:: This function operates by side-effect.  The plugin_info dictionay is modified
        directly.
    """
    for plugin_type, plugin_map in plugin_info.items():
        # First collect all routing targets
        routing_sources: defaultdict[str, list[str]] = defaultdict(list)
        for plugin_name, plugin_meta in collection_routing.get(plugin_type, {}).items():
            redirect = plugin_meta.get("redirect")
            if isinstance(redirect, str):
                routing_sources[redirect].append(plugin_name)
        # Now augment all plugin records
        for plugin_name, plugin_record in plugin_map.items():
            if plugin_record.get("return"):
                add_full_key(plugin_record["return"], "contains")
            if plugin_record.get("doc"):
                add_full_key(plugin_record["doc"]["options"], "suboptions")
                if plugin_record["doc"].get("seealso"):
                    _add_seealso(plugin_record["doc"]["seealso"], plugin_info)
                _add_aliases(
                    plugin_name, plugin_record["doc"], routing_sources[plugin_name]
                )
            if plugin_record.get("entry_points"):
                for entry_point in plugin_record["entry_points"].values():
                    add_full_key(entry_point["options"], "options")
