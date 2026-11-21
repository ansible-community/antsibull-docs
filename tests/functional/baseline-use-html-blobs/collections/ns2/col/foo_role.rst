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

.. raw:: html

  <table class="colwidths-auto ansible-option-table docutils align-default" style="width: 100%">
  <thead>
  <tr class="row-odd">
    <th class="head"><p>Parameter</p></th>
    <th class="head"><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr class="row-even">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-main--foo_param_1"></div>
      <p class="ansible-option-title"><strong>foo_param_1</strong></p>
      <a class="ansibleOptionLink" href="#parameter-main--foo_param_1" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>A string parameter</p>
      <p>If you set <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-main--foo_param_1"><span class="std std-ref"><span class="pre">foo_param_1</span></span></a></strong></code> while <code class="ansible-option-value literal notranslate"><a class="reference internal" href="#parameter-main--foo_param_2"><span class="std std-ref"><span class="pre">foo_param_2=3</span></span></a></code>, this might behave funny.</p>
    </div></td>
  </tr>
  <tr class="row-odd">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-main--foo_param_2"></div>
      <p class="ansible-option-title"><strong>foo_param_2</strong></p>
      <a class="ansibleOptionLink" href="#parameter-main--foo_param_2" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">integer</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>An integer parameter with a default.</p>
      <p class="ansible-option-line"><strong class="ansible-option-default-bold">Default:</strong> <code class="ansible-value literal notranslate ansible-option-default">13</code></p>
    </div></td>
  </tr>
  </tbody>
  </table>



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

.. raw:: html

  <table class="colwidths-auto ansible-option-table docutils align-default" style="width: 100%">
  <thead>
  <tr class="row-odd">
    <th class="head"><p>Key</p></th>
    <th class="head"><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr class="row-even">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="return-foo_facts"></div>
      <p class="ansible-option-title"><strong>foo_facts</strong></p>
      <a class="ansibleOptionLink" href="#return-foo_facts" title="Permalink to this return value"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">list</span>
        / <span class="ansible-option-elements">elements=dictionary</span>
      </p>
    </div></td>
    <td><div class="ansible-option-cell">
      <p>Information gathered by the role about the foo configuration.</p>
      <p>The role uses this to decide whether to set <code class="ansible-return-value literal notranslate"><a class="reference internal" href="#return-main--foo_reboot_required"><span class="std std-ref"><span class="pre">foo_reboot_required</span></span></a></code>.</p>
      <p class="ansible-option-line"><strong class="ansible-option-returned-bold">Returned:</strong> When <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-main--foo_param_1"><span class="std std-ref"><span class="pre">foo_param_1</span></span></a></strong></code> is set.</p>
      <p class="ansible-option-line ansible-option-sample"><strong class="ansible-option-sample-bold">Sample:</strong> <code class="ansible-value literal notranslate ansible-option-sample">[{&#34;default&#34;: true, &#34;name&#34;: &#34;example&#34;, &#34;value&#34;: &#34;foobar&#34;}]</code></p>
    </div></td>
  </tr>
  <tr class="row-odd">
    <td><div class="ansible-option-indent"></div><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="return-foo_facts/default"></div>
      <p class="ansible-option-title"><strong>default</strong></p>
      <a class="ansibleOptionLink" href="#return-foo_facts/default" title="Permalink to this return value"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">boolean</span>
      </p>
    </div></td>
    <td><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">
      <p>Whether this is the default entry.</p>
      <p class="ansible-option-line"><strong class="ansible-option-returned-bold">Returned:</strong> success</p>
    </div></td>
  </tr>
  <tr class="row-even">
    <td><div class="ansible-option-indent"></div><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="return-foo_facts/name"></div>
      <p class="ansible-option-title"><strong>name</strong></p>
      <a class="ansibleOptionLink" href="#return-foo_facts/name" title="Permalink to this return value"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>
    </div></td>
    <td><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">
      <p>The name of the entry.</p>
      <p class="ansible-option-line"><strong class="ansible-option-returned-bold">Returned:</strong> success</p>
    </div></td>
  </tr>
  <tr class="row-odd">
    <td><div class="ansible-option-indent"></div><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="return-foo_facts/value"></div>
      <p class="ansible-option-title"><strong>value</strong></p>
      <a class="ansibleOptionLink" href="#return-foo_facts/value" title="Permalink to this return value"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>
    </div></td>
    <td><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">
      <p>The value of the entry.</p>
      <p class="ansible-option-line"><strong class="ansible-option-returned-bold">Returned:</strong> success</p>
    </div></td>
  </tr>

  <tr class="row-even">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="return-foo_reboot_required"></div>
      <p class="ansible-option-title"><strong>foo_reboot_required</strong></p>
      <a class="ansibleOptionLink" href="#return-foo_reboot_required" title="Permalink to this return value"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">boolean</span>
      </p>
    </div></td>
    <td><div class="ansible-option-cell">
      <p><code class="ansible-value literal notranslate">true</code> means the host must reboot to apply the role&#x27;s changes.</p>
      <p>The role sets this when <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-main--foo_param_2"><span class="std std-ref"><span class="pre">foo_param_2</span></span></a></strong></code> is at least 2 and it made changes.</p>
      <p class="ansible-option-line"><strong class="ansible-option-returned-bold">Returned:</strong> always</p>
      <p class="ansible-option-line ansible-option-sample"><strong class="ansible-option-sample-bold">Sample:</strong> <code class="ansible-value literal notranslate ansible-option-sample">true</code></p>
    </div></td>
  </tr>
  </tbody>
  </table>




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
