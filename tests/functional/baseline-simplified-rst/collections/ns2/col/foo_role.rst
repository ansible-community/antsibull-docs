.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns2.col.foo role -- Foo role
++++++++++++++++++++++++++++

This role is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run :code:`ansible-galaxy collection list`.

To install it use: :code:`ansible\-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.foo`.

.. contents::
   :local:
   :depth: 2

.. _ansible_collections.ns2.col.foo_role__entrypoint-main:

Entry point ``main`` -- Foo role
--------------------------------

New in ns2.col 0.2.0

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

- This is the foo role.
- If you set :literal:`foo\_param\_1` (`link <#parameter-main--foo_param_1>`_) while :literal:`foo\_param\_2=3` (`link <#parameter-main--foo_param_2>`_)\ , this might behave funny.


Parameters
^^^^^^^^^^

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-main--foo_param_1"></div>
      <p style="display: inline;"><strong>foo_param_1</strong></p>
      <a class="ansibleOptionLink" href="#parameter-main--foo_param_1" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>A string parameter</p>
      <p>If you set <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-main--foo_param_1"><span class="std std-ref"><span class="pre">foo_param_1</span></span></a></strong></code> while <code class="ansible-option-value literal notranslate"><a class="reference internal" href="#parameter-main--foo_param_2"><span class="std std-ref"><span class="pre">foo_param_2=3</span></span></a></code>, this might behave funny.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-main--foo_param_2"></div>
      <p style="display: inline;"><strong>foo_param_2</strong></p>
      <a class="ansibleOptionLink" href="#parameter-main--foo_param_2" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>

    </td>
    <td valign="top">
      <p>An integer parameter with a default.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">13</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Attributes
^^^^^^^^^^

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Attribute
    - Support
    - Description

  * - .. _ansible_collections.ns2.col.foo_role__attribute-main__check_mode:

      **check_mode**

    - Support: full



    -
      Can run in check\_mode and return changed status prediction without modifying target



  * - .. _ansible_collections.ns2.col.foo_role__attribute-main__platform:

      **platform**

    - Platforms:Linux, macOS, FreeBSD


    -
      The supported platforms





See Also
^^^^^^^^

* `ns2.col.foo <foo_module.rst>`__

  The official documentation on the **ns2.col.foo** module.

Examples
^^^^^^^^

.. code-block:: yaml

    - name: Use role
      include_role: ns2.col.foo
      vars:
        foo_param_1: foobar
        foo_param_2: 23


Return Variables
^^^^^^^^^^^^^^^^

The following variables are set by this role:

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th colspan="2"><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="return-foo_facts"></div>
      <p style="display: inline;"><strong>foo_facts</strong></p>
      <a class="ansibleOptionLink" href="#return-foo_facts" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Information gathered by the role about the foo configuration.</p>
      <p>The role uses this to decide whether to set <code class="ansible-return-value literal notranslate"><a class="reference internal" href="#return-main--foo_reboot_required"><span class="std std-ref"><span class="pre">foo_reboot_required</span></span></a></code>.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> When <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-main--foo_param_1"><span class="std std-ref"><span class="pre">foo_param_1</span></span></a></strong></code> is set.</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[{&#34;default&#34;: true, &#34;name&#34;: &#34;example&#34;, &#34;value&#34;: &#34;foobar&#34;}]</code></p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-foo_facts/default"></div>
      <p style="display: inline;"><strong>default</strong></p>
      <a class="ansibleOptionLink" href="#return-foo_facts/default" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Whether this is the default entry.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-foo_facts/name"></div>
      <p style="display: inline;"><strong>name</strong></p>
      <a class="ansibleOptionLink" href="#return-foo_facts/name" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The name of the entry.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-foo_facts/value"></div>
      <p style="display: inline;"><strong>value</strong></p>
      <a class="ansibleOptionLink" href="#return-foo_facts/value" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The value of the entry.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
    </td>
  </tr>

  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="return-foo_reboot_required"></div>
      <p style="display: inline;"><strong>foo_reboot_required</strong></p>
      <a class="ansibleOptionLink" href="#return-foo_reboot_required" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p><code class="ansible-value literal notranslate">true</code> means the host must reboot to apply the role&#x27;s changes.</p>
      <p>The role sets this when <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-main--foo_param_2"><span class="std std-ref"><span class="pre">foo_param_2</span></span></a></strong></code> is at least 2 and it made changes.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>true</code></p>
    </td>
  </tr>
  </tbody>
  </table>



Authors
^^^^^^^

- Felix Fontein (@felixfontein)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible\-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible\-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible\-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible\-community/antsibull\-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__
