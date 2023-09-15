# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import difflib
import io
import os
from contextlib import redirect_stdout

import pytest
from ansible_doc_caching import ansible_doc_cache
from utils import replace_antsibull_version

from antsibull_docs.cli.antsibull_docs import run

pytest.importorskip("ansible")


TEST_CASES = [
    (
        [
            "current",
            "--skip-ansible-builtin",
            "--collection-dir",
            "tests/functional/collections/",
        ],
        # assumes that baseline-default contains all collections in tests/functional/collections/!
        "baseline-default",
    ),
    (
        ["collection", "--use-current", "ns.col1", "ns.col2", "ns2.col", "ns2.flatcol"],
        "baseline-default",
    ),
    (
        [
            "collection",
            "--use-current",
            "ns.col1",
            "ns.col2",
            "ns2.col",
            "ns2.flatcol",
            "--no-breadcrumbs",
        ],
        "baseline-no-breadcrumbs",
    ),
    (
        [
            "collection",
            "--use-current",
            "ns.col1",
            "ns2.col",
            "ns2.flatcol",
            "--fail-on-error",
            "--no-indexes",
        ],
        "baseline-no-indexes",
    ),
    (
        [
            "collection",
            "--use-current",
            "ns2.col",
            "--fail-on-error",
            "--use-html-blobs",
        ],
        "baseline-use-html-blobs",
    ),
    (
        [
            "collection",
            "--use-current",
            "ns2.col",
            "--fail-on-error",
            "--squash-hierarchy",
        ],
        "baseline-squash-hierarchy",
    ),
    (
        [
            "collection",
            "--use-current",
            "ns.col1",
            "ns.col2",
            "ns2.col",
            "ns2.flatcol",
            "--output-format",
            "simplified-rst",
        ],
        "baseline-simplified-rst",
    ),
    (
        [
            "collection",
            "--use-current",
            "ns2.col",
            "--fail-on-error",
            "--squash-hierarchy",
            "--output-format",
            "simplified-rst",
        ],
        "baseline-simplified-rst-squash-hierarchy",
    ),
]


def _scan_directories(root: str):
    result = {}
    for path, dirs, files in os.walk(root):
        result[os.path.relpath(path, root)] = (path, files)
    return result


def _compare_files(source, dest, path):
    with open(source) as f:
        src = f.read()
    with open(dest) as f:
        dst = f.read()
    if src == dst:
        return 0
    for line in difflib.unified_diff(src.splitlines(), dst.splitlines(), path, path):
        if line[0] == "@":
            print(line)
        elif line[0] == "-":
            print(f"\033[41m\033[9m{line}\033[29m\033[49m")
        elif line[0] == "+":
            print(f"\033[42m{line}\033[49m")
        else:
            print(line)
    return 1


def _compare_directories(source, dest):
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
            differences += _compare_files(
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


@pytest.mark.parametrize("arguments, directory", TEST_CASES)
def test_baseline(arguments, directory, tmp_path):
    tests_root = os.path.join("tests", "functional")

    config_file = tmp_path / "antsibull.cfg"
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("doc_parsing_backend = ansible-core-2.13\n")

    output_dir = tmp_path / "output"
    os.mkdir(output_dir, mode=0o700)

    # Re-build baseline
    command = (
        ["antsibull-docs", "--config-file", str(config_file)]
        + arguments
        + [
            "--dest-dir",
            str(output_dir),
        ]
    )
    os.environ.pop("ANSIBLE_COLLECTIONS_PATHS", None)
    os.environ["ANSIBLE_COLLECTIONS_PATH"] = os.path.join(tests_root, "collections")
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        with ansible_doc_cache():
            with replace_antsibull_version():
                rc = run(command)
    stdout = stdout.getvalue().splitlines()
    assert rc == 0

    # Compare baseline to expected result
    source = _scan_directories(os.path.join(tests_root, directory))
    dest = _scan_directories(str(output_dir))
    _compare_directories(source, dest)
