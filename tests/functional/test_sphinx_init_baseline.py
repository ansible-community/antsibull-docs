# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import difflib
import io
import os
from contextlib import redirect_stdout

import pytest
from utils import replace_antsibull_version

from antsibull_docs.cli.antsibull_docs import run

TEST_CASES = [
    (
        ["--use-current"],
        "baseline-sphinx-init-current",
    ),
    (
        ["ns.col1", "ns.col2", "ns2.col"],
        "baseline-sphinx-init-collections",
    ),
    (
        [
            "ns.col1",
            "--no-indexes",
            "--no-breadcrumbs",
            "--use-html-blobs",
            "--squash-hierarchy",
            "--lenient",
            "--fail-on-error",
            "--index-rst-source",
            os.path.join(os.path.dirname(__file__), "test.rst"),
            "--intersphinx",
            "identifier:https://server/path",
            "--intersphinx",
            "foo:https://bar/baz",
            "--sphinx-theme",
            "another-theme",
        ],
        "baseline-sphinx-init-config",
    ),
    (
        [
            "ns.col1",
            "--extra-conf",
            "key=value",
            "--extra-conf",
            "long key=very \"long\" 'value'",
            "--extra-html-context",
            "key=value",
            "--extra-html-context",
            "long key=very \"long\" 'value'",
            "--extra-html-theme-options",
            "key=value",
            "--extra-html-theme-options",
            "long key=very \"long\" 'value'",
            "--project",
            "Foo 'bar'",
            "--copyright",
            "Baz \"bam'",
            "--title",
            "A title",
            "--html-short-title",
            "A shorter title - not",
        ],
        "baseline-sphinx-init-extra",
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
    tests_root = os.path.dirname(__file__)

    # Re-build baseline
    command = ["antsibull-docs", "sphinx-init", "--dest-dir", str(tmp_path)] + arguments
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        with replace_antsibull_version():
            rc = run(command)
    stdout = stdout.getvalue().splitlines()
    assert rc == 0

    try:
        # Adjust 'cd' in build.sh
        filename = os.path.join(tmp_path, "build.sh")
        with open(filename, encoding="utf-8") as f:
            lines = list(f)
        for index, line in enumerate(lines):
            if line.startswith("cd "):
                lines[index] = "cd DESTINATION\n"
        with open(filename, "w", encoding="utf-8") as f:
            f.writelines(lines)

        # Compare baseline to expected result
        source = _scan_directories(os.path.join(tests_root, directory))
        dest = _scan_directories(str(tmp_path))
        _compare_directories(source, dest)

    except:
        print("STDOUT:\n" + "\n".join(stdout))
        raise
