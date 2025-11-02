# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project
"""Ansible-output data loading."""

from __future__ import annotations

import os
import typing as t
from dataclasses import dataclass
from pathlib import Path

import pydantic
from antsibull_core.logging import get_module_logger
from antsibull_core.pydantic import get_formatted_error_messages
from antsibull_docutils.rst_code_finder import (
    CodeBlockInfo,
    find_code_blocks,
    mark_antsibull_code_block,
)
from docutils import nodes
from docutils.parsers.rst import Directive
from yaml import MarkedYAMLError

from sphinx_antsibull_ext.directive_helper import YAMLDirective
from sphinx_antsibull_ext.schemas.ansible_output_data import (
    AnsibleOutputData,
    AnsibleOutputTemplate,
    NonRefPostprocessor,
    PostprocessorNameRef,
    combine,
)
from sphinx_antsibull_ext.schemas.ansible_output_meta import (
    ActionResetPreviousBlocks,
    ActionSetTemplate,
    AnsibleOutputMeta,
)

from ..schemas.collection_config import AnsibleOutputConfig, CollectionConfig

mlog = get_module_logger(__name__)


@dataclass
class Error:
    path: Path
    line: int | None
    col: int | None
    message: str


@dataclass
class Block:
    id: str

    path: Path
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


_ANSIBLE_OUTPUT_DATA_IDENTIFIER = "{}[]XXXXXXdata"
_ANSIBLE_OUTPUT_META_IDENTIFIER = "{}[]XXXXXXmeta"


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


class AnsibleOutputMetaDirective(YAMLDirective[AnsibleOutputMeta]):
    wrap_as_data = False
    schema = AnsibleOutputMeta

    def _handle_error(self, message: str, from_exc: Exception) -> list[nodes.Node]:
        literal = nodes.literal_block("", "")
        mark_antsibull_code_block(
            literal,
            language=_ANSIBLE_OUTPUT_META_IDENTIFIER,
            line=self.lineno,
            other={
                "error": message,
                "exception": from_exc,
            },
        )
        return [literal]

    def _run(self, content_str: str, content: AnsibleOutputMeta) -> list[nodes.Node]:
        literal = nodes.literal_block(content_str, "")
        mark_antsibull_code_block(
            literal,
            language=_ANSIBLE_OUTPUT_META_IDENTIFIER,
            line=self.lineno,
            other={
                "data": content,
            },
        )
        return [literal]


_DIRECTIVES: dict[str, type[Directive]] = {
    "ansible-output-data": AnsibleOutputDataDirective,
    "ansible-output-meta": AnsibleOutputMetaDirective,
}

_DirectiveName = t.Literal["ansible-output-data", "ansible-output-meta"]

_LANGUAGE_TO_DIRECTIVE: dict[str | None, _DirectiveName] = {
    _ANSIBLE_OUTPUT_DATA_IDENTIFIER: "ansible-output-data",
    _ANSIBLE_OUTPUT_META_IDENTIFIER: "ansible-output-meta",
}


@dataclass
class _AnsibleOutputDataExt:
    data: AnsibleOutputData
    line: int
    col: int


def _get_ansible_output_data_error(
    block: CodeBlockInfo, *, directive: str
) -> tuple[int, int, str]:
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
            f"Error while validating {directive} directive's contents:\n"
            + "\n".join(get_formatted_error_messages(exc))
        )
    return line, col, message


