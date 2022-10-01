
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-entry
.. role:: ansible-option-default
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.ns2.col.foo_shell:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

ns2.col.foo shell -- Foo shell
++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This shell plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.foo`.

.. version_added

.. rst-class:: ansible-version-added

New in ns2.col 1.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This is for the foo shell.


.. Aliases


.. Requirements






.. Options

Parameters
----------


.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-admin_users"></div>

      .. _ansible_collections.ns2.col.foo_shell__parameter-admin_users:

      .. rst-class:: ansible-option-title

      **admin_users**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-admin_users" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      list of users to be expected to have admin privileges. This is used by the controller to determine how to share temporary files between the remote user and the become user.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`["root", "toor"]`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [defaults]
          admin_users = root, toor


      - Environment variable: ANSIBLE\_ADMIN\_USERS

      - Variable: ansible\_admin\_users


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-async_dir"></div>

      .. _ansible_collections.ns2.col.foo_shell__parameter-async_dir:

      .. rst-class:: ansible-option-title

      **async_dir**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-async_dir" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Directory in which ansible will keep async job information


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"~/.ansible\_async"`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [defaults]
          async_dir = ~/.ansible_async


      - Environment variable: ANSIBLE\_ASYNC\_DIR

      - Variable: ansible\_async\_dir


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-common_remote_group"></div>

      .. _ansible_collections.ns2.col.foo_shell__parameter-common_remote_group:

      .. rst-class:: ansible-option-title

      **common_remote_group**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-common_remote_group" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in ansible-base 2.10`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Checked when Ansible needs to execute a module as a different user.

      If setfacl and chown both fail and do not let the different user access the module's files, they will be chgrp'd to this group.

      In order for this to work, the remote\_user and become\_user must share a common group and this setting must be set to that group.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [defaults]
          common_remote_group = VALUE


      - Environment variable: ANSIBLE\_COMMON\_REMOTE\_GROUP

      - Variable: ansible\_common\_remote\_group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-environment"></div>

      .. _ansible_collections.ns2.col.foo_shell__parameter-environment:

      .. rst-class:: ansible-option-title

      **environment**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-environment" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of dictionaries of environment variables and their values to use when executing commands.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[{}]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-remote_tmp"></div>

      .. _ansible_collections.ns2.col.foo_shell__parameter-remote_tmp:

      .. rst-class:: ansible-option-title

      **remote_tmp**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-remote_tmp" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Temporary directory to use on targets when executing tasks.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"~/.ansible/tmp"`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [defaults]
          remote_tmp = ~/.ansible/tmp


      - Environment variable: ANSIBLE\_REMOTE\_TEMP

      - Environment variable: ANSIBLE\_REMOTE\_TMP

      - Variable: ansible\_remote\_tmp


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system_tmpdirs"></div>

      .. _ansible_collections.ns2.col.foo_shell__parameter-system_tmpdirs:

      .. rst-class:: ansible-option-title

      **system_tmpdirs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system_tmpdirs" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of valid system temporary directories on the managed machine for Ansible to validate \ :literal:`remote\_tmp`\  against, when specific permissions are needed.  These must be world readable, writable, and executable. This list should only contain directories which the system administrator has pre-created with the proper ownership and permissions otherwise security issues can arise.

      When \ :literal:`remote\_tmp`\  is required to be a system temp dir and it does not match any in the list, the first one from the list will be used instead.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`["/var/tmp", "/tmp"]`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [defaults]
          system_tmpdirs = /var/tmp, /tmp


      - Environment variable: ANSIBLE\_SYSTEM\_TMPDIRS

      - Variable: ansible\_system\_tmpdirs


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-world_readable_temp"></div>

      .. _ansible_collections.ns2.col.foo_shell__parameter-world_readable_temp:

      .. rst-class:: ansible-option-title

      **world_readable_temp**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-world_readable_temp" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in ansible-base 2.10`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      This makes the temporary files created on the machine world-readable and will issue a warning instead of failing the task.

      It is useful when becoming an unprivileged user.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`false` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [defaults]
          allow_world_readable_tmpfiles = false


      - Environment variable: ANSIBLE\_SHELL\_ALLOW\_WORLD\_READABLE\_TEMP

      - Variable: ansible\_shell\_allow\_world\_readable\_temp


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples



.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/ansible-collections/community.general/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/ansible-collections/community.crypto" aria-role="button" target="_blank" rel="noopener external">Homepage</a>
    <a href="https://github.com/ansible-collections/community.internal_test_tools" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

