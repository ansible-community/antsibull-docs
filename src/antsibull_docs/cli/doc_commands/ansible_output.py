# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project
"""Entrypoint to the antsibull-docs script."""

from __future__ import annotations

import os
import subprocess
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from antsibull_core.logging import log
from antsibull_docutils.rst_code_finder import (
    CodeBlockInfo,
    find_code_blocks,
    mark_antsibull_code_block,
)
from docutils import nodes
from yaml import MarkedYAMLError

from sphinx_antsibull_ext.directive_helper import YAMLDirective
from sphinx_antsibull_ext.schemas.ansible_output_data import AnsibleOutputData

from ... import app_context

mlog = log.fields(mod=__name__)


_ANSIBLE_OUTPUT_DATA_IDENTIFIER = "{}[]XXXXXX"


class AnsibleOutputDataDirective(YAMLDirective[AnsibleOutputData]):
    wrap_as_data = False
    schema = AnsibleOutputData

    def _handle_error(self, message: str, from_exc: Exception) -> list[nodes.Node]:
        literal = nodes.literal_block("", "")
        mark_antsibull_code_block(
            literal,
            language=_ANSIBLE_OUTPUT_DATA_IDENTIFIER,
            line=self.lineno,
            other={
                "error": message,
                "exception": from_exc,
            },
        )
        return [literal]

    def _run(self, content_str: str, content: AnsibleOutputData) -> list[nodes.Node]:
        literal = nodes.literal_block(content_str, "")
        mark_antsibull_code_block(
            literal,
            language=_ANSIBLE_OUTPUT_DATA_IDENTIFIER,
            line=self.lineno,
            other={
                "data": content,
            },
        )
        return [literal]


_DIRECTIVES = {
    "ansible-output-data": AnsibleOutputDataDirective,
}


@dataclass
class AnsibleOutputDataExt:
    data: AnsibleOutputData
    line: int
    col: int


def _get_ansible_output_data_error(block: CodeBlockInfo) -> tuple[int, int, str]:
    message = block.attributes["antsibull-other-error"]
    exc = block.attributes.get("antsibull-other-exception")
    line = block.row_offset + 1
    col = block.col_offset + 1
    if isinstance(exc, MarkedYAMLError) and exc.problem_mark:
        # YAML's line/column are 0-based
        if isinstance(exc.problem_mark.line, int):
            line += exc.problem_mark.line
        if isinstance(exc.problem_mark.column, int):
            col += exc.problem_mark.column
    return line, col, message


def find_blocks(
    *,
    content: str,
    path: Path,
    root: Path | None = None,
    errors: list[tuple[Path, int | None, int | None, str]],
) -> list[tuple[CodeBlockInfo, AnsibleOutputDataExt]]:
    blocks: list[tuple[CodeBlockInfo, AnsibleOutputDataExt]] = []
    data: AnsibleOutputDataExt | None = None
    for block in find_code_blocks(
        content, path=path, root_prefix=root, extra_directives=_DIRECTIVES
    ):
        if block.language == _ANSIBLE_OUTPUT_DATA_IDENTIFIER:
            if "antsibull-other-data" in block.attributes:
                data = AnsibleOutputDataExt(
                    data=block.attributes["antsibull-other-data"],
                    line=block.row_offset + 1,
                    col=block.col_offset + 1,
                )
            if "antsibull-other-error" in block.attributes:
                line, col, message = _get_ansible_output_data_error(block)
                errors.append((path, line, col, message))
            continue
        if block.language != "ansible-output":
            continue
        if data is None:
            continue
        block_data, data = data, None
        if not block.directly_replacable_in_content:
            errors.append(
                (
                    path,
                    block.row_offset + 1,
                    block.col_offset + 1,
                    "Code block is not replacable",
                )
            )
            continue
        blocks.append((block, block_data))
    return blocks


def compute_code_block_content(
    data: AnsibleOutputDataExt, *, collection_path: Path | None = None
) -> list[str]:
    flog = mlog.fields(func="compute_code_block_content")

    flog.notice("Prepare environment")
    env = os.environ.copy()
    env.pop("ANSIBLE_FORCE_COLOR", None)
    env["NO_COLOR"] = "true"
    if collection_path is not None:
        collections_path = env.get("ANSIBLE_COLLECTIONS_PATH") or ""
        if collections_path:
            collections_path = f"{collection_path}:{collections_path}"
        else:
            collections_path = f"{collection_path}"
        env["ANSIBLE_COLLECTIONS_PATH"] = collections_path
    env.update(data.data.env)
    flog.notice("Environment: {}", env)

    flog.notice("Prepare temporary directory")
    with tempfile.TemporaryDirectory(prefix="antsibull-docs-output") as directory:
        file = Path(directory) / "playbook.yml"
        flog.notice("Directory: {}; playbook: {}", directory, file)
        with open(file, "w", encoding="utf-8") as f:
            f.write(data.data.playbook)

        command = ["ansible-playbook", "playbook.yml"]
        flog.notice("Run ansible-playbook: {}", command)
        result = subprocess.run(
            command,
            capture_output=True,
            cwd=str(directory),
            env=env,
            check=True,
            encoding="utf-8",
        )

        flog.notice("Post-process result")
        # Compute result lines
        lines = [line.rstrip() for line in result.stdout.split("\n")]
        first = 0
        last = len(lines)
        while first < last and not lines[first]:
            first += 1
        while first < last and not lines[last - 1]:
            last -= 1
        return lines[first:last]


