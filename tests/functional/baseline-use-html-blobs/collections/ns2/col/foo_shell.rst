
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
      <div class="ansibleOptionAnchor" id="parameter-remote_tmp"></div>
      <p class="ansible-option-title"><strong>remote_tmp</strong></p>
      <a class="ansibleOptionLink" href="#parameter-remote_tmp" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>
      <p><span class="ansible-option-versionadded">added in ansible-base 2.10</span></p>

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

