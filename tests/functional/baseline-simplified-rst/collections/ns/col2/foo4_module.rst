

ns.col2.foo4 module -- Markup reference linting test
++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ns.col2 collection <https://galaxy.ansible.com/ns/col2>`_ (version 0.0.1).

To install it, use: :code:`ansible-galaxy collection install ns.col2`.

To use it in a playbook, specify: :code:`ns.col2.foo4`.


.. contents::
   :local:
   :depth: 1


Synopsis
--------









Parameters
----------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-correct_array_stubs:

      **correct_array_stubs**

      :literal:`string`

      .. raw:: html

        </div></div>

    - 
      \ :literal:`tcp\_flags.flags[]` (of module `ansible.builtin.iptables <iptables_module.rst>`__)\ 

      \ :literal:`foo` (of filter plugin `ns2.col.bar <bar_filter.rst>`__)\ 

      \ :literal:`foo[]` (of filter plugin `ns2.col.bar <bar_filter.rst>`__)\ 

      \ :literal:`foo[baz].bar` (of module `ext.col.foo <foo_module.rst>`__)\ 

      \ :literal:`baz` (of module `ext.col.foo <foo_module.rst>`__)\ 

      \ :literal:`baz[ ]` (of module `ext.col.foo <foo_module.rst>`__)\ 



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-existing:

      **existing**

      :literal:`string`

      .. raw:: html

        </div></div>

    - 
      \ `ansible.builtin.service <service_module.rst>`__\ 

      \ `ansible.builtin.pipe <pipe_lookup.rst>`__\ 

      \ :literal:`state` (of module `ansible.builtin.file <file_module.rst>`__)\ 

      \ :literal:`stat.exists` (of module `ansible.builtin.stat <stat_module.rst>`__)\ 

      \ `ns2.flatcol.foo <foo_module.rst>`__\ 

      \ `ns2.flatcol.sub.foo2 <sub.foo2_module.rst>`__\ 

      \ :literal:`subbaz.bam` (of module `ns2.flatcol.foo <foo_module.rst>`__)\ 

      \ :literal:`bar` (of module `ns2.flatcol.sub.foo2 <sub.foo2_module.rst>`__)\ 

      \ `ns2.col.foo2 <foo2_module.rst>`__\ 

      \ `ns2.col.foo <foo_lookup.rst>`__\ 

      \ :literal:`foo[-1]` (of filter plugin `ns2.col.bar <bar_filter.rst>`__)\ 

      \ :literal:`\_value` (of test plugin `ns2.col.bar <bar_test.rst>`__)\ 

      \ `ns.col2.foo2 <foo2_module.rst>`__\ 

      \ `ns.col2.foo2 <foo2_module.rst>`__\ 

      \ :literal:`subfoo.foo` (of module `ns.col2.foo2 <foo2_module.rst>`__)\ 

      \ :literal:`bar` (of module `ns.col2.foo2 <foo2_module.rst>`__)\ 

      \ `ext.col.foo <foo_module.rst>`__\ 

      \ `ext.col.bar <bar_lookup.rst>`__\ 

      \ :literal:`foo[len(foo)].bar` (of module `ext.col.foo <foo_module.rst>`__)\ 

      \ :literal:`baz[]` (of module `ext.col.foo <foo_module.rst>`__)\ 

      \ :literal:`subfoo.BaZ` (of module `ns.col2.foo2 <foo2_module.rst>`__)\ 



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-incorrect_array_stubs:

      **incorrect_array_stubs**

      :literal:`string`

      .. raw:: html

        </div></div>

    - 
      \ :literal:`state[]` (of module `ansible.builtin.file <file_module.rst>`__)\ 

      \ :literal:`stat[foo.bar].exists` (of module `ansible.builtin.stat <stat_module.rst>`__)\ 

      \ :literal:`stat.exists[]` (of module `ansible.builtin.stat <stat_module.rst>`__)\ 

      \ :literal:`subfoo[` (of module `ns.col2.foo2 <foo2_module.rst>`__)\ 

      \ :literal:`bar[]` (of module `ns.col2.foo2 <foo2_module.rst>`__)\ 

      \ :literal:`foo.bar` (of module `ext.col.foo <foo_module.rst>`__)\ 



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-not_existing:

      **not_existing**

      :literal:`string`

      .. raw:: html

        </div></div>

    - 
      \ `ansible.builtin.foobar <foobar_module.rst>`__\ 

      \ `ansible.builtin.bazbam <bazbam_lookup.rst>`__\ 

      \ :literal:`foobarbaz` (of module `ansible.builtin.file <file_module.rst>`__)\ 

      \ :literal:`baz.bam[]` (of module `ansible.builtin.stat <stat_module.rst>`__)\ 

      \ :literal:`state` (of module `ansible.builtin.foobar <foobar_module.rst>`__)\ 

      \ :literal:`stat.exists` (of module `ansible.builtin.bazbam <bazbam_module.rst>`__)\ 

      \ `ns2.flatcol.foobarbaz <foobarbaz_module.rst>`__\ 

      \ `ns2.flatcol.sub.bazbam <sub.bazbam_module.rst>`__\ 

      \ :literal:`foofoofoobar` (of module `ns2.flatcol.foo <foo_module.rst>`__)\ 

      \ :literal:`bazbarbam` (of module `ns2.flatcol.sub.foo2 <sub.foo2_module.rst>`__)\ 

      \ :literal:`subbaz.bam` (of module `ns2.flatcol.foobar <foobar_module.rst>`__)\ 

      \ :literal:`bar` (of module `ns2.flatcol.sub.bazbam <sub.bazbam_module.rst>`__)\ 

      \ `ns2.col.joo <joo_module.rst>`__\ 

      \ `ns2.col.joo <joo_lookup.rst>`__\ 

      \ :literal:`jooo` (of filter plugin `ns2.col.bar <bar_filter.rst>`__)\ 

      \ :literal:`booo` (of test plugin `ns2.col.bar <bar_test.rst>`__)\ 

      \ :literal:`foo[-1]` (of filter plugin `ns2.col.joo <joo_filter.rst>`__)\ 

      \ :literal:`\_value` (of test plugin `ns2.col.joo <joo_test.rst>`__)\ 

      \ `ns.col2.foobarbaz <foobarbaz_module.rst>`__\ 

      \ `ns.col2.foobarbam <foobarbam_filter.rst>`__\ 

      \ :literal:`barbazbam.foo` (of module `ns.col2.foo2 <foo2_module.rst>`__)\ 

      \ :literal:`bambazbar` (of module `ns.col2.foo2 <foo2_module.rst>`__)\ 

      \ :literal:`subfoo.foo` (of test plugin `ns.col2.foofoo <foofoo_test.rst>`__)\ 

      \ :literal:`baz` (of lookup plugin `ns.col2.foofoo <foofoo_lookup.rst>`__)\ 

      \ `ext.col.notthere <notthere_module.rst>`__\ 

      \ `ext.col.notthere <notthere_lookup.rst>`__\ 

      \ :literal:`foo[len(foo)].notthere` (of module `ext.col.foo <foo_module.rst>`__)\ 

      \ :literal:`notthere[len(notthere)].bar` (of module `ext.col.foo <foo_module.rst>`__)\ 

      \ :literal:`notthere[]` (of module `ext.col.foo <foo_module.rst>`__)\ 

      \ :literal:`foo[len(foo)].bar` (of module `ext.col.notthere <notthere_module.rst>`__)\ 

      \ :literal:`baz[]` (of module `ext.col.notthere <notthere_module.rst>`__)\ 












Authors
~~~~~~~

- Nobody (@ansible)




