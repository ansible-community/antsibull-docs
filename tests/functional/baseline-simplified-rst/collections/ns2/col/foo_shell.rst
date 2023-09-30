
.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns2.col.foo shell -- Foo shell \ :literal:`bar` (`link <parameter-bar_>`_)\ 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This shell plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: ``ns2.col.foo``.

New in ns2.col 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This is for the foo shell.








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
      <p>Foo bar.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-remote_tmp"></div>
      <p style="display: inline;"><strong>remote_tmp</strong></p>
      <a class="ansibleOptionLink" href="#parameter-remote_tmp" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible-base 2.10</i></p>

    </td>
    <td valign="top">
      <p>Temporary directory to use on targets when executing tasks.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;~/.ansible/tmp&#34;</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[defaults]
  remote_tmp = ~/.ansible/tmp</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_REMOTE_TEMP</code></p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_REMOTE_TMP</code></p>

      </li>
      <li>
        <p>Variable: ansible_remote_tmp</p>

      </li>
      </ul>
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

