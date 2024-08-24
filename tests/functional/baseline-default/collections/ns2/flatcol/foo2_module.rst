.. Document meta

:orphan:
:github_url: https://github.com/ansible-collections/community.REPO_NAME/edit/main/plugins/modules/sub/foo2.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns2.flatcol.foo2_module:

.. Anchors: short name for ansible.builtin

.. Title

ns2.flatcol.foo2 module -- Another foo
++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ns2.flatcol collection <https://galaxy.ansible.com/ui/repo/published/ns2/flatcol/>`_.

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ns2.flatcol`.

    To use it in a playbook, specify: :code:`ns2.flatcol.foo2`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Foo bar.
- See :ansopt:`ns2.flatcol.foo#role:main:foo\_param\_1` for a random role parameter reference. And :ansopt:`ns2.flatcol.foo#role:main:foo\_param\_2=42` for one with a value.


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
        <div class="ansibleOptionAnchor" id="parameter-bar"></div>

      .. _ansible_collections.ns2.flatcol.foo2_module__parameter-bar:

      .. rst-class:: ansible-option-title

      **bar**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Some bar.

      See :ansopt:`ns2.flatcol.foo#role:main:foo\_param\_1` for a random role parameter reference. And :ansopt:`ns2.flatcol.foo#role:main:foo\_param\_2=42` for one with a value.


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
      ns2.flatcol.foo2:
        bar: foo



.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-bar"></div>

      .. _ansible_collections.ns2.flatcol.foo2_module__return-bar:

      .. rst-class:: ansible-option-title

      **bar**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-bar" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Some bar.

      Referencing myself as :ansretval:`ns2.flatcol.foo2#module:bar`.

      Do not confuse with :ansopt:`ns2.flatcol.foo2#module:bar`.


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

- Another one (@ansible-community)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Report an issue"
    url: "https://github.com/ansible-collections/community.REPO_NAME/issues/new/choose"
    external: true
  - title: Communication
    ref: communication_for_ns2.flatcol


.. Parsing errors
