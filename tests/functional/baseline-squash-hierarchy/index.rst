.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>


.. _plugins_in_ns2.col:

Ns2.Col
=======

Collection version 2.1.0

.. contents::
   :local:
   :depth: 1

Description
-----------

This is a description.
With multiple paragraphs.

**Author:**

* Ansible (https://github.com/ansible)

**Supported ansible-core versions:**

* 2.11.0 or newer
* older than 2.99.0
* version 2.12.2 is specifically not supported

.. ansible-links::

  - title: "Issue Tracker"
    url: "https://github.com/ansible-collections/community.general/issues"
    external: true
  - title: "Homepage"
    url: "https://github.com/ansible-collections/community.crypto"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/ansible-collections/community.internal_test_tools"
    external: true
  - title: "Submit a bug report"
    url: "https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug_report.md"
    external: true



.. Communication

.. _communication_for_ns2.col:

Communication
-------------

- Forum: `Ansible Forum <https://forum.ansible.com/>`__.
- Matrix room :literal:`#users:ansible.im`: `General usage and support questions <https://matrix.to/#/#users:ansible.im>`__.
- IRC channel :literal:`#ansible` (Libera network):
  `General usage and support questions <https://web.libera.chat/?channel=#ansible>`__.
- Mailing list: `Ansible Project List <https://groups.google.com/g/ansible-project>`__.
  (`Subscribe <mailto:ansible-project+subscribe@googlegroups.com?subject=subscribe>`__)

.. toctree::
    :maxdepth: 1

Changelog
---------

.. toctree::
    :maxdepth: 1

    changelog

Guides
------

.. toctree::
    :maxdepth: 1

    docsite/filter_guide

Plugin Index
------------

These are the plugins in the ns2.col collection:


Modules
~~~~~~~

* :ansplugin:`foo module <ns2.col.foo#module>` -- Do some foo :ansopt:`ns2.col.foo#module:bar`
* :ansplugin:`foo2 module <ns2.col.foo2#module>` -- Another foo
* :ansplugin:`sub.foo3 module <ns2.col.sub.foo3#module>` -- A sub-foo

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_module
    foo2_module
    sub.foo3_module


Become Plugins
~~~~~~~~~~~~~~

* :ansplugin:`foo become <ns2.col.foo#become>` -- Use foo :ansopt:`ns2.col.foo#become:bar` :ansdeprecatedmarker:`{"date": "", "version": "5.0.0"}`

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_become


Cache Plugins
~~~~~~~~~~~~~

* :ansplugin:`foo cache <ns2.col.foo#cache>` -- Foo files :ansopt:`ns2.col.foo#cache:bar`

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_cache


Callback Plugins
~~~~~~~~~~~~~~~~

* :ansplugin:`foo callback <ns2.col.foo#callback>` -- Foo output :ansopt:`ns2.col.foo#callback:bar`

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_callback


Cliconf Plugins
~~~~~~~~~~~~~~~

* :ansplugin:`foo cliconf <ns2.col.foo#cliconf>` -- Foo router CLI config

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_cliconf


Connection Plugins
~~~~~~~~~~~~~~~~~~

* :ansplugin:`foo connection <ns2.col.foo#connection>` -- Foo connection :ansopt:`ns2.col.foo#connection:bar`

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_connection


Filter Plugins
~~~~~~~~~~~~~~

* :ansplugin:`bar filter <ns2.col.bar#filter>` -- The bar filter
* :ansplugin:`foo filter <ns2.col.foo#filter>` -- The foo filter :ansopt:`ns2.col.foo#filter:bar`

.. toctree::
    :maxdepth: 1
    :hidden:

    bar_filter
    foo_filter


Inventory Plugins
~~~~~~~~~~~~~~~~~

* :ansplugin:`foo inventory <ns2.col.foo#inventory>` -- The foo inventory :ansopt:`ns2.col.foo#inventory:bar`

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_inventory


Lookup Plugins
~~~~~~~~~~~~~~

* :ansplugin:`foo lookup <ns2.col.foo#lookup>` -- Look up some foo :ansopt:`ns2.col.foo#lookup:bar`

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_lookup


Shell Plugins
~~~~~~~~~~~~~

* :ansplugin:`foo shell <ns2.col.foo#shell>` -- Foo shell :ansopt:`ns2.col.foo#shell:bar`

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_shell


Strategy Plugins
~~~~~~~~~~~~~~~~

* :ansplugin:`foo strategy <ns2.col.foo#strategy>` -- Executes tasks in foo

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_strategy


Test Plugins
~~~~~~~~~~~~

* :ansplugin:`bar test <ns2.col.bar#test>` -- Is something a bar
* :ansplugin:`foo test <ns2.col.foo#test>` -- Is something a foo :ansopt:`ns2.col.foo#test:bar`

.. toctree::
    :maxdepth: 1
    :hidden:

    bar_test
    foo_test


Vars Plugins
~~~~~~~~~~~~

* :ansplugin:`foo vars <ns2.col.foo#vars>` -- Load foo :ansopt:`ns2.col.foo#vars:bar`

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_vars


Role Index
----------

These are the roles in the ns2.col collection:

* :ansplugin:`foo role <ns2.col.foo#role>` -- Foo role :ansdeprecatedmarker:`{"date": "2020-01-01", "version": ""}`

.. toctree::
    :maxdepth: 1
    :hidden:

    foo_role
