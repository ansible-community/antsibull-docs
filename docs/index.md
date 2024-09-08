<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# antsibull-docs – Building Ansible documentation

[![Discuss on Matrix at #antsibull:ansible.com](https://img.shields.io/matrix/antsibull:ansible.com.svg?server_fqdn=ansible-accounts.ems.host&label=Discuss%20on%20Matrix%20at%20%23antsibull:ansible.com&logo=matrix)](https://matrix.to/#/#antsibull:ansible.com)
[![Discuss on Matrix at #docs:ansible.com](https://img.shields.io/matrix/docs:ansible.com.svg?server_fqdn=ansible-accounts.ems.host&label=Discuss%20on%20Matrix%20at%20%23docs:ansible.com&logo=matrix)](https://matrix.to/#/#docs:ansible.com)

This package provides tooling for validating and building Ansible documentation. It mainly consists of a CLI tool, `antsibull-docs`, and a Sphinx extension. The main output format are [reStructured Text (RST)](https://en.wikipedia.org/wiki/ReStructuredText) files for consumption by [Sphinx](https://en.wikipedia.org/wiki/Sphinx_\(documentation_generator\)).

**Collection maintainers and authors should look at the [Creating a collection docsite](collection-docs.md) section of this docsite.**

antsibull-docs is covered by the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).

!!! note
    Need help or want to discuss the project? See our [Community guide](community.md) to learn how to join the conversation!

## `antsibull-docs` subcommands

The main CLI tool, `antsibull-docs`, has multiple subcommands:

* The `devel` and `stable` subcommands are used for building the official Ansible docsites at [docs.ansible.com/ansible/devel](https://docs.ansible.com/ansible/devel/) and [docs.ansible.com/ansible/latest](https://docs.ansible.com/ansible/latest/).
* The `current` and `collection` subcommands are used for building docsites for individual collections.
* The `plugin` and `collection-plugins` subcommands are used for rendering documentation for individual (or all) plugins, modules, or roles.
* The `lint-collection-docs` and `lint-core-docs` subcommands are used for linting collection and ansible-core documentation.
  The former is described in more detail in [Creating a collection docsite](collection-docs.md).
* The `sphinx-init` subcommmand is used for setting up a Sphinx-based collection docsite.
  This is described in more detail in [Creating a collection docsite](collection-docs.md).

## Using the Sphinx extension

The `sphinx_antsibull_ext` [Sphinx extension](https://www.sphinx-doc.org/en/master/) provides minimal CSS and several roles used by the written RST files to render the documentation correctly. To use it, include it in your Sphinx configuration ``conf.py``:

```python
# Add it to 'extensions':
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'notfound.extension', 'sphinx_antsibull_ext']
```

It is possible to configure the color scheme used by the extension using the `antsibull_ext_color_scheme` configuration. Currently, the following values are supported:

1. `default`: the default colors.
2. `default-dark`: a dark color scheme.
3. `default-autodark`: the default colors or the dark colors, depending on a `prefers-color-scheme` media query.
4. `none`: define no colors. You can use this if you want to override all colors by your own definition and thus have no need for the default colors to be included.

The default color scheme can be found in [src/sphinx_antsibull_ext/css/colors-default.scss](https://github.com/ansible-community/antsibull-docs/blob/main/src/sphinx_antsibull_ext/css/colors-default.scss). See the [MDN page on using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties) for information on how the color definitions work.

Please note that the color scheme only works for HTML output. The colors for LaTeX / PDF output are hardcoded and currently cannot be modified.

## License

Unless otherwise noted in the code, it is licensed under the terms of the GNU
General Public License v3 or, at your option, later. See
[LICENSES/GPL-3.0-or-later.txt](https://github.com/ansible-community/antsibull-docs/tree/main/LICENSE)
for a copy of the license.

The repository follows the [REUSE Specification](https://reuse.software/spec/) for declaring copyright and
licensing information. The only exception are changelog fragments in ``changelog/fragments/``.
