# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

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