def _replace(
    content_lines: list[str], *, block: CodeBlockInfo, new_content: list[str]
) -> list[str]:
    first_line = block.row_offset
    last_line = first_line + block.content.count("\n") - 1
    before = content_lines[:first_line]
    after = content_lines[last_line + 1 :]
    indent = " " * block.col_offset
    new_lines = [f"{indent}{line}" if line else "" for line in new_content]
    return before + new_lines + after


def _apply_replacements(
    content: str, replacements: list[tuple[CodeBlockInfo, list[str]]]
) -> str:
    content_lines = content.split("\n")

    # Apply replacements sorted back to front
    for block, new_content in sorted(
        replacements, key=lambda entry: -entry[0].row_offset
    ):
        content_lines = _replace(content_lines, block=block, new_content=new_content)

    # Ensure trailing newline
    if content_lines and content_lines[-1]:
        content_lines.append("")
    return "\n".join(content_lines)


def _compute_replacements(
    content: str,
    *,
    path: Path,
    root: Path | None = None,
    errors: list[tuple[Path, int | None, int | None, str]],
    collection_path: Path | None = None,
) -> list[tuple[CodeBlockInfo, list[str]]]:
    flog = mlog.fields(func="_compute_replacements")
    flog.notice("Find code blocks in file")
    try:
        blocks = find_blocks(content=content, path=path, root=root, errors=errors)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        flog.notice("Error while finding code blocks: {}", exc)
        errors.append((path, None, None, f"Error while finding code blocks: {exc}"))
        return []

    flog.notice("Found {} blocks", len(blocks))

    replacements: list[tuple[CodeBlockInfo, list[str]]] = []
    for block, block_data in blocks:
        flog.notice("Processing block at line {}", block.row_offset + 1)
        try:
            new_content = compute_code_block_content(
                block_data, collection_path=collection_path
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            flog.notice("Error while computing code block's expeted contents: {}", exc)
            errors.append(
                (
                    path,
                    block_data.line,
                    block_data.col,
                    f"Error while computing code block's expected contents: {exc}",
                )
            )
            continue
        old_content = block.content.split("\n")
        if old_content and old_content[-1] == "":
            old_content.pop()
        if new_content != old_content:
            replacements.append((block, new_content))
    return replacements


def process_file(
    path: Path,
    *,
    root: Path | None = None,
    errors: list[tuple[Path, int | None, int | None, str]],
    collection_path: Path | None = None,
) -> None:
    """
    Process RST file.

    Note that this function must not be used in multiple threads at the same time!
    """
    flog = mlog.fields(func="process_file")

    flog.notice("Load {}", path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as exc:  # pylint: disable=broad-exception-caught
        flog.notice("Error while reading content: {}", exc)
        errors.append((path, None, None, f"Error while reading content: {exc}"))
        return

    flog.notice("Compute replacements")
    replacements = _compute_replacements(
        content,
        path=path,
        root=root,
        errors=errors,
        collection_path=collection_path,
    )
    if not replacements:
        return

    flog.notice("Do replacements for {}", path)
    content = _apply_replacements(content, replacements)

    flog.notice("Write {}", path)
    print(f"Write {path}...")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        flog.notice("Error while writing content: {}", exc)
        errors.append((path, None, None, f"Error while writing content: {exc}"))


def process_directory(
    path: Path,
    *,
    errors: list[tuple[Path, int | None, int | None, str]],
    collection_path: Path | None = None,
) -> None:
    flog = mlog.fields(func="process_directory")
    flog.notice("Walking {}", path)
    try:
        for dirpath, _, filenames in path.walk():
            flog.notice("Processing {}: found {}", dirpath, filenames)
            for filename in filenames:
                if filename.endswith(".rst"):
                    process_file(
                        dirpath / filename,
                        root=path,
                        errors=errors,
                        collection_path=collection_path,
                    )
    except Exception as exc:  # pylint: disable=broad-exception-caught
        errors.append((path, None, None, f"Error while listing files: {exc}"))


def check_rst_files(
    paths: Sequence[str],
) -> list[tuple[Path, int | None, int | None, str]]:
    errors: list[tuple[Path, int | None, int | None, str]] = []
    for path in paths:
        path_obj = Path(path)
        if path_obj.is_dir():
            process_directory(path_obj, errors=errors)
        elif path_obj.exists():
            process_file(path_obj, errors=errors)
        else:
            errors.append((path_obj, None, None, "Does not exist"))
    return errors


def print_errors(
    errors: list[tuple[Path, int | None, int | None, str]], *, with_header: bool
) -> None:
    if with_header and errors:
        print(f"\nFound {len(errors)} error{'' if len(errors) == 1 else 's'}:")
    for error_path, line, col, error in sorted(
        errors,
        key=lambda entry: (str(entry[0]), entry[1] or 0, entry[2] or 0, entry[3]),
    ):
        prefix = f"{error_path}:{line or '-'}:{col or '-'}: "
        error_lines = [error_line.rstrip() for error_line in error.split("\n")]
        print(f"{prefix}{error_lines[0]}")
        if len(error_lines) > 1:
            prefix = "   "
            for error_line in error_lines[1:]:
                if error_line:
                    print(f"{prefix}{error_line}")
                else:
                    print()


def run_ansible_output() -> int:
    """
    Lint collection documentation for inclusion into the collection's docsite.

    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func="run_ansible_output")
    flog.notice("Begin ansible-output rendering")

    app_ctx = app_context.app_ctx.get()

    paths: tuple[str, ...] = app_ctx.extra["paths"]

    errors = check_rst_files(paths)
    print_errors(errors, with_header=True)
    return 3 if len(errors) > 0 else 0
