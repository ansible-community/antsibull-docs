.. Created with antsibull-docs

ns2.col.foo connection -- Foo connection :literal:`bar` (`link <#parameter-bar>`_)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This connection plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: ``ns2.col.foo``.

New in ns2.col 1.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This is for the :literal:`foo` connection.








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
        <span style="color: purple;">integer</span>
      </p>

    </td>
    <td valign="top">
      <p>Foo bar.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-host"></div>
      <p style="display: inline;"><strong>host</strong></p>
      <a class="ansibleOptionLink" href="#parameter-host" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Hostname to connect to.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;inventory_hostname&#34;</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: inventory_hostname</p>

      </li>
      <li>
        <p>Variable: ansible_host</p>

      </li>
      <li>
        <p>Variable: ansible_ssh_host</p>

      </li>
      <li>
        <p>Variable: delegated_vars[&#39;ansible_host&#39;]</p>

      </li>
      <li>
        <p>Variable: delegated_vars[&#39;ansible_ssh_host&#39;]</p>

      </li>
      </ul>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- Some note. :strong:`Something in bold`. :literal:`And in code`. :emphasis:`And in italics`. An URL: \ `https://example.org <https://example.org>`__.
- And another one. \ `A link <https://example.com>`__.







Authors
~~~~~~~

- ansible (@core)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__
