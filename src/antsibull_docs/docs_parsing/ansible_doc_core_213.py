# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Parse documentation from ansible plugins using anible-doc from ansible-core 2.13+."""

from __future__ import annotations

import json
import shlex
import textwrap
import typing as t
from collections.abc import Mapping, MutableMapping

import semantic_version as semver
from antsibull_core.logging import log
from antsibull_core.subprocess_util import CalledProcessError
from antsibull_core.vendored.json_utils import _filter_non_json_lines
from packaging.version import Version as PypiVer

from ..constants import DOCUMENTABLE_PLUGINS
from . import AnsibleCollectionMetadata, _get_environment
from .ansible_doc import get_collection_metadata
from .fqcn import get_fqcn_parts, is_collection_name, is_wildcard_collection_name

if t.TYPE_CHECKING:
    from antsibull_core.venv import FakeVenvRunner, VenvRunner


mlog = log.fields(mod=__name__)


async def _call_ansible_doc(
    venv: VenvRunner | FakeVenvRunner,
    env: dict[str, str],
    *parameters: str,
) -> Mapping[str, t.Any]:
    try:
        p = await venv.async_log_run(
            [
                "ansible-doc",
                "-vvv",
                "--metadata-dump",
                "--no-fail-on-errors",
                *parameters,
            ],
            env=env,
        )
    except CalledProcessError as exc:
        if exc.returncode and exc.returncode > 0:
            raise RuntimeError(
                f"The command\n| {shlex.join(exc.cmd)}\nreturned exit status {exc.returncode}"
                f" with error output:\n{textwrap.indent(exc.stderr, '| ')}"
            ) from exc
        raise
    return json.loads(_filter_non_json_lines(p.stdout)[0])


# Versions when flatmapping was removed from collections, resp. when an explicit
# docs/docsite/config.yml file was added.
_MIN_UNFLATMAP_VERSIONS: Mapping[str, semver.Version] = {
    "community.general": semver.Version("6.0.0"),
    "community.network": semver.Version("5.0.0"),
}


def should_flatmap(
    collection: str, collection_metadata: Mapping[str, AnsibleCollectionMetadata]
) -> bool:
    """
    Decide whether a collection should use flatmapping or not.
    """
    # We need the collection metadata to do decide this. If we don't have it, assume that
    # flatmapping is not used.
    meta = collection_metadata.get(collection)
    if meta is None:
        return False

    # First see whether we can decide this by collection name and version. This is necessary
    # for older collections which were using flatmapping but did not have a config file.
    min_version = _MIN_UNFLATMAP_VERSIONS.get(collection)
    if meta.version is not None and min_version is not None:
        return semver.Version(meta.version) < min_version

    # The main resolution mechanism is asking the config file.
    return meta.docs_config.flatmap


def _get_ansible_doc_filters(
    ansible_core_version: PypiVer, collection_names: list[str] | None
) -> list[str]:
    if collection_names and len(collection_names) == 1:
        return collection_names[:1]
    if collection_names and ansible_core_version >= PypiVer("2.16.0.dev0"):
        # ansible-doc of ansible-core 2.16.0.dev0 or later allows multiple filters
        return collection_names
    # ansible-doc of ansible-core < 2.16 only allows *one* filter
    return []


def _get_matcher(wildcard: str) -> t.Callable[[str], bool]:
    namespace, collection = wildcard.split(".", 1)

    if namespace == "*":
        if collection == "*":
            return lambda collection_name: True
        postfix = f".{collection}"
        return lambda collection_name: collection_name.endswith(postfix)

    if collection == "*":
        prefix = f"{namespace}."
        return lambda collection_name: collection_name.startswith(prefix)

    return lambda collection_name: collection_name == wildcard


def _limit_by_wildcards(
    collection_metadata: dict[str, AnsibleCollectionMetadata],
    collection_names: list[str],
) -> tuple[dict[str, AnsibleCollectionMetadata], list[str]]:
    wildcard_matchers: dict[str, t.Callable[[str], bool]] = {}
    wildcard_counters: dict[str, int] = {}
    for wildcard in collection_names:
        wildcard_matchers[wildcard] = _get_matcher(wildcard)
        wildcard_counters[wildcard] = 0

    ret_collection_metadata = {}
    ret_collection_names = []

    for collection_name, collection_data in collection_metadata.items():
        found = False
        for wildcard, matcher in wildcard_matchers.items():
            if matcher(collection_name):
                wildcard_counters[wildcard] += 1
                found = True
        if not found:
            if collection_name == "ansible.builtin":
                ret_collection_metadata[collection_name] = collection_data
            continue
        ret_collection_metadata[collection_name] = collection_data
        ret_collection_names.append(collection_name)

    for wildcard, count in wildcard_counters.items():
        if count == 0:
            raise RuntimeError(
                f"{wildcard} does not match any of the collections"
                f" in {', '.join(sorted(collection_metadata))}"
            )
    return ret_collection_metadata, ret_collection_names


