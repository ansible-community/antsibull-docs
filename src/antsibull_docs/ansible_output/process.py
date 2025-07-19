# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project
"""Ansible-output data processing."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

import jinja2
from antsibull_core.logging import log
from antsibull_docutils.rst_code_finder import (
    CodeBlockInfo,
)
from antsibull_fileutils.tempfile import AnsibleTemporaryDirectory

from sphinx_antsibull_ext.schemas.ansible_output_data import (
    AnsibleOutputData,
    NonRefPostprocessor,
    PostprocessorCLI,
    VariableSource,
    VariableSourceCodeBlock,
    VariableSourceValue,
)

from .load import Block, Error

mlog = log.fields(mod=__name__)


def _get_variable_value(
    *, key: str, value: VariableSource, previous_blocks: list[CodeBlockInfo]
) -> str:
    if isinstance(value, VariableSourceValue):
        return value.value
    if not isinstance(value, VariableSourceCodeBlock):
        raise AssertionError(  # pragma: no cover
            "Implementation error: cannot handle {value!r}"
        )

    candidates = [
        block
        for block in previous_blocks
        if block.language == value.previous_code_block
    ]
    try:
        return candidates[value.previous_code_block_index].content
    except IndexError:
        raise ValueError(  # pylint: disable=raise-missing-from
            f"Found {len(candidates)} previous code block(s) of"
            f" language {value.previous_code_block!r} for variable {key!r},"
            f" which does not allow index {value.previous_code_block_index}"
        )


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


def _strip_empty_lines(lines: list[str]) -> list[str]:
    first = 0
    last = len(lines)
    while first < last and not lines[first]:
        first += 1
    while first < last and not lines[last - 1]:
        last -= 1
    return lines[first:last]


def _strip_common_indent(lines: list[str]) -> list[str]:
    indent = None
    for line in lines:
        line_strip = line.lstrip()
        if not line_strip:
            continue
        li = len(line) - len(line_strip)
        if indent is None or indent > li:
            indent = li
    if indent is None:
        raise ValueError("Output is empty")
    return [line[indent:] for line in lines]


def _massage_stdout(
    stdout: str,
    *,
    skip_first_lines: int = 0,
    skip_last_lines: int = 0,
    prepend_lines: str | None = None,
) -> list[str]:
    # Compute result lines
    lines = [line.rstrip() for line in stdout.split("\n")]
    lines = _strip_empty_lines(lines)

    # Skip lines
    if skip_first_lines > 0:
        lines = lines[skip_first_lines:]
    if skip_last_lines > 0:
        lines = lines[:-skip_last_lines]

    # Prepend lines
    if prepend_lines:
        lines = prepend_lines.split("\n") + lines

    return _strip_common_indent(_strip_empty_lines(lines))


def _apply_postprocessor(
    lines: list[str],
    *,
    env: dict[str, str],
    postprocessor: NonRefPostprocessor,
) -> list[str]:
    flog = mlog.fields(func="_apply_postprocessor")

    if isinstance(postprocessor, PostprocessorCLI):
        flog.notice("Run postprocessor command: {}", postprocessor.command)
        try:
            result = subprocess.run(
                postprocessor.command,
                capture_output=True,
                input="\n".join(lines) + "\n",
                env=env,
                check=True,
                encoding="utf-8",
            )
        except subprocess.CalledProcessError as exc:
            raise ValueError(
                f"{exc}\nError output:\n{exc.stderr}\n\nStandard output:\n{exc.stdout}"
            ) from exc
        lines = _massage_stdout(result.stdout)

    return lines


def _compute_code_block_content(
    block: Block,
) -> list[str]:
    flog = mlog.fields(func="_compute_code_block_content")

    flog.notice("Prepare environment")
    flog.notice("Environment: {}", block.merged_env)

    flog.notice("Prepare temporary directory")
    with AnsibleTemporaryDirectory(prefix="antsibull-docs-output") as directory:
        file = directory / "playbook.yml"
        flog.notice("Directory: {}; playbook: {}", directory, file)
        with open(file, "w", encoding="utf-8") as f:
            f.write(
                _compose_playbook(block.data, previous_blocks=block.previous_blocks)
            )

        command = ["ansible-playbook", "playbook.yml"]
        flog.notice("Run ansible-playbook: {}", command)
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                cwd=directory,
                env=block.merged_env,
                check=True,
                encoding="utf-8",
            )
        except subprocess.CalledProcessError as exc:
            raise ValueError(
                f"{exc}\nError output:\n{exc.stderr}\n\nStandard output:\n{exc.stdout}"
            ) from exc

        flog.notice("Post-process result")
        lines = _massage_stdout(
            result.stdout,
            skip_first_lines=block.data.skip_first_lines,
            skip_last_lines=block.data.skip_last_lines,
            prepend_lines=block.data.prepend_lines,
        )
        for postprocessor in block.merged_postprocessors:
            flog.notice("Run post-processor {}", postprocessor)
            try:
                lines = _apply_postprocessor(
                    lines,
                    env=block.merged_env,
                    postprocessor=postprocessor,
                )
            except ValueError as exc:
                raise ValueError(
                    f"Error while running post-processor {postprocessor}:\n{exc}"
                ) from exc
        return lines


@dataclass
class Replacement:
    path: Path
    codeblock: CodeBlockInfo
    new_content: list[str]


def compute_replacement(
    block: Block,
) -> Replacement | Error | None:
    """
    Compute replacement for a block.

    Returns either a ``Replacement`` object,
    ``None`` in case the replacement is identical to the current content,
    or an ``Error`` object in case the computation failed.
    """
    flog = mlog.fields(func="compute_replacement")

    try:
        new_content = _compute_code_block_content(block)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        flog.notice("Error while computing replacement: {}", exc)
        return Error(
            block.path,
            block.data_line,
            block.data_col,
            f"Error while computing code block's expected contents:\n{exc}",
        )

    flog.notice("Computed replacement: {}", new_content)

    old_content = block.codeblock.content.split("\n")
    if old_content and old_content[-1] == "":
        old_content.pop()
    if new_content == old_content:
        return None

    return Replacement(
        path=block.path,
        codeblock=block.codeblock,
        new_content=new_content,
    )
