=====================
Ns.Col1 Release Notes
=====================

.. contents:: Topics

This changelog describes changes after version 1.0.2.

v2.3.0-pre
==========

Release Summary
---------------

Just testing with pre-releases.

v2.2.0
======

Release Summary
---------------

Testing long changelog fragments. Nothing else in this release. Ignore the fragment contents!

Minor Changes
-------------

- And a final complex reStructuredText fragment.

  The way to import a PowerShell or C# module util from a collection has changed in the Ansible 2.9 release. In Ansible
  2.8 a util was imported with the following syntax:

  .. code-block:: powershell

      #AnsibleRequires -CSharpUtil AnsibleCollections.namespace_name.collection_name.util_filename
      #AnsibleRequires -PowerShell AnsibleCollections.namespace_name.collection_name.util_filename

  In Ansible 2.9 this was changed to:

  .. code-block:: powershell

      #AnsibleRequires -CSharpUtil ansible_collections.namespace_name.collection_name.plugins.module_utils.util_filename
      #AnsibleRequires -PowerShell ansible_collections.namespace_name.collection_name.plugins.module_utils.util_filename

  The change in the collection import name also requires any C# util namespaces to be updated with the newer name
  format. This is more verbose but is designed to make sure we avoid plugin name conflicts across separate plugin types
  and to standardise how imports work in PowerShell with how Python modules work.
- This is an example of a longer reStructuredText fragment.

  Ansible 2.9 handles "unsafe" data more robustly, ensuring that data marked "unsafe" is not templated. In previous versions, Ansible recursively marked all data returned by the direct use of ``lookup()`` as "unsafe", but only marked structured data returned by indirect lookups using ``with_X`` style loops as "unsafe" if the returned elements were strings. Ansible 2.9 treats these two approaches consistently.

  As a result, if you use ``with_dict`` to return keys with templatable values, your templates may no longer work as expected in Ansible 2.9.

  To allow the old behavior, switch from using ``with_X`` to using ``loop`` with a filter as described at :ref:`migrating_to_loop`.
- This is an example of a more complex reStructuredText fragment.

  Module and module_utils files can now use relative imports to include other module_utils files.
  This is useful for shortening long import lines, especially in collections.

  Example of using a relative import in collections:

  .. code-block:: python

    # File: ansible_collections/my_namespace/my_collection/plugins/modules/my_module.py
    # Old way to use an absolute import to import module_utils from the collection:
    from ansible_collections.my_namespace.my_collection.plugins.module_utils import my_util
    # New way using a relative import:
    from ..module_utils import my_util

  Modules and module_utils shipped with Ansible can use relative imports as well but the savings
  are smaller:

  .. code-block:: python

    # File: ansible/modules/system/ping.py
    # Old way to use an absolute import to import module_utils from core:
    from ansible.module_utils.basic import AnsibleModule
    # New way using a relative import:
    from ...module_utils.basic import AnsibleModule

  Each single dot (``.``) represents one level of the tree (equivalent to ``../`` in filesystem relative links).

  .. seealso:: `The Python Relative Import Docs <https://www.python.org/dev/peps/pep-0328/#guido-s-decision>`_ go into more detail of how to write relative imports.

Bugfixes
--------

- Renamed ``master`` git branch to ``main``.

v2.1.0
======

Release Summary
---------------

Bob was there, too!

Bugfixes
--------

- bob lookup - forgot to check whether ``Bob`` was already there.

New Plugins
-----------

Lookup
~~~~~~

- ns.col1.bob - Bob was there, too

v2.0.0
======

Release Summary
---------------

We're happy to release 2.0.0 with a new plugin!

Bugfixes
--------

- reverse lookup - fix bug in error message.

New Plugins
-----------

Lookup
~~~~~~

- ns.col1.reverse - reverse magic
