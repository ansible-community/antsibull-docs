#!/usr/bin/python
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os
import sys


root = os.path.join(os.getcwd(), 'collections')
data = json.load(sys.stdin)
result = {}
for path, collections in data.items():
    rel_root = os.path.relpath(path, root)
    if rel_root.startswith('.'):
        raise Exception(f'Cannot sanitize {doc[key]}')
    result[rel_root] = collections
json.dump(result, sys.stdout, indent=1, sort_keys=True)
