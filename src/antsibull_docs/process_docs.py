# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Utilities for processing documentation."""

from __future__ import annotations

import asyncio
import typing as t
from collections import defaultdict
from collections.abc import Iterable, Mapping, MutableMapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from string import ascii_uppercase as _CAPITAL_LETTERS_STRING

import pydantic as p
import pydantic_core
from antsibull_core.logging import log
from antsibull_core.schemas.collection_meta import CollectionsMetadata

from . import app_context
from .docs_parsing.fqcn import get_fqcn_parts
from .schemas.docs import DOCS_SCHEMAS
from .schemas.docs.base import BaseModel
from .write_docs import BasicPluginInfo

mlog = log.fields(mod=__name__)

#: Mapping of plugins to nonfatal errors.  This is the type to use when returning the mapping.
PluginErrorsRT = defaultdict[str, defaultdict[str, list[str]]]


def get_collection_namespaces(
    collection_names: Iterable[str], *, collection_meta: CollectionsMetadata | None
) -> dict[str, list[str]]:
    """
    Return the plugins which are in each collection.

    :arg collection_names: An iterable of collection names.
    :kwarg collection_meta: Optional collection metadata. If provided, will
        ensure that namespaces that only contain removed collections are also
        present (with an empty collection list).
    :returns: Mapping from collection namespaces to list of collection names.
    """
    namespaces = defaultdict(list)
    for collection_name in collection_names:
        namespace, name = collection_name.split(".", 1)
        namespaces[namespace].append(name)
    if collection_meta:
        for collection_name in collection_meta.removed_collections:
            namespace, name = collection_name.split(".", 1)
            # Simply make sure that there's an entry for the namespace:
            namespaces[namespace]  # pylint:disable=pointless-statement
    return namespaces


_CAPITAL_LETTERS = tuple(_CAPITAL_LETTERS_STRING)


_PREFIXES = [
    ("attributes", str),
    ("seealso", int),
    ("entry_points", str, "attributes", str),
    ("entry_points", str, "seealso", int),
    ("doc", "attributes", str),
    ("doc", "seealso", int),
    ("doc", "entry_points", str, "attributes", str),
    ("doc", "entry_points", str, "seealso", int),
]


def _match_prefix(
    location: Sequence[int | str], prefix: tuple[str | type, ...]
) -> bool:
    if len(location) < len(prefix) + 1:
        return False
    if not isinstance(last := location[len(prefix)], str) or not last.startswith(
        _CAPITAL_LETTERS
    ):
        return False
    for loc, elt in zip(location, prefix):
        if isinstance(elt, str):
            if loc != elt:
                return False
        else:
            if not isinstance(loc, elt):
                return False
    return True


def _exc_to_string(exc: p.ValidationError, model_name: str) -> str:
    def _display_error_loc(error: pydantic_core.ErrorDetails) -> str:
        # pydantic 2 includes the class name of a t.Union[] in the location list.
        # For example:
        #
        #   entry_points -> main -> seealso -> 1 -> SeeAlsoPluginSchema -> extra
        #
        # We don't want to expose that to the user, so we have to filter these
        # out. Simply checking for strings starting with an upper-case (or even
        # a specific list) won't work, since keys for `options` and `suboptions`
        # can be arbitrary strings.
        location = error["loc"]
        for prefix in _PREFIXES:
            if _match_prefix(location, prefix):
                location = location[: len(prefix)] + location[len(prefix) + 1 :]
        return " -> ".join(str(e) for e in location)

    def _display_error_type_and_ctx(error: pydantic_core.ErrorDetails) -> str:
        result = "type=" + error["type"]
        ctx = error.get("ctx")
        if ctx:
            result += "".join(f"; {k}={v}" for k, v in ctx.items())
        return result

    def display_errors(errors: list[pydantic_core.ErrorDetails]) -> str:
        return "\n".join(
            f'{_display_error_loc(e)}\n  {e["msg"]} ({_display_error_type_and_ctx(e)})'
            for e in errors
        )

    errors = exc.errors()
    no_errors = len(errors)
    return (
        f'{no_errors} validation error{"" if no_errors == 1 else "s"} for {model_name}\n'
        f"{display_errors(errors)}"
    )


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
        role_schema: type[BaseModel] = DOCS_SCHEMAS[
            plugin_type
        ]  # type: ignore[attr-defined, assignment]
        try:
            parsed = role_schema.model_validate(plugin_info)
            return parsed.model_dump(by_alias=True), errors
        except p.ValidationError as e:
            raise ValueError(  # pylint:disable=raise-missing-from
                _exc_to_string(e, role_schema.__name__)
            )

    new_info: dict[str, t.Any] = {}
    # Note: loop through "doc" before any other keys.
    for field in ("doc", "examples", "return"):
        schema: type[BaseModel] = DOCS_SCHEMAS[plugin_type][
            field
        ]  # type: ignore[index, assignment]
        try:
            field_model = schema.model_validate({field: plugin_info.get(field)})
        except p.ValidationError as e:
            if field == "doc":
                # We can't recover if there's not a doc field
                # pydantic exceptions are not picklable (probably due to bugs in the pickle module)
                # so convert it to an exception type which is picklable
                raise ValueError(  # pylint:disable=raise-missing-from
                    _exc_to_string(e, schema.__name__)
                )

            # But we can use the default value (some variant of "empty") for everything else
            # Note: We looped through doc first and returned an exception if doc did not normalize
            # so we're able to use it in the error message here.
            errors.append(
                f'Unable to normalize {new_info["doc"]["name"]}: {field}'
                f" due to: {_exc_to_string(e, schema.__name__)}"
            )

            field_model = DOCS_SCHEMAS[plugin_type][field]()  # type: ignore[index]

        new_info.update(field_model.model_dump(by_alias=True))

    return (new_info, errors)


