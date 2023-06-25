

ns2.flatcol.foo2 module -- Another foo
++++++++++++++++++++++++++++++++++++++

.. note::
    This module is part of the `ns2.flatcol collection <https://galaxy.ansible.com/ns2/flatcol>`_.

    To install it, use: :code:`ansible-galaxy collection install ns2.flatcol`.

    To use it in a playbook, specify: :code:`ns2.flatcol.foo2`.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Foo bar.
- See \ :literal:`foo\_param\_1` (of role `ns2.flatcol.foo <foo_role.rst>`__, entrypoint main)\  for a random role parameter reference. And \ :literal:`foo\_param\_2=42` (of role `ns2.flatcol.foo <foo_role.rst>`__, entrypoint main)\  for one with a value.








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

      See \ :literal:`foo\_param\_1` (of role `ns2.flatcol.foo <foo_role.rst>`__, entrypoint main)\  for a random role parameter reference. And \ :literal:`foo\_param\_2=42` (of role `ns2.flatcol.foo <foo_role.rst>`__, entrypoint main)\  for one with a value.







Examples
--------

.. code-block:: yaml+jinja

    
    - name: Do some foo
      ns2.flatcol.foo2:
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




