.. Document meta

:orphan:
:github_url: https://github.com/ansible-community/antsibull-docs/edit/main/tests/functional/collections/ansible_collections/ns2/col/roles/foo/meta/argument_specs.yml?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns2.col.foo_role:

.. Title

ns2.col.foo role -- Foo role
++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it use: :code:`ansible\-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.foo`.

.. contents::
   :local:
   :depth: 2

.. _ansible_collections.ns2.col.foo_role__entrypoint-main:

.. Entry point title

Entry point ``main`` -- Foo role
--------------------------------

.. version_added

.. rst-class:: ansible-version-added

New in ns2.col 0.2.0

.. Deprecated

DEPRECATED
^^^^^^^^^^
:Removed in: major release after 2020\-01\-01
:Why: Just some text.
      This one has more than one line.
      And one more.
:Alternative: I don't know
              of any
              alternative.

Synopsis
^^^^^^^^

.. Description

- This is the foo role.
- If you set :ansopt:`ns2.col.foo#role:main:foo\_param\_1` while :ansopt:`ns2.col.foo#role:main:foo\_param\_2=3`\ , this might behave funny.

.. Requirements


.. Options

Parameters
^^^^^^^^^^

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
        <div class="ansibleOptionAnchor" id="parameter-main--foo_param_1"></div>

      .. _ansible_collections.ns2.col.foo_role__parameter-main__foo_param_1:

      .. rst-class:: ansible-option-title

      **foo_param_1**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--foo_param_1" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A string parameter

      If you set :ansopt:`ns2.col.foo#role:main:foo\_param\_1` while :ansopt:`ns2.col.foo#role:main:foo\_param\_2=3`\ , this might behave funny.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--foo_param_2"></div>

      .. _ansible_collections.ns2.col.foo_role__parameter-main__foo_param_2:

      .. rst-class:: ansible-option-title

      **foo_param_2**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--foo_param_2" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      An integer parameter with a default.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`13`

      .. raw:: html

        </div>


.. Attributes


Attributes
^^^^^^^^^^

.. tabularcolumns:: \X{2}{10}\X{3}{10}\X{5}{10}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Attribute
    - Support
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="attribute-check_mode"></div>

      .. _ansible_collections.ns2.col.foo_role__attribute-main__check_mode:

      .. rst-class:: ansible-option-title

      **check_mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#attribute-check_mode" title="Permalink to this attribute"></a>

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-label:`Support: \ `\ :ansible-attribute-support-full:`full`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Can run in check\_mode and return changed status prediction without modifying target


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="attribute-platform"></div>

      .. _ansible_collections.ns2.col.foo_role__attribute-main__platform:

      .. rst-class:: ansible-option-title

      **platform**

      .. raw:: html

        <a class="ansibleOptionLink" href="#attribute-platform" title="Permalink to this attribute"></a>

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-property:`Platforms:` |antsibull-internal-nbsp|:ansible-attribute-support-full:`Linux`, :ansible-attribute-support-full:`macOS`, :ansible-attribute-support-full:`FreeBSD`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The supported platforms


      .. raw:: html

        </div>



.. Notes


.. Seealso

See Also
^^^^^^^^

.. seealso::

   :ref:`ns2.col.foo <ansible_collections.ns2.col.foo_module>`
       The official documentation on the **ns2.col.foo** module.

Examples
^^^^^^^^

.. code-block:: yaml+jinja

    - name: Use role
      include_role: ns2.col.foo
      vars:
        foo_param_1: foobar
        foo_param_2: 23


.. Return variables

Return Variables
^^^^^^^^^^^^^^^^

The following variables are set by this role:

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-foo_facts"></div>

      .. _ansible_collections.ns2.col.foo_role__return-main__foo_facts:

      .. rst-class:: ansible-option-title

      **foo_facts**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-foo_facts" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Information gathered by the role about the foo configuration.

      The role uses this to decide whether to set :ansretval:`ns2.col.foo#role:main:foo\_reboot\_required`.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` When :ansopt:`ns2.col.foo#role:main:foo\_param\_1` is set.

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`[{"default": true, "name": "example", "value": "foobar"}]`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-foo_facts/default"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ns2.col.foo_role__return-main__foo_facts/default:

      .. rst-class:: ansible-option-title

      **default**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-foo_facts/default" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Whether this is the default entry.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-foo_facts/name"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ns2.col.foo_role__return-main__foo_facts/name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-foo_facts/name" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The name of the entry.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-foo_facts/value"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ns2.col.foo_role__return-main__foo_facts/value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-foo_facts/value" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The value of the entry.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-foo_reboot_required"></div>

      .. _ansible_collections.ns2.col.foo_role__return-main__foo_reboot_required:

      .. rst-class:: ansible-option-title

      **foo_reboot_required**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-foo_reboot_required" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansval:`true` means the host must reboot to apply the role's changes.

      The role sets this when :ansopt:`ns2.col.foo#role:main:foo\_param\_2` is at least 2 and it made changes.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`true`


      .. raw:: html

        </div>




Authors
^^^^^^^

- Felix Fontein (@felixfontein)



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
