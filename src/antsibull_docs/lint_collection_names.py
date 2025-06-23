# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""Lint collection names."""

from __future__ import annotations

import dataclasses
import typing as t

from .markup.semantic_helper import split_option_like_name
from .utils.collection_names import (
    NameCollection,
    ValidCollectionRefs,
)

_NAME_SEPARATOR = "/"
_ROLE_ENTRYPOINT_SEPARATOR = "###"


def _get_fqcn_collection_name(fqcn: str) -> str:
    return ".".join(fqcn.split(".")[:2])


def _create_lookup(role_entrypoint: str | None, link: list[str]) -> str:
    lookup = _NAME_SEPARATOR.join(link)
    if role_entrypoint is not None:
        lookup = f"{role_entrypoint}{_ROLE_ENTRYPOINT_SEPARATOR}{lookup}"
    return lookup


@dataclasses.dataclass
class Plugin:
    plugin_fqcn: str
    plugin_type: str
    role_entrypoint: str | None = None


class CollectionNameLinter:
    def __init__(
        self,
        *,
        collection_name: str,
        name_collection: NameCollection,
        validate_collections_refs: ValidCollectionRefs = "self",
        disallow_unknown_collection_refs: bool = False,
    ):
        self._name_collection = name_collection
        self._collection_name_prefix = f"{collection_name}."
        self._validate_collections_refs = validate_collections_refs
        self._disallow_unknown_collection_refs = disallow_unknown_collection_refs

    def validate_collection_name(self, collection_name: str) -> list[str]:
        if self._validate_collections_refs == "self":
            if f"{collection_name}." == self._collection_name_prefix:
                return []
        else:
            if self._name_collection.is_valid_collection(f"{collection_name}."):
                return []
        if self._disallow_unknown_collection_refs:
            return [f"a reference to the collection {collection_name} is not allowed"]
        return []

    def has_plugins_of_type(self, collection_name: str, plugin_type: str) -> bool:
        if self._name_collection.is_valid_collection(f"{collection_name}."):
            return self._name_collection.has_plugins(collection_name, plugin_type)
        # In case we don't know, simply say "yes"
        return True

    def _report_disallowed_collection(
        self, errors: list[str], plugin_fqcn: str
    ) -> None:
        errors.append(
            f"a reference to the collection {_get_fqcn_collection_name(plugin_fqcn)} is not allowed"
        )

    def _validate_plugin_fqcn(self, errors: list[str], plugin: Plugin) -> bool:
        if self._validate_collections_refs == "self":
            if not plugin.plugin_fqcn.startswith(self._collection_name_prefix):
                if self._disallow_unknown_collection_refs:
                    self._report_disallowed_collection(errors, plugin.plugin_fqcn)
                return False
        if self._name_collection.is_valid_plugin(
            plugin.plugin_fqcn, plugin.plugin_type
        ):
            if (
                plugin.plugin_type == "role"
                and plugin.role_entrypoint is not None
                and not self._name_collection.is_valid_role_entrypoint(
                    plugin.plugin_fqcn, plugin.role_entrypoint
                )
            ):
                errors.append(
                    f"the role {plugin.plugin_fqcn} has no entrypoint {plugin.role_entrypoint}"
                )
            return True
        if self._name_collection.is_valid_collection(plugin.plugin_fqcn):
            prefix = "" if plugin.plugin_type in ("role", "module") else " plugin"
            errors.append(
                f"there is no {plugin.plugin_type}{prefix} {plugin.plugin_fqcn}"
            )
        elif self._disallow_unknown_collection_refs:
            self._report_disallowed_collection(errors, plugin.plugin_fqcn)
        return False

    def validate_plugin_fqcn(self, plugin: Plugin) -> list[str]:
        errors: list[str] = []
        self._validate_plugin_fqcn(errors, plugin)
        return errors

    def _validate_link(
        self,
        errors: list[str],
        role_entrypoint: str | None,
        name: str,
        name_parts: list[tuple[str, str | None]],
        what: t.Literal["option", "return value"],
        lookup: t.Callable[[str], str | None],
    ):
        link: list[str] = []
        for index, part in enumerate(name_parts):
            link.append(part[0])
            lookup_value = _create_lookup(role_entrypoint, link)
            part_type = lookup(lookup_value)
            if part_type == "list" and part[1] is None and index + 1 < len(name_parts):
                errors.append(
                    f"{what} name {name!r} refers to list {'.'.join(link)} without `[]`"
                )
            if part_type not in ("list", "dict", "dictionary") and part[1] is not None:
                errors.append(
                    f"{what} name {name!r} refers to {'.'.join(link)}"
                    " - which is neither list nor dictionary - with `[]`"
                )
            if (
                part_type in ("dict", "dictionary")
                and part[1] is not None
                and index + 1 < len(name_parts)
            ):
                errors.append(
                    f"{what} name {name!r} refers to dictionary {'.'.join(link)} with `[]`,"
                    " which is only allowed for the last part"
                )

    def validate_option_name(
        self,
        plugin: Plugin | None,
        name: str,
        link: list[str],
    ) -> list[str]:
        errors: list[str] = []
        try:
            name_parts = split_option_like_name(name)
        except ValueError as exc:
            errors.append(f"option name {name!r} cannot be parsed: {exc}")
        if not plugin:
            return errors
        if not self._validate_plugin_fqcn(errors, plugin):
            return errors
        lookup = _create_lookup(plugin.role_entrypoint, link)
        if not self._name_collection.is_valid_option(
            plugin.plugin_fqcn, plugin.plugin_type, lookup
        ):
            prefix = "" if plugin.plugin_type in ("role", "module") else " plugin"
            suffix = (
                ""
                if plugin.plugin_type != "role" or plugin.role_entrypoint is None
                else f"'s entrypoint {plugin.role_entrypoint}"
            )
            errors.append(
                "option name does not reference to an existing option"
                f" of the {plugin.plugin_type}{prefix} {plugin.plugin_fqcn}{suffix}"
            )
        else:
            self._validate_link(
                errors,
                plugin.role_entrypoint,
                name,
                name_parts,
                "option",
                lambda lookup_: self._name_collection.get_option_type(
                    plugin.plugin_fqcn, plugin.plugin_type, lookup_  # type: ignore[union-attr]
                ),
            )
        return errors

    def validate_return_value(
        self,
        plugin: Plugin | None,
        name: str,
        link: list[str],
    ) -> list[str]:
        errors: list[str] = []
        try:
            name_parts = split_option_like_name(name)
        except ValueError as exc:
            errors.append(f"return value name {name!r} cannot be parsed: {exc}")
        if not plugin:
            return errors
        if not self._validate_plugin_fqcn(errors, plugin):
            return errors
        lookup = _create_lookup(plugin.role_entrypoint, link)
        if not self._name_collection.is_valid_return_value(
            plugin.plugin_fqcn, plugin.plugin_type, lookup
        ):
            prefix = "" if plugin.plugin_type in ("role", "module") else " plugin"
            suffix = (
                ""
                if plugin.plugin_type != "role" or plugin.role_entrypoint is None
                else f"'s entrypoint {plugin.role_entrypoint}"
            )
            errors.append(
                "return value name does not reference to an existing return value"
                f" of the {plugin.plugin_type}{prefix} {plugin.plugin_fqcn}{suffix}"
            )
        else:
            self._validate_link(
                errors,
                plugin.role_entrypoint,
                name,
                name_parts,
                "return value",
                lambda lookup_: self._name_collection.get_return_value_type(
                    plugin.plugin_fqcn, plugin.plugin_type, lookup_  # type: ignore[union-attr]
                ),
            )
        return errors
