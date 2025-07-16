# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project
"""Entrypoint to the antsibull-docs script."""

from __future__ import annotations

import asyncio
import difflib
import os
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import jinja2
import pydantic
from antsibull_core.logging import log
from antsibull_core.pydantic import get_formatted_error_messages
from antsibull_docutils.rst_code_finder import (
    CodeBlockInfo,
    find_code_blocks,
    mark_antsibull_code_block,
)
from antsibull_fileutils.tempfile import AnsibleTemporaryDirectory
from docutils import nodes
from yaml import MarkedYAMLError

from sphinx_antsibull_ext.directive_helper import YAMLDirective
from sphinx_antsibull_ext.schemas.ansible_output_data import (
    AnsibleOutputData,
    VariableSource,
)

from ... import app_context
from ...collection_config import load_collection_config
from ...lint_helpers import load_collection_info
from ...schemas.collection_config import CollectionConfig
from ...utils.collection_copier import CollectionCopier

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
class _AnsibleOutputDataExt:
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
    if isinstance(exc, pydantic.ValidationError):
        message = (
            "Error while validating ansible-output-data directive's contents:\n"
            + "\n".join(get_formatted_error_messages(exc))
        )
    return line, col, message


def _find_blocks(
    *,
    content: str,
    path: Path,
    root: Path | None = None,
    errors: list[tuple[Path, int | None, int | None, str]],
) -> list[tuple[CodeBlockInfo, _AnsibleOutputDataExt, list[CodeBlockInfo]]]:
    blocks: list[tuple[CodeBlockInfo, _AnsibleOutputDataExt, list[CodeBlockInfo]]] = []
    data: _AnsibleOutputDataExt | None = None
    previous_blocks: list[CodeBlockInfo] = []
    for block in find_code_blocks(
        content, path=path, root_prefix=root, extra_directives=_DIRECTIVES
    ):
        if block.language == _ANSIBLE_OUTPUT_DATA_IDENTIFIER:
            if data is not None:
                errors.append(
                    (
                        path,
                        data.line,
                        data.col,
                        "ansible-output-data directive not used",
                    )
                )
            if "antsibull-other-data" in block.attributes:
                data = _AnsibleOutputDataExt(
                    data=block.attributes["antsibull-other-data"],
                    line=block.row_offset + 1,
                    col=block.col_offset + 1,
                )
            if "antsibull-other-error" in block.attributes:
                line, col, message = _get_ansible_output_data_error(block)
                errors.append((path, line, col, message))
            continue
        previous_blocks.append(block)
        if data is None:
            continue
        if block.language != data.data.language:
            continue
        blocks.append((block, data, previous_blocks[:-1]))
        data = None
    if data is not None:
        errors.append(
            (
                path,
                data.line,
                data.col,
                "ansible-output-data directive not used",
            )
        )
    return blocks


@dataclass
class Environment:
    env: dict[str, str]


def _get_variable_value(
    *, key: str, value: VariableSource, previous_blocks: list[CodeBlockInfo]
) -> str:
    if value.value is not None:
        return value.value
    if value.previous_code_block is None:
        raise AssertionError("Implementation error: cannot handle {value!r}")

    candidates = [
        block
        for block in previous_blocks
        if block.language == value.previous_code_block
    ]
    if not candidates:
        raise ValueError(
            "Cannot find previous code block of"
            f" language {value.previous_code_block!r} for variable {key!r}"
        )
    return candidates[-1].content


def _compose_playbook(
    data: AnsibleOutputData, *, previous_blocks: list[CodeBlockInfo]
) -> str:
    if all(s not in data.playbook for s in ("@{%", "@{{", "@{#")):
        return data.playbook

    variables = {}
    for key, value in data.variables.items():
        variables[key] = _get_variable_value(
            key=key, value=value, previous_blocks=previous_blocks
        )

    env = jinja2.Environment(
        block_start_string="@{%",
        block_end_string="%}@",
        variable_start_string="@{{",
        variable_end_string="}}@",
        comment_start_string="@{#",
        comment_end_string="#}@",
        trim_blocks=True,
        optimized=False,  # we use every template once
    )
    template = env.from_string(data.playbook)
    return template.render(**variables)


