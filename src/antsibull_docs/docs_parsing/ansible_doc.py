# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Parse documentation from ansible plugins using anible-doc."""

from __future__ import annotations

import json
import os
import re
import shlex
import textwrap
import typing as t
from collections.abc import Mapping

from antsibull_core.logging import log
from antsibull_core.subprocess_util import CalledProcessError
from antsibull_core.vendored.json_utils import _filter_non_json_lines
from packaging.version import Version as PypiVer

from ..collection_config import get_ansible_core_config, load_collection_config
from . import AnsibleCollectionMetadata

if t.TYPE_CHECKING:
    from antsibull_core.venv import FakeVenvRunner, VenvRunner


mlog = log.fields(mod=__name__)


def _extract_ansible_builtin_metadata(stdout: str) -> AnsibleCollectionMetadata:
    path: str | None = None
    version: str | None = None
    ansible_version_new = re.compile(r"^ansible \[(?:core|base) ([^\]]+)\]")
    ansible_version_old = re.compile(r"^ansible ([^\s]+)")
    for line in stdout.splitlines():
        if line.strip().startswith("ansible python module location"):
            path = line.split("=", 2)[1].strip()
        for regex in (ansible_version_new, ansible_version_old):
            match = regex.match(line)
            if match:
                version = match.group(1)
                break
    if path is None:
        raise RuntimeError(
            f"Cannot extract module location path from ansible --version output: {stdout}"
        )
    if version is None:
        raise RuntimeError(
            f"Cannot extract ansible-core version from ansible --version output: {stdout}"
        )
    return AnsibleCollectionMetadata(
        path=path, docs_config=get_ansible_core_config(), version=version
    )


def parse_ansible_galaxy_collection_list(
    json_output: Mapping[str, t.Any],
    collection_names: list[str] | None = None,
) -> list[tuple[str, str, str, str | None]]:
    result = []
    for path, collections in json_output.items():
        for collection, data in collections.items():
            if collection_names is None or collection in collection_names:
                namespace, name = collection.split(".", 2)
                version = data.get("version", "*")
                result.append(
                    (
                        namespace,
                        name,
                        os.path.join(path, namespace, name),
                        None if version == "*" else version,
                    )
                )
    return result


async def _call_ansible_version(
    venv: VenvRunner | FakeVenvRunner,
    env: dict[str, str] | None,
) -> str:
    p = await venv.async_log_run(["ansible", "--version"], env=env)
    return p.stdout


async def _call_ansible_galaxy_collection_list(
    venv: VenvRunner | FakeVenvRunner,
    env: dict[str, str],
) -> Mapping[str, t.Any]:
    try:
        p = await venv.async_log_run(
            ["ansible-galaxy", "collection", "list", "--format", "json"],
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


async def get_collection_metadata(
    venv: VenvRunner | FakeVenvRunner,
    env: dict[str, str],
    collection_names: list[str] | None = None,
) -> dict[str, AnsibleCollectionMetadata]:
    collection_metadata = {}

    # Obtain ansible.builtin version and path
    raw_result = await _call_ansible_version(venv, env)
    collection_metadata["ansible.builtin"] = _extract_ansible_builtin_metadata(
        raw_result
    )

    # Obtain collection versions
    json_result = await _call_ansible_galaxy_collection_list(venv, env)
    collection_list = parse_ansible_galaxy_collection_list(
        json_result, collection_names
    )
    for namespace, name, path, version in collection_list:
        collection_name = f"{namespace}.{name}"
        collection_config = await load_collection_config(collection_name, path)
        collection_metadata[collection_name] = AnsibleCollectionMetadata(
            path=path, docs_config=collection_config, version=version
        )

    return collection_metadata


async def _import_ansible_core_version(
    venv: VenvRunner | FakeVenvRunner,
    env: dict[str, str] | None = None,
) -> PypiVer | None:
    p = await venv.async_log_run(
        ["python", "-c", "import ansible.release; print(ansible.release.__version__)"],
        env=env,
        check=False,
    )
    output = p.stdout.strip()
    if p.returncode == 0 and output:
        return PypiVer(output)
    return None


async def get_ansible_core_version(
    venv: VenvRunner | FakeVenvRunner,
    env: dict[str, str] | None = None,
) -> PypiVer:
    version = await _import_ansible_core_version(venv, env)
    if version is not None:
        return version

    try:
        # Fallback: use `ansible --version`
        raw_result = await _call_ansible_version(venv, env)
        metadata = _extract_ansible_builtin_metadata(raw_result)
        if metadata.version is None:
            raise ValueError(
                "Cannot retrieve ansible-core version from `ansible --version`"
            )
        return PypiVer(metadata.version)
    except CalledProcessError as exc:
        raise ValueError(
            f"Cannot retrieve ansible-core version from `ansible --version`: {exc};"
            f" error output:\n{textwrap.indent(exc.stderr, '| ')}"
        ) from exc
