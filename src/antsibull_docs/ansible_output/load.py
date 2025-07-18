# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project
"""Ansible-output data loading."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import pydantic
from antsibull_core.logging import log
from antsibull_core.pydantic import get_formatted_error_messages
from antsibull_docutils.rst_code_finder import (
    CodeBlockInfo,
    find_code_blocks,
    mark_antsibull_code_block,
)
from docutils import nodes
from yaml import MarkedYAMLError

from sphinx_antsibull_ext.directive_helper import YAMLDirective
from sphinx_antsibull_ext.schemas.ansible_output_data import (
    AnsibleOutputData,
    NonRefPostprocessor,
    PostprocessorNameRef,
)

from ..schemas.collection_config import CollectionConfig

mlog = log.fields(mod=__name__)


@dataclass
class Error:
    path: Path
    line: int | None
    col: int | None
    message: str


@dataclass
class Block:
    codeblock: CodeBlockInfo
    data: AnsibleOutputData
    data_line: int
    data_col: int
    previous_blocks: list[CodeBlockInfo]

    merged_env: dict[str, str]
    merged_postprocessors: list[NonRefPostprocessor]


@dataclass
class Environment:
    env: dict[str, str]
    global_postprocessors: dict[str, NonRefPostprocessor]


@dataclass
class FileData:
    path: Path
    blocks: list[Block]


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


def _compose_block(
    codeblock: CodeBlockInfo,
    *,
    path: Path,
    data: _AnsibleOutputDataExt,
    previous_blocks: list[CodeBlockInfo],
    errors: list[Error],
    environment: Environment,
) -> Block:
    env = environment.env.copy()
    env.update(data.data.env)
    postprocessors = []
    for postprocessor in data.data.postprocessors:
        if isinstance(postprocessor, PostprocessorNameRef):
            ref = postprocessor.name
            try:
                postprocessor = environment.global_postprocessors[ref]
            except KeyError:
                errors.append(
                    Error(
                        path,
                        data.line,
                        data.col,
                        f"No global postprocessor of name {ref!r} defined",
                    )
                )
                continue
        postprocessors.append(postprocessor)
    return Block(
        codeblock=codeblock,
        data=data.data,
        data_line=data.line,
        data_col=data.col,
        previous_blocks=previous_blocks,
        merged_env=env,
        merged_postprocessors=postprocessors,
    )


def _find_blocks(
    *,
    content: str,
    path: Path,
    root: Path | None = None,
    errors: list[Error],
    environment: Environment,
) -> list[Block]:
    blocks: list[Block] = []
    data: _AnsibleOutputDataExt | None = None
    previous_blocks: list[CodeBlockInfo] = []
    for block in find_code_blocks(
        content, path=path, root_prefix=root, extra_directives=_DIRECTIVES
    ):
        if block.language == _ANSIBLE_OUTPUT_DATA_IDENTIFIER:
            if data is not None:
                errors.append(
                    Error(
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
                errors.append(Error(path, line, col, message))
            continue
        previous_blocks.append(block)
        if data is None:
            continue
        if block.language != data.data.language:
            continue
        blocks.append(
            _compose_block(
                block,
                path=path,
                data=data,
                previous_blocks=previous_blocks[:-1],
                errors=errors,
                environment=environment,
            )
        )
        data = None
    if data is not None:
        errors.append(
            Error(
                path,
                data.line,
                data.col,
                "ansible-output-data directive not used",
            )
        )
    return blocks


def load_blocks_from_content(
    content: str,
    *,
    path: Path,
    root: Path | None = None,
    errors: list[Error],
    environment: Environment,
) -> FileData | None:
    """
    Extract blocks from loaded RST file.

    Returns ``FileData`` object, or ``None`` in case a fatal error happened.

    **Note**: must not be used in parallel.
    """
    flog = mlog.fields(func="load_blocks_from_content")
    flog.notice("Find code blocks in file")
    try:
        blocks = _find_blocks(
            content=content,
            path=path,
            root=root,
            errors=errors,
            environment=environment,
        )
    except Exception as exc:  # pylint: disable=broad-exception-caught
        flog.notice("Error while finding code blocks: {}", exc)
        errors.append(
            Error(path, None, None, f"Error while finding code blocks: {exc}")
        )
        return None

    flog.notice("Found {} blocks", len(blocks))

    return FileData(
        path=path,
        blocks=blocks,
    )


def load_blocks_from_file(
    path: Path,
    *,
    root: Path | None = None,
    errors: list[Error],
    environment: Environment,
) -> FileData | None:
    """
    Extract blocks from RST file on disk.

    Returns ``FileData`` object, or ``None`` in case a fatal error happened.

    **Note**: must not be used in parallel.
    """
    flog = mlog.fields(func="load_blocks_from_file")

    flog.notice("Load {}", path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as exc:  # pylint: disable=broad-exception-caught
        flog.notice("Error while reading content: {}", exc)
        errors.append(Error(path, None, None, f"Error while reading content: {exc}"))
        return None

    return load_blocks_from_content(
        content,
        path=path,
        root=root,
        errors=errors,
        environment=environment,
    )


def get_environment(
    collection_path: Path | None = None,
    collection_config: CollectionConfig | None = None,
) -> Environment:
    """
    Load/create environment.
    """
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
    postprocessors = {}
    if collection_config is not None:
        env.update(collection_config.ansible_output.global_env)
        postprocessors.update(collection_config.ansible_output.global_postprocessors)
    flog.notice("Environment template: {}", env)
    return Environment(env=env, global_postprocessors=postprocessors)
