#!/usr/bin/python
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import ansible
import json
import os
import sys


root = os.path.join(os.getcwd(), 'collections')
ansible_root = os.path.dirname(ansible.__file__)
data = json.load(sys.stdin)
for plugin_type, plugins in data['all'].items():
    for plugin_fqcn, plugin_data in list(plugins.items()):
        if plugin_fqcn.startswith('ansible.builtin.'):
            del plugins[plugin_fqcn]
        for (doc_key, key) in [
            ('doc', 'filename'),
            ('', 'path'),
        ]:
            doc = plugin_data
            if doc_key:
                if doc_key not in doc:
                    continue
                doc = doc[doc_key]
            if key in doc:
                rel_root = os.path.relpath(doc[key], root)
                rel_ansible = os.path.relpath(doc[key], ansible_root)
                if not rel_root.startswith('.'):
                    doc[key] = os.path.join(rel_root)
                elif not rel_ansible.startswith('.'):
                    doc[key] = os.path.join('/ansible', rel_ansible)
                else:
                    raise Exception(f'Cannot sanitize {doc[key]}')
json.dump(data, sys.stdout, indent=1, sort_keys=True)
