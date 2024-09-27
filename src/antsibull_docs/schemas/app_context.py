# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Extended configuration file format."""

import typing as t

import pydantic as p
from antsibull_core.schemas.context import AppContext as CoreAppContext
from antsibull_core.schemas.validators import convert_bool

DEFAULT_COLLECTION_URL_TRANSFORM = (
    "https://galaxy.ansible.com/ui/repo/published/{namespace}/{name}/"
)
DEFAULT_COLLECTION_INSTALL_CMD = "ansible-galaxy collection install {namespace}.{name}"


class DocsAppContext(CoreAppContext):
    # These are antsibull-docs specific
    doc_parsing_backend: t.Literal["auto", "ansible-core-2.13"] = "auto"
    breadcrumbs: p.StrictBool = True
    indexes: p.StrictBool = True
    use_html_blobs: p.StrictBool = False
    add_antsibull_docs_version: p.StrictBool = True

    collection_url: dict[str, str] = {
        "*": DEFAULT_COLLECTION_URL_TRANSFORM,
    }
    collection_install: dict[str, str] = {
        "*": DEFAULT_COLLECTION_INSTALL_CMD,
    }

    # pylint: disable-next=unused-private-member
    __convert_docs_bools = p.field_validator(  # type: ignore
        "breadcrumbs",
        "indexes",
        "use_html_blobs",
        "add_antsibull_docs_version",
        mode="before",
    )(convert_bool)
