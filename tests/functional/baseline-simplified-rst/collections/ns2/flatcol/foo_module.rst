

ns2.flatcol.foo module -- Do some foo \ :literal:`bar` (`link <parameter-bar_>`_)\ 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ns2.flatcol collection <https://galaxy.ansible.com/ns2/flatcol>`_.

To install it, use: :code:`ansible-galaxy collection install ns2.flatcol`.

To use it in a playbook, specify: :code:`ns2.flatcol.foo`.

New in ns2.flatcol 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Does some foo on the remote host.
- Whether foo is magic or not has not yet been determined.








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

      .. _parameter-subbaz:
      .. _parameter-subfoo:

      **subfoo**

      aliases: subbaz

      :literal:`dictionary`

      added in ns2.flatcol 2.0.0


      .. raw:: html

        </div></div>

    - 
      Some recursive foo.


    
  * - .. raw:: html

        <div style="display: flex;"><div style="margin-left: 2em; border-right: 1px solid #000000;"></div><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-subbaz/bam:
      .. _parameter-subbaz/foo:
      .. _parameter-subfoo/bam:
      .. _parameter-subfoo/foo:

      **foo**

      aliases: bam

      :literal:`string` / :strong:`required`

      .. raw:: html

        </div></div>

    - 
      A sub foo.

      Whatever.

      Also required when \ :literal:`subfoo` (`link <parameter-subfoo_>`_)\  is specified when \ :literal:`foo=bar` (`link <parameter-foo_>`_)\  or \ :literal:`baz`\ .

      Note that \ :literal:`subfoo.foo` (`link <parameter-subfoo/foo_>`_)\  is the same as \ :literal:`subbaz.foo` (`link <parameter-subbaz/foo_>`_)\ , \ :literal:`subbaz.bam` (`link <parameter-subbaz/bam_>`_)\ , and \ :literal:`subfoo.bam` (`link <parameter-subfoo/bam_>`_)\ .

      \ :literal:`FOOBAR1`\ , \ :literal:`FOOBAR2`\ , \ :literal:`FOOBAR3`\ , \ :literal:`FOOBAR4`\ .








Examples
--------

.. code-block:: yaml

    
    - name: Do some foo
      ns2.flatcol.foo:
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