async def get_ansible_plugin_info(
    venv: VenvRunner | FakeVenvRunner,
    ansible_core_version: PypiVer,
    collection_dir: str | None,
    collection_names: list[str] | None = None,
    fetch_all_installed: bool = False,
) -> tuple[
    MutableMapping[str, MutableMapping[str, t.Any]],
    Mapping[str, AnsibleCollectionMetadata],
]:
    """
    Retrieve information about all of the Ansible Plugins. Requires ansible-core 2.13+.

    :arg venv: A VenvRunner into which Ansible has been installed.
    :arg ansible_core_version: The version of ansible-core. Needed to figure out how
                               many filters can be provided to ansible-doc.
    :arg collection_dir: Directory in which the collections have been installed.
                         If ``None``, the collections are assumed to be in the current
                         search path for Ansible.
    :arg collection_names: Optional list of collections. If specified, will only collect
                           information for plugins in these collections.
    :arg fetch_all_installed: If set to ``True``, will also retrieve plugins of installed
        collections outside ``collection_dir`` (if specified).
    :returns: An tuple. The first component is a nested directory structure that looks like:

            plugin_type:
                plugin_name:  # Includes namespace and collection.
                    {information from ansible-doc --json.  See the ansible-doc documentation
                     for more info.}

        The second component is a Mapping of collection names to metadata.
    """
    flog = mlog.fields(func="get_ansible_plugin_info")
    flog.debug("Enter")

    env = _get_environment(
        collection_dir, keep_current_collections_path=fetch_all_installed, venv=venv
    )

    has_wildcards = collection_names is not None and any(
        is_wildcard_collection_name(cn) and not is_collection_name(cn)
        for cn in collection_names
    )

    flog.debug("Retrieving collection metadata")
    collection_metadata = await get_collection_metadata(
        venv, env, None if has_wildcards else collection_names
    )

    if has_wildcards:
        flog.debug("Restricting collection list by wildcards")
        collection_metadata, collection_names = _limit_by_wildcards(
            collection_metadata, collection_names or []
        )

    flog.debug("Retrieving and loading plugin documentation")
    ansible_doc_output = await _call_ansible_doc(
        venv, env, *_get_ansible_doc_filters(ansible_core_version, collection_names)
    )

    flog.debug("Processing plugin documentation")
    plugin_map: MutableMapping[str, MutableMapping[str, t.Any]] = {}
    for plugin_type in DOCUMENTABLE_PLUGINS:
        plugin_type_data: dict[str, t.Any] = {}
        plugin_map[plugin_type] = plugin_type_data
        plugins_of_type = ansible_doc_output["all"].get(plugin_type, {})
        for plugin_name, plugin_data in plugins_of_type.items():
            # ansible-doc returns plugins shipped with ansible-core using no namespace and
            # collection.  For now, we fix these entries to use the ansible.builtin collection
            # here.  The reason we do it here instead of as part of a general normalization step
            # is that other plugins (site-specific ones from ANSIBLE_LIBRARY, for instance) will
            # also be returned with no collection name.  We know that we don't have any of those
            # in this code (because we set ANSIBLE_LIBRARY and other plugin path variables to
            # /dev/null) so we can safely fix this here but not outside the ansible-doc backend.
            fqcn = plugin_name
            try:
                namespace, collection, name = get_fqcn_parts(fqcn)
                collection = f"{namespace}.{collection}"

                if should_flatmap(collection, collection_metadata):
                    # ansible-core devel branch will soon start to emit non-flattened FQCNs. This
                    # needs to be handled better in antsibull-docs, but for now we modify the output
                    # of --metadata-dump to conform to the output we had before (through
                    # `ansible-doc --json` or the ansible-internal backend).
                    # (https://github.com/ansible/ansible/pull/74963#issuecomment-1041580237)
                    dot_position = name.rfind(".")
                    if dot_position >= 0:
                        name = name[dot_position + 1 :]

                fqcn = f"{collection}.{name}"
            except ValueError:
                name = plugin_name
                collection = "ansible.builtin"
                fqcn = f"{collection}.{name}"

            # ansible-core devel branch will soon start to prepend _ to deprecated plugins when
            # --metadata-dump is used.
            # (https://github.com/ansible/ansible/pull/74963#issuecomment-1041580237)
            if collection == "ansible.builtin" and fqcn.startswith("ansible.builtin._"):
                fqcn = fqcn.replace("_", "", 1)

            # Filter collection name
            if collection_names is not None and collection not in collection_names:
                flog.debug(f"Ignoring documenation for {plugin_type} plugin {fqcn}")
                continue

            plugin_type_data[fqcn] = plugin_data

    flog.debug("Leave")
    return (plugin_map, collection_metadata)
