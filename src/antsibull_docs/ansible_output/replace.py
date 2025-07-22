# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project
"""Ansible-output data replacing."""

from __future__ import annotations

import difflib
import sys
import typing as t
from pathlib import Path

from antsibull_core.logging import get_module_logger
from antsibull_docutils.rst_code_finder import (
    CodeBlockInfo,
)

from .load import Error
from .process import Replacement

mlog = get_module_logger(__name__)


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

ColorCode = t.Literal[
    "faint", "error", "bold", "unchanged", "remove", "add", "hint", "omit", "reset"
]


def colorize(text: str, *, color_code: ColorCode, color: bool) -> str:
    if not color:
        return text
    return f"{_COLORS[color_code]}{text}{_COLORS['reset']}"


def _colorize_diff(diff_line: str, *, color: bool) -> str:
    if not color:
        return diff_line
    col: ColorCode | None = None
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
        f"{diff_line[:skip]}{colorize(diff_line[skip:], color_code=col, color=color)}"
    )


def convert_replacements_to_errors(
    *,
    replacements: list[Replacement],
    environment_lines: int = 2,
    color: bool,
) -> list[Error]:
    """
    Given a list of replacements, convert them to ``Error`` objects.
    """
    if not replacements:
        return []
    d = difflib.Differ()
    errors = []
    for replacement in replacements:
        old_content = replacement.codeblock.content.rstrip().split("\n")
        changes: list[str] = []
        no_changes = 0
        last_change_add_lines = 0
        for change in d.compare(old_content, replacement.new_content):
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
            Error(
                replacement.path,
                replacement.codeblock.row_offset + 1,
                replacement.codeblock.col_offset + 1,
                message,
            )
        )
    return errors


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


def _apply_replacements_in_content(
    content: str,
    replacements: list[Replacement],
    *,
    path: Path,
    errors: list[Error],
) -> tuple[str, bool]:
    content_lines = content.split("\n")
    changed = False

    # Apply replacements sorted back to front
    for replacement in sorted(
        replacements, key=lambda replacement: -replacement.codeblock.row_offset
    ):
        if not replacement.codeblock.directly_replacable_in_content:
            errors.append(
                Error(
                    path,
                    replacement.codeblock.row_offset + 1,
                    replacement.codeblock.col_offset + 1,
                    "Code block is not replacable",
                )
            )
            continue
        content_lines = _replace(
            content_lines,
            block=replacement.codeblock,
            new_content=replacement.new_content,
        )
        changed = True

    # Ensure trailing newline
    if content_lines and content_lines[-1]:
        content_lines.append("")
    return "\n".join(content_lines), changed


def _apply_replacements_in_file(
    *,
    path: Path,
    replacements: list[Replacement],
    errors: list[Error],
) -> None:
    flog = mlog.fields(func="_apply_replacements_in_file", path=path)

    flog.notice("Load {}", path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as exc:  # pylint: disable=broad-exception-caught
        flog.notice("Error while reading content: {}", exc)
        errors.append(Error(path, None, None, f"Error while reading content: {exc}"))
        return

    content, changed = _apply_replacements_in_content(
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
        errors.append(Error(path, None, None, f"Error while writing content: {exc}"))


def apply_replacements(
    replacements: list[Replacement],
    *,
    errors: list[Error],
) -> None:
    """
    Apply replacements to RST files.
    """
    flog = mlog.fields(func="apply_replacements")

    flog.notice("Group replacements by file")
    replacements_by_file: dict[Path, list[Replacement]] = {}
    for replacement in replacements:
        if replacement.path not in replacements_by_file:
            replacements_by_file[replacement.path] = []
        replacements_by_file[replacement.path].append(replacement)

    flog.notice("Process {} files", len(replacements_by_file))
    for path, reps in sorted(replacements_by_file.items()):
        _apply_replacements_in_file(path=path, replacements=reps, errors=errors)


def detect_color(*, force: bool | None = None) -> bool:
    """
    Detect whether the output should be colorized.
    """
    if force is not None:
        return force
    return sys.stdout.isatty()
