

ns2.col.foo module -- Do some foo \ :literal:`bar` (`link <parameter-bar_>`_)\ 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ns2.col.foo_module_requirements_>`_ for details.

To use it in a playbook, specify: :code:`ns2.col.foo`.

New in ns2.col 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Does some foo on the remote host.
- Whether foo is magic or not has not yet been determined.
- \ :literal:`FOOBAR1`\ , \ :literal:`FOOBAR2`\ , \ :literal:`FOOBAR3`\ , \ :literal:`FOOBAR4`\ .


Aliases: foo_redirect

.. _ansible_collections.ns2.col.foo_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- Foo on remote.






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
      .. _parameter-baz:

      **bar**

      aliases: baz

      :literal:`list` / :literal:`elements=integer`

      .. raw:: html

        </div></div>

    - 
      A bar.

      Independent from \ :literal:`foo` (`link <parameter-foo_>`_)\ .

      Do not confuse with \ :literal:`bar` (`link <return-bar_>`_)\ .



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-foo:

      **foo**

      :literal:`string` / :strong:`required`

      .. raw:: html

        </div></div>

    - 
      The foo source.



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-subfoo:

      **subfoo**

      :literal:`dictionary`

      added in ns2.col 2.0.0


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

      Also required when \ :literal:`subfoo` (`link <parameter-subfoo_>`_)\  is specified when \ :literal:`foo=bar` (`link <parameter-foo_>`_)\  or \ :literal:`baz`\ .






Attributes
----------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Attribute
    - Support
    - Description

  * - .. _ansible_collections.ns2.col.foo_module__attribute-action_group:

      **action_group**

    - 
      Action group: \ns2.col.foo\_group


    - 
      Use \ :literal:`group/ns2.col.foo\_group`\  in \ :literal:`module\_defaults`\  to set defaults for this module.



  * - .. _ansible_collections.ns2.col.foo_module__attribute-check_mode:

      **check_mode**

    - 
      Support: full



    - 
      Can run in check\_mode and return changed status prediction without modifying target



  * - .. _ansible_collections.ns2.col.foo_module__attribute-diff_mode:

      **diff_mode**

    - 
      Support: full



    - 
      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode



  * - .. _ansible_collections.ns2.col.foo_module__attribute-platform:

      **platform**

    - 
      Platform:posix


    - 
      Target OS/families that can be operated against





See Also
--------

* \ `ns2.col.foo2 <foo2_module.rst>`__\ 

  Another foo.
* \ `ns2.col.foo <foo_lookup.rst>`__\  lookup plugin

  Look up some foo \ :literal:`bar` (`link <parameter-bar_>`_)\ .
* \ `ansible.builtin.service <service_module.rst>`__\ 

  The service module.
* \ `ansible.builtin.ssh <ssh_connection.rst>`__\  connection plugin

  The ssh connection plugin.

Examples
--------

.. code-block:: yaml

    
    - name: Do some foo
      ns2.col.foo:
        foo: '{{ foo }}'
        bar:
          - 1
          - 2
          - 3
        subfoo:
          foo: hoo!





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

      Referencing myself as \ :literal:`bar` (`link <return-bar_>`_)\ .

      Do not confuse with \ :literal:`bar` (`link <parameter-bar_>`_)\ .


      Returned: success

      Sample: :literal:`"baz"`




Authors
~~~~~~~

- Ansible Core Team
- Someone else (@ansible)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

