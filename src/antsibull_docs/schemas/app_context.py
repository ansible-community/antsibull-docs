# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Extended configuration file format."""

# Ignore Unitialized attribute errors because BaseModel works some magic
# to initialize the attributes when data is loaded into them.
# pyre-ignore-all-errors[13]

import pydantic as p
from antsibull_core.schemas.context import AppContext as CoreAppContext
from antsibull_core.schemas.validators import convert_bool

from antsibull_docs._pydantic_compat import Field

#: Valid choices for the docs parsing backend
DOC_PARSING_BACKEND_CHOICES_F = Field("auto", regex="^(auto|ansible-core-2\\.13)$")


DEFAULT_COLLECTION_URL_TRANSFORM = (
    "https://galaxy.ansible.com/ui/repo/published/{namespace}/{name}/"
)
DEFAULT_COLLECTION_INSTALL_CMD = "ansible-galaxy collection install {namespace}.{name}"


class DocsAppContext(CoreAppContext):
    # These are already defined in CoreConfigModel, but deprecated and will be removed in
    # antsibull-core 3.0.0
    doc_parsing_backend: str = DOC_PARSING_BACKEND_CHOICES_F

    # These are antsibull-docs specific
    breadcrumbs: p.StrictBool = True
    indexes: p.StrictBool = True
    use_html_blobs: p.StrictBool = False

    collection_url: dict[str, str] = {
        "*": DEFAULT_COLLECTION_URL_TRANSFORM,
    }
    collection_install: dict[str, str] = {
        "*": DEFAULT_COLLECTION_INSTALL_CMD,
    }

    # pylint: disable-next=unused-private-member
    __convert_docs_bools = p.validator(  # type: ignore
        "breadcrumbs", "indexes", "use_html_blobs", pre=True, allow_reuse=True
    )(convert_bool)