class _BlockCollector:
    def __init__(
        self,
        *,
        path: Path,
        relative_path: Path,
        errors: list[Error],
        environment: Environment,
    ) -> None:
        self.path = path
        self.relative_path = relative_path
        self.errors = errors
        self.environment = environment
        self.blocks: list[Block] = []
        self.data: _AnsibleOutputDataExt | None = None
        self.previous_blocks: list[CodeBlockInfo] = []
        self.template = AnsibleOutputTemplate()
        self.counter = 0

    def _process_reset_previous_blocks(
        self, action: ActionResetPreviousBlocks  # pylint: disable=unused-argument
    ) -> None:
        self.previous_blocks.clear()

    def _process_set_template(self, action: ActionSetTemplate) -> None:
        self.template = action.template

    def process_meta(
        self,
        meta: AnsibleOutputMeta,
        *,
        line: int,  # pylint: disable=unused-argument
        col: int,  # pylint: disable=unused-argument
    ) -> None:
        for action in meta.actions:
            if isinstance(action, ActionResetPreviousBlocks):
                self._process_reset_previous_blocks(action)
            elif isinstance(action, ActionSetTemplate):
                self._process_set_template(action)
            else:
                raise AssertionError("Unknown action")  # pragma: no cover

    def process_special_block(
        self, block: CodeBlockInfo, *, directive: _DirectiveName
    ) -> None:
        if self.data is not None:
            self.errors.append(
                Error(
                    self.path,
                    self.data.line,
                    self.data.col,
                    "ansible-output-data directive not used",
                )
            )
            self.data = None
        if "antsibull-other-error" in block.attributes:
            line, col, message = _get_ansible_output_data_error(
                block, directive=directive
            )
            self.errors.append(Error(self.path, line, col, message))
        if "antsibull-other-data" in block.attributes:
            if directive == "ansible-output-data":
                try:
                    data = combine(
                        data=block.attributes["antsibull-other-data"],
                        template=self.template,
                    )
                    self.data = _AnsibleOutputDataExt(
                        data=data,
                        line=block.row_offset + 1,
                        col=block.col_offset + 1,
                    )
                except ValueError as exc:
                    self.errors.append(
                        Error(
                            self.path,
                            block.row_offset + 1,
                            block.col_offset + 1,
                            str(exc),
                        )
                    )
            if directive == "ansible-output-meta":
                self.process_meta(
                    block.attributes["antsibull-other-data"],
                    line=block.row_offset + 1,
                    col=block.col_offset + 1,
                )

    def _add_block(
        self,
        codeblock: CodeBlockInfo,
        *,
        data: _AnsibleOutputDataExt,
    ) -> None:
        env = self.environment.env.copy()
        env.update(data.data.env)
        postprocessors = []
        error = False
        if data.data.postprocessors:
            for postprocessor in data.data.postprocessors:
                if isinstance(postprocessor, PostprocessorNameRef):
                    ref = postprocessor.name
                    try:
                        postprocessor = self.environment.global_postprocessors[ref]
                    except KeyError:
                        self.errors.append(
                            Error(
                                self.path,
                                data.line,
                                data.col,
                                f"No global postprocessor of name {ref!r} defined",
                            )
                        )
                        error = True
                        continue
                postprocessors.append(postprocessor)
        if error:
            return
        self.counter += 1
        block_id = f"{self.relative_path}-{self.counter}"
        self.blocks.append(
            Block(
                id=block_id,
                path=self.path,
                codeblock=codeblock,
                data=data.data,
                data_line=data.line,
                data_col=data.col,
                previous_blocks=self.previous_blocks[:-1],
                merged_env=env,
                merged_postprocessors=postprocessors,
            )
        )

    def found_block(self, block: CodeBlockInfo) -> None:
        directive = _LANGUAGE_TO_DIRECTIVE.get(block.language)
        if directive is not None:
            self.process_special_block(block, directive=directive)
            return
        self.previous_blocks.append(block)
        if self.data is None:
            return
        if block.language != self.data.data.language:
            return
        self._add_block(block, data=self.data)
        self.data = None

    def finish(self) -> list[Block]:
        if self.data is not None:
            self.errors.append(
                Error(
                    self.path,
                    self.data.line,
                    self.data.col,
                    "ansible-output-data directive not used",
                )
            )
        return self.blocks


def _find_blocks(
    *,
    content: str,
    path: Path,
    root: Path | None = None,
    errors: list[Error],
    environment: Environment,
) -> list[Block]:
    relative_path = path
    if root is not None:
        relative_path = relative_path.relative_to(root, walk_up=True)
    collector = _BlockCollector(
        path=path, relative_path=relative_path, errors=errors, environment=environment
    )
    for block in find_code_blocks(
        content, path=path, root_prefix=root, extra_directives=_DIRECTIVES
    ):
        collector.found_block(block)
    return collector.finish()


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
    *,
    collection_path: Path | None = None,
    collection_config: CollectionConfig | None = None,
    ansible_output_config: AnsibleOutputConfig | None = None,
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
        if ansible_output_config is not None:
            raise ValueError(
                "collection_config and ansible_output_config are mutually exclusive"
            )
        ansible_output_config = collection_config.ansible_output
    if ansible_output_config is not None:
        env.update(ansible_output_config.global_env)
        postprocessors.update(ansible_output_config.global_postprocessors)
    flog.notice("Environment template: {}", env)
    flog.notice("Global post-processors: {}", postprocessors)
    return Environment(env=env, global_postprocessors=postprocessors)
