
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

* ::

        6 validation errors for ModuleDocSchema
        doc -> short_description
          field required (type=value_error.missing)
        doc -> seealso
          value is not a valid list (type=type_error.list)
        doc -> options -> bar -> description -> 0
          str type expected (type=type_error.str)
        doc -> options -> bar -> type
          string does not match regex "^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$)
        doc -> options -> foo
          value is not a valid dict (type=type_error.dict)
        doc -> options -> subfoo -> bam
          extra fields not permitted (type=value_error.extra)


File a bug with the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ in order to have it corrected.