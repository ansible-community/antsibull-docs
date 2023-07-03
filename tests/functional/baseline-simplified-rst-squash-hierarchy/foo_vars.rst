

ns2.col.foo vars -- Load foo \ :literal:`bar` (`link <parameter-bar_>`_)\ 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This vars plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.
You need further requirements to be able to use this vars plugin,
see `Requirements <ansible_collections.ns2.col.foo_vars_requirements_>`_ for details.

To use it in a playbook, specify: :code:`ns2.col.foo`.

New in ns2.col 0.9.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Load some foo.
- This is so glorious.



.. _ansible_collections.ns2.col.foo_vars_requirements:

Requirements
------------
The below requirements are needed on the local controller node that executes this vars.

- Enabled in Ansible's configuration.






Parameters
----------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-_valid_extensions:

      **_valid_extensions**

      :literal:`list` / :literal:`elements=string`




      .. raw:: html

        </div></div>

    - 
      All extensions to check.


      Default: :literal:`[".foo", ".foobar"]`

      Configuration:

      - INI entry:

        .. code-block::

          [defaults]
          foo_valid_extensions = .foo, .foobar


      - Environment variable: :literal:`ANSIBLE\_FOO\_FILENAME\_EXT`



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-bar:

      **bar**

      :literal:`string`




      .. raw:: html

        </div></div>

    - 
      Foo bar.













.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

