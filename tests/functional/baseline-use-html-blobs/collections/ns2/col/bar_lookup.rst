
.. Document meta

:orphan:
:github_url: https://github.com/ansible-community/antsibull-docs/edit/main/tests/functional/collections/ansible_collections/ns2/col/plugins/lookup/bar.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns2.col.bar_lookup:

.. Anchors: short name for ansible.builtin

.. Title

ns2.col.bar lookup -- Look up some bar
++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This lookup plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.bar`.

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

- This one is private.


.. Aliases


.. Requirements




.. Terms

Terms
-----

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
      <div class="ansibleOptionAnchor" id="parameter-_terms"></div>
      <p class="ansible-option-title"><strong>Terms</strong></p>
      <a class="ansibleOptionLink" href="#parameter-_terms" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">list</span>
        / <span class="ansible-option-elements">elements=dictionary</span>
        / <span class="ansible-option-required">required</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>Something</p>
    </div></td>
  </tr>
  </tbody>
  </table>






.. Options


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: Look up!
      ansible.builtin.debug:
        msg: "{{ lookup('ns2.col.bar', {}) }}"




.. Facts


.. Return values

Return Value
------------

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
      <div class="ansibleOptionAnchor" id="return-_raw"></div>
      <p class="ansible-option-title"><strong>Return value</strong></p>
      <a class="ansibleOptionLink" href="#return-_raw" title="Permalink to this return value"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">list</span>
        / <span class="ansible-option-elements">elements=dictionary</span>
      </p>
    </div></td>
    <td><div class="ansible-option-cell">
      <p>The resulting stuff.</p>
      <p class="ansible-option-line"><strong class="ansible-option-returned-bold">Returned:</strong> success</p>
    </div></td>
  </tr>
  </tbody>
  </table>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Felix Fontein (@felixfontein)


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

