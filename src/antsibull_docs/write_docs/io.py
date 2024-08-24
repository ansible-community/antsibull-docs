# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output helpers."""

from __future__ import annotations

import os
import typing as t

from antsibull_core.utils.io import copy_file as _copy_file
from antsibull_core.utils.io import write_file as _write_file

if t.TYPE_CHECKING:
    from _typeshed import StrOrBytesPath


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

    def ensure_directory(self, directory: StrOrBytesPath, /):
        """
        Ensure that the directory (relative to our root) exists.
        """
        path = os.path.join(self.root, directory)  # type: ignore
        # This is dangerous but the code that takes dest_dir from the user checks
        # permissions on it to make it as safe as possible.
        os.makedirs(path, mode=0o755, exist_ok=True)

    async def write_file(self, filename: StrOrBytesPath, /, content: str):
        """
        Write the given text content to a file (relative to our root).
        """
        path = os.path.join(self.root, filename)  # type: ignore
        await _write_file(path, content)

    async def copy_file(
        self,
        source_path: StrOrBytesPath,
        dest_path: StrOrBytesPath,
        /,
        *,
        check_content: bool = True,
    ):
        """
        Copy the given ``source_path`` (relative to CWD) to the ``dest_path``
        (relative to our root).
        """
        src_path = os.path.join(self.root, dest_path)  # type: ignore
        await _copy_file(source_path, src_path, check_content=check_content)
