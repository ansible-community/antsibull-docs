
.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns2.col.bar lookup -- Look up some bar
++++++++++++++++++++++++++++++++++++++

This lookup plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.bar`.

New in ns2.col 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This one is private.






Terms
-----

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
      <div class="ansibleOptionAnchor" id="parameter-_terms"></div>
      <p style="display: inline;"><strong>Terms</strong></p>
      <a class="ansibleOptionLink" href="#parameter-_terms" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=dictionary</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>Something</p>
    </td>
  </tr>
  </tbody>
  </table>










Examples
--------

.. code-block:: yaml

    
    - name: Look up!
      ansible.builtin.debug:
        msg: "{{ lookup('ns2.col.bar', {}) }}"





Return Value
------------

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
      <div class="ansibleOptionAnchor" id="return-_raw"></div>
      <p style="display: inline;"><strong>Return value</strong></p>
      <a class="ansibleOptionLink" href="#return-_raw" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>The resulting stuff.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Felix Fontein (@felixfontein)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

