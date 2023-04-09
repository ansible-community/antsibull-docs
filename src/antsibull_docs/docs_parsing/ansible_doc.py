# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Parse documentation from ansible plugins using anible-doc."""

import os
import re
import typing as t

import sh
from antsibull_core.logging import log
from packaging.version import Version as PypiVer

from . import AnsibleCollectionMetadata

if t.TYPE_CHECKING:
    from antsibull_core.venv import FakeVenvRunner, VenvRunner


mlog = log.fields(mod=__name__)


def _extract_ansible_builtin_metadata(stdout: str) -> AnsibleCollectionMetadata:
    path: t.Optional[str] = None
    version: t.Optional[str] = None
    ansible_version_new = re.compile(r'^ansible \[(?:core|base) ([^\]]+)\]')
    ansible_version_old = re.compile(r'^ansible ([^\s]+)')
    for line in stdout.splitlines():
        if line.strip().startswith('ansible python module location'):
            path = line.split('=', 2)[1].strip()
        for regex in (ansible_version_new, ansible_version_old):
            match = regex.match(line)
            if match:
                version = match.group(1)
                break
    if path is None:
        raise RuntimeError(
            f'Cannot extract module location path from ansible --version output: {stdout}')
    if version is None:
        raise RuntimeError(
            f'Cannot extract ansible-core version from ansible --version output: {stdout}')
    return AnsibleCollectionMetadata(path=path, version=version)


def parse_ansible_galaxy_collection_list(raw_output: str,
                                         collection_names: t.Optional[t.List[str]] = None,
                                         ) -> t.List[t.Tuple[str, str, str, t.Optional[str]]]:
    result = []
    current_base_path = None
    for line in raw_output.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            if parts[0] == '#':
                current_base_path = parts[1]
            elif current_base_path is not None:
                collection_name = parts[0]
                version = parts[1]
                if '.' in collection_name:
                    if collection_names is None or collection_name in collection_names:
                        namespace, name = collection_name.split('.', 2)
                        result.append((
                            namespace,
                            name,
                            os.path.join(current_base_path, namespace, name),
                            None if version == '*' else version
                        ))
    return result


def _call_ansible_version(
    venv: t.Union['VenvRunner', 'FakeVenvRunner'],
    env: t.Dict[str, str],
) -> str:
    venv_ansible = venv.get_command('ansible')
    ansible_version_cmd = venv_ansible('--version', _env=env)
    return ansible_version_cmd.stdout.decode('utf-8', errors='surrogateescape')


def _call_ansible_galaxy_collection_list(
    venv: t.Union['VenvRunner', 'FakeVenvRunner'],
    env: t.Dict[str, str],
) -> str:
    venv_ansible_galaxy = venv.get_command('ansible-galaxy')
    ansible_collection_list_cmd = venv_ansible_galaxy('collection', 'list', _env=env)
    return ansible_collection_list_cmd.stdout.decode('utf-8', errors='surrogateescape')


def get_collection_metadata(venv: t.Union['VenvRunner', 'FakeVenvRunner'],
                            env: t.Dict[str, str],
                            collection_names: t.Optional[t.List[str]] = None,
                            ) -> t.Dict[str, AnsibleCollectionMetadata]:
    collection_metadata = {}

    # Obtain ansible.builtin version and path
    raw_result = _call_ansible_version(venv, env)
    collection_metadata['ansible.builtin'] = _extract_ansible_builtin_metadata(raw_result)

    # Obtain collection versions
    raw_result = _call_ansible_galaxy_collection_list(venv, env)
    collection_list = parse_ansible_galaxy_collection_list(raw_result, collection_names)
    for namespace, name, path, version in collection_list:
        collection_name = f'{namespace}.{name}'
        collection_metadata[collection_name] = AnsibleCollectionMetadata(
            path=path, version=version)

    return collection_metadata


def get_ansible_core_version(venv: t.Union['VenvRunner', 'FakeVenvRunner'],
                             env: t.Optional[t.Dict[str, str]] = None,
                             ) -> PypiVer:
    try:
        venv_python = venv.get_command('python')
        ansible_version_cmd = venv_python(
            '-c', 'import ansible.release; print(ansible.release.__version__)', _env=env)
        output = ansible_version_cmd.stdout.decode('utf-8', errors='surrogateescape').strip()
        return PypiVer(output)
    except sh.ErrorReturnCode:
        pass

    try:
        # Fallback: use `ansible --version`
        venv_ansible = venv.get_command('ansible')
        ansible_version_cmd = venv_ansible('--version', _env=env)
        raw_result = ansible_version_cmd.stdout.decode('utf-8', errors='surrogateescape')
        metadata = _extract_ansible_builtin_metadata(raw_result)
        if metadata.version is None:
            raise ValueError('Cannot retrieve ansible-core version from `ansible --version`')
        return PypiVer(metadata.version)
    except sh.ErrorReturnCode as exc:
        raise ValueError(
            f'Cannot retrieve ansible-core version from `ansible --version`: {exc}'
        ) from exc
