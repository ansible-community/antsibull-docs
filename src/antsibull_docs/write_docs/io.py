# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output helpers."""

from __future__ import annotations

import fnmatch
import os
import shutil
import typing as t
from collections import defaultdict
from threading import Lock

from antsibull_core import app_context
from antsibull_core.logging import log
from antsibull_fileutils.io import copy_file as _copy_file
from antsibull_fileutils.io import write_file as _write_file

if t.TYPE_CHECKING:
    from _typeshed import StrOrBytesPath

mlog = log.fields(mod=__name__)


class Output:
    """
    Thread-safe class that allows to create directories and copy/write files into the output tree.
    """

    def __init__(self, root: StrOrBytesPath):
        """
        Create Output object.

        ``root`` is assumed to be an existing directory the user can write to.
        """
        self.root = root

    def ensure_directory(self, directory: StrOrBytesPath, /) -> None:
        """
        Ensure that the directory (relative to our root) exists.
        """
        path = os.path.join(self.root, directory)  # type: ignore
        # This is dangerous but the code that takes dest_dir from the user checks
        # permissions on it to make it as safe as possible.
        os.makedirs(path, mode=0o755, exist_ok=True)

    async def write_file(self, filename: StrOrBytesPath, /, content: str) -> None:
        """
        Write the given text content to a file (relative to our root).
        """
        path = os.path.join(self.root, filename)  # type: ignore
        lib_ctx = app_context.lib_ctx.get()
        await _write_file(path, content, file_check_content=lib_ctx.file_check_content)

    async def copy_file(
        self,
        source_path: StrOrBytesPath,
        dest_path: StrOrBytesPath,
        /,
        *,
        check_content: bool = True,
    ) -> None:
        """
        Copy the given ``source_path`` (relative to CWD) to the ``dest_path``
        (relative to our root).
        """
        src_path = os.path.join(self.root, dest_path)  # type: ignore
        lib_ctx = app_context.lib_ctx.get()
        await _copy_file(
            source_path,
            src_path,
            check_content=check_content,
            file_check_content=lib_ctx.file_check_content,
            chunksize=lib_ctx.chunksize,
        )


class TrackingOutput(Output):
    lock: Lock
    directories: set[str]
    files: defaultdict[str, set[str]]
    patterns: defaultdict[str, set[str]]

    @staticmethod
    def _normalize_directory(directory: StrOrBytesPath) -> str:
        norm_dir_or_bytes = os.path.normpath(directory)
        norm_dir = (
            norm_dir_or_bytes.decode("utf-8")
            if isinstance(norm_dir_or_bytes, bytes)
            else norm_dir_or_bytes
        )
        if norm_dir == ".":
            norm_dir = ""
        return norm_dir

    @staticmethod
    def _normalize_filename(filename: StrOrBytesPath) -> str:
        norm_fn_or_bytes = os.path.normpath(filename)
        return (
            norm_fn_or_bytes.decode("utf-8")
            if isinstance(norm_fn_or_bytes, bytes)
            else norm_fn_or_bytes
        )

    def __init__(self, root: StrOrBytesPath):
        super().__init__(root=root)
        self.directories = {""}
        self.files = defaultdict(set)
        self.patterns = defaultdict(set)
        self.lock = Lock()

    def ensure_directory(self, directory: StrOrBytesPath, /) -> None:
        super().ensure_directory(directory)
        directories = []
        norm_directory = self._normalize_directory(directory)
        while norm_directory:
            directories.append(norm_directory)
            norm_directory, prev_directory = (
                os.path.basename(norm_directory),
                norm_directory,
            )
            if norm_directory == prev_directory:
                break
        with self.lock:
            self.directories.update(directories)

    def _register_file(self, filename: StrOrBytesPath, /) -> None:
        filename_dir, filename_name = os.path.split(filename)
        directory = self._normalize_directory(filename_dir)
        norm_filename = self._normalize_filename(filename_name)
        with self.lock:
            self.directories.add(directory)
            self.files[directory].add(norm_filename)

    async def write_file(self, filename: StrOrBytesPath, /, content: str) -> None:
        await super().write_file(filename, content=content)
        self._register_file(filename)

    def register_pattern(self, directory: StrOrBytesPath, pattern: str, /) -> None:
        norm_directory = self._normalize_directory(directory)
        with self.lock:
            self.patterns[norm_directory].add(pattern)

    async def copy_file(
        self,
        source_path: StrOrBytesPath,
        dest_path: StrOrBytesPath,
        /,
        *,
        check_content: bool = True,
    ) -> None:
        await super().copy_file(source_path, dest_path, check_content=check_content)
        self._register_file(dest_path)

    @staticmethod
    def _limit_by_patterns(filenames: list[str], patterns: set[str]) -> list[str]:
        result = set()
        for pattern in patterns:
            result.update(fnmatch.filter(filenames, pattern))
        return sorted(result)

    def _delete(self, directories_to_prune: set[str], files_to_prune: set[str]) -> None:
        flog = mlog.fields(func="TrackingOutput._delete")
        flog.notice("Begin")
        for filename in sorted(files_to_prune):
            full_filename = os.path.join(self.root, filename)  # type: ignore
            try:
                os.unlink(full_filename)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                flog.warning(f"Error while deleting file {full_filename!r}: {exc}")
        for directory in sorted(directories_to_prune):
            full_directory = os.path.join(self.root, directory)  # type: ignore
            try:
                shutil.rmtree(full_directory)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                flog.warning(
                    f"Error while deleting directory {full_directory!r}: {exc}"
                )
        flog.notice("Done")

    def cleanup(
        self,
        root: StrOrBytesPath,
        cleanup: t.Literal["similar-files", "similar-files-and-dirs", "everything"],
        /,
    ) -> None:
        flog = mlog.fields(func="TrackingOutput.cleanup")
        flog.notice("Begin")

        with self.lock:
            flog.notice("Collecting files and directories to delete")
            directories_to_prune: set[str] = set()
            files_to_prune: set[str] = set()
            root_dir = os.path.join(self.root, root)  # type: ignore
            for dirpath, dirnames, filenames in os.walk(root_dir):
                rel_dirpath = os.path.relpath(dirpath, self.root)  # type: ignore
                directory = self._normalize_directory(rel_dirpath)
                flog.notice(f"Processing {directory}")
                if directory not in self.directories:
                    # Stop iteration
                    flog.notice("Unknown directory")
                    dirnames.clear()
                    if cleanup != "similar-files":
                        directories_to_prune.add(directory)
                    continue

                expected_filenames = self.files[directory]
                superfluous_filenames = [
                    filename
                    for filename in filenames
                    if filename not in expected_filenames
                ]
                if (
                    cleanup != "everything"
                    and directory in self.patterns
                    and superfluous_filenames
                ):
                    superfluous_filenames = self._limit_by_patterns(
                        superfluous_filenames, self.patterns[directory]
                    )

                flog.notice(f"Found {len(superfluous_filenames)} superfluous file(s)")
                for filename in superfluous_filenames:
                    files_to_prune.add(os.path.join(directory, filename))

        flog.notice("Doing actual delete")
        self._delete(directories_to_prune, files_to_prune)

        flog.notice("Done")
