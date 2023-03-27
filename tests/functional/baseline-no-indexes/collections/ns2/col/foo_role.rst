
.. Document meta

:orphan:
:github_url: https://github.com/ansible-community/antsibull-docs/edit/main/tests/functional/collections/ansible_collections/ns2/col/roles/foo/meta/argument_specs.yml?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

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

.. Anchors

.. _ansible_collections.ns2.col.foo_role:

.. Anchors: aliases


.. Title

ns2.col.foo role -- Foo role
++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

    To install it use: :code:`ansible-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.foo`.

.. contents::
   :local:
   :depth: 2


.. Entry point title

Entry point ``main`` -- Foo role
--------------------------------

.. version_added

.. rst-class:: ansible-version-added

New in ns2.col 0.2.0

.. Deprecated


Synopsis
^^^^^^^^

.. Description

- This is the foo role.
- If you set \ :ansopt:`ns2.col.foo#role:main:foo\_param\_1`\  while \ :ansopt:`ns2.col.foo#role:main:foo\_param\_2=3`\ , this might behave funny.

.. Requirements


.. Options

Parameters
^^^^^^^^^^

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--foo_param_1"></div>

      .. _ansible_collections.ns2.col.foo_role__parameter-main__foo_param_1:

      .. rst-class:: ansible-option-title

      **foo_param_1**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--foo_param_1" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A string parameter

      If you set \ :ansopt:`ns2.col.foo#role:main:foo\_param\_1`\  while \ :ansopt:`ns2.col.foo#role:main:foo\_param\_2=3`\ , this might behave funny.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--foo_param_2"></div>

      .. _ansible_collections.ns2.col.foo_role__parameter-main__foo_param_2:

      .. rst-class:: ansible-option-title

      **foo_param_2**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--foo_param_2" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      An integer parameter with a default.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`13`

      .. raw:: html

        </div>


.. Attributes


Attributes
----------

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Attribute
    - Support
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="attribute-check_mode"></div>

      .. _ansible_collections.ns2.col.foo_role__attribute-check_mode:

      .. rst-class:: ansible-option-title

      **check_mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#attribute-check_mode" title="Permalink to this attribute"></a>

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-label:`Support: \ `\ :ansible-attribute-support-full:`full`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Can run in check\_mode and return changed status prediction without modifying target


      .. raw:: html

        </div>



.. Notes


.. Seealso

See Also
^^^^^^^^

.. seealso::

   \ :ref:`ns2.col.foo <ansible_collections.ns2.col.foo_module>`\ 
       The official documentation on the **ns2.col.foo** module.

Authors
^^^^^^^

- Felix Fontein (@felixfontein)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/ansible-collections/community.general/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/ansible-collections/community.crypto" aria-role="button" target="_blank" rel="noopener external">Homepage</a>
    <a href="https://github.com/ansible-collections/community.internal_test_tools" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
    <a href="https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&amp;labels=&amp;template=bug_report.md" aria-role="button" target="_blank" rel="noopener external">Submit a bug report</a>
    <a href="./#communication-for-ns2-col" aria-role="button" target="_blank">Communication</a>
  </p>

.. Parsing errors

