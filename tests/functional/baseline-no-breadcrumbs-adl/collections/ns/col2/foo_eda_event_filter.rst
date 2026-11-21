.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns.col2.foo_eda_event_filter:

.. Anchors: short name for ansible.builtin

.. Title

ns.col2.foo event filter -- Do fancy stuff
++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This EDA event filter plugin is part of the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ (version 0.0.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install ns.col2`.

    To use it in a playbook, specify: :code:`ns.col2.foo`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This is some fancy filter.


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
        <div class="ansibleOptionAnchor" id="parameter-foobar"></div>

      .. _ansible_collections.ns.col2.foo_eda_event_filter__parameter-foobar:

      .. rst-class:: ansible-option-title

      **foobar**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-foobar" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Something.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - ns.col2.bar:
      filters:
        - ns.col2.foo:
            overwrite: false



.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors


.. Extra links


.. Parsing errors
