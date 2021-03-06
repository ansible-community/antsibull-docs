===================================================================
antsibull-docs -- Ansible Documentation Build Scripts Release Notes
===================================================================

.. contents:: Topics


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
