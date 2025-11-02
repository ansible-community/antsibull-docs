# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project
"""Ansible-output data processing."""

from __future__ import annotations

import asyncio
import subprocess
from dataclasses import dataclass
from pathlib import Path

import jinja2
from antsibull_core.logging import get_module_logger
from antsibull_docutils.rst_code_finder import (
    CodeBlockInfo,
)
from antsibull_fileutils.tempfile import AnsibleTemporaryDirectory
from antsibull_fileutils.yaml import store_yaml_file

from sphinx_antsibull_ext.schemas.ansible_output_data import (
    AnsibleOutputData,
    NonRefPostprocessor,
    PostprocessorCLI,
    VariableSource,
    VariableSourceCodeBlock,
    VariableSourceValue,
)

from .load import Block, Error

mlog = get_module_logger(__name__)


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
    if data.playbook is None:
        raise AssertionError("playbook cannot be None at this point")

    if all(s not in data.playbook for s in ("@{%", "@{{", "@{#")):
        return data.playbook

    variables = {}
    for key, value in data.variables.items():
        variables[key] = _get_variable_value(
            key=key, value=value, previous_blocks=previous_blocks
        )

    try:
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
    except Exception as exc:
        raise ValueError(f"Error while templating playbook:\n{exc}") from exc


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


def _compose_error(
    *, command: list[str], returncode: int, stdout: str, stderr: str
) -> str:
    return (
        f"Command {command} returned non-zero exit status {returncode}.\n"
        f"Error output:\n{stderr}\n\nStandard output:\n{stdout}"
    )


async def _execute(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    stdin: str | None = None,
) -> str:
    try:
        result = await asyncio.create_subprocess_exec(
            *command,
            stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            env=env,
        )
    except IOError as exc:
        raise ValueError(f"Cannot execute command {command}:\n{exc}") from exc
    b_stdout, b_stderr = await result.communicate(
        input=stdin.encode("utf-8") if stdin is not None else None
    )
    assert result.returncode is not None
    stdout = b_stdout.decode("utf-8")
    stderr = b_stderr.decode("utf-8")
    if result.returncode == 0:
        return stdout
    raise ValueError(
        _compose_error(
            command=command, returncode=result.returncode, stdout=stdout, stderr=stderr
        )
    )


async def _apply_postprocessor(
    lines: list[str],
    *,
    block_id: str,
    env: dict[str, str],
    postprocessor: NonRefPostprocessor,
) -> list[str]:
    flog = mlog.fields(func="_apply_postprocessor", block_id=block_id)

    if isinstance(postprocessor, PostprocessorCLI):
        flog.notice("Run postprocessor command: {}", postprocessor.command)
        stdout = await _execute(
            postprocessor.command, env=env, stdin="\n".join(lines) + "\n"
        )
        return _massage_stdout(stdout)

    raise AssertionError(
        f"Unknown post-processor type {type(postprocessor)}"
    )  # pragma: no cover


async def _compute_code_block_content(
    block: Block,
) -> list[str]:
    flog = mlog.fields(func="_compute_code_block_content", block_id=block.id)

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
        if block.data.inventory is not None:
            inventory_filename = "inventory.yaml"
            store_yaml_file(
                directory / inventory_filename,
                block.data.inventory.model_dump(mode="json", exclude_unset=True),
                nice=True,
                sort_keys=True,
            )
            command.extend(["-i", inventory_filename])

        flog.notice("Run ansible-playbook: {}", command)
        stdout = await _execute(command, cwd=directory, env=block.merged_env)

        flog.notice("Post-process result")
        lines = _massage_stdout(
            stdout,
            skip_first_lines=block.data.skip_first_lines or 0,
            skip_last_lines=block.data.skip_last_lines or 0,
            prepend_lines=block.data.prepend_lines,
        )
        for postprocessor in block.merged_postprocessors:
            flog.notice("Run post-processor {}", postprocessor)
            try:
                lines = await _apply_postprocessor(
                    lines,
                    block_id=block.id,
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
    id: str

    path: Path
    codeblock: CodeBlockInfo
    new_content: list[str]


async def compute_replacement(
    block: Block,
) -> Replacement | Error | None:
    """
    Compute replacement for a block.

    Returns either a ``Replacement`` object,
    ``None`` in case the replacement is identical to the current content,
    or an ``Error`` object in case the computation failed.
    """
    flog = mlog.fields(func="compute_replacement", block_id=block.id)

    try:
        new_content = await _compute_code_block_content(block)
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
        id=block.id,
        path=block.path,
        codeblock=block.codeblock,
        new_content=new_content,
    )
