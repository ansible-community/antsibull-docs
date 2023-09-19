
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns.col2.foo3_module:

.. Anchors: short name for ansible.builtin

.. Title

ns.col2.foo3 module -- Foo III
++++++++++++++++++++++++++++++

.. ansible-plugin::

  fqcn: ns.col2.foo3
  plugin_type: module
  short_description: "Foo III"

.. Collection note

.. note::
    This module is part of the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ (version 0.0.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ns.col2`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.ns.col2.foo3_module_requirements>` for details.

    To use it in a playbook, specify: :code:`ns.col2.foo3`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Does some foo on the remote host.


.. Aliases


.. Requirements

Requirements
------------

.. ansible-requirements-anchor::

  fqcn: ns.col2.foo3
  plugin_type: module

The below requirements are needed on the host that executes this module.

- Foo.






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

      .. ansible-option::

        fqcn: ns.col2.foo3
        plugin_type: module
        name: "bar"
        full_keys:
          - ["bar"]

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Bar.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">

      .. ansible-option::

        fqcn: ns.col2.foo3
        plugin_type: module
        name: "foo"
        full_keys:
          - ["foo"]

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The foo source.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">

      .. ansible-option::

        fqcn: ns.col2.foo3
        plugin_type: module
        name: "subfoo"
        full_keys:
          - ["subfoo"]

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Some recursive foo.


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. ansible-option::

        fqcn: ns.col2.foo3
        plugin_type: module
        name: "foo"
        full_keys:
          - ["subfoo", "foo"]

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A sub foo.

      Whatever.

      Also required when \ :emphasis:`subfoo`\  is specified when \ :emphasis:`foo=bar`\  or \ :literal:`baz`\ .


      .. raw:: html

        </div>



.. Attributes


Attributes
----------

.. tabularcolumns:: \X{2}{10}\X{3}{10}\X{5}{10}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Attribute
    - Support
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">

      .. ansible-attribute::

        fqcn: ns.col2.foo3
        plugin_type: module
        name: "check_mode"

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


  * - .. raw:: html

        <div class="ansible-option-cell">

      .. ansible-attribute::

        fqcn: ns.col2.foo3
        plugin_type: module
        name: "diff_mode"

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-label:`Support: \ `\ :ansible-attribute-support-full:`full`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">

      .. ansible-attribute::

        fqcn: ns.col2.foo3
        plugin_type: module
        name: "platform"

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-property:`Platform:` |antsibull-internal-nbsp|:ansible-attribute-support-full:`posix`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Target OS/families that can be operated against


      .. raw:: html

        </div>



.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    This is not YAML.




.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Someone else (@ansible)



.. Extra links


.. Parsing errors

There were some errors parsing the documentation for this plugin.  Please file a bug with the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_.

The errors were:

* ::

        Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema
        return -> bar -> type
          string does not match regex "^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$)
        return -> baz
          value is not a valid dict (type=type_error.dict)

