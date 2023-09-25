
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

ns2.col.foo become -- Use foo \ :ansopt:`ns2.col.foo#become:bar`\ 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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
      <p class="ansible-option-title"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>
      <p><em class="ansible-option-versionadded">added in ns2.col 1.2.0</em></p>
  <p>Removed in: version 4.0.0</p>
  <p>Why: Just some other text.
  This one has more than one line though.
  One more.
  </p>
  <p>Alternative: nothing
  relevant
  I know of
  </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>Bar. <b>BAR!</b></p>
      <p>Totally unrelated to <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-become_user"><span class="std std-ref"><span class="pre">become_user</span></span></a></strong></code>. Even with <code class="ansible-option-value literal notranslate"><a class="reference internal" href="#parameter-become_user"><span class="std std-ref"><span class="pre">become_user=foo</span></span></a></code>.</p>
      <p>Might not be compatible when <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-become_user"><span class="std std-ref"><span class="pre">become_user</span></span></a></strong></code> is <code class="ansible-value literal notranslate">bar</code>, though.</p>
    </div></td>
  </tr>
  <tr class="row-odd">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-become_exe"></div>
      <p class="ansible-option-title"><strong>become_exe</strong></p>
      <a class="ansibleOptionLink" href="#parameter-become_exe" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>
      <p><em class="ansible-option-versionadded">added in ns2.col 0.2.0</em></p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>Foo executable.</p>
      <p class="ansible-option-line"><strong class="ansible-option-default-bold">Default:</strong> <code class="ansible-value literal notranslate ansible-option-default">&#34;foo&#34;</code></p>
      <p class="ansible-option-line"><strong class="ansible-option-configuration">Configuration:</strong></p>
      <ul class="simple">
      <li>
        <p>INI entries</p>
        <div class="highlight-YAML+Jinja notranslate"><div class="highlight"><pre><span class="p p-Indicator">[</span><span class="nv">privilege_escalation</span><span class="p p-Indicator">]</span>
  <span class="l l-Scalar l-Scalar-Plain">become_exe = foo</span></pre></div></div>

        <div class="highlight-YAML+Jinja notranslate"><div class="highlight"><pre><span class="p p-Indicator">[</span><span class="nv">foo_become_plugin</span><span class="p p-Indicator">]</span>
  <span class="l l-Scalar l-Scalar-Plain">executable = foo</span></pre></div></div>
  <p>Removed in: version 3.0.0</p>
  <p>Why: Just some text.</p>
  <p>Alternative: nothing</p>

      </li>
      <li>
        <p>Environment variable: <code class="xref std std-envvar literal notranslate">ANSIBLE_BECOME_EXE</code></p>

      </li>
      <li>
        <p>Environment variable: <code class="xref std std-envvar literal notranslate">ANSIBLE_FOO_EXE</code></p>
  <p>Removed in: version 3.0.0</p>
  <p>Why: Just some text.</p>
  <p>Alternative: nothing</p>

      </li>
      <li>
        <p>Variable: ansible_become_exe</p>

      </li>
      <li>
        <p>Variable: ansible_foo_exe</p>
  <p>Removed in: version 3.0.0</p>
  <p>Why: Just some text.</p>
  <p>Alternative: nothing</p>

      </li>
      <li>
        <p>Keyword: become_exe</p>

      </li>
      </ul>
    </div></td>
  </tr>
  <tr class="row-even">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-become_user"></div>
      <p class="ansible-option-title"><strong>become_user</strong></p>
      <a class="ansibleOptionLink" href="#parameter-become_user" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>User you &#x27;become&#x27; to execute the task.</p>
      <p class="ansible-option-line"><strong class="ansible-option-default-bold">Default:</strong> <code class="ansible-value literal notranslate ansible-option-default">&#34;root&#34;</code></p>
      <p class="ansible-option-line"><strong class="ansible-option-configuration">Configuration:</strong></p>
      <ul class="simple">
      <li>
        <p>INI entries</p>
        <div class="highlight-YAML+Jinja notranslate"><div class="highlight"><pre><span class="p p-Indicator">[</span><span class="nv">privilege_escalation</span><span class="p p-Indicator">]</span>
  <span class="l l-Scalar l-Scalar-Plain">become_user = root</span></pre></div></div>
        <p><em class="ansible-option-versionadded">added in ns2.col 0.1.0</em></p>

        <div class="highlight-YAML+Jinja notranslate"><div class="highlight"><pre><span class="p p-Indicator">[</span><span class="nv">foo_become_plugin</span><span class="p p-Indicator">]</span>
  <span class="l l-Scalar l-Scalar-Plain">user = root</span></pre></div></div>

      </li>
      <li>
        <p>Environment variable: <code class="xref std std-envvar literal notranslate">ANSIBLE_BECOME_USER</code></p>
        <p><em class="ansible-option-versionadded">added in ns2.col 0.1.0</em></p>

      </li>
      <li>
        <p>Environment variable: <code class="xref std std-envvar literal notranslate">ANSIBLE_FOO_USER</code></p>

      </li>
      <li>
        <p>Variable: ansible_become_user</p>

      </li>
      <li>
        <p>Variable: ansible_foo_user</p>
        <p><em class="ansible-option-versionadded">added in ns2.col 0.1.0</em></p>

      </li>
      <li>
        <p>Keyword: become_user</p>
        <p><em class="ansible-option-versionadded">added in ns2.col 0.1.0</em></p>

      </li>
      </ul>
    </div></td>
  </tr>
  </tbody>
  </table>



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

