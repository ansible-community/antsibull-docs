# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import os
import typing as t
from collections.abc import Mapping
from contextlib import contextmanager
from unittest import mock

import pytest

ansible = pytest.importorskip("ansible")

if t.TYPE_CHECKING:
    from antsibull_core.venv import FakeVenvRunner, VenvRunner


@contextmanager
def ansible_doc_cache():
    async def call_ansible_doc(
        venv: VenvRunner | FakeVenvRunner,
        env: dict[str, str],
        *parameters: str,
    ) -> Mapping[str, t.Any]:
        if len(parameters) > 1:
            raise Exception(
                f"UNEXPECTED parameters to call_ansible_doc: {parameters!r}"
            )
        root = env["ANSIBLE_COLLECTIONS_PATH"]
        arg = "all" if len(parameters) == 0 else parameters[0]
        filename = os.path.join(
            os.path.dirname(__file__), f"ansible-doc-cache-{arg}.json"
        )
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
        for plugin_type, plugins in data["all"].items():
            for plugin_fqcn, plugin_data in list(plugins.items()):
                if plugin_fqcn.startswith("ansible.builtin."):
                    del plugins[plugin_fqcn]
                for doc_key, key in [
                    ("doc", "filename"),
                    ("", "path"),
                ]:
                    doc = plugin_data
                    if doc_key:
                        if doc_key not in doc:
                            continue
                        doc = doc[doc_key]
                    if key in doc:
                        doc[key] = os.path.join(root, doc[key])
        return data

    async def call_ansible_version(
        venv: VenvRunner | FakeVenvRunner,
        env: t.Optional[t.Dict[str, str]],
    ) -> str:
        filename = os.path.join(os.path.dirname(__file__), "ansible-version.output")
        with open(filename, encoding="utf-8") as f:
            content = f.read()

        root = (
            env["ANSIBLE_COLLECTIONS_PATH"]
            if env and "ANSIBLE_COLLECTIONS_PATH" in env
            else "/collections"
        )
        content = content.replace("<<<<<COLLECTIONS>>>>>", root)
        content = content.replace("<<<<<HOME>>>>>", (env or os.environ)["HOME"])
        content = content.replace(
            "<<<<<ANSIBLE>>>>>", os.path.dirname(ansible.__file__)
        )
        return content

    async def call_ansible_galaxy_collection_list(
        venv: VenvRunner | FakeVenvRunner,
        env: t.Dict[str, str],
    ) -> t.Mapping[str, t.Any]:
        filename = os.path.join(
            os.path.dirname(__file__), "ansible-galaxy-cache-all.json"
        )
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
        root = env["ANSIBLE_COLLECTIONS_PATH"]
        result = {}
        for path, collections in data.items():
            result[os.path.join(root, path)] = collections
        return result

    with mock.patch(
        "antsibull_docs.docs_parsing.ansible_doc_core_213._call_ansible_doc",
        call_ansible_doc,
    ):
        with mock.patch(
            "antsibull_docs.docs_parsing.ansible_doc._call_ansible_version",
            call_ansible_version,
        ):
            with mock.patch(
                "antsibull_docs.docs_parsing.ansible_doc._call_ansible_galaxy_collection_list",
                call_ansible_galaxy_collection_list,
            ):
                yield
