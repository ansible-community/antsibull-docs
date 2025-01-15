.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns2.col.foo module -- Do some foo :literal:`bar` (`link <#parameter-bar>`_)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns2.col`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ns2.col.foo_module_requirements_>`_ for details.

To use it in a playbook, specify: ``ns2.col.foo``.

New in ns2.col 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Does some foo on the remote host.
- Whether foo is magic or not has not yet been determined.
- :literal:`FOOBAR1`\ , :literal:`FOOBAR2`\ , :literal:`FOOBAR3`\ , :literal:`FOOBAR4`.


Aliases: foo_1_redirect, foo_2_redirect, foo_redirect

.. _ansible_collections.ns2.col.foo_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- Foo on remote.






Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th colspan="2"><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-bar"></div>
      <div class="ansibleOptionAnchor" id="parameter-baz"></div>
      <p style="display: inline;"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;"><span style="color: darkgreen; white-space: normal;">aliases: baz</span></p>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=integer</span>
      </p>
    </td>
    <td valign="top">
      <p>A bar.</p>
      <p>Independent from <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-foo"><span class="std std-ref"><span class="pre">foo</span></span></a></strong></code>.</p>
      <p>Do not confuse with <code class="ansible-return-value literal notranslate"><a class="reference internal" href="#return-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></code>.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-foo"></div>
      <p style="display: inline;"><strong>foo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-foo" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>The foo source.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-manager"></div>
      <p style="display: inline;"><strong>manager</strong></p>
      <a class="ansibleOptionLink" href="#parameter-manager" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The package manager(s) used by the system so we can query the package information. This is a list and can support multiple package managers per system, since version 2.8.</p>
      <p>The &#x27;portage&#x27; and &#x27;pkg&#x27; options were added in version 2.8.</p>
      <p>The &#x27;apk&#x27; option was added in version 2.11.</p>
      <p>The &#x27;pkg_info&#x27; option was added in version 2.13.</p>
      <p>Aliases were added in 2.18, to support using <code class='docutils literal notranslate'>auto={{ansible_facts[&#x27;pkg_mgr&#x27;]}}</code></p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li>
          <p><code>&#34;apk&#34;</code>:
          Alpine Linux package manager</p>
        </li>
        <li>
          <p><code>&#34;apt&#34;</code>:
          For DEB based distros, <code class='docutils literal notranslate'>python-apt</code> package must be installed on targeted hosts</p>
        </li>
        <li>
          <p><code style="color: blue;"><b>&#34;auto&#34;</b></code> <span style="color: blue;">(default)</span>:
          Depending on <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-strategy"><span class="std std-ref"><span class="pre">strategy</span></span></a></strong></code>, will match the first or all package managers provided, in order</p>
        </li>
        <li>
          <p><code>&#34;dnf&#34;</code>:
          Alias to rpm</p>
        </li>
        <li>
          <p><code>&#34;dnf5&#34;</code>:
          Alias to rpm</p>
        </li>
        <li>
          <p><code>&#34;openbsd_pkg&#34;</code>:
          Alias to pkg_info</p>
        </li>
        <li>
          <p><code>&#34;pacman&#34;</code>:
          Archlinux package manager/builder</p>
        </li>
        <li>
          <p><code>&#34;pkg&#34;</code>:
          libpkg front end (FreeBSD)</p>
        </li>
        <li>
          <p><code>&#34;pkg5&#34;</code>:
          Alias to pkg</p>
        </li>
        <li>
          <p><code>&#34;pkg_info&#34;</code>:
          OpenBSD package manager</p>
        </li>
        <li>
          <p><code>&#34;pkgng&#34;</code>:
          Alias to pkg</p>
        </li>
        <li>
          <p><code>&#34;portage&#34;</code>:
          Handles ebuild packages, it requires the <code class='docutils literal notranslate'>qlist</code> utility, which is part of &#x27;app-portage/portage-utils&#x27;</p>
        </li>
        <li>
          <p><code>&#34;rpm&#34;</code>:
          For RPM based distros, requires RPM Python bindings, not installed by default on Suse (python3-rpm)</p>
        </li>
        <li>
          <p><code>&#34;yum&#34;</code>:
          Alias to rpm</p>
        </li>
        <li>
          <p><code>&#34;zypper&#34;</code>:
          Alias to rpm</p>
        </li>
      </ul>

      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">[&#34;auto&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-subfoo"></div>
      <p style="display: inline;"><strong>subfoo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-subfoo" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ns2.col 2.0.0</i></p>
    </td>
    <td valign="top">
      <p>Some recursive foo.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-subfoo/foo"></div>
      <p style="display: inline;"><strong>foo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-subfoo/foo" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>A sub foo.</p>
      <p>Whatever.</p>
      <p>Also required when <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-subfoo"><span class="std std-ref"><span class="pre">subfoo</span></span></a></strong></code> is specified when <code class="ansible-option-value literal notranslate"><a class="reference internal" href="#parameter-foo"><span class="std std-ref"><span class="pre">foo=bar</span></span></a></code> or <code class="ansible-value literal notranslate">baz</code>.</p>
    </td>
  </tr>

  </tbody>
  </table>




Attributes
----------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Attribute
    - Support
    - Description

  * - .. _ansible_collections.ns2.col.foo_module__attribute-action_group:

      **action_group**

    - Action group: \ns2.col.foo\_group


    -
      Use :literal:`group/ns2.col.foo\_group` in :literal:`module\_defaults` to set defaults for this module.



  * - .. _ansible_collections.ns2.col.foo_module__attribute-check_mode:

      **check_mode**

    - Support: full



    -
      Can run in check\_mode and return changed status prediction without modifying target



  * - .. _ansible_collections.ns2.col.foo_module__attribute-diff_mode:

      **diff_mode**

    - Support: full



    -
      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode



  * - .. _ansible_collections.ns2.col.foo_module__attribute-platform:

      **platform**

    - Platform:posix


    -
      Target OS/families that can be operated against





See Also
--------

* `ns2.col.foo2 <foo2_module.rst>`__

  Another foo.
* `ns2.col.foo <foo_lookup.rst>`__ lookup plugin

  Look up some foo :literal:`bar` (`link <#parameter-bar>`_).
* `ansible.builtin.service <service_module.rst>`__

  The service module.
* `ansible.builtin.ssh <ssh_connection.rst>`__ connection plugin

  The ssh connection plugin.

Examples
--------

.. code-block:: yaml

    - name: Do some foo
      ns2.col.foo:
        foo: '{{ foo }}'
        bar:
          - 1
          - 2
          - 3
        subfoo:
          foo: hoo!




Return Values
-------------
The following are the fields unique to this module:

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-bar"></div>
      <p style="display: inline;"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#return-bar" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Some bar.</p>
      <p>Referencing myself as <code class="ansible-return-value literal notranslate"><a class="reference internal" href="#return-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></code>.</p>
      <p>Do not confuse with <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></strong></code>.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;baz&#34;</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Ansible Core Team
- Someone else (@ansible)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__
