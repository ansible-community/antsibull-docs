# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Tools for copying collections."""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import typing as t

from antsibull_core.subprocess_util import log_run
from antsibull_core.vendored.json_utils import _filter_non_json_lines
from antsibull_fileutils.tempfile import ansible_mkdtemp

from ..docs_parsing.ansible_doc import parse_ansible_galaxy_collection_list
from ..lint_helpers import load_collection_info


class CollectionCopier:
    dir: str | None

    def __init__(self):
        self.dir = None

    def __enter__(self):
        if self.dir is not None:
            raise AssertionError("Collection copier already initialized")
        self.dir = os.path.realpath(ansible_mkdtemp(prefix="antsibull-docs-"))
        return self

    def add_collection(
        self, collecion_source_path: str, namespace: str, name: str
    ) -> None:
        self_dir = self.dir
        if self_dir is None:
            raise AssertionError("Collection copier not initialized")
        collection_container_dir = os.path.join(
            self_dir, "ansible_collections", namespace
        )
        os.makedirs(collection_container_dir, exist_ok=True)

        collection_dir = os.path.join(collection_container_dir, name)
        shutil.copytree(collecion_source_path, collection_dir, symlinks=True)

    def __exit__(self, type_, value, traceback_):
        self_dir = self.dir
        if self_dir is None:
            raise AssertionError("Collection copier not initialized")
        shutil.rmtree(self_dir, ignore_errors=True)
        self.dir = None


def _call_ansible_galaxy_collection_list() -> t.Mapping[str, t.Any]:
    p = log_run(["ansible-galaxy", "collection", "list", "--format", "json"])
    return json.loads(_filter_non_json_lines(p.stdout)[0])


class CollectionFinder:
    def __init__(self):
        self.collections = {}
        data = _call_ansible_galaxy_collection_list()
        for namespace, name, path, _ in reversed(
            parse_ansible_galaxy_collection_list(data)
        ):
            self.collections[f"{namespace}.{name}"] = path

    def find(self, namespace, name):
        return self.collections.get(f"{namespace}.{name}")


class CollectionLoadError(Exception):
    def __init__(self, *, path: str, error: str) -> None:
        self.path = path
        self.error = error


@contextlib.contextmanager
def load_collection_infos(
    *,
    path_to_collection: str,
    copy_dependencies: bool = True,
) -> t.Generator[tuple[str, str, list[str], list[CollectionLoadError]]]:
    try:
        info = load_collection_info(path_to_collection)
        namespace = info["namespace"]
        name = info["name"]
        dependencies = info.get("dependencies") or {}
    except Exception as exc:
        raise CollectionLoadError(
            path=path_to_collection,
            error="Cannot identify collection with galaxy.yml or MANIFEST.json at this path",
        ) from exc
    collection_name = f"{namespace}.{name}"
    done_dependencies = {collection_name}
    dependencies = sorted(dependencies)
    errors = []
    with CollectionCopier() as copier:
        # Copy collection
        copier.add_collection(path_to_collection, namespace, name)
        # Copy all dependencies
        if dependencies and copy_dependencies:
            collection_finder = CollectionFinder()
            while dependencies:
                dependency = dependencies.pop(0)
                if dependency in done_dependencies:
                    continue
                done_dependencies.add(dependency)
                dep_namespace, dep_name = dependency.split(".", 2)
                dep_collection_path = collection_finder.find(dep_namespace, dep_name)
                if dep_collection_path:
                    copier.add_collection(dep_collection_path, dep_namespace, dep_name)
                    try:
                        info = load_collection_info(dep_collection_path)
                        dependencies.extend(sorted(info.get("dependencies") or {}))
                    except Exception:  # pylint:disable=broad-except
                        errors.append(
                            CollectionLoadError(
                                path=dep_collection_path,
                                error=(
                                    "Cannot identify collection with galaxy.yml"
                                    " or MANIFEST.json at this path"
                                ),
                            )
                        )

        yield collection_name, copier.dir, sorted(done_dependencies), errors


__all__ = (
    "CollectionCopier",
    "CollectionFinder",
    "CollectionLoadError",
    "load_collection_infos",
)