def _compute_code_block_content(
    data: _AnsibleOutputDataExt,
    *,
    environment: Environment,
    previous_blocks: list[CodeBlockInfo],
) -> list[str]:
    flog = mlog.fields(func="_compute_code_block_content")

    flog.notice("Prepare environment")
    env = environment.env.copy()
    env.update(data.data.env)
    flog.notice("Environment: {}", env)

    flog.notice("Prepare temporary directory")
    with AnsibleTemporaryDirectory(prefix="antsibull-docs-output") as directory:
        file = directory / "playbook.yml"
        flog.notice("Directory: {}; playbook: {}", directory, file)
        with open(file, "w", encoding="utf-8") as f:
            f.write(_compose_playbook(data.data, previous_blocks=previous_blocks))

        command = ["ansible-playbook", "playbook.yml"]
        flog.notice("Run ansible-playbook: {}", command)
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                cwd=directory,
                env=env,
                check=True,
                encoding="utf-8",
            )
        except subprocess.CalledProcessError as exc:
            raise ValueError(f"{exc}\nError output:\n{exc.stderr}") from exc

        flog.notice("Post-process result")
        # Compute result lines
        lines = [line.rstrip() for line in result.stdout.split("\n")]
        first = 0
        last = len(lines)
        while first < last and not lines[first]:
            first += 1
        while first < last and not lines[last - 1]:
            last -= 1
        # Prepend lines
        prepend_lines = (
            data.data.prepend_lines.split("\n") if data.data.prepend_lines else []
        )
        return prepend_lines + lines[first:last]


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
    content: str,
    replacements: list[tuple[CodeBlockInfo, list[str]]],
    *,
    path: Path,
    errors: list[tuple[Path, int | None, int | None, str]],
) -> tuple[str, bool]:
    content_lines = content.split("\n")
    changed = False

    # Apply replacements sorted back to front
    for block, new_content in sorted(
        replacements, key=lambda entry: -entry[0].row_offset
    ):
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
        content_lines = _replace(content_lines, block=block, new_content=new_content)
        changed = True

    # Ensure trailing newline
    if content_lines and content_lines[-1]:
        content_lines.append("")
    return "\n".join(content_lines), changed


def _compute_replacements(
    content: str,
    *,
    path: Path,
    root: Path | None = None,
    errors: list[tuple[Path, int | None, int | None, str]],
    environment: Environment,
) -> list[tuple[CodeBlockInfo, list[str]]]:
    flog = mlog.fields(func="_compute_replacements")
    flog.notice("Find code blocks in file")
    try:
        blocks = _find_blocks(content=content, path=path, root=root, errors=errors)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        flog.notice("Error while finding code blocks: {}", exc)
        errors.append((path, None, None, f"Error while finding code blocks: {exc}"))
        return []

    flog.notice("Found {} blocks", len(blocks))

    replacements: list[tuple[CodeBlockInfo, list[str]]] = []
    for block, block_data, previous_blocks in blocks:
        flog.notice("Processing block at line {}", block.row_offset + 1)
        try:
            new_content = _compute_code_block_content(
                block_data, previous_blocks=previous_blocks, environment=environment
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            flog.notice("Error while computing code block's expected contents: {}", exc)
            errors.append(
                (
                    path,
                    block_data.line,
                    block_data.col,
                    f"Error while computing code block's expected contents:\n{exc}",
                )
            )
            continue
        old_content = block.content.split("\n")
        if old_content and old_content[-1] == "":
            old_content.pop()
        if new_content != old_content:
            replacements.append((block, new_content))
    return replacements


_COLORS = {
    # Regular
    "faint": "\033[2m",  # faint
    "error": "\033[0;31m",  # red
    "bold": "\033[1m",  # bold
    # Diff
    "unchanged": "\033[2m",  # faint
    "remove": "\033[0;31m",  # red
    "add": "\033[0;32m",  # green
    "hint": "\033[1m",  # bold
    "omit": "\033[1m",  # bold
    # Reset
    "reset": "\033[0m",
}


def _colorize(text: str, *, color_code: str, color: bool) -> str:
    if not color:
        return text
    return f"{_COLORS[color_code]}{text}{_COLORS['reset']}"


def _colorize_diff(diff_line: str, *, color: bool) -> str:
    if not color:
        return diff_line
    col = None
    skip = 0
    if diff_line.startswith("+"):
        col = "add"
        skip = 1
    if diff_line.startswith("-"):
        col = "remove"
        skip = 1
    if diff_line.startswith("?"):
        col = "hint"
        skip = 1
    if diff_line.startswith(" "):
        col = "unchanged"
        skip = 1
    if diff_line.startswith("["):
        col = "omit"
    if col is None:
        return diff_line
    return (
        f"{diff_line[:skip]}{_colorize(diff_line[skip:], color_code=col, color=color)}"
    )


def _add_replacements_as_errors(
    errors: list[tuple[Path, int | None, int | None, str]],
    *,
    path: Path,
    replacements: list[tuple[CodeBlockInfo, list[str]]],
    environment_lines: int = 2,
    color: bool,
) -> None:
    if not replacements:
        return
    d = difflib.Differ()
    for code_block, new_content in replacements:
        old_content = code_block.content.rstrip().split("\n")
        changes: list[str] = []
        no_changes = 0
        last_change_add_lines = 0
        for change in d.compare(old_content, new_content):
            if change.startswith("?") and change.endswith("\n"):
                change = change[:-1]
            changes.append(_colorize_diff(change, color=color))
            if change.startswith(" "):
                no_changes += 1
            else:
                if no_changes > environment_lines + last_change_add_lines + 1:
                    lines_to_skip = (
                        no_changes - environment_lines - last_change_add_lines
                    )
                    changes[
                        -lines_to_skip - environment_lines - 1 : -environment_lines - 1
                    ] = [
                        _colorize_diff(
                            f"[... {lines_to_skip} lines skipped ...]", color=color
                        )
                    ]
                no_changes = 0
                last_change_add_lines = environment_lines
        if no_changes > environment_lines + 1:
            lines_to_skip = no_changes - environment_lines
            changes[-lines_to_skip:] = [
                _colorize_diff(f"[... {lines_to_skip} lines skipped ...]", color=color)
            ]
        message = "Output would differ:\n" + "\n".join(changes)
        errors.append(
            (path, code_block.row_offset + 1, code_block.col_offset + 1, message)
        )


def process_file(
    path: Path,
    *,
    root: Path | None = None,
    errors: list[tuple[Path, int | None, int | None, str]],
    environment: Environment,
    check: bool,
    color: bool,
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
        environment=environment,
    )
    if not replacements:
        return

    if check:
        _add_replacements_as_errors(
            errors, path=path, replacements=replacements, color=color
        )
        return

    flog.notice("Do replacements for {}", path)
    content, changed = _apply_replacements(
        content, replacements, path=path, errors=errors
    )
    if not changed:
        return

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
    environment: Environment,
    check: bool,
    color: bool,
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
                        environment=environment,
                        check=check,
                        color=color,
                    )
    except Exception as exc:  # pylint: disable=broad-exception-caught
        errors.append((path, None, None, f"Error while listing files: {exc}"))


