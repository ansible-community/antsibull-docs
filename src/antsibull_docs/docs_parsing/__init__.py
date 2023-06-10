# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Parse documentation from ansible plugins using anible-doc."""

from __future__ import annotations

import os

from antsibull_core.venv import FakeVenvRunner, VenvRunner

from ..schemas.collection_config import CollectionConfig

#: Clear Ansible environment variables that set paths where plugins could be found.
ANSIBLE_PATH_ENVIRON: dict[str, str] = os.environ.copy()
ANSIBLE_PATH_ENVIRON.update(
    {
        "ANSIBLE_COLLECTIONS_PATH": "/dev/null",
        "ANSIBLE_ACTION_PLUGINS": "/dev/null",
        "ANSIBLE_CACHE_PLUGINS": "/dev/null",
        "ANSIBLE_CALLBACK_PLUGINS": "/dev/null",
        "ANSIBLE_CLICONF_PLUGINS": "/dev/null",
        "ANSIBLE_CONNECTION_PLUGINS": "/dev/null",
        "ANSIBLE_FILTER_PLUGINS": "/dev/null",
        "ANSIBLE_HTTPAPI_PLUGINS": "/dev/null",
        "ANSIBLE_INVENTORY_PLUGINS": "/dev/null",
        "ANSIBLE_LOOKUP_PLUGINS": "/dev/null",
        "ANSIBLE_LIBRARY": "/dev/null",
        "ANSIBLE_MODULE_UTILS": "/dev/null",
        "ANSIBLE_NETCONF_PLUGINS": "/dev/null",
        "ANSIBLE_ROLES_PATH": "/dev/null",
        "ANSIBLE_STRATEGY_PLUGINS": "/dev/null",
        "ANSIBLE_TERMINAL_PLUGINS": "/dev/null",
        "ANSIBLE_TEST_PLUGINS": "/dev/null",
        "ANSIBLE_VARS_PLUGINS": "/dev/null",
        "ANSIBLE_DOC_FRAGMENT_PLUGINS": "/dev/null",
    }
)
try:
    del ANSIBLE_PATH_ENVIRON["ANSIBLE_COLLECTIONS_PATHS"]
except KeyError:
    # ANSIBLE_COLLECTIONS_PATHS is the deprecated name replaced by
    # ANSIBLE_COLLECTIONS_PATH
    pass


class ParsingError(Exception):
    """Error raised while parsing plugins for documentation."""


def _get_existing_collections_path() -> str | None:
    for env_var in ("ANSIBLE_COLLECTIONS_PATH", "ANSIBLE_COLLECTIONS_PATHS"):
        if os.environ.get(env_var):
            return os.environ[env_var]
    return None


def _get_environment(
    collection_dir: str | None,
    venv: VenvRunner | FakeVenvRunner,
    keep_current_collections_path: bool = False,
) -> dict[str, str]:
    env = ANSIBLE_PATH_ENVIRON.copy()
    if isinstance(venv, VenvRunner):
        try:
            del env["PYTHONPATH"]
        except KeyError:
            # We just wanted to make sure there was no PYTHONPATH set...
            # all Python libs will come from the venv
            pass
    for env_var in ("ANSIBLE_COLLECTIONS_PATH", "ANSIBLE_COLLECTIONS_PATHS"):
        try:
            del env[env_var]
        except KeyError:
            pass
    existing_collections_path = _get_existing_collections_path()
    if collection_dir is not None:
        if keep_current_collections_path and existing_collections_path:
            collection_dir = f"{collection_dir}:{existing_collections_path}"
        env["ANSIBLE_COLLECTIONS_PATH"] = collection_dir
    elif existing_collections_path:
        env["ANSIBLE_COLLECTIONS_PATH"] = existing_collections_path
    return env


class AnsibleCollectionMetadata:
    path: str
    version: str | None
    requires_ansible: str | None
    docs_config: CollectionConfig

    def __init__(
        self,
        path: str,
        docs_config: CollectionConfig,
        version: str | None = None,
        requires_ansible: str | None = None,
    ):
        self.path = path
        self.version = version
        self.requires_ansible = requires_ansible
        self.docs_config = docs_config

    def __repr__(self):
        return f"AnsibleCollectionMetadata({repr(self.path)}, {repr(self.version)})"

    @classmethod
    def empty(cls, path="."):
        return cls(path=path, docs_config=CollectionConfig.parse_obj({}), version=None)
