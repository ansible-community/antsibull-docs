#!/usr/bin/env python
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys

from utils import ANTSIBULL_DOCS_CI_VERSION

import antsibull_docs
from antsibull_docs.cli.antsibull_docs import main

if __name__ == "__main__":
    antsibull_docs.__version__ = ANTSIBULL_DOCS_CI_VERSION
    sys.exit(main())