def get_environment(
    collection_path: Path | None = None,
    collection_config: CollectionConfig | None = None,
) -> Environment:
    flog = mlog.fields(func="get_environment")
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
    if collection_config is not None:
        env.update(collection_config.ansible_output.global_env)
    flog.notice("Environment template: {}", env)
    return Environment(env=env)


def detect_color(*, force: bool | None = None) -> bool:
    if force is not None:
        return force
    return sys.stdout.isatty()


def check_rst_files(
    paths: Sequence[str],
    *,
    environment: Environment | None = None,
    check: bool = False,
    color: bool | None = None,
) -> list[tuple[Path, int | None, int | None, str]]:
    if environment is None:
        environment = get_environment()
    if color is None:
        color = detect_color()
    errors: list[tuple[Path, int | None, int | None, str]] = []
    for path in paths:
        path_obj = Path(path)
        if path_obj.is_dir():
            process_directory(
                path_obj,
                errors=errors,
                environment=environment,
                check=check,
                color=color,
            )
        elif path_obj.exists():
            process_file(
                path_obj,
                errors=errors,
                environment=environment,
                check=check,
                color=color,
            )
        else:
            errors.append((path_obj, None, None, "Does not exist"))
    return errors


def print_errors(
    errors: list[tuple[Path, int | None, int | None, str]],
    *,
    with_header: bool,
    color: bool,
) -> None:
    if with_header and errors:
        print()
        print(
            _colorize(
                f"Found {len(errors)} error{'' if len(errors) == 1 else 's'}:",
                color_code="bold",
                color=color,
            )
        )
    for error_path, line, col, error in sorted(
        errors,
        key=lambda entry: (str(entry[0]), entry[1] or 0, entry[2] or 0, entry[3]),
    ):
        prefix = _colorize(
            f"{error_path}:{line or '-'}:{col or '-'}: ", color_code="bold", color=color
        )
        error_lines = [error_line.rstrip() for error_line in error.split("\n")]
        print(f"{prefix}{_colorize(error_lines[0], color_code='error', color=color)}")
        if len(error_lines) > 1:
            prefix = "   "
            for error_line in error_lines[1:]:
                if error_line:
                    print(f"{prefix}{error_line}")
                else:
                    print()


def _run_ansible_output(
    *,
    paths: tuple[str, ...],
    environment: Environment | None = None,
    check: bool,
    force_color: bool | None,
) -> int:
    color = detect_color(force=force_color)
    errors = check_rst_files(paths, environment=environment, check=check, color=color)
    print_errors(errors, with_header=True, color=color)
    return 3 if len(errors) > 0 else 0


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
    check: bool = app_ctx.extra["check"]
    force_color: bool | None = app_ctx.extra["force_color"]

    if paths:
        return _run_ansible_output(
            paths=paths,
            check=check,
            force_color=force_color,
        )

    path_to_collection = "."
    try:
        info = load_collection_info(path_to_collection)
        namespace = info["namespace"]
        name = info["name"]
    except Exception:  # pylint: disable=broad-exception-caught
        errors: list[tuple[Path, int | None, int | None, str]] = []
        errors.append(
            (
                Path(path_to_collection),
                None,
                None,
                "Cannot identify collection with galaxy.yml or MANIFEST.json at this path",
            )
        )
        print_errors(errors, with_header=True, color=detect_color(force=force_color))
        return 3 if len(errors) > 0 else 0

    collection_config = asyncio.run(
        load_collection_config(f"{namespace}.{name}", path_to_collection)
    )

    with CollectionCopier() as copier:
        copier.add_collection(path_to_collection, namespace, name)
        environment = get_environment(
            collection_path=Path(copier.dir), collection_config=collection_config
        )
        rst_dir = "docs/docsite/rst"
        if os.path.exists(rst_dir):
            paths = (rst_dir,)
        return _run_ansible_output(
            paths=paths,
            environment=environment,
            check=check,
            force_color=force_color,
        )
