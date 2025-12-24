# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import difflib
import os
import typing as t
from contextlib import contextmanager
from unittest import mock

import antsibull_docs

ANTSIBULL_DOCS_CI_VERSION = "<ANTSIBULL_DOCS_VERSION>"


@contextmanager
def replace_antsibull_version(
    new_version: str = ANTSIBULL_DOCS_CI_VERSION,
) -> t.Iterator[None]:
    with mock.patch(
        "antsibull_docs.__version__",
        new_version,
    ):
        yield


@contextmanager
def change_cwd(directory: str | os.PathLike[str]) -> t.Iterator[None]:
    old_dir = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(old_dir)


@contextmanager
def update_environment(environment: dict[str, str | None]) -> t.Iterator[None]:
    backup = {}
    for k, v in environment.items():
        if k in os.environ:
            backup[k] = os.environ[k]
        if v is not None:
            os.environ[k] = v
        elif k in os.environ:
            del os.environ[k]
    yield
    for k in environment:
        if k in backup:
            os.environ[k] = backup[k]
        elif k in os.environ:
            del os.environ[k]


def scan_directories(root: os.PathLike[str] | str) -> dict[str, tuple[str, list[str]]]:
    result: dict[str, tuple[str, list[str]]] = {}
    for path, dirs, files in os.walk(root):
        result[os.path.relpath(path, root)] = (path, files)
    return result


def compare_files(
    source: os.PathLike[str] | str, dest: os.PathLike[str] | str, path: str
) -> int:
    with open(source, "rb") as f:
        src = f.read()
    with open(dest, "rb") as f:
        dst = f.read()
    if src == dst:
        return 0
    src_lines = src.decode("utf-8", errors="surrogateescape").splitlines()
    dst_lines = dst.decode("utf-8", errors="surrogateescape").splitlines()
    for line in difflib.unified_diff(src_lines, dst_lines, path, path):
        if line[0] == "@":
            print(line)
        elif line[0] == "-":
            print(f"\033[41m\033[9m{line}\033[29m\033[49m")
        elif line[0] == "+":
            print(f"\033[42m{line}\033[49m")
        else:
            print(line)
    return 1


def compare_directories(
    source: dict[str, tuple[str, list[str]]], dest: dict[str, tuple[str, list[str]]]
) -> None:
    differences = 0
    for path in source:
        if path not in dest:
            print(f"Directory {path} exists only in the baseline!")
            differences += 1
            continue
        source_files = set(source[path][1])
        dest_files = set(dest[path][1])
        for file in source_files:
            if file not in dest_files:
                differences += 1
                print(f"File {os.path.join(path, file)} exists only in the baseline!")
                continue
            source_path = os.path.join(source[path][0], file)
            dest_path = os.path.join(dest[path][0], file)
            differences += compare_files(
                source_path, dest_path, os.path.join(path, file)
            )
        for file in dest_files:
            if file not in source_files:
                differences += 1
                print(
                    f"File {os.path.join(path, file)} exists only in the generated result!"
                )
    for path in dest:
        if path not in source:
            print(f"Directory {path} exists only in the generated result!")
            differences += 1
            continue
    if differences:
        print(f"Found {differences} differences.")
    assert differences == 0
