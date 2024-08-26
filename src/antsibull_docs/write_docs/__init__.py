# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output documentation."""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from typing import Any

from antsibull_core.logging import log
from jinja2 import Template

import antsibull_docs

from ..schemas.docs.base import DeprecationSchema, DocSchema
from ..utils.text import sanitize_whitespace as _sanitize_whitespace
from .io import Output

mlog = log.fields(mod=__name__)


class BasicPluginInfo:
    short_description: str
    deprecation: DeprecationSchema | None

    def __init__(self, short_description: str, deprecation: DeprecationSchema | None):
        self.short_description = short_description
        self.deprecation = deprecation

    @classmethod
    def from_doc_schema(cls, doc_schema: DocSchema):
        return cls(doc_schema.short_description, doc_schema.deprecated)

    @classmethod
    def from_doc(cls, plugin_desc: Mapping[str, Any], plugin_type: str):
        desc: str
        deprecation: DeprecationSchema | None = None
        if plugin_type == "role":
            desc = ""
            if "entry_points" in plugin_desc and "main" in plugin_desc["entry_points"]:
                entrypoint = plugin_desc["entry_points"]["main"]
                desc = entrypoint.get("short_description") or ""
                deprecation = entrypoint.get("deprecated")
        elif "doc" in plugin_desc:
            desc = plugin_desc["doc"].get("short_description") or ""
            deprecation = plugin_desc["doc"].get("deprecated")
        else:
            desc = ""
        return cls(desc, deprecation)

    @classmethod
    def empty(cls):
        return cls("", None)


#: Mapping of plugins to nonfatal errors.  This is the type to use when accepting the plugin.
#: The mapping is of plugin_type: plugin_name: [error_msgs]
PluginErrorsT = Mapping[str, Mapping[str, Sequence[str]]]

#: Mapping to collections to plugins.
#: The mapping is collection_name: plugin_type: plugin_name: basic_plugin_info
CollectionInfoT = Mapping[str, Mapping[str, Mapping[str, BasicPluginInfo]]]

#: Plugins grouped first by plugin type, then by collection
#: The mapping is plugin_type: collection_name: plugin_name: basic_plugin_info
PluginCollectionInfoT = Mapping[str, Mapping[str, Mapping[str, BasicPluginInfo]]]


def _render_template(
    _template: Template,
    _name: str,
    /,
    *,
    add_version: bool,
    sanitize_whitespace: bool = True,
    **kwargs,
) -> str:
    try:
        result = _template.render(
            antsibull_docs_version=antsibull_docs.__version__ if add_version else None,
            **kwargs,
        )
        if sanitize_whitespace:
            result = _sanitize_whitespace(
                result, trailing_newline=True, remove_common_leading_whitespace=False
            )
        return result
    except Exception as exc:
        raise RuntimeError(f"Error while rendering {_name}") from exc


def _get_collection_dir(
    output: Output,
    namespace: str,
    collection: str,
    /,
    *,
    squash_hierarchy: bool = False,
    create_if_not_exists: bool = False,
):
    """
    Compose collection directory, for consumption by ``Output``.

    :arg output: Output helper for writing output.
    :arg namespace: The collection's namespace.
    :arg collection: The collection's name.
    :kwarg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                             Undefined behavior if documentation for multiple collections are
                             created.
    :kwarg create_if_not_exists: If set to ``True``, the directory will be created if it does
                                 not exist.
    """
    if squash_hierarchy:
        return "."

    collection_dir = os.path.join("collections", namespace, collection)
    if create_if_not_exists:
        output.ensure_directory(collection_dir)
    return collection_dir
