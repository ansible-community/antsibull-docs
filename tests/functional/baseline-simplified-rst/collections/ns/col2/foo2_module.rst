

ns.col2.foo2 module -- Foo two
++++++++++++++++++++++++++++++

.. note::
    This module is part of the `ns.col2 collection <https://galaxy.ansible.com/ns/col2>`_ (version 0.0.1).

    To install it, use: :code:`ansible-galaxy collection install ns.col2`.
    You need further requirements to be able to use this module,
    see `Requirements <ansible_collections.ns.col2.foo2_module_requirements_>`_ for details.

    To use it in a playbook, specify: :code:`ns.col2.foo2`.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Does some foo on the remote host.
- A broken reference \ :ref:`asdfasdfoobarTHISDOESNOTEXIST <asdfasdfoobarTHISDOESNOTEXIST>`\ .
- The option \ :literal:`foo` (`link <parameter-foo_>`_)\  exists, but \ :literal:`foobar` (`link <parameter-foobar_>`_)\  does not.
- The return value \ :literal:`bar` (`link <return-bar_>`_)\  exists, but \ :literal:`barbaz` (`link <return-barbaz_>`_)\  does not.
- Again existing: \ :literal:`foo=1` (of module `ns.col2.foo <foo_module.rst>`__)\ , \ :literal:`bar=2` (of module `ns.col2.foo <foo_module.rst>`__)\ 
- Again not existing: \ :literal:`foobar=1` (of module `ns.col2.foo <foo_module.rst>`__)\ , \ :literal:`barbaz=2` (of module `ns.col2.foo <foo_module.rst>`__)\ 



.. _ansible_collections.ns.col2.foo2_module_requirements:

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

      Some \ :literal:`broken markup` (`link <parameter-broken markup_>`_)\ .



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

      .. _parameter-subfoo/baz:

      **BaZ**

      :literal:`integer`

      .. raw:: html

        </div></div>

    - 
      Funky.



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

      \ :literal:`foobarbaz` (`link <return-foobarbaz_>`_)\  does not exist.






Attributes
----------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Attribute
    - Support
    - Description

  * - .. _ansible_collections.ns.col2.foo2_module__attribute-check_mode:

      **check_mode**

    - 
      Support: full



    - 
      Can run in check\_mode and return changed status prediction without modifying target



  * - .. _ansible_collections.ns.col2.foo2_module__attribute-diff_mode:

      **diff_mode**

    - 
      Support: full



    - 
      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode



  * - .. _ansible_collections.ns.col2.foo2_module__attribute-platform:

      **platform**

    - 
      Platform:posix

      The module \ :strong:`ERROR while parsing`\ : While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN\  is not using an FQCN.

      Sometimes our markup is \ :strong:`ERROR while parsing`\ : While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter\ 


    - 
      Target OS/families that can be operated against





See Also
--------

* \ `ns.col2.foo3 <foo3_module.rst>`__\ 

  Foo III.
* \ `ns.col2.foobarbaz <foobarbaz_module.rst>`__\ 

  The official documentation on the **ns.col2.foobarbaz** module.
* \ `ns.col2.foo4 <foo4_module.rst>`__\  module plugin

  Markup reference linting test.
* \ `ns.col2.foobarbaz <foobarbaz_inventory.rst>`__\  inventory plugin

  The official documentation on the **ns.col2.foobarbaz** inventory plugin.
* \ `ansible.builtin.service <service_module.rst>`__\ 

  The service module.
* \ `ansible.builtin.foobarbaz <foobarbaz_module.rst>`__\ 

  A non-existing module.
* \ `ansible.builtin.linear <linear_strategy.rst>`__\  strategy plugin

  The linear strategy plugin.
* \ `ansible.builtin.foobarbaz <foobarbaz_strategy.rst>`__\  strategy plugin

  A non-existing stragey plugin

Examples
--------

.. code-block:: yaml+jinja

    
    name: This is YAML.





Return Values
-------------
The following are the fields unique to this module:

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _return-bar:

      **bar**

      :literal:`string`

      .. raw:: html

        </div></div>
    - 
      Some bar.


      Returned: success

      Sample: :literal:`"baz"`




Authors
~~~~~~~

- Someone else (@ansible)




