# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def bar(input):
    return False


class TestModule(object):
    def tests(self):
        return {
            "bar": bar,
            "is_bar": bar,
        }
