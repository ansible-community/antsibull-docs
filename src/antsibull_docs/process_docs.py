# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Utilities for processing documentation."""

import asyncio
import typing as t
from collections import defaultdict
from collections.abc import Iterable, Mapping, MutableMapping
from concurrent.futures import ProcessPoolExecutor

from antsibull_core.logging import log

from antsibull_docs._pydantic_compat import v1

from . import app_context
from .docs_parsing.fqcn import get_fqcn_parts
from .schemas.docs import DOCS_SCHEMAS

mlog = log.fields(mod=__name__)

#: Mapping of plugins to nonfatal errors.  This is the type to use when returning the mapping.
PluginErrorsRT = defaultdict[str, defaultdict[str, list[str]]]


def get_collection_namespaces(collection_names: Iterable[str]) -> dict[str, list[str]]:
    """
    Return the plugins which are in each collection.

    :arg collection_names: An iterable of collection names.
    :returns: Mapping from collection namespaces to list of collection names.
    """
    namespaces = defaultdict(list)
    for collection_name in collection_names:
        namespace, name = collection_name.split(".", 1)
        namespaces[namespace].append(name)
    return namespaces


def normalize_plugin_info(
    plugin_type: str, plugin_info: Mapping[str, t.Any]
) -> tuple[dict[str, t.Any], list[str]]:
    """
    Normalize and validate all of the plugin docs.

    :arg plugin_type: The type of plugins that we're getting docs for.
    :arg plugin_info: Mapping of plugin_info.  The toplevel keys are plugin names.
        See the schema in :mod:`antsibull.schemas.docs` for what the data should look like and just
        how much conversion we can perform on it.
    :returns: A tuple containing a "copy" of plugin_info with all of the data normalized and a list
        of nonfatal errors.  The plugin_info dict will follow the structure expressed in the schemas
        in :mod:`antsibull.schemas.docs`.  The nonfatal errors are strings representing the problems
        encountered.
    """
    # If you wonder why this code isn't showing up in code coverage: that's because it's executed
    # in a subprocess. See normalize_all_plugin_info below.

    if "error" in plugin_info:
        return ({}, [plugin_info["error"]])

    errors: list[str] = []
    if plugin_type == "role":
        try:
            parsed = DOCS_SCHEMAS[plugin_type].parse_obj(plugin_info)  # type: ignore[attr-defined]
            return parsed.dict(by_alias=True), errors
        except v1.ValidationError as e:
            raise ValueError(str(e))  # pylint:disable=raise-missing-from

    new_info: dict[str, t.Any] = {}
    # Note: loop through "doc" before any other keys.
    for field in ("doc", "examples", "return"):
        try:
            schema = DOCS_SCHEMAS[plugin_type][field]  # type: ignore[index]
            field_model = schema.parse_obj({field: plugin_info.get(field)})
        except v1.ValidationError as e:
            if field == "doc":
                # We can't recover if there's not a doc field
                # pydantic exceptions are not picklable (probably due to bugs in the pickle module)
                # so convert it to an exception type which is picklable
                raise ValueError(str(e))  # pylint:disable=raise-missing-from

            # But we can use the default value (some variant of "empty") for everything else
            # Note: We looped through doc first and returned an exception if doc did not normalize
            # so we're able to use it in the error message here.
            errors.append(
                f'Unable to normalize {new_info["doc"]["name"]}: {field}'
                f" due to: {str(e)}"
            )

            field_model = DOCS_SCHEMAS[plugin_type][field].parse_obj({})  # type: ignore[index]

        new_info.update(field_model.dict(by_alias=True))

    return (new_info, errors)


async def normalize_all_plugin_info(
    plugin_info: Mapping[str, Mapping[str, t.Any]]
) -> tuple[dict[str, MutableMapping[str, t.Any]], PluginErrorsRT]:
    """
    Normalize the data in plugin_info so that it is ready to be passed to the templates.

    :arg plugin_info: Mapping of information about plugins.  This contains information about all of
        the plugins that are to be documented. See the schema in :mod:`antsibull.schemas.docs` for
        the structure of the information.
    :returns: A tuple of plugin_info (this is a "copy" of the input plugin_info with all of the
        data normalized) and a mapping of errors.  The plugin_info may have less records than the
        input plugin_info if there were plugin records which failed to validate.  The mapping of
        errors takes the form of:

        .. code-block:: yaml

            plugin_type:
                plugin_name:
                    - error string
                    - error string
    """
    loop = asyncio.get_running_loop()
    lib_ctx = app_context.lib_ctx.get()
    executor = ProcessPoolExecutor(max_workers=lib_ctx.process_max)

    # Normalize each plugin in a subprocess since normalization is CPU bound
    normalizers = {}
    for plugin_type, plugin_list_for_type in plugin_info.items():
        for plugin_name, plugin_record in plugin_list_for_type.items():
            normalizers[(plugin_type, plugin_name)] = loop.run_in_executor(
                executor, normalize_plugin_info, plugin_type, plugin_record
            )

    results = await asyncio.gather(*normalizers.values(), return_exceptions=True)

    new_plugin_info: defaultdict[str, MutableMapping[str, t.Any]]
    new_plugin_info = defaultdict(dict)  # pyre-ignore[9]
    nonfatal_errors: PluginErrorsRT = defaultdict(lambda: defaultdict(list))
    for (plugin_type, plugin_name), plugin_record in zip(normalizers, results):
        # Errors which broke doc parsing (and therefore we won't have enough info to
        # build a docs page)
        if isinstance(plugin_record, Exception):
            # An exception means there is no usable documentation for this plugin
            # Record a nonfatal error and then move on
            nonfatal_errors[plugin_type][plugin_name].append(str(plugin_record))
            continue

        # Errors where we have at least docs.  We can still create a docs page for these with some
        # information left out
        if plugin_record[1]:
            nonfatal_errors[plugin_type][plugin_name].extend(plugin_record[1])

        new_plugin_info[plugin_type][plugin_name] = plugin_record[0]

    return new_plugin_info, nonfatal_errors


