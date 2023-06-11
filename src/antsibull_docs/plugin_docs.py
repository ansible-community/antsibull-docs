# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Lint plugin docs."""

from __future__ import annotations

import typing as t
from collections.abc import Sequence


class _PluginDocsTextWalker:
    _callback: t.Callable[[str, str, str | None], None]

    def _walk_markup_entry(
        self, entry: str, key: str, role_entrypoint: str | None = None
    ) -> None:
        self._callback(entry, key, role_entrypoint)

    def _walk_markup_dict_entry(
        self,
        dictionary: dict[str, t.Any],
        key: str,
        key_path: str,
        role_entrypoint: str | None = None,
    ) -> None:
        value = dictionary.get(key)
        if value is None:
            return
        full_key = f"{key_path} -> {key}"
        if isinstance(value, str):
            self._walk_markup_entry(value, full_key, role_entrypoint=role_entrypoint)
        elif isinstance(value, Sequence):
            for index, entry in enumerate(value):
                if isinstance(entry, str):
                    self._walk_markup_entry(
                        entry,
                        f"{full_key}[{index + 1}]",
                        role_entrypoint=role_entrypoint,
                    )

    def _walk_deprecation(
        self, owner: dict[str, t.Any], key_path: str, role_entrypoint: str | None = None
    ) -> None:
        if "deprecated" not in owner:
            return
        key_path = f"{key_path} -> deprecated"
        deprecated = owner["deprecated"]
        self._walk_markup_dict_entry(
            deprecated, "why", key_path, role_entrypoint=role_entrypoint
        )
        self._walk_markup_dict_entry(
            deprecated, "alternative", key_path, role_entrypoint=role_entrypoint
        )

    def _walk_options(
        self,
        options: dict[str, t.Any],
        key_path: str,
        role_entrypoint: str | None = None,
    ) -> None:
        for opt, data in sorted(options.items()):
            opt_key = f"{key_path} -> {opt}"
            self._walk_markup_dict_entry(
                data, "description", opt_key, role_entrypoint=role_entrypoint
            )
            self._walk_deprecation(data, opt_key, role_entrypoint=role_entrypoint)
            for sub in ("cli", "env", "ini", "vars", "keyword"):
                if sub in data:
                    for index, sub_data in enumerate(data[sub]):
                        sub_key = f"{opt_key} -> {sub}[{index + 1}]"
                        self._walk_deprecation(
                            sub_data, sub_key, role_entrypoint=role_entrypoint
                        )
            for sub_key in ("options", "suboptions"):
                if sub_key in data:
                    self._walk_options(
                        data[sub_key],
                        f"{opt_key} -> {sub_key}",
                        role_entrypoint=role_entrypoint,
                    )

    def _walk_return_values(
        self,
        return_values: dict[str, t.Any],
        key_path: str,
        role_entrypoint: str | None = None,
    ) -> None:
        for rv, data in sorted(return_values.items()):
            rv_key = f"{key_path} -> {rv}"
            self._walk_markup_dict_entry(
                data, "description", rv_key, role_entrypoint=role_entrypoint
            )
            self._walk_markup_dict_entry(
                data, "returned", rv_key, role_entrypoint=role_entrypoint
            )
            if "contains" in data:
                self._walk_return_values(
                    data["contains"],
                    f"{rv_key} -> contains",
                    role_entrypoint=role_entrypoint,
                )

    def _walk_seealso(
        self, owner: dict[str, t.Any], key_path: str, role_entrypoint: str | None = None
    ) -> None:
        if "seealso" not in owner:
            return
        key_path = f"{key_path} -> seealso"
        seealso = owner["seealso"]
        for index, entry in enumerate(seealso):
            entry_path = f"{key_path}[{index + 1}]"
            self._walk_markup_dict_entry(
                entry, "description", entry_path, role_entrypoint=role_entrypoint
            )
            self._walk_markup_dict_entry(
                entry, "name", entry_path, role_entrypoint=role_entrypoint
            )

    def _walk_attributes(
        self, owner: dict[str, t.Any], key_path: str, role_entrypoint: str | None = None
    ) -> None:
        if "attributes" not in owner:
            return
        key_path = f"{key_path} -> attributes"
        attributes = owner["attributes"]
        for attribute, data in sorted(attributes.items()):
            attribute_path = f"{key_path} -> {attribute}"
            self._walk_markup_dict_entry(
                data, "description", attribute_path, role_entrypoint=role_entrypoint
            )
            self._walk_markup_dict_entry(
                data, "details", attribute_path, role_entrypoint=role_entrypoint
            )

    def _walk_main(
        self, main: dict[str, t.Any], key_path: str, role_entrypoint: str | None = None
    ) -> None:
        self._walk_deprecation(main, key_path, role_entrypoint=role_entrypoint)
        self._walk_markup_dict_entry(
            main, "short_description", key_path, role_entrypoint=role_entrypoint
        )
        self._walk_markup_dict_entry(
            main, "author", key_path, role_entrypoint=role_entrypoint
        )
        self._walk_markup_dict_entry(
            main, "description", key_path, role_entrypoint=role_entrypoint
        )
        self._walk_markup_dict_entry(
            main, "notes", key_path, role_entrypoint=role_entrypoint
        )
        self._walk_markup_dict_entry(
            main, "requirements", key_path, role_entrypoint=role_entrypoint
        )
        self._walk_markup_dict_entry(
            main, "todo", key_path, role_entrypoint=role_entrypoint
        )
        self._walk_seealso(main, key_path, role_entrypoint=role_entrypoint)
        self._walk_attributes(main, key_path, role_entrypoint=role_entrypoint)
        if "options" in main:
            self._walk_options(
                main["options"],
                f"{key_path} -> options",
                role_entrypoint=role_entrypoint,
            )

    def __init__(
        self,
        plugin_record: dict[str, t.Any],
        callback: t.Callable[[str, str, str | None], None],
    ):
        self._callback = callback
        self._plugin_record = plugin_record

    def walk(self):
        if "doc" in self._plugin_record:
            self._walk_main(self._plugin_record["doc"], "DOCUMENTATION")
        if "return" in self._plugin_record:
            self._walk_return_values(self._plugin_record["return"], "RETURN")
        if "entry_points" in self._plugin_record:
            for entry_point, data in sorted(
                self._plugin_record["entry_points"].items()
            ):
                self._walk_main(
                    data,
                    f"entry_points -> {entry_point}",
                    role_entrypoint=entry_point,
                )


def walk_plugin_docs_texts(
    plugin_record: dict[str, t.Any],
    callback: t.Callable[[str, str, str | None], None],
) -> None:
    """
    Walk over all text fields of a plugin/module/role documentation.

    For every text, calls ``callback(entry, human_readable_key, role_entrypoint)``.
    """
    _PluginDocsTextWalker(plugin_record, callback).walk()
