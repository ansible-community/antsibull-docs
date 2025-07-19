# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025, Ansible Project
"""Entrypoint to the antsibull-docs script."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Sequence
from pathlib import Path

from antsibull_core.logging import log

from ... import app_context
from ...ansible_output.load import (
    Block,
    Environment,
    Error,
    get_environment,
    load_blocks_from_file,
)
from ...ansible_output.process import Replacement, compute_replacement
from ...ansible_output.replace import (
    apply_replacements,
    colorize,
    convert_replacements_to_errors,
    detect_color,
)
from ...collection_config import load_collection_config
from ...lint_helpers import load_collection_info
from ...utils.collection_copier import CollectionCopier

mlog = log.fields(mod=__name__)


def find_blocks_in_file(
    path: Path,
    *,
    root: Path | None = None,
    errors: list[Error],
    blocks: list[Block],
    environment: Environment,
) -> None:
    """
    Process RST file.

    Note that this function must not be used in multiple threads at the same time!
    """
    data = load_blocks_from_file(
        path, root=root, errors=errors, environment=environment
    )
    if data:
        blocks.extend(data.blocks)


def find_blocks_in_directory(
    path: Path,
    *,
    errors: list[Error],
    blocks: list[Block],
    environment: Environment,
) -> None:
    flog = mlog.fields(func="find_blocks_in_directory")
    flog.notice("Walking {}", path)
    try:
        for dirpath, _, filenames in path.walk():
            flog.notice("Processing {}: found {}", dirpath, filenames)
            for filename in filenames:
                if filename.endswith(".rst"):
                    find_blocks_in_file(
                        dirpath / filename,
                        root=path,
                        errors=errors,
                        blocks=blocks,
                        environment=environment,
                    )
    except Exception as exc:  # pylint: disable=broad-exception-caught
        errors.append(Error(path, None, None, f"Error while listing files: {exc}"))


def find_blocks(
    paths: Sequence[str],
    *,
    environment: Environment | None = None,
) -> tuple[list[Error], list[Block]]:
    if environment is None:
        environment = get_environment()
    errors: list[Error] = []
    blocks: list[Block] = []
    for path in paths:
        path_obj = Path(path)
        if path_obj.is_dir():
            find_blocks_in_directory(
                path_obj,
                errors=errors,
                blocks=blocks,
                environment=environment,
            )
        elif path_obj.exists():
            find_blocks_in_file(
                path_obj,
                errors=errors,
                blocks=blocks,
                environment=environment,
            )
        else:
            errors.append(Error(path_obj, None, None, "Does not exist"))
    return errors, blocks


def print_errors(
    errors: list[Error],
    *,
    with_header: bool,
    color: bool,
) -> None:
    if with_header and errors:
        print()
        print(
            colorize(
                f"Found {len(errors)} error{'' if len(errors) == 1 else 's'}:",
                color_code="bold",
                color=color,
            )
        )
    for error in sorted(
        errors,
        key=lambda error: (error.path, error.line or 0, error.col or 0, error.message),
    ):
        prefix = colorize(
            f"{error.path}:{error.line or '-'}:{error.col or '-'}: ",
            color_code="bold",
            color=color,
        )
        error_lines = [error_line.rstrip() for error_line in error.message.split("\n")]
        print(f"{prefix}{colorize(error_lines[0], color_code='error', color=color)}")
        if len(error_lines) > 1:
            prefix = "   "
            for error_line in error_lines[1:]:
                if error_line:
                    print(f"{prefix}{error_line}")
                else:
                    print()


async def _compute_replacement(
    block: Block, *, semaphore: asyncio.Semaphore
) -> Replacement | Error | None:
    async with semaphore:
        return await compute_replacement(block)


def _get_parallelism() -> int:
    lib_ctx = app_context.lib_ctx.get()
    if lib_ctx.process_max is not None and lib_ctx.process_max > 0:
        return lib_ctx.process_max
    process_cpu_count = os.process_cpu_count()
    if process_cpu_count is not None and process_cpu_count > 0:
        return process_cpu_count
    cpu_count = os.cpu_count()
    if cpu_count is not None and cpu_count > 0:
        return cpu_count
    return 1


async def _compute_replacements(
    blocks: list[Block], *, errors: list[Error]
) -> list[Replacement]:
    flog = mlog.fields(func="_compute_replacements")
    flog.notice("Processing {} blocks", len(blocks))

    parallelism = _get_parallelism()
    flog.notice("Limiting to {} parallel subprocesses", parallelism)

    semaphore = asyncio.Semaphore(parallelism)
    computers = [_compute_replacement(block, semaphore=semaphore) for block in blocks]
    computed_results = await asyncio.gather(*computers)

    result = []
    for replacement in computed_results:
        if replacement is None:
            continue
        if isinstance(replacement, Error):
            errors.append(replacement)
        else:
            result.append(replacement)
    return result


def _run_ansible_output(
    *,
    paths: tuple[str, ...],
    environment: Environment | None = None,
    check: bool,
    force_color: bool | None,
) -> int:
    color = detect_color(force=force_color)
    errors, blocks = find_blocks(paths, environment=environment)
    replacements = asyncio.run(_compute_replacements(blocks, errors=errors))
    if check:
        errors.extend(
            convert_replacements_to_errors(replacements=replacements, color=color)
        )
    else:
        apply_replacements(replacements, errors=errors)
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
        errors: list[Error] = []
        errors.append(
            Error(
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