def get_plugin_contents(
    plugin_info: Mapping[str, Mapping[str, t.Any]], nonfatal_errors: PluginErrorsRT
) -> defaultdict[str, defaultdict[str, dict[str, str]]]:
    """
    Return the collections with their plugins for every plugin type.

    :arg plugin_info: Mapping of plugin type to a mapping of plugin name to plugin record.
        The plugin_type, plugin_name, and short_description from plugin_records are used.
    :arg nonfatal_errors: mapping of plugin type to plugin name to list of error messages.
        The plugin_type and plugin_name are used.
    :returns: A Mapping of plugin type to a mapping of collection name to a mapping of plugin names
        to short_descriptions.
    plugin_type:
        collection:
            - plugin_short_name: short_description
    """
    plugin_contents: defaultdict[str, defaultdict[str, dict[str, str]]]
    plugin_contents = defaultdict(lambda: defaultdict(dict))
    # Some plugins won't have an entry in the plugin_info because documentation failed to parse.
    # Those should be documented in the nonfatal_errors information.
    for plugin_type, plugin_list in nonfatal_errors.items():
        for plugin_name, dummy_ in plugin_list.items():
            namespace, collection, short_name = get_fqcn_parts(plugin_name)
            plugin_contents[plugin_type][".".join((namespace, collection))][
                short_name
            ] = ""

    for plugin_type, plugin_dict in plugin_info.items():
        for plugin_name, plugin_desc in plugin_dict.items():
            namespace, collection, short_name = get_fqcn_parts(plugin_name)
            if plugin_type == "role":
                desc = ""
                if (
                    "entry_points" in plugin_desc
                    and "main" in plugin_desc["entry_points"]
                ):
                    desc = (
                        plugin_desc["entry_points"]["main"].get("short_description")
                        or ""
                    )
            elif "doc" in plugin_desc:
                desc = plugin_desc["doc"].get("short_description") or ""
            else:
                desc = ""
            plugin_contents[plugin_type][".".join((namespace, collection))][
                short_name
            ] = desc

    return plugin_contents


def get_callback_plugin_contents(
    plugin_info: Mapping[str, Mapping[str, t.Any]],
) -> defaultdict[str, defaultdict[str, dict[str, str]]]:
    """
    Return the collections with their plugins for every callback plugin type.

    :arg plugin_info: Mapping of plugin type to a mapping of plugin name to plugin record.
        The plugin_type, plugin_name, and short_description from plugin_records are used.
    :returns: A Mapping of callback plugin type to a mapping of collection name to a mapping of
        plugin names to short_descriptions.
    callback_type:
        collection:
            - plugin_short_name: short_description
    """
    callback_plugin_contents: defaultdict[str, defaultdict[str, dict[str, str]]]
    callback_plugin_contents = defaultdict(lambda: defaultdict(dict))

    if plugin_info.get("callback"):
        for plugin_name, plugin_desc in plugin_info["callback"].items():
            if "doc" in plugin_desc:
                desc = plugin_desc["doc"].get("short_description") or ""
                callback_type = plugin_desc["doc"].get("type") or ""
                if callback_type:
                    namespace, collection, short_name = get_fqcn_parts(plugin_name)
                    collection_name = ".".join((namespace, collection))
                    callback_plugin_contents[callback_type][collection_name][
                        short_name
                    ] = desc

    return callback_plugin_contents


def get_collection_contents(
    plugin_content: Mapping[str, Mapping[str, Mapping[str, str]]],
) -> defaultdict[str, dict[str, Mapping[str, str]]]:
    """
    Return the plugins which are in each collection.

    :arg plugin_content: Mapping of plugin type to a mapping of collection name to a mapping of
        plugin name to short description.
    :returns: A Mapping of collection name to a mapping of plugin type to a mapping of plugin names
        to short_descriptions.
    collection:
        plugin_type:
            - plugin_short_name: short_description
    """
    collection_plugins: defaultdict[str, dict[str, Mapping[str, str]]] = defaultdict(
        dict
    )

    for plugin_type, collection_data in plugin_content.items():
        for collection_name, plugin_data in collection_data.items():
            collection_plugins[collection_name][plugin_type] = plugin_data

    return collection_plugins