async def normalize_all_plugin_info(
    plugin_info: Mapping[str, Mapping[str, t.Any]],
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
    new_plugin_info = defaultdict(dict)
    nonfatal_errors: PluginErrorsRT = defaultdict(lambda: defaultdict(list))
    for (plugin_type, plugin_name), plugin_record in zip(normalizers, results):
        # Errors which broke doc parsing (and therefore we won't have enough info to
        # build a docs page)
        if isinstance(plugin_record, BaseException):
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
) -> defaultdict[str, defaultdict[str, dict[str, BasicPluginInfo]]]:
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
    plugin_contents: defaultdict[str, defaultdict[str, dict[str, BasicPluginInfo]]]
    plugin_contents = defaultdict(lambda: defaultdict(dict))
    # Some plugins won't have an entry in the plugin_info because documentation failed to parse.
    # Those should be documented in the nonfatal_errors information.
    for plugin_type, plugin_list in nonfatal_errors.items():
        for plugin_name, dummy_ in plugin_list.items():
            namespace, collection, short_name = get_fqcn_parts(plugin_name)
            plugin_contents[plugin_type][".".join((namespace, collection))][
                short_name
            ] = BasicPluginInfo.empty()

    for plugin_type, plugin_dict in plugin_info.items():
        for plugin_name, plugin_desc in plugin_dict.items():
            namespace, collection, short_name = get_fqcn_parts(plugin_name)
            plugin_contents[plugin_type][".".join((namespace, collection))][
                short_name
            ] = BasicPluginInfo.from_doc(plugin_desc, plugin_type)

    return plugin_contents


def get_callback_plugin_contents(
    plugin_info: Mapping[str, Mapping[str, t.Any]],
) -> defaultdict[str, defaultdict[str, dict[str, BasicPluginInfo]]]:
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
    callback_plugin_contents: defaultdict[
        str, defaultdict[str, dict[str, BasicPluginInfo]]
    ]
    callback_plugin_contents = defaultdict(lambda: defaultdict(dict))

    if plugin_info.get("callback"):
        for plugin_name, plugin_desc in plugin_info["callback"].items():
            if "doc" in plugin_desc:
                callback_type = plugin_desc["doc"].get("type") or ""
                if callback_type:
                    namespace, collection, short_name = get_fqcn_parts(plugin_name)
                    collection_name = ".".join((namespace, collection))
                    callback_plugin_contents[callback_type][collection_name][
                        short_name
                    ] = BasicPluginInfo.from_doc(plugin_desc, "callback")

    return callback_plugin_contents


def get_collection_contents(
    plugin_content: Mapping[str, Mapping[str, Mapping[str, BasicPluginInfo]]],
) -> defaultdict[str, dict[str, Mapping[str, BasicPluginInfo]]]:
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
    collection_plugins: defaultdict[str, dict[str, Mapping[str, BasicPluginInfo]]] = (
        defaultdict(dict)
    )

    for plugin_type, collection_data in plugin_content.items():
        for collection_name, plugin_data in collection_data.items():
            collection_plugins[collection_name][plugin_type] = plugin_data

    return collection_plugins
