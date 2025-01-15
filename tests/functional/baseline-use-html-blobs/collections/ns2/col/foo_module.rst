.. Document meta

:orphan:
:github_url: https://github.com/ansible-community/antsibull-docs/edit/main/tests/functional/collections/ansible_collections/ns2/col/plugins/modules/foo.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns2.col.foo_module:

.. Anchors: short name for ansible.builtin

.. Title

ns2.col.foo module -- Do some foo :ansopt:`ns2.col.foo#module:bar`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.ns2.col.foo_module_requirements>` for details.

    To use it in a playbook, specify: :code:`ns2.col.foo`.

.. version_added

.. rst-class:: ansible-version-added

New in ns2.col 2.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Does some foo on the remote host.
- Whether foo is magic or not has not yet been determined.
- :ansenvvarref:`FOOBAR1`\ , :ansenvvarref:`FOOBAR2`\ , :ansenvvar:`FOOBAR3`\ , :ansenvvar:`FOOBAR4`.


.. Aliases

Aliases: foo_1_redirect, foo_2_redirect, foo_redirect

.. Requirements

.. _ansible_collections.ns2.col.foo_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- Foo on remote.






.. Options

Parameters
----------

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
      <div class="ansibleOptionAnchor" id="parameter-bar"></div>
      <div class="ansibleOptionAnchor" id="parameter-baz"></div>
      <p class="ansible-option-title"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>
      <p class="ansible-option-type-line"><span class="ansible-option-aliases">aliases: baz</span></p>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">list</span>
        / <span class="ansible-option-elements">elements=integer</span>
      </p>
    </div></td>
    <td><div class="ansible-option-cell">
      <p>A bar.</p>
      <p>Independent from <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-foo"><span class="std std-ref"><span class="pre">foo</span></span></a></strong></code>.</p>
      <p>Do not confuse with <code class="ansible-return-value literal notranslate"><a class="reference internal" href="#return-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></code>.</p>
    </div></td>
  </tr>
  <tr class="row-odd">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-foo"></div>
      <p class="ansible-option-title"><strong>foo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-foo" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
        / <span class="ansible-option-required">required</span>
      </p>
    </div></td>
    <td><div class="ansible-option-cell">
      <p>The foo source.</p>
    </div></td>
  </tr>
  <tr class="row-even">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-manager"></div>
      <p class="ansible-option-title"><strong>manager</strong></p>
      <a class="ansibleOptionLink" href="#parameter-manager" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">list</span>
        / <span class="ansible-option-elements">elements=string</span>
      </p>
    </div></td>
    <td><div class="ansible-option-cell">
      <p>The package manager(s) used by the system so we can query the package information. This is a list and can support multiple package managers per system, since version 2.8.</p>
      <p>The &#x27;portage&#x27; and &#x27;pkg&#x27; options were added in version 2.8.</p>
      <p>The &#x27;apk&#x27; option was added in version 2.11.</p>
      <p>The &#x27;pkg_info&#x27; option was added in version 2.13.</p>
      <p>Aliases were added in 2.18, to support using <code class='docutils literal notranslate'>auto={{ansible_facts[&#x27;pkg_mgr&#x27;]}}</code></p>
      <p class="ansible-option-line"><strong class="ansible-option-choices">Choices:</strong></p>
      <ul class="simple">
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;apk&#34;</code>:
          Alpine Linux package manager</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;apt&#34;</code>:
          For DEB based distros, <code class='docutils literal notranslate'>python-apt</code> package must be installed on targeted hosts</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-default-bold"><strong>&#34;auto&#34;</strong></code> <span class="ansible-option-choices-default-mark">(default)</span>:
          Depending on <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-strategy"><span class="std std-ref"><span class="pre">strategy</span></span></a></strong></code>, will match the first or all package managers provided, in order</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;dnf&#34;</code>:
          Alias to rpm</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;dnf5&#34;</code>:
          Alias to rpm</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;openbsd_pkg&#34;</code>:
          Alias to pkg_info</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;pacman&#34;</code>:
          Archlinux package manager/builder</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;pkg&#34;</code>:
          libpkg front end (FreeBSD)</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;pkg5&#34;</code>:
          Alias to pkg</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;pkg_info&#34;</code>:
          OpenBSD package manager</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;pkgng&#34;</code>:
          Alias to pkg</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;portage&#34;</code>:
          Handles ebuild packages, it requires the <code class='docutils literal notranslate'>qlist</code> utility, which is part of &#x27;app-portage/portage-utils&#x27;</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;rpm&#34;</code>:
          For RPM based distros, requires RPM Python bindings, not installed by default on Suse (python3-rpm)</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;yum&#34;</code>:
          Alias to rpm</p>
        </li>
        <li>
          <p><code class="ansible-value literal notranslate ansible-option-choices-entry">&#34;zypper&#34;</code>:
          Alias to rpm</p>
        </li>
      </ul>

      <p class="ansible-option-line"><strong class="ansible-option-default-bold">Default:</strong> <code class="ansible-value literal notranslate ansible-option-default">[&#34;auto&#34;]</code></p>
    </div></td>
  </tr>
  <tr class="row-odd">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-subfoo"></div>
      <p class="ansible-option-title"><strong>subfoo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-subfoo" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">dictionary</span>
      </p>
      <p><em class="ansible-option-versionadded">added in ns2.col 2.0.0</em></p>
    </div></td>
    <td><div class="ansible-option-cell">
      <p>Some recursive foo.</p>
    </div></td>
  </tr>
  <tr class="row-even">
    <td><div class="ansible-option-indent"></div><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-subfoo/foo"></div>
      <p class="ansible-option-title"><strong>foo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-subfoo/foo" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
        / <span class="ansible-option-required">required</span>
      </p>
    </div></td>
    <td><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">
      <p>A sub foo.</p>
      <p>Whatever.</p>
      <p>Also required when <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-subfoo"><span class="std std-ref"><span class="pre">subfoo</span></span></a></strong></code> is specified when <code class="ansible-option-value literal notranslate"><a class="reference internal" href="#parameter-foo"><span class="std std-ref"><span class="pre">foo=bar</span></span></a></code> or <code class="ansible-value literal notranslate">baz</code>.</p>
    </div></td>
  </tr>

  </tbody>
  </table>



.. Attributes


Attributes
----------

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
        <div class="ansibleOptionAnchor" id="attribute-action_group"></div>

      .. _ansible_collections.ns2.col.foo_module__attribute-action_group:

      .. rst-class:: ansible-option-title

      **action_group**

      .. raw:: html

        <a class="ansibleOptionLink" href="#attribute-action_group" title="Permalink to this attribute"></a>

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-property:`Action group:` |antsibull-internal-nbsp|:ansible-attribute-support-full:`ns2.col.foo\_group`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Use :literal:`group/ns2.col.foo\_group` in :literal:`module\_defaults` to set defaults for this module.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="attribute-check_mode"></div>

      .. _ansible_collections.ns2.col.foo_module__attribute-check_mode:

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
        <div class="ansibleOptionAnchor" id="attribute-diff_mode"></div>

      .. _ansible_collections.ns2.col.foo_module__attribute-diff_mode:

      .. rst-class:: ansible-option-title

      **diff_mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#attribute-diff_mode" title="Permalink to this attribute"></a>

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-label:`Support: \ `\ :ansible-attribute-support-full:`full`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="attribute-platform"></div>

      .. _ansible_collections.ns2.col.foo_module__attribute-platform:

      .. rst-class:: ansible-option-title

      **platform**

      .. raw:: html

        <a class="ansibleOptionLink" href="#attribute-platform" title="Permalink to this attribute"></a>

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-property:`Platform:` |antsibull-internal-nbsp|:ansible-attribute-support-full:`posix`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Target OS/families that can be operated against


      .. raw:: html

        </div>



.. Notes


.. Seealso

See Also
--------

.. seealso::

   :ref:`ns2.col.foo2 <ansible_collections.ns2.col.foo2_module>`
       Another foo.
   :ref:`ns2.col.foo <ansible_collections.ns2.col.foo_lookup>` lookup plugin
       Look up some foo :ansopt:`ns2.col.foo#module:bar`.
   :ref:`ansible.builtin.service <ansible_collections.ansible.builtin.service_module>`
       The service module.
   :ref:`ansible.builtin.ssh <ansible_collections.ansible.builtin.ssh_connection>` connection plugin
       The ssh connection plugin.

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - name: Do some foo
      ns2.col.foo:
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
      <div class="ansibleOptionAnchor" id="return-bar"></div>
      <p class="ansible-option-title"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#return-bar" title="Permalink to this return value"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>
    </div></td>
    <td><div class="ansible-option-cell">
      <p>Some bar.</p>
      <p>Referencing myself as <code class="ansible-return-value literal notranslate"><a class="reference internal" href="#return-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></code>.</p>
      <p>Do not confuse with <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></strong></code>.</p>
      <p class="ansible-option-line"><strong class="ansible-option-returned-bold">Returned:</strong> success</p>
      <p class="ansible-option-line ansible-option-sample"><strong class="ansible-option-sample-bold">Sample:</strong> <code class="ansible-value literal notranslate ansible-option-sample">&#34;baz&#34;</code></p>
    </div></td>
  </tr>
  </tbody>
  </table>



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
