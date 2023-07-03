

ns2.col.foo connection -- Foo connection \ :literal:`bar` (`link <parameter-bar_>`_)\ 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This connection plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.foo`.

New in ns2.col 1.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This is for the \ :literal:`foo`\  connection.








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

      :literal:`integer`




      .. raw:: html

        </div></div>

    - 
      Foo bar.



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-host:

      **host**

      :literal:`string`




      .. raw:: html

        </div></div>

    - 
      Hostname to connect to.


      Default: :literal:`"inventory\_hostname"`

      Configuration:

      - Variable: inventory\_hostname

      - Variable: ansible\_host

      - Variable: ansible\_ssh\_host

      - Variable: delegated\_vars['ansible\_host']

      - Variable: delegated\_vars['ansible\_ssh\_host']





Notes
-----

- Some note. \ :strong:`Something in bold`\ . \ :literal:`And in code`\ . \ :emphasis:`And in italics`\ . An URL: \ https://example.org\ .
- And another one. \ `A link <https://example.com>`__\ .







Authors
~~~~~~~

- ansible (@core)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

