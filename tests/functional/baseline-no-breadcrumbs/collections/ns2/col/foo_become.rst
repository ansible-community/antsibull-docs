.. Document meta

:orphan:
:github_url: https://github.com/ansible-community/antsibull-docs/edit/main/tests/functional/collections/ansible_collections/ns2/col/plugins/become/foo.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns2.col.foo_become:

.. Anchors: short name for ansible.builtin

.. Title

ns2.col.foo become -- Use foo :ansopt:`ns2.col.foo#become:bar`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This become plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.foo`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated

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

.. Description

- This become plugin uses foo.
- This is a second paragraph.


.. Aliases


.. Requirements






.. Options

Parameters
----------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-bar"></div>

      .. _ansible_collections.ns2.col.foo_become__parameter-bar:

      .. rst-class:: ansible-option-title

      **bar**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in ns2.col 1.2.0`



      Removed in: version 4.0.0

      Why: Just some other text.
      This one has more than one line though.
      One more.

      Alternative: nothing
      relevant
      I know of




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Bar. :strong:`BAR!`

      Totally unrelated to :ansopt:`ns2.col.foo#become:become\_user`. Even with :ansopt:`ns2.col.foo#become:become\_user=foo`.

      Might not be compatible when :ansopt:`ns2.col.foo#become:become\_user` is :ansval:`bar`\ , though.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-become_exe"></div>

      .. _ansible_collections.ns2.col.foo_become__parameter-become_exe:

      .. rst-class:: ansible-option-title

      **become_exe**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-become_exe" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in ns2.col 0.2.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Foo executable.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"foo"`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entries:

        .. code-block:: ini

          [privilege_escalation]
          become_exe = foo



        .. code-block:: ini

          [foo_become_plugin]
          executable = foo


        Removed in: version 3.0.0

        Why: Just some text.

        Alternative: nothing


      - Environment variable: :envvar:`ANSIBLE\_BECOME\_EXE`

      - Environment variable: :envvar:`ANSIBLE\_FOO\_EXE`

        Removed in: version 3.0.0

        Why: Just some text.

        Alternative: nothing


      - Variable: ansible\_become\_exe

      - Variable: ansible\_foo\_exe

        Removed in: version 3.0.0

        Why: Just some text.

        Alternative: nothing


      - Keyword: become\_exe


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-become_user"></div>

      .. _ansible_collections.ns2.col.foo_become__parameter-become_user:

      .. rst-class:: ansible-option-title

      **become_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-become_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      User you 'become' to execute the task.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"root"`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entries:

        .. code-block:: ini

          [privilege_escalation]
          become_user = root

        :ansible-option-versionadded:`added in ns2.col 0.1.0`


        .. code-block:: ini

          [foo_become_plugin]
          user = root


      - Environment variable: :envvar:`ANSIBLE\_BECOME\_USER`

        :ansible-option-versionadded:`added in ns2.col 0.1.0`

      - Environment variable: :envvar:`ANSIBLE\_FOO\_USER`

      - Variable: ansible\_become\_user

      - Variable: ansible\_foo\_user

        :ansible-option-versionadded:`added in ns2.col 0.1.0`

      - Keyword: become\_user

        :ansible-option-versionadded:`added in ns2.col 0.1.0`


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples



.. Facts


.. Return values


..  Status (Presently only deprecated)

Status
------

.. Deprecated note

- This become will be removed in version 5.0.0.
  *[deprecated]*
- For more information see `DEPRECATED`_.


.. Authors

Authors
~~~~~~~

- Nobody


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Issue Tracker"
    url: "https://github.com/ansible-collections/community.general/issues"
    external: true
  - title: "Homepage"
    url: "https://github.com/ansible-collections/community.crypto"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/ansible-collections/community.internal_test_tools"
    external: true
  - title: "Submit a bug report"
    url: "https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug_report.md"
    external: true
  - title: Communication
    ref: communication_for_ns2.col


.. Parsing errors
