.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns2.col.foo test -- Is something a foo :literal:`bar` (`link <#parameter-bar>`_)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This test plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: ``ns2.col.foo``.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Check whether the input dictionary is a foo.







Input
-----

This describes the input of the test, the value before ``is ns2.col.foo`` or ``is not ns2.col.foo``.

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
      <div class="ansibleOptionAnchor" id="parameter-_input"></div>
      <p style="display: inline;"><strong>Input</strong></p>
      <a class="ansibleOptionLink" href="#parameter-_input" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>Something to test.</p>
    </td>
  </tr>
  </tbody>
  </table>





Keyword parameters
------------------

This describes keyword parameters of the test. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
examples: ``input is ns2.col.foo(key1=value1, key2=value2, ...)`` and ``input is not ns2.col.foo(key1=value1, key2=value2, ...)``

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
  </tbody>
  </table>






Examples
--------

.. code-block:: yaml

    some_var: "{{ {'a': 1} is ns2.col.foo }}"




Return Value
------------

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
      <div class="ansibleOptionAnchor" id="return-_value"></div>
      <p style="display: inline;"><strong>Return value</strong></p>
      <a class="ansibleOptionLink" href="#return-_value" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Whether the input is a foo.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
    </td>
  </tr>
  </tbody>
  </table>




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
