.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns2.col.foo vars -- Load foo :literal:`bar` (`link <#parameter-bar>`_)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This vars plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns2.col`.
You need further requirements to be able to use this vars plugin,
see `Requirements <ansible_collections.ns2.col.foo_vars_requirements_>`_ for details.

To use it in a playbook, specify: ``ns2.col.foo``.

New in ns2.col 0.9.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Load some foo.
- This is so glorious.



.. _ansible_collections.ns2.col.foo_vars_requirements:

Requirements
------------
The below requirements are needed on the local controller node that executes this vars.

- Enabled in Ansible's configuration.






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
      <div class="ansibleOptionAnchor" id="parameter-_valid_extensions"></div>
      <p style="display: inline;"><strong>_valid_extensions</strong></p>
      <a class="ansibleOptionLink" href="#parameter-_valid_extensions" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>

    </td>
    <td valign="top">
      <p>All extensions to check.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">[&#34;.foo&#34;, &#34;.foobar&#34;]</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[defaults]
  foo_valid_extensions = .foo, .foobar</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_FOO_FILENAME_EXT</code></p>

      </li>
      </ul>
    </td>
  </tr>
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
      <p>Foo bar.</p>
    </td>
  </tr>
  </tbody>
  </table>












.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__
