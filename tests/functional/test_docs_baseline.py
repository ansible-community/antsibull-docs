# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import io
import os
from contextlib import redirect_stdout

import pytest
from ansible_doc_caching import ansible_doc_cache
from utils import compare_directories, replace_antsibull_version, scan_directories

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
            "--no-add-antsibull-docs-version",
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
            "plugin",
            "--plugin-type",
            "lookup",
            "ns2.col.foo",
            "--fail-on-error",
        ],
        "baseline-plugin",
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
            "--no-add-antsibull-docs-version",
            "--output-format",
            "simplified-rst",
        ],
        "baseline-simplified-rst-squash-hierarchy",
    ),
]


@pytest.mark.parametrize("arguments, directory", TEST_CASES)
def test_baseline(arguments: list[str], directory: str, tmp_path) -> None:
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
    print(stdout.getvalue())
    assert rc == 0

    # Compare baseline to expected result
    source = scan_directories(os.path.join(tests_root, directory))
    dest = scan_directories(str(output_dir))
    compare_directories(source, dest)
