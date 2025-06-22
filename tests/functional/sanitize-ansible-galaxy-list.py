#!/usr/bin/python
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import os
import sys

import ansible

root = os.path.join(os.getcwd(), "collections")
ansible_root = os.path.dirname(ansible.__file__)
other_root = os.path.join(os.getcwd(), "other-collections")
data = json.load(sys.stdin)
result = {}
for path, collections in data.items():
    rel_ansible_root = os.path.relpath(path, ansible_root)
    if not rel_ansible_root.startswith("."):
        # Skip ansible._protomatter and other things that are part of ansible-core
        continue
    rel_root = os.path.relpath(path, root)
    if rel_root.startswith(".") and not rel_root.startswith("../other-collections/"):
        raise Exception(f"Cannot sanitize {path!r} w.r.t. {root!r}; got {rel_root!r}")
    result[rel_root] = collections
json.dump(result, sys.stdout, indent=1, sort_keys=True)
