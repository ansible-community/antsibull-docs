
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
      <div class="ansibleOptionAnchor" id="parameter-admin_users"></div>
      <p class="ansible-option-title"><strong>admin_users</strong></p>
      <a class="ansibleOptionLink" href="#parameter-admin_users" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">list</span>
        / <span class="ansible-option-elements">elements=string</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>list of users to be expected to have admin privileges. This is used by the controller to determine how to share temporary files between the remote user and the become user.</p>
      <p class="ansible-option-line"><span class="ansible-option-default-bold">Default:</span> <span class="ansible-option-default">[&#34;root&#34;, &#34;toor&#34;]</span></p>
      <p class="ansible-option-line"><span class="ansible-option-configuration">Configuration:</span></p>
      <ul class="simple">
      <li>
        <p>INI entry</p>
        <div class="highlight-YAML+Jinja notranslate"><div class="highlight"><pre><span class="p p-Indicator">[</span><span class="nv">defaults</span><span class="p p-Indicator">]</span>
  <span class="l l-Scalar l-Scalar-Plain">admin_users = root, toor</span></pre></div></div>

      </li>
      <li>
        <p>Environment variable: ANSIBLE_ADMIN_USERS</p>

      </li>
      <li>
        <p>Variable: ansible_admin_users</p>

      </li>
      </ul>
    </div></td>
  </tr>
  <tr class="row-odd">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-async_dir"></div>
      <p class="ansible-option-title"><strong>async_dir</strong></p>
      <a class="ansibleOptionLink" href="#parameter-async_dir" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>Directory in which ansible will keep async job information</p>
      <p class="ansible-option-line"><span class="ansible-option-default-bold">Default:</span> <span class="ansible-option-default">&#34;~/.ansible_async&#34;</span></p>
      <p class="ansible-option-line"><span class="ansible-option-configuration">Configuration:</span></p>
      <ul class="simple">
      <li>
        <p>INI entry</p>
        <div class="highlight-YAML+Jinja notranslate"><div class="highlight"><pre><span class="p p-Indicator">[</span><span class="nv">defaults</span><span class="p p-Indicator">]</span>
  <span class="l l-Scalar l-Scalar-Plain">async_dir = ~/.ansible_async</span></pre></div></div>

      </li>
      <li>
        <p>Environment variable: ANSIBLE_ASYNC_DIR</p>

      </li>
      <li>
        <p>Variable: ansible_async_dir</p>

      </li>
      </ul>
    </div></td>
  </tr>
  <tr class="row-even">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-common_remote_group"></div>
      <p class="ansible-option-title"><strong>common_remote_group</strong></p>
      <a class="ansibleOptionLink" href="#parameter-common_remote_group" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>
      <p><span class="ansible-option-versionadded">added in ansible-base 2.10</span></p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>Checked when Ansible needs to execute a module as a different user.</p>
      <p>If setfacl and chown both fail and do not let the different user access the module&#x27;s files, they will be chgrp&#x27;d to this group.</p>
      <p>In order for this to work, the remote_user and become_user must share a common group and this setting must be set to that group.</p>
      <p class="ansible-option-line"><span class="ansible-option-configuration">Configuration:</span></p>
      <ul class="simple">
      <li>
        <p>INI entry</p>
        <div class="highlight-YAML+Jinja notranslate"><div class="highlight"><pre><span class="p p-Indicator">[</span><span class="nv">defaults</span><span class="p p-Indicator">]</span>
  <span class="l l-Scalar l-Scalar-Plain">common_remote_group = VALUE</span></pre></div></div>

      </li>
      <li>
        <p>Environment variable: ANSIBLE_COMMON_REMOTE_GROUP</p>

      </li>
      <li>
        <p>Variable: ansible_common_remote_group</p>

      </li>
      </ul>
    </div></td>
  </tr>
  <tr class="row-odd">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-environment"></div>
      <p class="ansible-option-title"><strong>environment</strong></p>
      <a class="ansibleOptionLink" href="#parameter-environment" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">list</span>
        / <span class="ansible-option-elements">elements=dictionary</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>List of dictionaries of environment variables and their values to use when executing commands.</p>
      <p class="ansible-option-line"><span class="ansible-option-default-bold">Default:</span> <span class="ansible-option-default">[{}]</span></p>
    </div></td>
  </tr>
  <tr class="row-even">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-remote_tmp"></div>
      <p class="ansible-option-title"><strong>remote_tmp</strong></p>
      <a class="ansibleOptionLink" href="#parameter-remote_tmp" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>Temporary directory to use on targets when executing tasks.</p>
      <p class="ansible-option-line"><span class="ansible-option-default-bold">Default:</span> <span class="ansible-option-default">&#34;~/.ansible/tmp&#34;</span></p>
      <p class="ansible-option-line"><span class="ansible-option-configuration">Configuration:</span></p>
      <ul class="simple">
      <li>
        <p>INI entry</p>
        <div class="highlight-YAML+Jinja notranslate"><div class="highlight"><pre><span class="p p-Indicator">[</span><span class="nv">defaults</span><span class="p p-Indicator">]</span>
  <span class="l l-Scalar l-Scalar-Plain">remote_tmp = ~/.ansible/tmp</span></pre></div></div>

      </li>
      <li>
        <p>Environment variable: ANSIBLE_REMOTE_TEMP</p>

      </li>
      <li>
        <p>Environment variable: ANSIBLE_REMOTE_TMP</p>

      </li>
      <li>
        <p>Variable: ansible_remote_tmp</p>

      </li>
      </ul>
    </div></td>
  </tr>
  <tr class="row-odd">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-system_tmpdirs"></div>
      <p class="ansible-option-title"><strong>system_tmpdirs</strong></p>
      <a class="ansibleOptionLink" href="#parameter-system_tmpdirs" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">list</span>
        / <span class="ansible-option-elements">elements=string</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>List of valid system temporary directories on the managed machine for Ansible to validate <code class='docutils literal notranslate'>remote_tmp</code> against, when specific permissions are needed.  These must be world readable, writable, and executable. This list should only contain directories which the system administrator has pre-created with the proper ownership and permissions otherwise security issues can arise.</p>
      <p>When <code class='docutils literal notranslate'>remote_tmp</code> is required to be a system temp dir and it does not match any in the list, the first one from the list will be used instead.</p>
      <p class="ansible-option-line"><span class="ansible-option-default-bold">Default:</span> <span class="ansible-option-default">[&#34;/var/tmp&#34;, &#34;/tmp&#34;]</span></p>
      <p class="ansible-option-line"><span class="ansible-option-configuration">Configuration:</span></p>
      <ul class="simple">
      <li>
        <p>INI entry</p>
        <div class="highlight-YAML+Jinja notranslate"><div class="highlight"><pre><span class="p p-Indicator">[</span><span class="nv">defaults</span><span class="p p-Indicator">]</span>
  <span class="l l-Scalar l-Scalar-Plain">system_tmpdirs = /var/tmp, /tmp</span></pre></div></div>

      </li>
      <li>
        <p>Environment variable: ANSIBLE_SYSTEM_TMPDIRS</p>

      </li>
      <li>
        <p>Variable: ansible_system_tmpdirs</p>

      </li>
      </ul>
    </div></td>
  </tr>
  <tr class="row-even">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-world_readable_temp"></div>
      <p class="ansible-option-title"><strong>world_readable_temp</strong></p>
      <a class="ansibleOptionLink" href="#parameter-world_readable_temp" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">boolean</span>
      </p>
      <p><span class="ansible-option-versionadded">added in ansible-base 2.10</span></p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>This makes the temporary files created on the machine world-readable and will issue a warning instead of failing the task.</p>
      <p>It is useful when becoming an unprivileged user.</p>
      <p class="ansible-option-line"><span class="ansible-option-choices">Choices:</span></p>
      <ul class="simple">
        <li><p><span class="ansible-option-default-bold">false</span> <span class="ansible-option-default">← (default)</span></p></li>
        <li><p><span class="ansible-option-choices-entry">true</span></p></li>
      </ul>

      <p class="ansible-option-line"><span class="ansible-option-configuration">Configuration:</span></p>
      <ul class="simple">
      <li>
        <p>INI entry</p>
        <div class="highlight-YAML+Jinja notranslate"><div class="highlight"><pre><span class="p p-Indicator">[</span><span class="nv">defaults</span><span class="p p-Indicator">]</span>
  <span class="l l-Scalar l-Scalar-Plain">allow_world_readable_tmpfiles = false</span></pre></div></div>

      </li>
      <li>
        <p>Environment variable: ANSIBLE_SHELL_ALLOW_WORLD_READABLE_TEMP</p>

      </li>
      <li>
        <p>Variable: ansible_shell_allow_world_readable_temp</p>

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

