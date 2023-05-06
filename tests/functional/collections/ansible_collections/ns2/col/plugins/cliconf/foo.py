# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
author: "Felix Fontein (@felixfontein) <felix@fontein.de>"
name: foo
short_description: Foo router CLI config
description:
  - This is a CLI config for foo routers. Whatever these are.
"""

from ansible.plugins.cliconf import CliconfBase


class Cliconf(CliconfBase):
    pass
