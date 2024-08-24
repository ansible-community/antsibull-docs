.. Document meta

:orphan:
:github_url: https://github.com/ansible-community/antsibull-docs/edit/main/tests/functional/collections/ansible_collections/ns2/col/plugins/connection/foo.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns2.col.foo_connection:

.. Anchors: short name for ansible.builtin

.. Title

ns2.col.foo connection -- Foo connection :ansopt:`ns2.col.foo#connection:bar`
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This connection plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.foo`.

.. version_added

.. rst-class:: ansible-version-added

New in ns2.col 1.2.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This is for the :literal:`foo` connection.


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
        <span class="ansible-option-type">integer</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>Foo bar.</p>
    </div></td>
  </tr>
  <tr class="row-odd">
    <td><div class="ansible-option-cell">
      <div class="ansibleOptionAnchor" id="parameter-host"></div>
      <p class="ansible-option-title"><strong>host</strong></p>
      <a class="ansibleOptionLink" href="#parameter-host" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">string</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>Hostname to connect to.</p>
      <p class="ansible-option-line"><strong class="ansible-option-default-bold">Default:</strong> <code class="ansible-value literal notranslate ansible-option-default">&#34;inventory_hostname&#34;</code></p>
      <p class="ansible-option-line"><strong class="ansible-option-configuration">Configuration:</strong></p>
      <ul class="simple">
      <li>
        <p>Variable: inventory_hostname</p>

      </li>
      <li>
        <p>Variable: ansible_host</p>

      </li>
      <li>
        <p>Variable: ansible_ssh_host</p>

      </li>
      <li>
        <p>Variable: delegated_vars[&#39;ansible_host&#39;]</p>

      </li>
      <li>
        <p>Variable: delegated_vars[&#39;ansible_ssh_host&#39;]</p>

      </li>
      </ul>
    </div></td>
  </tr>
  </tbody>
  </table>



.. Attributes


.. Notes

Notes
-----

.. note::
   - Some note. :strong:`Something in bold`. :literal:`And in code`. :emphasis:`And in italics`. An URL: \ `https://example.org <https://example.org>`__.
   - And another one. \ `A link <https://example.com>`__.

.. Seealso


.. Examples



.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- ansible (@core)


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
