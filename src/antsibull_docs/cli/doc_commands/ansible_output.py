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
    Environment,
    Error,
    get_environment,
    load_blocks_from_file,
)
from ...ansible_output.process import compute_replacement
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


def process_file(
    path: Path,
    *,
    root: Path | None = None,
    errors: list[Error],
    environment: Environment,
    check: bool,
    color: bool,
) -> None:
    """
    Process RST file.

    Note that this function must not be used in multiple threads at the same time!
    """
    flog = mlog.fields(func="process_file")

    data = load_blocks_from_file(
        path, root=root, errors=errors, environment=environment
    )
    if not data:
        return

    flog.notice("Compute replacements")
    replacements = []
    for block in data.blocks:
        replacement = compute_replacement(block, path=path)
        if replacement is None:
            continue
        if isinstance(replacement, Error):
            errors.append(replacement)
        else:
            replacements.append(replacement)

    if check:
        errors.extend(
            convert_replacements_to_errors(replacements=replacements, color=color)
        )
        return

    apply_replacements(replacements, errors=errors)


def process_directory(
    path: Path,
    *,
    errors: list[Error],
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
        errors.append(Error(path, None, None, f"Error while listing files: {exc}"))


def check_rst_files(
    paths: Sequence[str],
    *,
    environment: Environment | None = None,
    check: bool = False,
    color: bool | None = None,
) -> list[Error]:
    if environment is None:
        environment = get_environment()
    if color is None:
        color = detect_color()
    errors: list[Error] = []
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
            errors.append(Error(path_obj, None, None, "Does not exist"))
    return errors


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
