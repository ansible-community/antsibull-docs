

ns2.col.foo cache -- Foo files \ :literal:`bar` (`link <parameter-bar_>`_)\ 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This cache plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.foo`.

New in ns2.col 1.9.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Cache foo files.








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
      <div class="ansibleOptionAnchor" id="parameter-_uri"></div>
      <p style="display: inline;"><strong>_uri</strong></p>
      <a class="ansibleOptionLink" href="#parameter-_uri" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">path</span>
        / <span style="color: red;">required</span>
      </p>

    </div></td>
    <td>
      <p>Path in which the cache plugin will save the foo files.</p>
      <p style="margin-top: 8px;"><span style="font-weight: 700;">Configuration:</span></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[defaults]
  fact_caching_connection = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_CACHE_PLUGIN_CONNECTION</code></p>

      </li>
      </ul>
    </td>
  </tr>
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
      <p>Nothing.</p>
    </td>
  </tr>
  </tbody>
  </table>











Authors
~~~~~~~

- Ansible Core (@ansible-core)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

