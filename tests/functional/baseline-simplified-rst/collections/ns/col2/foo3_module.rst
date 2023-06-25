

ns.col2.foo3 module -- Foo III
++++++++++++++++++++++++++++++

.. note::
    This module is part of the `ns.col2 collection <https://galaxy.ansible.com/ns/col2>`_ (version 0.0.1).

    To install it, use: :code:`ansible-galaxy collection install ns.col2`.
    You need further requirements to be able to use this module,
    see `Requirements <ansible_collections.ns.col2.foo3_module_requirements_>`_ for details.

    To use it in a playbook, specify: :code:`ns.col2.foo3`.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Does some foo on the remote host.



.. _ansible_collections.ns.col2.foo3_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- Foo.






Parameters
----------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-bar:

      **bar**

      :literal:`list` / :literal:`elements=integer`

      .. raw:: html

        </div></div>

    - 
      Bar.



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-foo:

      **foo**

      :literal:`string`

      .. raw:: html

        </div></div>

    - 
      The foo source.



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-subfoo:

      **subfoo**

      :literal:`dictionary`

      .. raw:: html

        </div></div>

    - 
      Some recursive foo.


    
  * - .. raw:: html

        <div style="display: flex;"><div style="margin-left: 2em; border-right: 1px solid #000000;"></div><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-subfoo/foo:

      **foo**

      :literal:`string` / :strong:`required`

      .. raw:: html

        </div></div>

    - 
      A sub foo.

      Whatever.

      Also required when \ :emphasis:`subfoo`\  is specified when \ :emphasis:`foo=bar`\  or \ :literal:`baz`\ .






Attributes
----------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Attribute
    - Support
    - Description

  * - .. _ansible_collections.ns.col2.foo3_module__attribute-check_mode:

      **check_mode**

    - 
      Support: full



    - 
      Can run in check\_mode and return changed status prediction without modifying target



  * - .. _ansible_collections.ns.col2.foo3_module__attribute-diff_mode:

      **diff_mode**

    - 
      Support: full



    - 
      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode



  * - .. _ansible_collections.ns.col2.foo3_module__attribute-platform:

      **platform**

    - 
      Platform:posix


    - 
      Target OS/families that can be operated against






Examples
--------

.. code-block:: yaml+jinja

    
    This is not YAML.







Authors
~~~~~~~

- Someone else (@ansible)




There were some errors parsing the documentation for this plugin.  Please file a bug with the `ns.col2 collection <https://galaxy.ansible.com/ns/col2>`_.

The errors were:

* ::

        Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema
        return -> bar -> type
          string does not match regex "^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$)
        return -> baz
          value is not a valid dict (type=type_error.dict)

