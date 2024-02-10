<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# antsibull-docs -- Building Ansible documentation

[![Discuss on Matrix at #docs:ansible.com](https://img.shields.io/matrix/docs:ansible.com.svg?server_fqdn=ansible-accounts.ems.host&label=Discuss%20on%20Matrix%20at%20%23docs:ansible.com&logo=matrix)](https://matrix.to/#/#docs:ansible.com)

This package provides tooling for building Ansible documentation. It mainly consists of a CLI tool, `antsibull-docs`, and a Sphinx extension. The main output format are [reStructured Text (RST)](https://en.wikipedia.org/wiki/ReStructuredText) files for consumption by [Sphinx](https://en.wikipedia.org/wiki/Sphinx_\(documentation_generator\)).

antsibull-docs is covered by the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).

## `antsibull-docs` subcommands

The main CLI tool, `antsibull-docs`, has multiple subcommands:

* The `devel` and `stable` subcommands are used for building the official Ansible docsites at https://docs.ansible.com/ansible/devel/ and https://docs.ansible.com/ansible/latest/.
* The `current` and `collection` subcommands are used for building docsites for individual collections.
* The `plugin` and `collection-plugins` subcommands are used for rendering documentation for individual (or all) plugins, modules, or roles.
* The `lint-collection-docs` and `lint-core-docs` subcommands are used for linting collection and ansible-core documentation.
* The `sphinx-init` subcommmand is used for setting up a Sphinx-based collection docsite.

## Using the Sphinx extension

The `sphinx_antsibull_ext` [Sphinx extension](https://www.sphinx-doc.org/en/master/) provides minimal CSS and several roles used by the written RST files to render the documentation correctly. To use it, include it in your Sphinx configuration ``conf.py``:

```
# Add it to 'extensions':
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'notfound.extension', 'sphinx_antsibull_ext']
```

## License

Unless otherwise noted in the code, it is licensed under the terms of the GNU
General Public License v3 or, at your option, later. See
[LICENSES/GPL-3.0-or-later.txt](https://github.com/ansible-community/antsibull-docs/tree/main/LICENSE)
for a copy of the license.

The repository follows the [REUSE Specification](https://reuse.software/spec/) for declaring copyright and
licensing information. The only exception are changelog fragments in ``changelog/fragments/``.
