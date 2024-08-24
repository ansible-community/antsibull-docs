.. Document meta

:orphan:
:github_url: https://github.com/ansible-collections/community.REPO_NAME/edit/main/plugins/modules/foo.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. Anchors

.. _ansible_collections.ns2.flatcol.foo_module:

.. Anchors: short name for ansible.builtin

.. Title

ns2.flatcol.foo module -- Do some foo :ansopt:`ns2.flatcol.foo#module:bar`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ns2.flatcol collection <https://galaxy.ansible.com/ui/repo/published/ns2/flatcol/>`_.

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ns2.flatcol`.

    To use it in a playbook, specify: :code:`ns2.flatcol.foo`.

.. version_added

.. rst-class:: ansible-version-added

New in ns2.flatcol 2.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Does some foo on the remote host.
- Whether foo is magic or not has not yet been determined.


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
        <div class="ansibleOptionAnchor" id="parameter-baz"></div>

      .. _ansible_collections.ns2.flatcol.foo_module__parameter-bar:
      .. _ansible_collections.ns2.flatcol.foo_module__parameter-baz:

      .. rst-class:: ansible-option-title

      **bar**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: baz`

        :ansible-option-type:`list` / :ansible-option-elements:`elements=integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A bar.

      Independent from :ansopt:`ns2.flatcol.foo#module:foo`.

      Do not confuse with :ansretval:`ns2.flatcol.foo#module:bar`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-foo"></div>

      .. _ansible_collections.ns2.flatcol.foo_module__parameter-foo:

      .. rst-class:: ansible-option-title

      **foo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-foo" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The foo source.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-subfoo"></div>
        <div class="ansibleOptionAnchor" id="parameter-subbaz"></div>

      .. _ansible_collections.ns2.flatcol.foo_module__parameter-subbaz:
      .. _ansible_collections.ns2.flatcol.foo_module__parameter-subfoo:

      .. rst-class:: ansible-option-title

      **subfoo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subfoo" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: subbaz`

        :ansible-option-type:`dictionary`

      :ansible-option-versionadded:`added in ns2.flatcol 2.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Some recursive foo.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-subfoo/foo"></div>
        <div class="ansibleOptionAnchor" id="parameter-subbaz/foo"></div>
        <div class="ansibleOptionAnchor" id="parameter-subfoo/bam"></div>
        <div class="ansibleOptionAnchor" id="parameter-subbaz/bam"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ns2.flatcol.foo_module__parameter-subbaz/bam:
      .. _ansible_collections.ns2.flatcol.foo_module__parameter-subbaz/foo:
      .. _ansible_collections.ns2.flatcol.foo_module__parameter-subfoo/bam:
      .. _ansible_collections.ns2.flatcol.foo_module__parameter-subfoo/foo:

      .. rst-class:: ansible-option-title

      **foo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subfoo/foo" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: bam`

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A sub foo.

      Whatever.

      Also required when :ansopt:`ns2.flatcol.foo#module:subfoo` is specified when :ansopt:`ns2.flatcol.foo#module:foo=bar` or :ansval:`baz`.

      Note that :ansopt:`ns2.flatcol.foo#module:subfoo.foo` is the same as :ansopt:`ns2.flatcol.foo#module:subbaz.foo`\ , :ansopt:`ns2.flatcol.foo#module:subbaz.bam`\ , and :ansopt:`ns2.flatcol.foo#module:subfoo.bam`.

      :ansenvvarref:`FOOBAR1`\ , :ansenvvarref:`FOOBAR2`\ , :ansenvvar:`FOOBAR3`\ , :ansenvvar:`FOOBAR4`.


      .. raw:: html

        </div>



.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - name: Do some foo
      ns2.flatcol.foo:
        foo: '{{ foo }}'
        bar:
          - 1
          - 2
          - 3
        subfoo:
          foo: hoo!



.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

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
        <div class="ansibleOptionAnchor" id="return-bar"></div>

      .. _ansible_collections.ns2.flatcol.foo_module__return-bar:

      .. rst-class:: ansible-option-title

      **bar**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-bar" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Some bar.

      Referencing myself as :ansretval:`ns2.flatcol.foo#module:bar`.

      Do not confuse with :ansopt:`ns2.flatcol.foo#module:bar`.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"baz"`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Ansible Core Team
- Someone else (@ansible)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Report an issue"
    url: "https://github.com/ansible-collections/community.REPO_NAME/issues/new/choose"
    external: true
  - title: Communication
    ref: communication_for_ns2.flatcol


.. Parsing errors
