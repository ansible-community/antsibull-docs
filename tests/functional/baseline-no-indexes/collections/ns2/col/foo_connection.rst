
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

.. _ansible_collections.ns2.col.foo_connection:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

ns2.col.foo connection -- Foo connection
++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This connection plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.foo`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This is for the \ :literal:`foo`\  connection.


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
        <div class="ansibleOptionAnchor" id="parameter-host"></div>

      .. _ansible_collections.ns2.col.foo_connection__parameter-host:

      .. rst-class:: ansible-option-title

      **host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-host" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Hostname to connect to.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"inventory\_hostname"`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Variable: inventory\_hostname

      - Variable: ansible\_host

      - Variable: ansible\_ssh\_host

      - Variable: delegated\_vars['ansible\_host']

      - Variable: delegated\_vars['ansible\_ssh\_host']


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-pipelining"></div>

      .. _ansible_collections.ns2.col.foo_connection__parameter-pipelining:

      .. rst-class:: ansible-option-title

      **pipelining**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-pipelining" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Pipelining reduces the number of connection operations required to execute a module on the remote server, by executing many Ansible modules without actual file transfers.

      This can result in a very significant performance improvement when enabled.

      However this can conflict with privilege escalation (become). For example, when using sudo operations you must first disable 'requiretty' in the sudoers file for the target hosts, which is why this feature is disabled by default.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`false` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entries:

        .. code-block::

          [defaults]
          pipelining = false



        .. code-block::

          [connection]
          pipelining = false


      - Environment variable: ANSIBLE\_PIPELINING

      - Variable: ansible\_pipelining


      .. raw:: html

        </div>


.. Attributes


.. Notes

Notes
-----

.. note::
   - Some note. \ :strong:`Something in bold`\ . \ :literal:`And in code`\ . \ :emphasis:`And in italics`\ . An URL: \ https://example.org\ .
   - And another one. \ `A link <https://example.com>`__\ .

.. Seealso


.. Examples



.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- ansible (@core)


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

