
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-default-mark
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.ns2.flatcol.foo_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

ns2.flatcol.foo module -- Do some foo \ :ansopt:`ns2.flatcol.foo#module:bar`\ 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ns2.flatcol collection <https://galaxy.ansible.com/ns2/flatcol>`_.

    To install it, use: :code:`ansible-galaxy collection install ns2.flatcol`.

    To use it in a playbook, specify: :code:`ns2.flatcol.foo`.

.. version_added

.. rst-class:: ansible-version-added

New in ns2.flatcol 2.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Does some foo on the remote host.
- Whether foo is magic or not has not yet been determined.


.. Aliases


.. Requirements






.. Options

Parameters
----------

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-bar"></div>
        <div class="ansibleOptionAnchor" id="parameter-baz"></div>

      .. _ansible_collections.ns2.flatcol.foo_module__parameter-bar:
      .. _ansible_collections.ns2.flatcol.foo_module__parameter-baz:

      .. rst-class:: ansible-option-title

      **bar**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-aliases:`aliases: baz`

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A bar.

      Independent from \ :ansopt:`ns2.flatcol.foo#module:foo`\ .

      Do not confuse with \ :ansretval:`ns2.flatcol.foo#module:bar`\ .


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-foo"></div>

      .. _ansible_collections.ns2.flatcol.foo_module__parameter-foo:

      .. rst-class:: ansible-option-title

      **foo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-foo" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The foo source.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-subfoo"></div>

      .. _ansible_collections.ns2.flatcol.foo_module__parameter-subfoo:

      .. rst-class:: ansible-option-title

      **subfoo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subfoo" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      :ansible-option-versionadded:`added in ns2.flatcol 2.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Some recursive foo.


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-subfoo/foo"></div>

      .. _ansible_collections.ns2.flatcol.foo_module__parameter-subfoo/foo:

      .. rst-class:: ansible-option-title

      **foo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subfoo/foo" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A sub foo.

      Whatever.

      Also required when \ :ansopt:`ns2.flatcol.foo#module:subfoo`\  is specified when \ :ansopt:`ns2.flatcol.foo#module:foo=bar`\  or \ :ansval:`baz`\ .


      .. raw:: html

        </div>



.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: Do some foo
      ns2.flatcol.foo:
        foo: '{{ foo }}'
        bar:
          - 1
          - 2
          - 3
        subfoo:
          foo: hoo!




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-bar"></div>

      .. _ansible_collections.ns2.flatcol.foo_module__return-bar:

      .. rst-class:: ansible-option-title

      **bar**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-bar" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Some bar.

      Referencing myself as \ :ansretval:`ns2.flatcol.foo#module:bar`\ .

      Do not confuse with \ :ansopt:`ns2.flatcol.foo#module:bar`\ .


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"baz"`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Ansible Core Team
- Someone else (@ansible)



.. Extra links


.. Parsing errors

