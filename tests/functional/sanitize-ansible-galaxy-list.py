#!/usr/bin/python
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import os
import sys

root = os.path.join(os.getcwd(), "collections")
other_root = os.path.join(os.getcwd(), "other-collections")
data = json.load(sys.stdin)
result = {}
for path, collections in data.items():
    rel_root = os.path.relpath(path, root)
    if rel_root.startswith(".") and not rel_root.startswith("../other-collections/"):
        raise Exception(f"Cannot sanitize {doc[key]}")
    result[rel_root] = collections
json.dump(result, sys.stdout, indent=1, sort_keys=True)
