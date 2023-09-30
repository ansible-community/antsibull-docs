
.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns2.flatcol.foo2 module -- Another foo
++++++++++++++++++++++++++++++++++++++

This module is part of the `ns2.flatcol collection <https://galaxy.ansible.com/ui/repo/published/ns2/flatcol/>`_.

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns2.flatcol`.

To use it in a playbook, specify: ``ns2.flatcol.foo2``.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Foo bar.
- See \ :literal:`foo\_param\_1` (of role `ns2.flatcol.foo <foo_role.rst>`__, entrypoint main)\  for a random role parameter reference. And \ :literal:`foo\_param\_2=42` (of role `ns2.flatcol.foo <foo_role.rst>`__, entrypoint main)\  for one with a value.








Parameters
----------

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
      <div class="ansibleOptionAnchor" id="parameter-bar"></div>
      <p style="display: inline;"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Some bar.</p>
      <p>See <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns2/flatcol/foo_role.html#parameter-main--foo_param_1"><span class="std std-ref"><span class="pre">foo_param_1</span></span></a></strong></code> for a random role parameter reference. And <code class="ansible-option-value literal notranslate"><a class="reference internal" href="../../ns2/flatcol/foo_role.html#parameter-main--foo_param_2"><span class="std std-ref"><span class="pre">foo_param_2=42</span></span></a></code> for one with a value.</p>
    </td>
  </tr>
  </tbody>
  </table>






Examples
--------

.. code-block:: yaml

    
    - name: Do some foo
      ns2.flatcol.foo2:
        bar: foo





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

- Another one (@ansible-community)




