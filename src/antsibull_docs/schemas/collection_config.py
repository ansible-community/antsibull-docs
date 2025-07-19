# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""Schemas for collection config files."""

import pydantic as p

from sphinx_antsibull_ext.schemas.ansible_output_data import (
    NonRefPostprocessor,
)


class ChangelogConfig(p.BaseModel):
    # Whether to write the changelog
    write_changelog: bool = False


class AnsibleOutputConfig(p.BaseModel):
    # Environment variables to inject for every ansible-output-data
    global_env: dict[str, str] = {}

    # Named postprocessors
    global_postprocessors: dict[str, NonRefPostprocessor] = {}

    @p.field_validator("global_env", mode="before")
    @classmethod
    def convert_dict_values(cls, obj):
        """
        Convert dictionary values to strings that have a unique string representation.
        Values without a unique string representation (floats, booleans, ...)
        are not converted.
        """
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, int):
                    obj[k] = str(v)
        return obj


class CollectionConfig(p.BaseModel):
    # Whether the collection uses flatmapping to flatten subdirectories in
    # `plugins/*/`.
    flatmap: bool = False

    # List of environment variables that are defined by `.. envvar::` directives
    # in the extra docsite RST files.
    envvar_directives: list[str] = []

    # Changelog configuration (added in version 2.10.0)
    changelog: ChangelogConfig = ChangelogConfig()

    # ansible-output subcommand configuration (added in version 2.19.0)
    ansible_output: AnsibleOutputConfig = AnsibleOutputConfig()
