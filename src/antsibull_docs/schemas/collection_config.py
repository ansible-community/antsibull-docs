# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""Schemas for collection config files."""

# Ignore Unitialized attribute errors because BaseModel works some magic
# to initialize the attributes when data is loaded into them.
# pyre-ignore-all-errors[13]

from antsibull_docs._pydantic_compat import v1 as p


class CollectionConfig(p.BaseModel):
    # Whether the collection uses flatmapping to flatten subdirectories in
    # `plugins/*/`.
    flatmap: bool = False

    # List of environment variables that are defined by `.. envvar::` directives
    # in the extra docsite RST files.
    envvar_directives: list[str] = []
