.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns.col2.foo2 module -- Foo two
++++++++++++++++++++++++++++++

This module is part of the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ (version 0.0.1).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns.col2`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ns.col2.foo2_module_requirements_>`_ for details.

To use it in a playbook, specify: ``ns.col2.foo2``.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Does some foo on the remote host.
- A broken reference :ref:`asdfasdfoobarTHISDOESNOTEXIST <asdfasdfoobarTHISDOESNOTEXIST>`.
- The option :literal:`foo` (`link <#parameter-foo>`_) exists, but :literal:`foobar` (`link <#parameter-foobar>`_) does not.
- The return value :literal:`bar` (`link <#return-bar>`_) exists, but :literal:`barbaz` (`link <#return-barbaz>`_) does not.
- Again existing: :literal:`foo=1` (of module `ns.col2.foo <foo_module.rst>`__)\ , :literal:`bar=2` (of module `ns.col2.foo <foo_module.rst>`__)
- Again not existing: :literal:`foobar=1` (of module `ns.col2.foo <foo_module.rst>`__)\ , :literal:`barbaz=2` (of module `ns.col2.foo <foo_module.rst>`__)
- :literal:`\ ` :emphasis:`\ ` :strong:`\ ` :literal:`\ `   :ref:`\  <>` :literal:`\ ` :literal:`` (`link <#parameter->`_) :literal:`` (`link <#return->`_) :literal:``
- Foo bar baz. Bamm - Bar baz
  bam bum.
  Bumm - Foo bar
  baz bam!



.. _ansible_collections.ns.col2.foo2_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- Foo.






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
      <p style="display: inline;"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=integer</span>
      </p>
    </td>
    <td valign="top">
      <p>Bar.</p>
      <p>Some <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-broken%2520markup"><span class="std std-ref"><span class="pre">broken markup</span></span></a></strong></code>.</p>
      <p>Foo bar baz. Bamm - Bar baz
      bam bum.
      Bumm - Foo bar
      baz bam!</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-foo"></div>
      <p style="display: inline;"><strong>foo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-foo" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The foo source.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-subfoo"></div>
      <p style="display: inline;"><strong>subfoo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-subfoo" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Some recursive foo.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-subfoo/BaZ"></div>
      <p style="display: inline;"><strong>BaZ</strong></p>
      <a class="ansibleOptionLink" href="#parameter-subfoo/BaZ" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>
    </td>
    <td valign="top">
      <p>Funky.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-subfoo/foo"></div>
      <p style="display: inline;"><strong>foo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-subfoo/foo" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>A sub foo.</p>
      <p>Whatever.</p>
      <p>Also required when <em>subfoo</em> is specified when <em>foo=bar</em> or <code class='docutils literal notranslate'>baz</code>.</p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="#return-foobarbaz"><span class="std std-ref"><span class="pre">foobarbaz</span></span></a></code> does not exist.</p>
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

  * - .. _ansible_collections.ns.col2.foo2_module__attribute-check_mode:

      **check_mode**

    - Support: full



    -
      Can run in check\_mode and return changed status prediction without modifying target



  * - .. _ansible_collections.ns.col2.foo2_module__attribute-diff_mode:

      **diff_mode**

    - Support: full



    -
      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode

      Foo bar baz. Bamm - Bar baz
      bam bum.
      Bumm - Foo bar
      baz bam!



  * - .. _ansible_collections.ns.col2.foo2_module__attribute-platform:

      **platform**

    - Platform:posix

      The module :strong:`ERROR while parsing`\ : While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN is not using an FQCN.

      Sometimes our markup is :strong:`ERROR while parsing`\ : While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter

      Foo bar baz. Bamm - Bar baz
      bam bum.
      Bumm - Foo bar
      baz bam!


    -
      Target OS/families that can be operated against




Notes
-----

- Foo bar baz. Bamm - Bar baz
  bam bum.
  Bumm - Foo bar
  baz bam!

See Also
--------

* `ns.col2.foo3 <foo3_module.rst>`__

  Foo III.
* `ns.col2.foobarbaz <foobarbaz_module.rst>`__

  The official documentation on the **ns.col2.foobarbaz** module.
* `ns.col2.foo4 <foo4_module.rst>`__ module plugin

  Markup reference linting test.
* `ns.col2.foobarbaz <foobarbaz_inventory.rst>`__ inventory plugin

  The official documentation on the **ns.col2.foobarbaz** inventory plugin.
* `ansible.builtin.service <service_module.rst>`__

  The service module.
* `ansible.builtin.foobarbaz <foobarbaz_module.rst>`__

  A non-existing module.
* `ansible.builtin.linear <linear_strategy.rst>`__ strategy plugin

  The linear strategy plugin.
* `ansible.builtin.foobarbaz <foobarbaz_strategy.rst>`__ strategy plugin

  Foo bar baz. Bamm - Bar baz
  bam bum.
  Bumm - Foo bar
  baz bam!

Examples
--------

.. code-block:: yaml

    name: This is YAML.




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
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;baz&#34;</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Someone else (@ansible)
