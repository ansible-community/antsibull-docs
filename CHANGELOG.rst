===================================================================
antsibull-docs -- Ansible Documentation Build Scripts Release Notes
===================================================================

.. contents:: Topics

v2.17.0
=======

Release Summary
---------------

Feature and bugfix release.

Minor Changes
-------------

- Extend deprecation/removal note that collections can be installed manually after removal (https://github.com/ansible-community/antsibull-docs/pull/371).

Bugfixes
--------

- Make sure that all errors are caught during documentation normalization. Until now exceptions derived from ``BaseException`` that are not derived from ``Exception`` are not handled correctly (https://github.com/ansible-community/antsibull-docs/pull/389).

v2.16.3
=======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Fix rendering of ``HORIZONTALLINE`` in reStructuredText output. An earlier fix for leading whitespace mangled the resulting ``raw`` directive (https://github.com/ansible-community/antsibull-docs/pull/370).
- When ``choices`` are provided as a dictionary with explanations, links to options, return values, modules, plugins, and roles were not correctly rendered (https://github.com/ansible-community/antsibull-docs/pull/369).

v2.16.2
=======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Fix role section heading levels. Examples and attributes should be below role entrypoints (https://github.com/ansible-community/antsibull-docs/issues/366, https://github.com/ansible-community/antsibull-docs/pull/367).

v2.16.1
=======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Also consider action plugin redirects/deprecations in runtime metadata for modules, since for users there is no difference. Also ``ansible.builtin.yum`` only has a action plugin redirect to ``ansible.builtin.dnf``, so this is needed to ensure that a stub page generated for ``ansible.builtin.yum`` (https://github.com/ansible-community/antsibull-docs/pull/360).

v2.16.0
=======

Release Summary
---------------

Feature release.

Minor Changes
-------------

- Allow to cancel collection deprecations (https://github.com/ansible-community/antsibull-docs/pull/352).
- Declare support for Python 3.13 (https://github.com/ansible-community/antsibull-docs/pull/349).
- antsibull-docs now depends on antsibull-core >= 3.4.0 (https://github.com/ansible-community/antsibull-docs/pull/352).

v2.15.0
=======

Release Summary
---------------

Bugfix and feature release which migrates to Pydantic 2.

Minor Changes
-------------

- Migrated all models to Pydantic 2. This is mostly transparent, except that validation error messages slightly change, and that some validation is more strict. For example, if a boolean is used instead of a string, say in a description, this now results in an error instead of a silent coercion. Numbers are still accepted for strings (for example ``version_added`` with float values like ``2.14``) (https://github.com/ansible-community/antsibull-docs/pull/331, https://github.com/ansible-community/antsibull-core/pull/333, https://github.com/ansible-community/antsibull-core/pull/344).
- This project now depends on antsibull-core >= 3.2.0 and pydantic 2 (https://github.com/ansible-community/antsibull-docs/pull/330).
- Use Proxy configuration settings from the environment. Check out the `aiohttp documentation on Proxy support <https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support>`__ for information on which environment variables are supported (https://github.com/ansible/ansible-documentation/issues/1936, https://github.com/ansible-community/antsibull-docs/pull/346).
- Use language ``ini`` for example INI code blocks (https://github.com/ansible-community/antsibull-docs/pull/335).
- When rendering the Ansible docsite with the ``stable`` and ``devel`` subcommands, information on deprecated collections is shown (https://github.com/ansible-community/ansible-build-data/pull/450, https://github.com/ansible-community/antsibull-docs/pull/330).
- When rendering the Ansible docsite with the ``stable`` and ``devel`` subcommands, stub pages for removed collections are added (https://github.com/ansible-community/ansible-build-data/pull/459, https://github.com/ansible-community/antsibull-docs/pull/341).

v2.14.0
=======

Release Summary
---------------

Feature release.

Minor Changes
-------------

- Add dependency on antsibull-fileutils. Some functionality from antsibull-core is moving there, so we can use it from there directly (https://github.com/ansible-community/antsibull-docs/pull/322).
- Add deprecation markers next to module/plugin/role descriptions in lists (https://github.com/ansible-community/antsibull-docs/issues/141, https://github.com/ansible-community/antsibull-docs/pull/320).
- Remove ansible-project Google Groups mailing list from ansible.builtin links (https://github.com/ansible-community/antsibull-docs/pull/325).

v2.13.1
=======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- The output filename used by the ``plugin`` subcommand contained two dots before the ``rst`` extension (https://github.com/ansible-community/antsibull-docs/issues/317, https://github.com/ansible-community/antsibull-docs/pull/318).

v2.13.0
=======

Release Summary
---------------

Bugfix and feature release.

Minor Changes
-------------

- Allow to disable adding the antsibull-docs version to the generated files with the ``--no-add-antsibull-docs-version`` command line flag, or the ``add_antsibull_docs_version = false`` setting in the antsibull-docs config file (https://github.com/ansible-community/antsibull-docs/issues/304, https://github.com/ansible-community/antsibull-docs/pull/308).
- Bump minimal required version of dependency antsibull-docs-parser to 1.1.0 This allows to use a new whitespace-removal feature (https://github.com/ansible-community/antsibull-docs/pull/312).
- If you are using `argcomplete <https://pypi.org/project/argcomplete/>`__, you can now tab-complete ``antsibull-docs`` command lines. See `Activating global completion <https://pypi.org/project/argcomplete/#activating-global-completion>`__ in the argcomplete README for how to enable tab completion globally. This will also tab-complete Ansible commands such as ``ansible-playbook`` and ``ansible-test`` (https://github.com/ansible-community/antsibull-docs/pull/302).
- Most documentation generating subcommands now have a ``--cleanup`` parameter which allows to delete files and directories that were not created by antsibull-docs in the destination directory (https://github.com/ansible-community/antsibull-docs/pull/315).
- No longer use ``rsync`` when creating a build script with the ``sphinx-init`` subcommand (https://github.com/ansible-community/antsibull-docs/pull/315).
- Remove superfluous whitespace or escaped spaces from templates (https://github.com/ansible-community/antsibull-docs/pull/313).
- Remove trailing whitespace and leading and trailing empty lines from rendered templates, and ensure they end with a newline if not empty (https://github.com/ansible-community/antsibull-docs/pull/314).

Bugfixes
--------

- Fix RST escaping of the title in the collections per namespace list. This causes a space to vanish between namespace name and the word ``Namespace`` with newer versions of antsibull-docs-parser (https://github.com/ansible-community/antsibull-docs/pull/311).

v2.12.0
=======

Release Summary
---------------

Bugfix and feature release.

Minor Changes
-------------

- Allow to mention forums in the Communication section of collection links (https://github.com/ansible-community/antsibull-docs/pull/288).
- Bump minimum dependency of ``antsibull-docs-parser`` to 1.0.2 or newer (https://github.com/ansible-community/antsibull-docs/pull/290).
- The ``lint-collection-docs`` subcommand will now complain about unchanged default values in ``docs/docsite/links.yml`` taken from the `community collection template <https://github.com/ansible-collections/collection_template/>`__ (https://github.com/ansible-community/antsibull-docs/issues/273, https://github.com/ansible-community/antsibull-docs/pull/277).
- The collection docs linter now reports empty markup, like ``I()``, ``L(,https://example.com)`` (https://github.com/ansible-community/antsibull-docs/pull/292).

Bugfixes
--------

- Improve handling of empty markup parameters for RST (https://github.com/ansible-community/antsibull-docs/pull/290).
- Improve rendering of empty or broken changelogs (https://github.com/ansible-community/antsibull-docs/pull/289).
- Remove leading spaces in paragraphs to avoid unintended RST blockquotes (https://github.com/ansible-community/antsibull-docs/pull/289).
- Render errors as code blocks of language ``text`` instead of using the default lexer (https://github.com/ansible-community/antsibull-docs/pull/289).

v2.11.0
=======

Release Summary
---------------

Feature and bugfix release.

Minor Changes
-------------

- Support examples for role entrypoints (https://github.com/ansible-community/antsibull-docs/pull/244).

Bugfixes
--------

- Fix handling of ``choices`` that are dictionaries for ``type=list`` (https://github.com/ansible-community/antsibull-docs/pull/276).
- Fix handling of ``default`` for ``type=list`` if ``choices`` is present (https://github.com/ansible-community/antsibull-docs/pull/276).

v2.10.0
=======

Release Summary
---------------

Bugfix and feature release.

Minor Changes
-------------

- It is now possible to render the collection changelog as part of the collection docsite by using the ``changelog`` option in ``docs/docsite/config.yml`` (https://github.com/ansible-community/antsibull-docs/issues/31, https://github.com/ansible-community/antsibull-docs/pull/267).

Bugfixes
--------

- Fix internal links to options and return values in simplified RST output (https://github.com/ansible-community/antsibull-docs/pull/269).
- Include role in role attribute references (https://github.com/ansible-community/antsibull-docs/pull/269).

v2.9.0
======

Release Summary
---------------

Maintenance release.

Minor Changes
-------------

- Add support for the antsibull-core v3 (https://github.com/ansible-community/antsibull-docs/pull/261).

v2.8.0
======

Release Summary
---------------

Bugfix and feature release.

Minor Changes
-------------

- Add support for "dark mode" to the option table styling (https://github.com/ansible-community/antsibull-docs/pull/253, https://github.com/ansible-community/antsibull-docs/pull/258).
- Add support for the latest antsibull-core v3 pre-release, ``3.0.0a1`` (https://github.com/ansible-community/antsibull-docs/pull/250).
- Declare support for Python 3.12 (https://github.com/ansible-community/antsibull-docs/pull/255).
- The colors used by the CSS provided by the Antsibull Sphinx extension can now be overridden (https://github.com/ansible-community/antsibull-docs/pull/254).

Bugfixes
--------

- Fix duplicate docs detection (for aliases) for latest ansible-core devel (https://github.com/ansible-community/antsibull-docs/pull/257).

v2.7.0
======

Release Summary
---------------

Bugfix and refactoring release.

Minor Changes
-------------

- Explicitly set up Galaxy context instead of relying on deprecated functionality (https://github.com/ansible-community/antsibull-docs/pull/234).

Bugfixes
--------

- Fix schema for ``seealso`` in role entrypoints. Plugin references now work (https://github.com/ansible-community/antsibull-docs/issues/237, https://github.com/ansible-community/antsibull-docs/pull/240).
- Make error reporting for invalid references in ``plugin`` ``seealso`` entries more precise (https://github.com/ansible-community/antsibull-docs/pull/240).
- Support new ``ansible-doc --json`` output field ``plugin_name`` (https://github.com/ansible-community/antsibull-docs/pull/242).
- Use certain fields from library context instead of app context that are deprecated in the app context and will be removed from antsibull-core 3.0.0 (https://github.com/ansible-community/antsibull-docs/pull/233).

v2.6.1
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- For role argument specs, allow ``author``, ``description``, and ``todo`` to be a string instead of a list of strings, similarly as with ansible-doc and with modules and plugins (https://github.com/ansible-community/antsibull-docs/pull/227).
- Make sure that title underlines have the correct width for wide Unicode characters (https://github.com/ansible-community/antsibull-docs/issues/228, https://github.com/ansible-community/antsibull-docs/pull/229).

v2.6.0
======

Release Summary
---------------

Fix parsing of ``EXAMPLES`` and improve error message

Minor Changes
-------------

- Improve error messages when calls to ``ansible-doc`` fail (https://github.com/ansible-community/antsibull-docs/pull/223).

Bugfixes
--------

- When ``EXAMPLES`` has the format specified by ``# fmt: <format>``, this value is used to determine the code block type (https://github.com/ansible-community/antsibull-docs/pull/225).

v2.5.0
======

Release Summary
---------------

Release to support the updated Ansible Galaxy codebase.

Minor Changes
-------------

- The default collection URL template has been changed from ``https://galaxy.ansible.com/{namespace}/{name}`` to ``https://galaxy.ansible.com/ui/repo/published/{namespace}/{name}/`` to adjust for the Galaxy codebase change on September 30th, 2023 (https://github.com/ansible-community/antsibull-docs/issues/147, https://github.com/ansible-community/antsibull-docs/pull/220).

v2.4.0
======

Release Summary
---------------

Bugfix and feature release. Improves support for other builders than ``html``.

There will be a follow-up release after `Ansible Galaxy <https://galaxy.ansible.com/>`__
switched to the new ``galaxy_ng`` codebase, which is scheduled for September 30th.
That release will only adjust the URLs to Galaxy, except potentially bugfixes.

Minor Changes
-------------

- Add basic support for other HTML based Sphinx builders such as ``epub`` and ``singlehtml`` (https://github.com/ansible-community/antsibull-docs/pull/201).
- Adjust default RST output to work better with Spinx's LaTeX builder (https://github.com/ansible-community/antsibull-docs/pull/195).
- Allow specifying wildcards for the collection names for the ``collections`` subcommand if ``--use-current`` is specified (https://github.com/ansible-community/antsibull-docs/pull/219).
- Antsibull-docs now depends on antsibull-core >= 2.1.0 (https://github.com/ansible-community/antsibull-docs/pull/209).
- Create collection links with a custom directive. This makes them compatible with builders other than the HTML builder (https://github.com/ansible-community/antsibull-docs/pull/200).
- Fix indent for nested options and return values with Spinx's LaTeX builder (https://github.com/ansible-community/antsibull-docs/pull/198).
- Improve linting of option and return value names in semantic markup with respect to array stubs: forbid array stubs for dictionaries if the dictionary is not the last part of the option (https://github.com/ansible-community/antsibull-docs/pull/208).
- Improve the info box for ``ansible.builtin`` plugins and modules to explain FQCN and link to the ``collection`` keyword docs (https://github.com/ansible-community/antsibull-docs/pull/218).
- Improve the info box for modules, plugins, and roles in collections to show note that they are not included in ``ansible-core`` and show instructions on how to check whether the collection is installed (https://github.com/ansible-community/antsibull-docs/pull/218).
- Insert the antsibull-docs version as a comment or metadata into the generated files (https://github.com/ansible-community/antsibull-docs/pull/205).
- Make sure that the antsibull Sphinx extension contains the correct version (same as antsibull-docs itself) and licensing information (GPL-3.0-or-later), and that the version is kept up-to-date for new releases (https://github.com/ansible-community/antsibull-docs/pull/202).
- Move roles from templates and structural styling from stylesheet to antsibull Sphinx extension. This makes sure that HTML tags such as ``<strong>`` and ``<em>`` are used for bold and italic texts, and that the same formattings are used for the LaTeX builder (https://github.com/ansible-community/antsibull-docs/pull/199).
- Support multiple filters in ``ansible-doc`` of ansible-core 2.16 and later. This makes building docsites and linting more efficient when documentation for more than one and less than all installed collections needs to be queried (https://github.com/ansible-community/antsibull-docs/issues/193, https://github.com/ansible-community/antsibull-docs/pull/213).
- The ``current`` subcommand now has a ``--skip-ansible-builtin`` option which skips building documentation for ``ansible.builtin`` (https://github.com/ansible-community/antsibull-docs/pull/215).
- Use same colors for LaTeX builder's output as for HTML builder's output (https://github.com/ansible-community/antsibull-docs/pull/199).

Deprecated Features
-------------------

- The ``--use-html-blobs`` feature that inserts HTML blobs for the options and return value tables for the ``ansible-docsite`` output format is deprecated and will be removed soon. The HTML tables cause several features to break, such as references to options and return values. If you think this feature needs to stay, please create an issue in the `antsibull-docs repository <https://github.com/ansible-community/antsibull-docs/issues/>`__ and provide good reasons for it (https://github.com/ansible-community/antsibull-docs/pull/217).

Bugfixes
--------

- Document and ensure that the ``collection`` subcommand with ``--use-current`` can only be used with collection names (https://github.com/ansible-community/antsibull-docs/pull/214).
- Fix FQCN detection (https://github.com/ansible-community/antsibull-docs/pull/214).
- The ``collection`` subcommand claimed to support paths to directories, which was never supported. Removed the mention of paths from the help, and added validation (https://github.com/ansible-community/antsibull-docs/pull/214).
- The ``plugin`` subcommand claimed to support paths to plugin files, which was never supported. Removed the mention of paths from the help (https://github.com/ansible-community/antsibull-docs/pull/214).
- When running ``antsibull-docs --help``, the correct program name is now shown for the ``--version`` option (https://github.com/ansible-community/antsibull-docs/pull/209).
- When running ``antsibull-docs --version``, the correct version is now shown also for editable installs and other installs that do not allow ``importlib.metadata`` to show the correct version (https://github.com/ansible-community/antsibull-docs/pull/209).
- When using the ``action_group`` or ``platform`` attributes in a role, a RST symbol was used that was not defined (https://github.com/ansible-community/antsibull-docs/pull/206).

Known Issues
------------

- When using Sphinx builders other than HTML and LaTeX, the indentation for nested options and return values is missing (https://github.com/ansible-community/antsibull-docs/pull/195).

v2.3.1
======

Release Summary
---------------

Bugfix release with a CSS fix for the Sphinx extension.

Bugfixes
--------

- Fix antsibull Sphinx extension CSS so that the option/return value anchors for module/plugin/role documentation can also be used on WebKit-based browsers such as Gnome Web and Safari (https://github.com/ansible-community/antsibull-docs/issues/188, https://github.com/ansible-community/antsibull-docs/pull/189).

v2.3.0
======

Release Summary
---------------

Bugfix and feature release.

Minor Changes
-------------

- Add a ``:ansplugin:`` role to the Sphinx extension. This allows to reference a module, plugin, or role with the ``fqcn#type`` syntax from semantic markup instead of having to manually compose a ``ansible_collections.{fqcn}_{type}`` label. An explicit reference title can also be provided with the ``title <fqcn#type>`` syntax similar to the ``:ref:`` role (https://github.com/ansible-community/antsibull-docs/pull/180).
- Add a new subcommand ``lint-core-docs`` which lints the ansible-core documentation (https://github.com/ansible-community/antsibull-docs/pull/182).
- Add a new subcommand, ``collection-plugins``, for rendering files for all plugins and roles in a collection without any indexes (https://github.com/ansible-community/antsibull-docs/pull/177).
- Add support for different output formats. Next to the default format, ``ansible-docsite``, a new **experimental** format ``simplified-rst`` is supported. Experimental means that it will likely change considerably in the next few releases until it stabilizes. Such changes will not be considered breaking changes, and could potentially even be bugfixes (https://github.com/ansible-community/antsibull-docs/pull/177).
- Use Dart sass compiler instead of sassc to compile CSS for Sphinx extension (https://github.com/ansible-community/antsibull-docs/issues/185, https://github.com/ansible-community/antsibull-docs/pull/186).
- When parsing errors happen in the Sphinx extension, the extension now emits error messages during the build process in addition to error markup (https://github.com/ansible-community/antsibull-docs/pull/187).

Bugfixes
--------

- Consider module/plugin aliases when linting references to other modules and plugins (https://github.com/ansible-community/antsibull-docs/pull/184).
- Make sure that all aliases are actually listed for plugins (https://github.com/ansible-community/antsibull-docs/pull/183).
- When looking for redirects, the ``aliases`` field and filesystem redirects in ansible-core were not properly considered. This ensures that all redirect stubs are created, and that no duplicates show up, not depending on whether ansible-core is installed in editable mode or not (https://github.com/ansible-community/antsibull-docs/pull/183).

v2.2.0
======

Release Summary
---------------

Bugfix and feature release improving rendering and linting.

Minor Changes
-------------

- Collection docs linter - also validate ``seealso`` module and plugin destinations (https://github.com/ansible-community/antsibull-docs/issues/168, https://github.com/ansible-community/antsibull-docs/pull/171).
- When linting collection plugin docs, make sure that array stubs ``[...]`` are used when referencing sub-options or sub-return values inside lists, and are not used outside lists and dictionaries (https://github.com/ansible-community/antsibull-docs/pull/173).

Bugfixes
--------

- Fix the way the Sphinx extension creates nodes for options and return values so they look identical for internal references, external (intersphinx) references, and unresolved references (https://github.com/ansible-community/antsibull-docs/pull/175).
- Make sure that ``:ansopt:`` and ``:ansretval:`` create the same references as the labels created in the RST files (https://github.com/ansible-community/antsibull-docs/issues/167, https://github.com/ansible-community/antsibull-docs/pull/172).
- Make sure that broken ``:ansopt:`` and ``:ansretval:`` parameters result in correctly rendered error messages (https://github.com/ansible-community/antsibull-docs/pull/175).
- When trying to copying descriptions of non-existing plugins to ``seealso``, references to these non-existing plugins were added in some cases, crashing the docs augmentation process (https://github.com/ansible-community/antsibull-docs/pull/169).

v2.1.0
======

Release Summary
---------------

Feature and bugfix release with many improvements related to semantic markup and validation.

Minor Changes
-------------

- Add option ``--disallow-unknown-collection-refs`` to disallow references to other collections than the one covered by ``--validate-collection-refs`` (https://github.com/ansible-community/antsibull-docs/pull/157).
- Add option ``--validate-collection-refs`` to the ``lint-collection-docs`` subcommand to also control which references to plugin/module/role names in (other) collections and their options and return values should be validated (https://github.com/ansible-community/antsibull-docs/pull/157).
- Add the new collection config field ``envvar_directives`` which allows to declare which environment variables are declared with an ``.. envvar::`` directive in the collection's extra docsite documentation. This is used, next to the plugin configuration information and the ansible-core configuration information, to determine whether an environment variable is referencable or not (https://github.com/ansible-community/antsibull-docs/pull/166).
- Add the roles ``:ansenvvar:`` and ``:ansenvvarref:`` to the antsibull-docs Sphinx extension (https://github.com/ansible-community/antsibull-docs/pull/166).
- Render ``E(...)`` markup with ``:ansenvvarref:`` or ``:ansenvvar:`` depending on whether the environment variable is known to be referencable or not (https://github.com/ansible-community/antsibull-docs/pull/166).
- When linting markup in collection docs, validate plugin/module/role names, and also option/return value names for other plugins/modules/roles in the same collection, (transitively) dependent collections, and ansible.builtin (https://github.com/ansible-community/antsibull-docs/pull/157).
- When linting semantic markup in collection docs, also accept aliases when checking ``O()`` values (https://github.com/ansible-community/antsibull-docs/pull/155).
- When refering to markup in multi-paragraph texts, like ``description``, now includes the paragraph number in error messages (https://github.com/ansible-community/antsibull-docs/pull/163).

Bugfixes
--------

- Allow role entrypoint deprecations without having to specify the collection the role is removed from (https://github.com/ansible-community/antsibull-docs/pull/156).
- Indent module/plugin and role entrypoint deprecations correctly if 'Why' or 'Alternative' texts need more than one line (https://github.com/ansible-community/antsibull-docs/pull/156).
- When collecting collection dependencies for the ``lint-collection-docs`` subcommand, a bug prevented the duplicate detection to work (https://github.com/ansible-community/antsibull-docs/pull/160).

v2.0.0
======

Release Summary
---------------

Major new release that drops support for older Python and Ansible/ansible-base/ansible-core versions.

Major Changes
-------------

- Change pyproject build backend from ``poetry-core`` to ``hatchling``. ``pip install antsibull-docs`` works exactly the same as before, but some users may be affected depending on how they build/install the project (https://github.com/ansible-community/antsibull-docs/pull/115).

Minor Changes
-------------

- Allow to use the currently installed ansible-core version for the ``devel`` and ``stable`` subcommands (https://github.com/ansible-community/antsibull-docs/pull/121).
- Ansibull-docs now no longer depends directly on ``sh`` (https://github.com/ansible-community/antsibull-docs/pull/122).
- Bump version range of antsibull-docs requirement written by ``sphinx-init`` subcommand to ``>= 2.0.0, < 3.0.0``. Previously, this was set to ``>=2.0.0a2, <3.0.0`` (https://github.com/ansible-community/antsibull-docs/pull/151).
- Now depends antsibull-core 2.0.0 or newer; antsibull-core 1.x.y is no longer supported (https://github.com/ansible-community/antsibull-docs/pull/122).
- Remove residual compatability code for Python 3.6 and 3.7 (https://github.com/ansible-community/antsibull-docs/pulls/70).
- Support a per-collection docs config file ``docs/docsite/config.yml``. It is also linted by the ``lint-collection-docs`` subcommand (https://github.com/ansible-community/antsibull-docs/pull/134).
- The antsibull-docs requirement in the ``requirements.txt`` file created by the sphinx-init subcommand now has version range ``>= 2.0.0, < 3.0.0`` (https://github.com/ansible-community/antsibull-docs/pull/126).
- The dependency `antsibull-docs-parser <https://github.com/ansible-community/antsibull-docs-parser>`__ has been added and is used for processing Ansible markup (https://github.com/ansible-community/antsibull-docs/pull/124).

Breaking Changes / Porting Guide
--------------------------------

- Disable flatmapping for all collections except community.general < 6.0.0 and community.network < 5.0.0. You can enable flatmapping for your collection by setting ``flatmap: true`` in ``docs/docsite/config.yml`` (https://github.com/ansible-community/antsibull-docs/pull/134).
- Drop support for Python 3.6, 3.7, and 3.8 (https://github.com/ansible-community/antsibull-docs/pull/115)."
- No longer removes ``PYTHONPATH`` from the environment when calling ``ansible``, ``ansible-galaxy``, or ``ansible-doc`` outside a self-created venv (https://github.com/ansible-community/antsibull-docs/pull/121).
- No longer supports Ansible 2.9, ansible-base 2.10, and ansible-core 2.11 and 2.12. The minimum required ansible-core version is 2.13. This allows for simpler and more efficient docs parsing and information retrieval (https://github.com/ansible-community/antsibull-docs/pull/120).
- The ``ansible-doc`` and ``ansible-internal`` values for ``doc_parsing_backend`` in the configuration file have been removed. Change the value to ``auto`` for best compatibility (https://github.com/ansible-community/antsibull-docs/pull/120).

Bugfixes
--------

- Bump version range of antsibull-docs requirement written by ``sphinx-init`` subcommand to ``>= 2.0.0a2, < 3.0.0``. Previously, this was set to ``>=2.0.0, <3.0.0`` which could not be satisfied (https://github.com/ansible-community/antsibull-docs/pull/149).
- Use ``doc_parsing_backend`` from the application context instead of the library context. This prevents removal of ``doc_parsing_backend`` from the antsibull-core library context (https://github.com/ansible-community/antsibull-docs/pull/125).

v1.11.0
=======

Release Summary
---------------

Feature release.

Minor Changes
-------------

- Add support for semantic markup in roles (https://github.com/ansible-community/antsibull-docs/pull/113).
- Internal refactoring of markup code (https://github.com/ansible-community/antsibull-docs/pull/108).
- The ``lint-collection-docs`` subcommand can be told not to run rstcheck when ``--plugin-docs`` is used by passing ``--skip-rstcheck``. This speeds up testing for large collections (https://github.com/ansible-community/antsibull-docs/pull/112).
- The ``lint-collection-docs`` subcommand will now also validate Ansible markup when ``--plugin-docs`` is passed. It can also ensure that no semantic markup is used with the new ``--disallow-semantic-markup`` option. This can for example be used by collections to avoid semantic markup being backported to older stable branches (https://github.com/ansible-community/antsibull-docs/pull/112).

v1.10.0
=======

Release Summary
---------------

Bugfix and feature release.

Major Changes
-------------

- Support new semantic markup in documentation (https://github.com/ansible-community/antsibull-docs/pull/4).

Minor Changes
-------------

- Add a note about the ordering of positional and named parameter to the plugin page. Also mention positional and keyword parameters for lookups (https://github.com/ansible-community/antsibull-docs/pull/101).
- Update schema for roles argument spec to allow specifying attributes on the entrypoint level. These are now also rendered when present (https://github.com/ansible-community/antsibull-docs/pull/103).

Bugfixes
--------

- Explicitly declare the ``sh`` dependency and limit it to before 2.0.0. Also explicitly declare the dependencies on ``pydantic``, ``semantic_version``, ``aiohttp``, ``twiggy``, and ``PyYAML`` (https://github.com/ansible-community/antsibull-docs/pull/99).
- Restrict the ``pydantic`` dependency to major version 1 (https://github.com/ansible-community/antsibull-docs/pull/102).

v1.9.0
======

Release Summary
---------------

Feature release.

Minor Changes
-------------

- Improve build script generated by ``antsibull-docs sphinx-init`` to change to the directory where the script is located, instead of hardcoding the script's path. This also fixed the existing bug that the path was not quoted (https://github.com/ansible-community/antsibull-docs/issues/91, https://github.com/ansible-community/antsibull-docs/pull/92).
- Show callback plugin type on callback plugin pages. Also write callback indexes by callback plugin type (https://github.com/ansible-community/antsibull-docs/issues/89, https://github.com/ansible-community/antsibull-docs/pull/90).

v1.8.2
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Fix the new options ``--extra-html-context`` and ``--extra-html-theme-options`` of the ``sphinx-init`` subcommand (https://github.com/ansible-community/antsibull-docs/pull/86).

v1.8.1
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- When creating toctrees for breadcrumbs, place subtree for a plugin type in the plugin type's section (https://github.com/ansible-community/antsibull-docs/pull/83).

v1.8.0
======

Release Summary
---------------

Feature and bugfix release.

Minor Changes
-------------

- Add new options ``--project``, ``--copyright``, ``--title``, ``--html-short-title``, ``--extra-conf``, ``--extra-html-context``, and ``--extra-html-theme-options`` to the ``sphinx-init`` subcommand to allow to customize the generated ``conf.py`` Sphinx configuration (https://github.com/ansible-community/antsibull-docs/pull/77).
- Automatically use a module's or plugin's short description as the "See also" description if no description is provided (https://github.com/ansible-community/antsibull-docs/issues/64, https://github.com/ansible-community/antsibull-docs/pull/74).
- It is now possible to provide a path to an existing file to be used as ``rst/index.rst`` for ``antsibull-docs sphinx-init`` (https://github.com/ansible-community/antsibull-docs/pull/68).
- Make compatible with antsibull-core 2.x.y (https://github.com/ansible-community/antsibull-docs/pull/78).
- Remove support for ``forced_action_plugin``, a module attribute that was removed during the development phase of attributes (https://github.com/ansible-community/antsibull-docs/pull/63).
- Stop mentioning the version features were added for Ansible if the Ansible version is before 2.7 (https://github.com/ansible-community/antsibull-docs/pull/76).
- The default ``index.rst`` created by ``antsibull-docs sphinx-init`` includes the new environment variable index (https://github.com/ansible-community/antsibull-docs/pull/80).
- Use correct markup (``envvar`` role) for environment variables. Compile an index of all environment variables used by plugins (https://github.com/ansible-community/antsibull-docs/pull/73).

Bugfixes
--------

- Make sure that ``build.sh`` created by the ``sphinx-init`` subcommand sets proper permissions for antsibull-docs on the ``temp-rst`` directory it creates (https://github.com/ansible-community/antsibull-docs/pull/79).

v1.7.4
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Removed ``sphinx`` restriction in ``requirements.txt`` file created by ``antsibull-docs sphinx-init`` since the bug in ``sphinx-rtd-theme`` has been fixed (https://github.com/ansible-community/antsibull-docs/pull/69).
- The license header for the template for the ``rst/index.rst`` file created by ``antsibull-docs sphinx-init`` was commented incorrectly and thus showed up in the templated file (https://github.com/ansible-community/antsibull-docs/pull/67).
- When using ``--squash-hierarchy``, do not mention the list of collections on the collection's index page (https://github.com/ansible-community/antsibull-docs/pull/72).

v1.7.3
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Fix rendering of the ``action_group`` attribute (https://github.com/ansible-community/antsibull-docs/pull/62).

v1.7.2
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Fix ``version_added`` processing for ansible.builtin 0.x to represent this as ``Ansible 0.x`` instead of ``ansible-core 0.x`` (https://github.com/ansible-community/antsibull-docs/pull/61).

v1.7.1
======

Release Summary
---------------

Bugfix release.

Bugfixes
--------

- Prevent crash during ``stable`` docsite build when ``_python`` entry is present in deps file (https://github.com/ansible-community/antsibull-docs/pull/57).

v1.7.0
======

Release Summary
---------------

Bugfix and feature release.

Minor Changes
-------------

- Add ``--intersphinx`` option to the ``sphinx-init`` subcommand to allow adding additional ``intersphinx_mapping`` entries to ``conf.py`` (https://github.com/ansible-community/antsibull-docs/issues/35, https://github.com/ansible-community/antsibull-docs/pull/44).
- Allow the ``toctree`` entries for in a collection's ``docs/docsite/extra-docs.yml`` to be a dictionary with ``ref`` and ``title`` keys instead of just a reference as a string (https://github.com/ansible-community/antsibull-docs/pull/45).
- Antsibull-docs now depends on `packaging <https://pypi.org/project/packaging/>`__ (https://github.com/ansible-community/antsibull-docs/pull/49).
- The collection index pages now contain the supported versions of ansible-core of the collection in case collection's ``meta/runtime.yml`` specifies ``requires_ansible`` (https://github.com/ansible-community/antsibull-docs/issues/48, https://github.com/ansible-community/antsibull-docs/pull/49).
- The output of the ``lint-collection-docs`` command has been improved; in particular multi-line messages are now indented (https://github.com/ansible-community/antsibull-docs/pull/52).
- Use ``ansible --version`` to figure out ansible-core version when ansible-core is not installed for the same Python interpreter / venv that is used for antsibull-docs (https://github.com/ansible-community/antsibull-docs/pull/50).
- Use code formatting for all values, such as choice entries, defaults, and samples (https://github.com/ansible-community/antsibull-docs/issues/38, https://github.com/ansible-community/antsibull-docs/pull/42).

Bugfixes
--------

- Avoid long aliases list to make left column too wide (https://github.com/ansible-collections/amazon.aws/issues/1101, https://github.com/ansible-community/antsibull-docs/pull/54).
- Make ``lint-collection-docs --plugin-docs`` subcommand actually work (https://github.com/ansible-community/antsibull-docs/pull/47).

v1.6.1
======

Release Summary
---------------

Bugfix release for ansible-core 2.14.

Bugfixes
--------

- Fix formulation of top-level ``version_added`` (https://github.com/ansible-community/antsibull-docs/pull/43).

v1.6.0
======

Release Summary
---------------

Bugfix and feature release.

Minor Changes
-------------

- Allow to specify choices as dictionary instead of list (https://github.com/ansible-community/antsibull-docs/pull/36).
- Use JSON serializer to format choices (https://github.com/ansible-community/antsibull-docs/pull/37).
- Use special serializer to format INI values in examples (https://github.com/ansible-community/antsibull-docs/pull/37).

Bugfixes
--------

- Avoid collection names with ``_`` in them appear wrongly escaped in the HTML output (https://github.com/ansible-community/antsibull-docs/pull/41).
- For INI examples which have no default, write ``VALUE`` as intended instead of ``None`` (https://github.com/ansible-community/antsibull-docs/pull/37).
- Format lists correctly for INI examples (https://github.com/ansible-community/antsibull-docs/pull/37).
- The ``sphinx-init`` subcommand's ``requirement.txt`` file avoids Sphinx 5.2.0.post0, which triggers a bug in sphinx-rtd-theme which happens to be the parent theme of the default theme sphinx_ansible_theme used by ``sphinx-init`` (https://github.com/ansible-community/antsibull-docs/issues/39, https://github.com/ansible-community/antsibull-docs/pull/40).

v1.5.0
======

Release Summary
---------------

Feature and bugfix release.

Minor Changes
-------------

- Detect filter and test plugin aliases and avoid them being emitted multiple times. Instead insert redirects so that stub pages will be created (https://github.com/ansible-community/antsibull-docs/pull/33).
- Replace ``ansible.builtin`` with ``ansible-core``, ``ansible-base``, or ``Ansible`` in version added collection names. Also write ``<collection_name> <version>`` instead of ``<version> of <collection_name>`` (https://github.com/ansible-community/antsibull-docs/pull/34).

Bugfixes
--------

- Fix escaping of collection names in version added statements, and fix collection names for roles options (https://github.com/ansible-community/antsibull-docs/pull/34).

v1.4.0
======

Release Summary
---------------

Feature and bugfix release.

Minor Changes
-------------

- The ``sphinx-init`` subcommand now also creates an ``antsibull-docs.cfg`` file and moves configuration settings from CLI flags in ``build.sh`` to this configuration file (https://github.com/ansible-community/antsibull-docs/pull/26).
- There are two new options for explicitly specified configuration files named ``collection_url`` and ``collection_install``. These allow to override the URLs pointing to collections (default link to galaxy.ansible.com), and the commands to install collections (use ``ansible-galaxy collection install`` by default). This can be useful when documenting (internal) collections that are not available on Ansible Galaxy. The default ``antsibull-docs.cfg`` generated by the ``sphinx-init`` subcommand shows how this can be configured (https://github.com/ansible-community/antsibull-docs/issues/15, https://github.com/ansible-community/antsibull-docs/pull/26).
- When generating plugin error pages, or showing non-fatal errors in plugins or roles, link to the collection's issue tracker instead of the collection's URL if available (https://github.com/ansible-community/antsibull-docs/pull/29).

Bugfixes
--------

- Make handling of bad documentation more robust when certain values are ``None`` while the keys are present (https://github.com/ansible-community/antsibull-docs/pull/32).

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
