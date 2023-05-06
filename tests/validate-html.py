#!/usr/bin/python3
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import sys

import html5lib

errors = 0
for path in sys.argv[1:]:
    for dirname, _, files in os.walk(path):
        for file in files:
            if not file.endswith(".html"):
                continue
            path = os.path.join(dirname, file)
            try:
                parser = html5lib.HTMLParser(strict=True)
                with open(path, "rb") as f:
                    document = parser.parse(f)
            except Exception as e:
                errors += 1
                print(f"{path}: {e}")

if errors > 0:
    print(f"Found {errors} errors!")
    sys.exit(1)
