

ns2.col.bar test -- Is something a bar
++++++++++++++++++++++++++++++++++++++

This test plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.bar`.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Check whether a path is a bar.


Aliases: is_bar





Input
-----

This describes the input of the test, the value before ``is ns2.col.bar`` or ``is not ns2.col.bar``.

.. raw:: html

  <table style="width: 100%; height: 1px;">
  <thead>
  <tr>
    <th><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr style="height: 100%;">
    <td style="height: inherit; display: flex; flex-direction: row;"><div style="padding: 8px 16px; border-top: 1px solid #000000; height: inherit; flex: 1 0 auto; white-space: nowrap; max-width: 100%;">
      <div class="ansibleOptionAnchor" id="parameter-_input"></div>
      <p style="display: inline;"><strong>Input</strong></p>
      <a class="ansibleOptionLink" href="#parameter-_input" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">path</span>
      </p>

    </div></td>
    <td>
      <p>A path.</p>
    </td>
  </tr>
  </tbody>
  </table>









Examples
--------

.. code-block:: yaml

    is_path_bar: "{{ '/etc/hosts' is ns2.col.bar }}}"





Return Value
------------

.. raw:: html

  <table style="width: 100%; height: 1px;">
  <thead>
  <tr>
    <th><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr style="height: 100%;">
    <td style="height: inherit; display: flex; flex-direction: row;"><div style="padding: 8px 16px; border-top: 1px solid #000000; height: inherit; flex: 1 0 auto; white-space: nowrap; max-width: 100%;">
      <div class="ansibleOptionAnchor" id="return-_value"></div>
      <p style="display: inline;"><strong>Return value</strong></p>
      <a class="ansibleOptionLink" href="#return-_value" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </div></td>
    <td>
      <p>Returns <code class='docutils literal notranslate'>true</code> if the path is a bar, <code class='docutils literal notranslate'>false</code> if it is not a bar.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Ansible Core


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

