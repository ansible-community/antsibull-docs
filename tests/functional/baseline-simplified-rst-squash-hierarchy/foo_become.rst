

ns2.col.foo become -- Use foo \ :literal:`bar` (`link <parameter-bar_>`_)\ 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This become plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.foo`.


.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in: version 5.0.0
:Why: Just some text.
      This one has more than one line.
      And one more.

:Alternative: I don't know
              of any
              alternative.


Synopsis
--------

- This become plugin uses foo.
- This is a second paragraph.








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
      <p><span style="font-style: italic; font-size: small; color: darkgreen;">added in ns2.col 1.2.0</span></p>
  <p>Removed in: version 4.0.0</p>
  <p>Why: Just some other text.
  This one has more than one line though.
  One more.
  </p>
  <p>Alternative: nothing
  relevant
  I know of
  </p>

    </div></td>
    <td>
      <p>Bar. <b>BAR!</b></p>
      <p>Totally unrelated to <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-become_user"><span class="std std-ref"><span class="pre">become_user</span></span></a></strong></code>. Even with <code class="ansible-option-value literal notranslate"><a class="reference internal" href="#parameter-become_user"><span class="std std-ref"><span class="pre">become_user=foo</span></span></a></code>.</p>
      <p>Might not be compatible when <code class="ansible-option literal notranslate"><strong><a class="reference internal" href="#parameter-become_user"><span class="std std-ref"><span class="pre">become_user</span></span></a></strong></code> is <code class="ansible-value literal notranslate">bar</code>, though.</p>
    </td>
  </tr>
  <tr style="height: 100%;">
    <td style="height: inherit; display: flex; flex-direction: row;"><div style="padding: 8px 16px; border-top: 1px solid #000000; height: inherit; flex: 1 0 auto; white-space: nowrap; max-width: 100%;">
      <div class="ansibleOptionAnchor" id="parameter-become_exe"></div>
      <p style="display: inline;"><strong>become_exe</strong></p>
      <a class="ansibleOptionLink" href="#parameter-become_exe" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><span style="font-style: italic; font-size: small; color: darkgreen;">added in ns2.col 0.2.0</span></p>

    </div></td>
    <td>
      <p>Foo executable.</p>
      <p style="margin-top: 8px;"><span style="color: blue; font-weight: 700;">Default:</span> <code style="color: blue;">&#34;foo&#34;</code></p>
      <p style="margin-top: 8px;"><span style="font-weight: 700;">Configuration:</span></p>
      <ul>
      <li>
        <p>INI entries</p>
        <pre>[privilege_escalation]
  become_exe = foo</pre>

        <pre>[foo_become_plugin]
  executable = foo</pre>
  <p>Removed in: version 3.0.0</p>
  <p>Why: Just some text.</p>
  <p>Alternative: nothing</p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_BECOME_EXE</code></p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_FOO_EXE</code></p>
  <p>Removed in: version 3.0.0</p>
  <p>Why: Just some text.</p>
  <p>Alternative: nothing</p>

      </li>
      <li>
        <p>Variable: ansible_become_exe</p>

      </li>
      <li>
        <p>Variable: ansible_foo_exe</p>
  <p>Removed in: version 3.0.0</p>
  <p>Why: Just some text.</p>
  <p>Alternative: nothing</p>

      </li>
      <li>
        <p>Keyword: become_exe</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr style="height: 100%;">
    <td style="height: inherit; display: flex; flex-direction: row;"><div style="padding: 8px 16px; border-top: 1px solid #000000; height: inherit; flex: 1 0 auto; white-space: nowrap; max-width: 100%;">
      <div class="ansibleOptionAnchor" id="parameter-become_user"></div>
      <p style="display: inline;"><strong>become_user</strong></p>
      <a class="ansibleOptionLink" href="#parameter-become_user" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </div></td>
    <td>
      <p>User you &#x27;become&#x27; to execute the task.</p>
      <p style="margin-top: 8px;"><span style="color: blue; font-weight: 700;">Default:</span> <code style="color: blue;">&#34;root&#34;</code></p>
      <p style="margin-top: 8px;"><span style="font-weight: 700;">Configuration:</span></p>
      <ul>
      <li>
        <p>INI entries</p>
        <pre>[privilege_escalation]
  become_user = root</pre>
        <p><span style="font-style: italic; font-size: small; color: darkgreen;">added in ns2.col 0.1.0</span></p>

        <pre>[foo_become_plugin]
  user = root</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_BECOME_USER</code></p>
        <p><span style="font-style: italic; font-size: small; color: darkgreen;">added in ns2.col 0.1.0</span></p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_FOO_USER</code></p>

      </li>
      <li>
        <p>Variable: ansible_become_user</p>

      </li>
      <li>
        <p>Variable: ansible_foo_user</p>
        <p><span style="font-style: italic; font-size: small; color: darkgreen;">added in ns2.col 0.1.0</span></p>

      </li>
      <li>
        <p>Keyword: become_user</p>
        <p><span style="font-style: italic; font-size: small; color: darkgreen;">added in ns2.col 0.1.0</span></p>

      </li>
      </ul>
    </td>
  </tr>
  </tbody>
  </table>










Status
------

- This become will be removed in version 5.0.0.
  *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Nobody 


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

