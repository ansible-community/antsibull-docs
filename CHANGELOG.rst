===================================================================
antsibull-docs -- Ansible Documentation Build Scripts Release Notes
===================================================================

.. contents:: Topics


v1.3.0
======

Release Summary
---------------

Feature and bugfix release.

Minor Changes
-------------

- Ensure that values for ``default``, ``choices``, and ``sample`` use the types specified for the option / return value (https://github.com/ansible-community/antsibull-docs/pull/19).
- If a plugin or module has requirements listed, add a disclaimer next to the installation line at the top that further requirements are needed (https://github.com/ansible-community/antsibull-docs/issues/23, https://github.com/ansible-community/antsibull-docs/pull/24).
- Show the 'you might already have this collection installed if you are using the ``ansible`` package' disclaimer for plugins only for official docsite builds (subcommands ``devel`` and ``stable``). Also include this disclaimer for roles on official docsite builds (https://github.com/ansible-community/antsibull-docs/pull/25).
- Use ``true`` and ``false`` for booleans instead of ``yes`` and ``no`` (https://github.com/ansible-community/community-topics/issues/116, https://github.com/ansible-community/antsibull-docs/pull/19).
- When processing formatting directives, make sure to properly escape all other text for RST respectively HTML instead of including it verbatim (https://github.com/ansible-community/antsibull-docs/issues/21, https://github.com/ansible-community/antsibull-docs/pull/22).

Bugfixes
--------

- Improve indentation of HTML blocks for tables to avoid edge cases which generate invalid RST (https://github.com/ansible-community/antsibull-docs/pull/22).

v1.2.2
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Fix rstcheck-core support (https://github.com/ansible-community/antsibull-docs/pull/20).

v1.2.1
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Do not escape ``<``, ``>``, ``&``, and ``'`` in JSONified defaults and examples as the `Jinja2 tojson filter <https://jinja.palletsprojects.com/en/2.11.x/templates/#tojson>`_ does. Also improve formatting by making sure ``,`` is followed by a space (https://github.com/ansible-community/antsibull-docs/pull/18).
- The collection filter was ignored when parsing the ``ansible-galaxy collection list`` output for the docs build (https://github.com/ansible-community/antsibull-docs/issues/16, https://github.com/ansible-community/antsibull-docs/pull/17).

v1.2.0
======

Release Summary
---------------

Feature and bugfix release.

Minor Changes
-------------

- Support plugin ``seealso`` from the `semantic markup specification <https://hackmd.io/VjN60QSoRSSeRfvGmOH1lQ?both>`__ (https://github.com/ansible-community/antsibull-docs/pull/8).
- The ``lint-collection-docs`` subcommand has a new boolean flag ``--plugin-docs`` which renders the plugin docs to RST and validates them with rstcheck. This can be used as a lighter version of rendering the docsite in CI (https://github.com/ansible-community/antsibull-docs/pull/12).
- The files in the source repository now follow the `REUSE Specification <https://reuse.software/spec/>`_. The only exceptions are changelog fragments in ``changelogs/fragments/`` (https://github.com/ansible-community/antsibull-docs/pull/14).

Bugfixes
--------

- Make sure that ``_input`` does not show up twice for test or filter arguments when the plugin mentions it in ``positional`` (https://github.com/ansible-community/antsibull-docs/pull/10).
- Mark rstcheck 4.x and 5.x as compatible. Support rstcheck 6.x as well (https://github.com/ansible-community/antsibull-docs/pull/13).

v1.1.0
======

Release Summary
---------------

Feature release with support for ansible-core 2.14's sidecar docs feature.

Minor Changes
-------------

- If lookup plugins have a single return value starting with ``_``, that return value is now labelled ``Return value`` (https://github.com/ansible-community/antsibull-docs/pull/6).
- If lookup plugins have an option called ``_terms``, it is now shown in its own section ``Terms``, and not in the regular ``Parameters`` section (https://github.com/ansible-community/antsibull-docs/pull/6).
- More robust handling of parsing errors when ansible-doc was unable to extract documentation (https://github.com/ansible-community/antsibull-docs/pull/6).
- Support parameter type ``any``, and show ``raw`` as ``any`` (https://github.com/ansible-community/antsibull-docs/pull/6).
- Support test and filter plugins when ansible-core 2.14+ is used. This works with the current ``devel`` branch of ansible-core (https://github.com/ansible-community/antsibull-docs/pull/6).

v1.0.1
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Make sure that aliases of module/plugin options and return values that result in identical RST labels under docutil's normalization are only emitted once (https://github.com/ansible-community/antsibull-docs/pull/7).
- Properly escape module/plugin option and return value slugs in generated HTML (https://github.com/ansible-community/antsibull-docs/pull/7).

v1.0.0
======

Release Summary
---------------

First stable release.

Major Changes
-------------

- From version 1.0.0 on, antsibull-docs is sticking to semantic versioning and aims at providing no backwards compatibility breaking changes **to the command line API (antsibull-docs)** during a major release cycle. We explicitly exclude code compatibility. **antsibull-docs is not supposed to be used as a library,** and when used as a library it might not conform to semantic versioning (https://github.com/ansible-community/antsibull-docs/pull/2).

Minor Changes
-------------

- Only mention 'These are the collections with docs hosted on docs.ansible.com' for ``stable`` and ``devel`` subcommands (https://github.com/ansible-community/antsibull-docs/pull/3).
- Stop using some API from antsibull-core that is being removed (https://github.com/ansible-community/antsibull-docs/pull/1).

v0.1.0
======

Release Summary
---------------

Initial release. The ``antsibull-docs`` tool is compatible to the one from antsibull 0.43.0.
