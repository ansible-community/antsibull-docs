# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""Schemas for collection config files."""

import pydantic as p


class ChangelogConfig(p.BaseModel):
    # Whether to write the changelog
    write_changelog: bool = False


class CollectionConfig(p.BaseModel):
    # Whether the collection uses flatmapping to flatten subdirectories in
    # `plugins/*/`.
    flatmap: bool = False

    # List of environment variables that are defined by `.. envvar::` directives
    # in the extra docsite RST files.
    envvar_directives: list[str] = []

    # Changelog configuration (added in version 2.10.0)
    changelog: ChangelogConfig = ChangelogConfig()
