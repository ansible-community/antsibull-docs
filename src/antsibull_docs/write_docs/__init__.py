# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output documentation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from antsibull_core.logging import log
from jinja2 import Template

import antsibull_docs

mlog = log.fields(mod=__name__)

#: Mapping of plugins to nonfatal errors.  This is the type to use when accepting the plugin.
#: The mapping is of plugin_type: plugin_name: [error_msgs]
PluginErrorsT = Mapping[str, Mapping[str, Sequence[str]]]

#: Mapping to collections to plugins.
#: The mapping is collection_name: plugin_type: plugin_name: plugin_short_description
CollectionInfoT = Mapping[str, Mapping[str, Mapping[str, str]]]

#: Plugins grouped first by plugin type, then by collection
#: The mapping is plugin_type: collection_name: plugin_name: plugin_short_description
PluginCollectionInfoT = Mapping[str, Mapping[str, Mapping[str, str]]]


def _render_template(_template: Template, _name: str, **kwargs) -> str:
    try:
        return _template.render(
            antsibull_docs_version=antsibull_docs.__version__, **kwargs
        )
    except Exception as exc:
        raise RuntimeError(f"Error while rendering {_name}") from exc
