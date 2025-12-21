.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns.col2.extra role
++++++++++++++++++

The documentation for the role plugin, ns.col2.extra, was malformed.

The errors were:

* ::

        63 validation errors for RoleSchema
        entry_points -> baz -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 0 -> description
          Field required (type=missing)
        entry_points -> main -> seealso -> 0 -> link
          Field required (type=missing)
        entry_points -> main -> seealso -> 0 -> name
          Field required (type=missing)
        entry_points -> main -> seealso -> 0 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 0 -> module
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 0 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 0 -> plugin
          Field required (type=missing)
        entry_points -> main -> seealso -> 0 -> plugin_type
          Field required (type=missing)
        entry_points -> main -> seealso -> 0 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 0 -> module
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 0 -> description
          Field required (type=missing)
        entry_points -> main -> seealso -> 0 -> ref
          Field required (type=missing)
        entry_points -> main -> seealso -> 0 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 0 -> module
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 1 -> description
          Field required (type=missing)
        entry_points -> main -> seealso -> 1 -> link
          Field required (type=missing)
        entry_points -> main -> seealso -> 1 -> name
          Field required (type=missing)
        entry_points -> main -> seealso -> 1 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 1 -> module
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 1 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 1 -> plugin
          Field required (type=missing)
        entry_points -> main -> seealso -> 1 -> plugin_type
          Field required (type=missing)
        entry_points -> main -> seealso -> 1 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 1 -> module
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 1 -> description
          Field required (type=missing)
        entry_points -> main -> seealso -> 1 -> ref
          Field required (type=missing)
        entry_points -> main -> seealso -> 1 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 1 -> module
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 2 -> description
          Field required (type=missing)
        entry_points -> main -> seealso -> 2 -> link
          Field required (type=missing)
        entry_points -> main -> seealso -> 2 -> name
          Field required (type=missing)
        entry_points -> main -> seealso -> 2 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 2 -> plugin
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 2 -> plugin_type
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 2 -> module
          Field required (type=missing)
        entry_points -> main -> seealso -> 2 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 2 -> plugin
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 2 -> plugin_type
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 2 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 2 -> description
          Field required (type=missing)
        entry_points -> main -> seealso -> 2 -> ref
          Field required (type=missing)
        entry_points -> main -> seealso -> 2 -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 2 -> plugin
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> seealso -> 2 -> plugin_type
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> options -> bar -> options -> subbar -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> options -> bar -> options -> subfoo -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> options -> bar -> mutually_exclusive -> 1
          Input should be a valid list (type=list_type)
        entry_points -> main -> options -> bar -> required_together -> 1
          Input should be a valid list (type=list_type)
        entry_points -> main -> options -> bar -> required_one_of -> 1
          Input should be a valid list (type=list_type)
        entry_points -> main -> options -> bar -> required_if -> 1
          Input should be a valid tuple (type=tuple_type)
        entry_points -> main -> options -> bar -> required_if -> 2 -> 0
          Field required (type=missing)
        entry_points -> main -> options -> bar -> required_if -> 2 -> 1
          Field required (type=missing)
        entry_points -> main -> options -> bar -> required_if -> 2 -> 2
          Field required (type=missing)
        entry_points -> main -> options -> bar -> required_if -> 2 -> 3
          Field required (type=missing)
        entry_points -> main -> options -> bar -> required_if -> 3 -> 2
          Field required (type=missing)
        entry_points -> main -> options -> bar -> required_if -> 3 -> 3
          Field required (type=missing)
        entry_points -> main -> options -> bar -> required_if -> 4
          Tuple should have at most 4 items after validation, not 5 (type=too_long; field_type=Tuple; max_length=4; actual_length=5)
        entry_points -> main -> options -> bar -> required_if -> 5 -> 2
          Input should be a valid list (type=list_type)
        entry_points -> main -> options -> bar -> required_if -> 5 -> 3
          Input should be a valid boolean, unable to interpret input (type=bool_parsing)
        entry_points -> main -> options -> bar -> required_by -> else
          Input should be a valid list (type=list_type)
        entry_points -> main -> options -> foo -> extra
          Extra inputs are not permitted (type=extra_forbidden)
        entry_points -> main -> extra
          Extra inputs are not permitted (type=extra_forbidden)


File a bug with the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ in order to have it corrected.
