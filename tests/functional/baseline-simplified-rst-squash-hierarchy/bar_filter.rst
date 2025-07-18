.. Created with antsibull-docs

ns2.col.bar filter -- The bar filter
++++++++++++++++++++++++++++++++++++

This filter plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ui/repo/published/ns2/col/>`_ (version 2.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: ``ns2.col.bar``.

New in ns2.col 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Do some barring.







Input
-----

This describes the input of the filter, the value before ``| ns2.col.bar``.

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
      <p>The main input.</p>
    </td>
  </tr>
  </tbody>
  </table>





Positional parameters
---------------------

This describes positional parameters of the filter. These are the values ``positional1``, ``positional2`` and so on in the following
example: ``input | ns2.col.bar(positional1, positional2, ...)``

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
      <div class="ansibleOptionAnchor" id="parameter-foo"></div>
      <p style="display: inline;"><strong>foo</strong></p>
      <a class="ansibleOptionLink" href="#parameter-foo" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=dictionary</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>Some foo.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-bar"></div>
      <p style="display: inline;"><strong>bar</strong></p>
      <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>And some bar.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  </tbody>
  </table>




Keyword parameters
------------------

This describes keyword parameters of the filter. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
example: ``input | ns2.col.bar(key1=value1, key2=value2, ...)``

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
      <div class="ansibleOptionAnchor" id="parameter-baz"></div>
      <p style="display: inline;"><strong>baz</strong></p>
      <a class="ansibleOptionLink" href="#parameter-baz" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Something else.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li>
          <p><code>&#34;a&#34;</code>:
          Whatever <code class='docutils literal notranslate'>a</code> is.</p>
        </li>
        <li>
          <p><code>&#34;b&#34;</code>:
          What is <code class='docutils literal notranslate'>b</code>? I don&#x27;t know.</p>
        </li>
        <li>
          <p><code>&#34;cde&#34;</code>:
          This is some more unknown. There are rumors this is related to the alphabet.</p>
        </li>
        <li>
          <p><code style="color: blue;"><b>&#34;foo&#34;</b></code> <span style="color: blue;">(default)</span>:
          Our default value, the glorious <code class='docutils literal notranslate'>foo</code>.</p>
          <p>Even has two paragraphs.</p>
        </li>
      </ul>

    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters:
  ``input | ns2.col.bar(positional1, positional2, key1=value1, key2=value2)``


Examples
--------

.. code-block:: yaml

    {'a': 1} | ns2.col.bar({'b': 2}, baz='cde')




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
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>The result.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
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
