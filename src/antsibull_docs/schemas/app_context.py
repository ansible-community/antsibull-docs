# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Extended configuration file format."""

# Ignore Unitialized attribute errors because BaseModel works some magic
# to initialize the attributes when data is loaded into them.
# pyre-ignore-all-errors[13]

import typing as t

import pydantic as p

from antsibull_core.schemas.validators import convert_bool
from antsibull_core.schemas.context import AppContext as CoreAppContext


#: Valid choices for a logging level field
DOC_PARSING_BACKEND_CHOICES_F = p.Field(
    'ansible-internal', regex='^(auto|ansible-doc|ansible-core-2.13|ansible-internal)$')


class DocsAppContext(CoreAppContext):
    # These are already defined in CoreConfigModel, but might vanish from there eventually
    breadcrumbs: p.StrictBool = True
    doc_parsing_backend: str = DOC_PARSING_BACKEND_CHOICES_F
    indexes: p.StrictBool = True
    use_html_blobs: p.StrictBool = False

    # These are antsibull-docs specific
    collection_url: t.Dict[str, str] = {
        '*': 'https://galaxy.ansible.com/{namespace}/{name}',
    }
    collection_install: t.Dict[str, str] = {
        '*': 'ansible-galaxy collection install {namespace}.{name}',
    }

    # pylint: disable-next=unused-private-member
    __convert_docs_bools = p.validator('breadcrumbs', 'indexes', 'use_html_blobs',
                                       pre=True, allow_reuse=True)(convert_bool)
