

ns2.col.foo2 module -- Another foo
++++++++++++++++++++++++++++++++++

This module is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.foo2`.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Foo bar.
- See \ :literal:`foo\_param\_1` (of role `ns2.col.foo <foo_role.rst>`__, entrypoint main)\  for a random role parameter reference. And \ :literal:`foo\_param\_2=42` (of role `ns2.col.foo <foo_role.rst>`__, entrypoint main)\  for one with a value.
- Reference using alias - \ :literal:`bar` (of module `ns2.col.foo\_redirect <foo_redirect_module.rst>`__)\  and \ :literal:`baz` (of module `ns2.col.foo\_redirect <foo_redirect_module.rst>`__)\ .








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

      :literal:`string`

      .. raw:: html

        </div></div>

    - 
      Some bar.

      See \ :literal:`foo\_param\_1` (of role `ns2.col.foo <foo_role.rst>`__, entrypoint main)\  for a random role parameter reference. And \ :literal:`foo\_param\_2=42` (of role `ns2.col.foo <foo_role.rst>`__, entrypoint main)\  for one with a value.





Attributes
----------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Attribute
    - Support
    - Description

  * - .. _ansible_collections.ns2.col.foo2_module__attribute-action_group:

      **action_group**

    - 
      Action groups: \ns2.col.bar\_group, ns2.col.foo\_group


    - 
      Use \ :literal:`group/ns2.col.foo\_group`\  or \ :literal:`group/ns2.col.bar\_group`\  in \ :literal:`module\_defaults`\  to set defaults for this module.



  * - .. _ansible_collections.ns2.col.foo2_module__attribute-check_mode:

      **check_mode**

    - 
      Support: full



    - 
      Can run in check\_mode and return changed status prediction without modifying target



  * - .. _ansible_collections.ns2.col.foo2_module__attribute-diff_mode:

      **diff_mode**

    - 
      Support: N/A



    - 
      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode



  * - .. _ansible_collections.ns2.col.foo2_module__attribute-platform:

      **platform**

    - 
      Platform:posix


    - 
      Target OS/families that can be operated against






Examples
--------

.. code-block:: yaml

    
    - name: Do some foo
      ns2.col.foo2:
        bar: foo





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

- Another one (@ansible-community)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

