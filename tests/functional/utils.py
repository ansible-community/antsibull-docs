# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
from contextlib import contextmanager
from unittest import mock

import antsibull_docs

ANTSIBULL_DOCS_CI_VERSION = "<ANTSIBULL_DOCS_VERSION>"


@contextmanager
def replace_antsibull_version(new_version=ANTSIBULL_DOCS_CI_VERSION):
    with mock.patch(
        "antsibull_docs.__version__",
        new_version,
    ):
        yield


@contextmanager
def change_cwd(directory: str) -> None:
    old_dir = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(old_dir)


@contextmanager
def update_environment(environment: dict[str, str | None]) -> None:
    backup = {}
    for k, v in environment.items():
        if k in os.environ:
            backup[k] = os.environ[k]
        if v is not None:
            os.environ[k] = v
        elif k in os.environ:
            del os.environ[k]
    yield
    for k in environment:
        if k in backup:
            os.environ[k] = backup[k]
        elif k in os.environ:
            del os.environ[k]
