
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
.. role:: ansible-option-choices-entry
.. role:: ansible-option-default
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.ns2.col.foo_vars:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

ns2.col.foo vars -- Load foo
++++++++++++++++++++++++++++

.. Collection note

.. note::
    This vars plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.
    You need further requirements to be able to use this vars plugin,
    see :ref:`Requirements <ansible_collections.ns2.col.foo_vars_requirements>` for details.

    To use it in a playbook, specify: :code:`ns2.col.foo`.

.. version_added

.. rst-class:: ansible-version-added

New in ns2.col 0.9.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Load some foo.
- This is so glorious.


.. Aliases


.. Requirements

.. _ansible_collections.ns2.col.foo_vars_requirements:

Requirements
------------
The below requirements are needed on the local controller node that executes this vars.

- Enabled in Ansible's configuration.






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
        <div class="ansibleOptionAnchor" id="parameter-_valid_extensions"></div>

      .. _ansible_collections.ns2.col.foo_vars__parameter-_valid_extensions:

      .. rst-class:: ansible-option-title

      **_valid_extensions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-_valid_extensions" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      All extensions to check.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[".foo", ".foobar"]`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [defaults]
          foo_valid_extensions = .foo, .foobar


      - Environment variable: ANSIBLE\_FOO\_FILENAME\_EXT


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-stage"></div>

      .. _ansible_collections.ns2.col.foo_vars__parameter-stage:

      .. rst-class:: ansible-option-title

      **stage**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-stage" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in ansible-base 2.10`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Control when this vars plugin may be executed.

      Setting this option to \ :literal:`all`\  will run the vars plugin after importing inventory and whenever it is demanded by a task.

      Setting this option to \ :literal:`task`\  will only run the vars plugin whenever it is demanded by a task.

      Setting this option to \ :literal:`inventory`\  will only run the vars plugin after parsing inventory.

      If this option is omitted, the global \ :emphasis:`RUN\_VARS\_PLUGINS`\  configuration is used to determine when to execute the vars plugin.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"all"`
      - :ansible-option-choices-entry:`"task"`
      - :ansible-option-choices-entry:`"inventory"`


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


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/ansible-collections/community.general/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/ansible-collections/community.crypto" aria-role="button" target="_blank" rel="noopener external">Homepage</a>
    <a href="https://github.com/ansible-collections/community.internal_test_tools" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

