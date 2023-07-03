

ns2.col.foo become -- Use foo \ :literal:`bar` (`link <parameter-bar_>`_)\ 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This become plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.foo`.


.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in: version 5.0.0
:Why: Just some text.
      This one has more than one line.
      And one more.

:Alternative: I don't know
              of any
              alternative.


Synopsis
--------

- This become plugin uses foo.
- This is a second paragraph.








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

      added in ns2.col 1.2.0



      Removed in: version 4.0.0

      Why: Just some other text.
      This one has more than one line though.
      One more.


      Alternative: nothing
      relevant
      I know of





      .. raw:: html

        </div></div>

    - 
      Bar. \ :strong:`BAR!`\ 

      Totally unrelated to \ :literal:`become\_user` (`link <parameter-become_user_>`_)\ . Even with \ :literal:`become\_user=foo` (`link <parameter-become_user_>`_)\ .

      Might not be compatible when \ :literal:`become\_user` (`link <parameter-become_user_>`_)\  is \ :literal:`bar`\ , though.



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-become_exe:

      **become_exe**

      :literal:`string`

      added in ns2.col 0.2.0





      .. raw:: html

        </div></div>

    - 
      Foo executable.


      Default: :literal:`"foo"`

      Configuration:

      - INI entries:

        .. code-block::

          [privilege_escalation]
          become_exe = foo



        .. code-block::

          [foo_become_plugin]
          executable = foo


        Removed in: version 3.0.0

        Why: Just some text.

        Alternative: nothing


      - Environment variable: :literal:`ANSIBLE\_BECOME\_EXE`

      - Environment variable: :literal:`ANSIBLE\_FOO\_EXE`

        Removed in: version 3.0.0

        Why: Just some text.

        Alternative: nothing


      - Variable: ansible\_become\_exe

      - Variable: ansible\_foo\_exe

        Removed in: version 3.0.0

        Why: Just some text.

        Alternative: nothing


      - Keyword: become\_exe



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-become_user:

      **become_user**

      :literal:`string`




      .. raw:: html

        </div></div>

    - 
      User you 'become' to execute the task.


      Default: :literal:`"root"`

      Configuration:

      - INI entries:

        .. code-block::

          [privilege_escalation]
          become_user = root

        added in ns2.col 0.1.0


        .. code-block::

          [foo_become_plugin]
          user = root


      - Environment variable: :literal:`ANSIBLE\_BECOME\_USER`

        added in ns2.col 0.1.0

      - Environment variable: :literal:`ANSIBLE\_FOO\_USER`

      - Variable: ansible\_become\_user

      - Variable: ansible\_foo\_user

        added in ns2.col 0.1.0

      - Keyword: become\_user

        added in ns2.col 0.1.0











Status
------

- This become will be removed in version 5.0.0.
  *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Nobody 


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

