# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""
Output format enum.
"""

from __future__ import annotations

from enum import Enum

from antsibull_changelog.config import TextFormat


class OutputFormat(Enum):
    def __init__(
        self,
        output_format: str,
        template_extension: str,
        output_extension: str,
        changelog_format: TextFormat,
    ):
        self._output_format = output_format
        self._template_extension = template_extension
        self._output_extension = output_extension
        self._changelog_format = changelog_format

    ANSIBLE_DOCSITE = (
        "ansible-docsite",
        ".rst.j2",
        ".rst",
        TextFormat.RESTRUCTURED_TEXT,
    )
    SIMPLIFIED_RST = ("simplified-rst", ".rst.j2", ".rst", TextFormat.RESTRUCTURED_TEXT)

    @property
    def output_format(self) -> str:
        return self._output_format

    @property
    def template_extension(self) -> str:
        return self._template_extension

    @property
    def output_extension(self) -> str:
        return self._output_extension

    @property
    def changelog_format(self) -> TextFormat:
        return self._changelog_format

    @classmethod
    def parse(cls, output_format: str) -> OutputFormat:
        for elt in cls:
            if elt.output_format == output_format:
                return elt
        output_formats = ", ".join(sorted(f"'{elt.output_format}'" for elt in cls))
        raise ValueError(
            f"Unknown output format '{output_format}'. Allowed values are {output_formats}"
        )


class FilenameGenerator:
    def __init__(self, *, include_collection_name_in_plugins: bool = False):
        """
        :kwarg include_collection_name_in_plugins: Default False.  Set to True to use the FQCN
            for plugin files instead of only the part without the collection name.
        """
        self._include_collection_name_in_plugins = include_collection_name_in_plugins

    def plugin_basename(self, plugin_fqcn: str, plugin_type: str) -> str:
        """
        Given the plugin's FQCN and type, return the basename for the plugin's documentation's
        filename.
        """
        col_namespace, col_name, plugin_name = plugin_fqcn.split(".", 2)
        prefix = ""
        if self._include_collection_name_in_plugins:
            prefix = f"{col_namespace}.{col_name}."
        return f"{prefix}{plugin_name}_{plugin_type}"

    def plugin_filename(
        self, plugin_fqcn: str, plugin_type: str, output_format: OutputFormat
    ) -> str:
        """
        Given the plugin's FQCN and type, return the plugin's documentation's filename.
        """
        basename = self.plugin_basename(plugin_fqcn, plugin_type)
        return f"{basename}{output_format.output_extension}"
