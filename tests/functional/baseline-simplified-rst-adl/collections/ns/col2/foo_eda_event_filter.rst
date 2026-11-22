.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns.col2.foo event filter -- Do fancy stuff
++++++++++++++++++++++++++++++++++++++++++

This EDA event filter plugin is part of the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ (version 0.0.1).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible\-galaxy collection install ns.col2`.

To use it in a playbook, specify: ``ns.col2.foo``.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This is some fancy filter.








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
      <div class="ansibleOptionAnchor" id="parameter-foobar"></div>
      <p style="display: inline;"><strong>foobar</strong></p>
      <a class="ansibleOptionLink" href="#parameter-foobar" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>Something.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

    </td>
  </tr>
  </tbody>
  </table>






Examples
--------

.. code-block:: yaml

    - ns.col2.bar:
      filters:
        - ns.col2.foo:
            overwrite: false
