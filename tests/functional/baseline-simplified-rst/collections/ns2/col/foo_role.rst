.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns2.col.foo role -- Foo role
++++++++++++++++++++++++++++

This role is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run :code:`ansible-galaxy collection list`.

To install it use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.foo`.

.. contents::
   :local:
   :depth: 2


Entry point ``main`` -- Foo role
--------------------------------

New in ns2.col 0.2.0

DEPRECATED
^^^^^^^^^^
:Removed in: major release after 2020-01-01
:Why: Just some text.
      This one has more than one line.
      And one more.
:Alternative: I don't know
              of any
              alternative.

Synopsis
^^^^^^^^

- This is the foo role.
- If you set :literal:`foo\_param\_1` (`link <#parameter-main--foo_param_1>`_) while :literal:`foo\_param\_2=3` (`link <#parameter-main--foo_param_2>`_)\ , this might behave funny.


Parameters
^^^^^^^^^^

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
      <div class="ansibleOptionAnchor" id="parameter-main--foo_param_1"></div>
      <p style="display: inline;"><strong>foo_param_1</strong></p>
      <a class="ansibleOptionLink" href="#parameter-main--foo_param_1" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>A string parameter</p>
      <p>If you set <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-main--foo_param_1"><span class="std std-ref"><span class="pre">foo_param_1</span></span></a></strong></code> while <code class="ansible-option-value literal notranslate"><a class="reference internal" href="#parameter-main--foo_param_2"><span class="std std-ref"><span class="pre">foo_param_2=3</span></span></a></code>, this might behave funny.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-main--foo_param_2"></div>
      <p style="display: inline;"><strong>foo_param_2</strong></p>
      <a class="ansibleOptionLink" href="#parameter-main--foo_param_2" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>

    </td>
    <td valign="top">
      <p>An integer parameter with a default.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">13</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Attributes
^^^^^^^^^^

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Attribute
    - Support
    - Description

  * - .. _ansible_collections.ns2.col.foo_role__attribute-main__check_mode:

      **check_mode**

    - Support: full



    -
      Can run in check\_mode and return changed status prediction without modifying target



  * - .. _ansible_collections.ns2.col.foo_role__attribute-main__platform:

      **platform**

    - Platforms:Linux, macOS, FreeBSD


    -
      The supported platforms





See Also
^^^^^^^^

* `ns2.col.foo <foo_module.rst>`__

  The official documentation on the **ns2.col.foo** module.

Examples
^^^^^^^^

.. code-block:: yaml

    - name: Use role
      include_role: ns2.col.foo
      vars:
        foo_param_1: foobar
        foo_param_2: 23


Authors
^^^^^^^

- Felix Fontein (@felixfontein)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__
