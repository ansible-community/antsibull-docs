
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns.col2.foo4_module:

.. Anchors: short name for ansible.builtin

.. Title

ns.col2.foo4 module -- Markup reference linting test
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ (version 0.0.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ns.col2`.

    To use it in a playbook, specify: :code:`ns.col2.foo4`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description



.. Aliases


.. Requirements






.. Options

Parameters
----------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-correct_array_stubs"></div>

      .. _ansible_collections.ns.col2.foo4_module__parameter-correct_array_stubs:

      .. rst-class:: ansible-option-title

      **correct_array_stubs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-correct_array_stubs" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      \ :ansopt:`ansible.builtin.iptables#module:tcp\_flags.flags[]`\ 

      \ :ansopt:`ns2.col.bar#filter:foo`\ 

      \ :ansopt:`ns2.col.bar#filter:foo[]`\ 

      \ :ansopt:`ext.col.foo#module:foo[baz].bar`\ 

      \ :ansretval:`ext.col.foo#module:baz`\ 

      \ :ansretval:`ext.col.foo#module:baz[ ]`\ 

      \ :ansretval:`ansible.builtin.stat#module:stat[foo.bar]`\ 


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-existing"></div>

      .. _ansible_collections.ns.col2.foo4_module__parameter-existing:

      .. rst-class:: ansible-option-title

      **existing**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-existing" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      \ :ref:`ansible.builtin.service <ansible_collections.ansible.builtin.service_module>`\ 

      \ :ref:`ansible.builtin.pipe <ansible_collections.ansible.builtin.pipe_lookup>`\ 

      \ :ansopt:`ansible.builtin.file#module:state`\ 

      \ :ansretval:`ansible.builtin.stat#module:stat.exists`\ 

      \ :ref:`ns2.flatcol.foo <ansible_collections.ns2.flatcol.foo_module>`\ 

      \ :ref:`ns2.flatcol.sub.foo2 <ansible_collections.ns2.flatcol.sub.foo2_module>`\ 

      \ :ansopt:`ns2.flatcol.foo#module:subbaz.bam`\ 

      \ :ansretval:`ns2.flatcol.sub.foo2#module:bar`\ 

      \ :ref:`ns2.col.foo2 <ansible_collections.ns2.col.foo2_module>`\ 

      \ :ref:`ns2.col.foo <ansible_collections.ns2.col.foo_lookup>`\ 

      \ :ansopt:`ns2.col.bar#filter:foo[-1]`\ 

      \ :ansretval:`ns2.col.bar#test:\_value`\ 

      \ :ref:`ns.col2.foo2 <ansible_collections.ns.col2.foo2_module>`\ 

      \ :ref:`ns.col2.foo2 <ansible_collections.ns.col2.foo2_module>`\ 

      \ :ansopt:`ns.col2.foo2#module:subfoo.foo`\ 

      \ :ansretval:`ns.col2.foo2#module:bar`\ 

      \ :ref:`ext.col.foo <ansible_collections.ext.col.foo_module>`\ 

      \ :ref:`ext.col.bar <ansible_collections.ext.col.bar_lookup>`\ 

      \ :ansopt:`ext.col.foo#module:foo[len(foo)].bar`\ 

      \ :ansretval:`ext.col.foo#module:baz[]`\ 

      \ :ansopt:`ns.col2.foo2#module:subfoo.BaZ`\ 


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-incorrect_array_stubs"></div>

      .. _ansible_collections.ns.col2.foo4_module__parameter-incorrect_array_stubs:

      .. rst-class:: ansible-option-title

      **incorrect_array_stubs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-incorrect_array_stubs" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      \ :ansopt:`ansible.builtin.file#module:state[]`\ 

      \ :ansretval:`ansible.builtin.stat#module:stat[foo.bar].exists`\ 

      \ :ansretval:`ansible.builtin.stat#module:stat.exists[]`\ 

      \ :ansopt:`ns.col2.foo2#module:subfoo[`\ 

      \ :ansretval:`ns.col2.foo2#module:bar[]`\ 

      \ :ansopt:`ext.col.foo#module:foo.bar`\ 


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-not_existing"></div>

      .. _ansible_collections.ns.col2.foo4_module__parameter-not_existing:

      .. rst-class:: ansible-option-title

      **not_existing**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-not_existing" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      \ :ref:`ansible.builtin.foobar <ansible_collections.ansible.builtin.foobar_module>`\ 

      \ :ref:`ansible.builtin.bazbam <ansible_collections.ansible.builtin.bazbam_lookup>`\ 

      \ :ansopt:`ansible.builtin.file#module:foobarbaz`\ 

      \ :ansretval:`ansible.builtin.stat#module:baz.bam[]`\ 

      \ :ansopt:`ansible.builtin.foobar#module:state`\ 

      \ :ansretval:`ansible.builtin.bazbam#module:stat.exists`\ 

      \ :ref:`ns2.flatcol.foobarbaz <ansible_collections.ns2.flatcol.foobarbaz_module>`\ 

      \ :ref:`ns2.flatcol.sub.bazbam <ansible_collections.ns2.flatcol.sub.bazbam_module>`\ 

      \ :ansopt:`ns2.flatcol.foo#module:foofoofoobar`\ 

      \ :ansretval:`ns2.flatcol.sub.foo2#module:bazbarbam`\ 

      \ :ansopt:`ns2.flatcol.foobar#module:subbaz.bam`\ 

      \ :ansretval:`ns2.flatcol.sub.bazbam#module:bar`\ 

      \ :ref:`ns2.col.joo <ansible_collections.ns2.col.joo_module>`\ 

      \ :ref:`ns2.col.joo <ansible_collections.ns2.col.joo_lookup>`\ 

      \ :ansopt:`ns2.col.bar#filter:jooo`\ 

      \ :ansretval:`ns2.col.bar#test:booo`\ 

      \ :ansopt:`ns2.col.joo#filter:foo[-1]`\ 

      \ :ansretval:`ns2.col.joo#test:\_value`\ 

      \ :ref:`ns.col2.foobarbaz <ansible_collections.ns.col2.foobarbaz_module>`\ 

      \ :ref:`ns.col2.foobarbam <ansible_collections.ns.col2.foobarbam_filter>`\ 

      \ :ansopt:`ns.col2.foo2#module:barbazbam.foo`\ 

      \ :ansretval:`ns.col2.foo2#module:bambazbar`\ 

      \ :ansopt:`ns.col2.foofoo#test:subfoo.foo`\ 

      \ :ansretval:`ns.col2.foofoo#lookup:baz`\ 

      \ :ref:`ext.col.notthere <ansible_collections.ext.col.notthere_module>`\ 

      \ :ref:`ext.col.notthere <ansible_collections.ext.col.notthere_lookup>`\ 

      \ :ansopt:`ext.col.foo#module:foo[len(foo)].notthere`\ 

      \ :ansopt:`ext.col.foo#module:notthere[len(notthere)].bar`\ 

      \ :ansretval:`ext.col.foo#module:notthere[]`\ 

      \ :ansopt:`ext.col.notthere#module:foo[len(foo)].bar`\ 

      \ :ansretval:`ext.col.notthere#module:baz[]`\ 


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples



.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Nobody (@ansible)



.. Extra links


.. Parsing errors

