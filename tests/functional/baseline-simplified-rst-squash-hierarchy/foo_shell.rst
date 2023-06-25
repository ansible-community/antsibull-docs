

ns2.col.foo shell -- Foo shell \ :literal:`bar` (`link <parameter-bar_>`_)\ 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. note::
    This shell plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.foo`.

New in ns2.col 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This is for the foo shell.








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
      Foo bar.



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-remote_tmp:

      **remote_tmp**

      :literal:`string`

      added in ansible-base 2.10





      .. raw:: html

        </div></div>

    - 
      Temporary directory to use on targets when executing tasks.


      Default: :literal:`"~/.ansible/tmp"`

      Configuration:

      - INI entry:

        .. code-block::

          [defaults]
          remote_tmp = ~/.ansible/tmp


      - Environment variable: :literal:`ANSIBLE\_REMOTE\_TEMP`

      - Environment variable: :literal:`ANSIBLE\_REMOTE\_TMP`

      - Variable: ansible\_remote\_tmp













.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

