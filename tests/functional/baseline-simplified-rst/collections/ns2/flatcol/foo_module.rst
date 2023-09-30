
.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns2.flatcol.foo module -- Do some foo \ :literal:`bar` (`link <parameter-bar_>`_)\ 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ns2.flatcol collection <https://galaxy.ansible.com/ui/repo/published/ns2/flatcol/>`_.

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns2.flatcol`.

To use it in a playbook, specify: ``ns2.flatcol.foo``.

New in ns2.flatcol 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Does some foo on the remote host.
- Whether foo is magic or not has not yet been determined.








Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th colspan="2"><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-bar"></div>
      <div class="ansibleOptionAnchor" id="parameter-baz"></div>
      <p style="display: inline;"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;"><span style="color: darkgreen; white-space: normal;">aliases: baz</span></p>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=integer</span>
      </p>
    </td>
    <td valign="top">
      <p>A bar.</p>
      <p>Independent from <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-foo"><span class="std std-ref"><span class="pre">foo</span></span></a></strong></code>.</p>
      <p>Do not confuse with <code class="ansible-return-value literal notranslate"><a class="reference internal" href="#return-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></code>.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-foo"></div>
      <p style="display: inline;"><strong>foo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-foo" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>The foo source.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-subfoo"></div>
      <div class="ansibleOptionAnchor" id="parameter-subbaz"></div>
      <p style="display: inline;"><strong>subfoo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-subfoo" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;"><span style="color: darkgreen; white-space: normal;">aliases: subbaz</span></p>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ns2.flatcol 2.0.0</i></p>
    </td>
    <td valign="top">
      <p>Some recursive foo.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-subfoo/foo"></div>
      <div class="ansibleOptionAnchor" id="parameter-subbaz/foo"></div>
      <div class="ansibleOptionAnchor" id="parameter-subfoo/bam"></div>
      <div class="ansibleOptionAnchor" id="parameter-subbaz/bam"></div>
      <p style="display: inline;"><strong>foo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-subfoo/foo" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;"><span style="color: darkgreen; white-space: normal;">aliases: bam</span></p>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>A sub foo.</p>
      <p>Whatever.</p>
      <p>Also required when <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-subfoo"><span class="std std-ref"><span class="pre">subfoo</span></span></a></strong></code> is specified when <code class="ansible-option-value literal notranslate"><a class="reference internal" href="#parameter-foo"><span class="std std-ref"><span class="pre">foo=bar</span></span></a></code> or <code class="ansible-value literal notranslate">baz</code>.</p>
      <p>Note that <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-subfoo/foo"><span class="std std-ref"><span class="pre">subfoo.foo</span></span></a></strong></code> is the same as <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-subbaz/foo"><span class="std std-ref"><span class="pre">subbaz.foo</span></span></a></strong></code>, <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-subbaz/bam"><span class="std std-ref"><span class="pre">subbaz.bam</span></span></a></strong></code>, and <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-subfoo/bam"><span class="std std-ref"><span class="pre">subfoo.bam</span></span></a></strong></code>.</p>
      <p><code class="xref std std-envvar literal notranslate">FOOBAR1</code>, <code class="xref std std-envvar literal notranslate">FOOBAR2</code>, <code class="xref std std-envvar literal notranslate">FOOBAR3</code>, <code class="xref std std-envvar literal notranslate">FOOBAR4</code>.</p>
    </td>
  </tr>

  </tbody>
  </table>






Examples
--------

.. code-block:: yaml

    
    - name: Do some foo
      ns2.flatcol.foo:
        foo: '{{ foo }}'
        bar:
          - 1
          - 2
          - 3
        subfoo:
          foo: hoo!





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

- Ansible Core Team
- Someone else (@ansible)




