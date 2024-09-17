.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns.col2.foo3 module -- Foo III
++++++++++++++++++++++++++++++

This module is part of the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ (version 0.0.1).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns.col2`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ns.col2.foo3_module_requirements_>`_ for details.

To use it in a playbook, specify: ``ns.col2.foo3``.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Does some foo on the remote host.



.. _ansible_collections.ns.col2.foo3_module_requirements:

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

  * - .. _ansible_collections.ns.col2.foo3_module__attribute-check_mode:

      **check_mode**

    - Support: full



    -
      Can run in check\_mode and return changed status prediction without modifying target



  * - .. _ansible_collections.ns.col2.foo3_module__attribute-diff_mode:

      **diff_mode**

    - Support: full



    -
      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode



  * - .. _ansible_collections.ns.col2.foo3_module__attribute-platform:

      **platform**

    - Platform:posix


    -
      Target OS/families that can be operated against






Examples
--------

.. code-block:: yaml

    This is not YAML.






Authors
~~~~~~~

- Someone else (@ansible)




There were some errors parsing the documentation for this plugin.  Please file a bug with the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_.

The errors were:

* ::

        Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema
        return -> bar -> type
          Input should be 'any', 'bits', 'bool', 'bytes', 'complex', 'dict', 'float', 'int', 'json', 'jsonarg', 'list', 'path', 'sid', 'str', 'pathspec' or 'pathlist' (type=literal_error; expected='any', 'bits', 'bool', 'bytes', 'complex', 'dict', 'float', 'int', 'json', 'jsonarg', 'list', 'path', 'sid', 'str', 'pathspec' or 'pathlist')
        return -> baz
          Input should be a valid dictionary or instance of OuterReturnSchema (type=model_type; class_name=OuterReturnSchema)
