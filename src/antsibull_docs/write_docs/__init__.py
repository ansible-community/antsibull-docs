# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output documentation."""

from __future__ import annotations

import os
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


def _get_collection_dir(
    dest_dir: str,
    namespace: str,
    collection: str,
    /,
    squash_hierarchy: bool = False,
    create_if_not_exists: bool = False,
):
    """
    Compose collection directory.

    :arg dest_dir: Destination directory for the plugin data.  For instance,
        :file:`ansible-checkout/docs/docsite/rst/`.  The directory structure underneath this
        directory will be created if needed.
    :arg namespace: The collection's namespace.
    :arg collection: The collection's name.
    :kwarg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                             Undefined behavior if documentation for multiple collections are
                             created.
    :kwarg create_if_not_exists: If set to ``True``, the directory will be created if it does
                                 not exist. The ``dest_dir`` is assumed to exist.
    """
    if squash_hierarchy:
        return dest_dir

    collection_dir = os.path.join(dest_dir, "collections", namespace, collection)
    if create_if_not_exists:
        # This is dangerous but the code that takes dest_dir from the user checks
        # permissions on it to make it as safe as possible.
        os.makedirs(collection_dir, mode=0o755, exist_ok=True)
    return collection_dir
