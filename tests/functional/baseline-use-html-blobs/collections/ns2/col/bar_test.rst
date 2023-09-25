
.. Document meta

:orphan:
:github_url: https://github.com/ansible-community/antsibull-docs/edit/main/tests/functional/collections/ansible_collections/ns2/col/plugins/test/bar.yml?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns2.col.bar_test:

.. Anchors: short name for ansible.builtin

.. Title

ns2.col.bar test -- Is something a bar
++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This test plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.bar`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Check whether a path is a bar.


.. Aliases

Aliases: is_bar

.. Requirements





.. Input

Input
-----

This describes the input of the test, the value before ``is ns2.col.bar`` or ``is not ns2.col.bar``.

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
      <div class="ansibleOptionAnchor" id="parameter-_input"></div>
      <p class="ansible-option-title"><strong>Input</strong></p>
      <a class="ansibleOptionLink" href="#parameter-_input" title="Permalink to this option"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">path</span>
      </p>

    </div></td>
    <td><div class="ansible-option-cell">
      <p>A path.</p>
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

    is_path_bar: "{{ '/etc/hosts' is ns2.col.bar }}}"




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
      <div class="ansibleOptionAnchor" id="return-_value"></div>
      <p class="ansible-option-title"><strong>Return value</strong></p>
      <a class="ansibleOptionLink" href="#return-_value" title="Permalink to this return value"></a>
      <p class="ansible-option-type-line">
        <span class="ansible-option-type">boolean</span>
      </p>
    </div></td>
    <td><div class="ansible-option-cell">
      <p>Returns <code class='docutils literal notranslate'>true</code> if the path is a bar, <code class='docutils literal notranslate'>false</code> if it is not a bar.</p>
      <p class="ansible-option-line"><strong class="ansible-option-returned-bold">Returned:</strong> success</p>
    </div></td>
  </tr>
  </tbody>
  </table>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Ansible Core


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

