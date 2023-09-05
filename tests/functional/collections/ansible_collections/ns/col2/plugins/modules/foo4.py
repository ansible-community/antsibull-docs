#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: foo4
author:
    - "Nobody (@ansible)"
short_description: Markup reference linting test
description: []
options:
    existing:
        description:
            - M(ansible.builtin.service)
            - P(ansible.builtin.pipe#lookup)
            - O(ansible.builtin.file#module:state)
            - RV(ansible.builtin.stat#module:stat.exists)
            - M(ns2.flatcol.foo)
            - P(ns2.flatcol.sub.foo2#module)
            - O(ns2.flatcol.foo#module:subbaz.bam)
            - RV(ns2.flatcol.sub.foo2#module:bar)
            - M(ns2.col.foo2)
            - P(ns2.col.foo#lookup)
            - O(ns2.col.bar#filter:foo[-1])
            - RV(ns2.col.bar#test:_value)
            - M(ns.col2.foo2)
            - P(ns.col2.foo2#module)
            - O(ns.col2.foo2#module:subfoo.foo)
            - RV(ns.col2.foo2#module:bar)
            - M(ext.col.foo)
            - P(ext.col.bar#lookup)
            - O(ext.col.foo#module:foo[len(foo\)].bar)
            - RV(ext.col.foo#module:baz[])
            - O(ns.col2.foo2#module:subfoo.BaZ)
    not_existing:
        description:
            - M(ansible.builtin.foobar)
            - P(ansible.builtin.bazbam#lookup)
            - O(ansible.builtin.file#module:foobarbaz)
            - RV(ansible.builtin.stat#module:baz.bam[])
            - O(ansible.builtin.foobar#module:state)
            - RV(ansible.builtin.bazbam#module:stat.exists)
            - M(ns2.flatcol.foobarbaz)
            - P(ns2.flatcol.sub.bazbam#module)
            - O(ns2.flatcol.foo#module:foofoofoobar)
            - RV(ns2.flatcol.sub.foo2#module:bazbarbam)
            - O(ns2.flatcol.foobar#module:subbaz.bam)
            - RV(ns2.flatcol.sub.bazbam#module:bar)
            - M(ns2.col.joo)
            - P(ns2.col.joo#lookup)
            - O(ns2.col.bar#filter:jooo)
            - RV(ns2.col.bar#test:booo)
            - O(ns2.col.joo#filter:foo[-1])
            - RV(ns2.col.joo#test:_value)
            - M(ns.col2.foobarbaz)
            - P(ns.col2.foobarbam#filter)
            - O(ns.col2.foo2#module:barbazbam.foo)
            - RV(ns.col2.foo2#module:bambazbar)
            - O(ns.col2.foofoo#test:subfoo.foo)
            - RV(ns.col2.foofoo#lookup:baz)
            - M(ext.col.notthere)
            - P(ext.col.notthere#lookup)
            - O(ext.col.foo#module:foo[len(foo\)].notthere)
            - O(ext.col.foo#module:notthere[len(notthere\)].bar)
            - RV(ext.col.foo#module:notthere[])
            - O(ext.col.notthere#module:foo[len(foo\)].bar)
            - RV(ext.col.notthere#module:baz[])
    correct_array_stubs:
        description:
            - O(ansible.builtin.iptables#module:tcp_flags.flags[])
            - O(ns2.col.bar#filter:foo)
            - O(ns2.col.bar#filter:foo[])
            - O(ext.col.foo#module:foo[baz].bar)
            - RV(ext.col.foo#module:baz)
            - RV(ext.col.foo#module:baz[ ])
            - RV(ansible.builtin.stat#module:stat[foo.bar])
    incorrect_array_stubs:
        description:
            - O(ansible.builtin.file#module:state[])
            - RV(ansible.builtin.stat#module:stat[foo.bar].exists)
            - RV(ansible.builtin.stat#module:stat.exists[])
            - O(ns.col2.foo2#module:subfoo[)
            - RV(ns.col2.foo2#module:bar[])
            - O(ext.col.foo#module:foo.bar)
"""

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(existing=dict(), not_existing=dict()),
        supports_check_mode=True,
    )
    module.exit_json(bar="baz")


if __name__ == "__main__":
    main()
