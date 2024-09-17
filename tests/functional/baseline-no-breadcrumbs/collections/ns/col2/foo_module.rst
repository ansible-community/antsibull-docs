.. Document meta section

:orphan:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Document body

.. Anchors

.. _ansible_collections.ns.col2.foo_module:

.. Title

ns.col2.foo module
++++++++++++++++++


The documentation for the module plugin, ns.col2.foo,  was malformed.

The errors were:

* .. code-block:: text

        7 validation errors for ModuleDocSchema
        doc -> short_description
          Field required (type=missing)
        doc -> seealso
          Input should be a valid list (type=list_type)
        doc -> options -> bar -> description -> 0
          Input should be a valid string (type=string_type)
        doc -> options -> bar -> description -> 1
          Input should be a valid string (type=string_type)
        doc -> options -> bar -> type
          Input should be 'any', 'bits', 'bool', 'bytes', 'dict', 'float', 'int', 'json', 'jsonarg', 'list', 'path', 'raw', 'sid', 'str', 'tmppath', 'pathspec' or 'pathlist' (type=literal_error; expected='any', 'bits', 'bool', 'bytes', 'dict', 'float', 'int', 'json', 'jsonarg', 'list', 'path', 'raw', 'sid', 'str', 'tmppath', 'pathspec' or 'pathlist')
        doc -> options -> foo
          Input should be a valid dictionary or instance of ModuleOptionsSchema (type=model_type; class_name=ModuleOptionsSchema)
        doc -> options -> subfoo -> bam
          Extra inputs are not permitted (type=extra_forbidden)


File a bug with the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ in order to have it corrected.
