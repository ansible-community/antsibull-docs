

ns2.col.sub.foo3 module -- A sub-foo
++++++++++++++++++++++++++++++++++++

This module is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.sub.foo3`.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Foo sub bar.
- See \ :literal:`foo\_param\_1` (of role `ns2.col.foo <foo_role.rst>`__, entrypoint main)\  for a random role parameter reference. And \ :literal:`foo\_param\_2=42` (of role `ns2.col.foo <foo_role.rst>`__, entrypoint main)\  for one with a value.








Parameters
----------

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
      <div class="ansibleOptionAnchor" id="parameter-bar"></div>
      <p style="display: inline;"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </div></td>
    <td>
      <p>Some bar.</p>
      <p>See <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns2/col/foo_role.html#parameter-main--foo_param_1"><span class="std std-ref"><span class="pre">foo_param_1</span></span></a></strong></code> for a random role parameter reference. And <code class="ansible-option-value literal notranslate"><a class="reference internal" href="../../ns2/col/foo_role.html#parameter-main--foo_param_2"><span class="std std-ref"><span class="pre">foo_param_2=42</span></span></a></code> for one with a value.</p>
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

  * - .. _ansible_collections.ns2.col.sub.foo3_module__attribute-action_group:

      **action_group**

    - 
      Action groups: \ns2.col.bar\_group, ns2.col.foo\_group


    - 
      Use \ :literal:`group/ns2.col.foo\_group`\  or \ :literal:`group/ns2.col.bar\_group`\  in \ :literal:`module\_defaults`\  to set defaults for this module.



  * - .. _ansible_collections.ns2.col.sub.foo3_module__attribute-check_mode:

      **check_mode**

    - 
      Support: full



    - 
      Can run in check\_mode and return changed status prediction without modifying target



  * - .. _ansible_collections.ns2.col.sub.foo3_module__attribute-diff_mode:

      **diff_mode**

    - 
      Support: N/A



    - 
      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode



  * - .. _ansible_collections.ns2.col.sub.foo3_module__attribute-platform:

      **platform**

    - 
      Platform:posix


    - 
      Target OS/families that can be operated against






Examples
--------

.. code-block:: yaml

    
    - name: Do some foobar
      ns2.col.sub.foo3:
        bar: baz





Return Values
-------------
The following are the fields unique to this module:

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
      <div class="ansibleOptionAnchor" id="return-bar"></div>
      <p style="display: inline;"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#return-bar" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </div></td>
    <td>
      <p>Some bar.</p>
      <p>Referencing myself as <code class="ansible-return-value literal notranslate"><a class="reference internal" href="#return-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></code>.</p>
      <p>Do not confuse with <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></strong></code>.</p>
      <p style="margin-top: 8px;"><span style="font-weight: 700;">Returned:</span> success</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><span style="color: black; font-weight: 700;">Sample:</span> <code>&#34;baz&#34;</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Another one (@ansible-community)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

