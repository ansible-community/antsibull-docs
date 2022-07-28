<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# antsibull-docs -- Ansible Documentation Build Scripts
[![Python linting badge](https://github.com/ansible-community/antsibull-docs/workflows/Python%20linting/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull-docs/actions?query=workflow%3A%22Python+linting%22+branch%3Amain)
[![Python testing badge](https://github.com/ansible-community/antsibull-docs/workflows/Python%20testing/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull-docs/actions?query=workflow%3A%22Python+testing%22+branch%3Amain)
[![Build docs testing badge](https://github.com/ansible-community/antsibull-docs/workflows/antsibull-docs%20tests/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull-docs/actions?query=workflow%3A%22antsibull-docs+tests%22+branch%3Amain)
[![Build CSS testing badge](https://github.com/ansible-community/antsibull-docs/workflows/Build%20CSS/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull-docs/actions?query=workflow%3A%22Build+CSS%22+branch%3Amain)
[![Codecov badge](https://img.shields.io/codecov/c/github/ansible-community/antsibull-docs)](https://codecov.io/gh/ansible-community/antsibull-docs)

Tooling for building Ansible documentation.

Script that is here:

* antsibull-docs - Extracts documentation from ansible plugins

This also includes a [Sphinx extension](https://www.sphinx-doc.org/en/master/) `sphinx_antsibull_ext` which provides a minimal CSS file to render the output of `antsibull-docs` correctly.

You can find a list of changes in [the antsibull-docs changelog](./CHANGELOG.rst).

Unless otherwise noted in the code, it is licensed under the terms of the GNU
General Public License v3 or, at your option, later.

antsibull-docs is covered by the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).

## Versioning and compatibility

From version 1.0.0 on, antsibull-docs sticks to semantic versioning and aims at providing no backwards compatibility breaking changes **to the command line API (antsibull-docs)** during a major release cycle. We might make exceptions from this in case of security fixes for vulnerabilities that are severe enough.

We explicitly exclude code compatibility. **antsibull-docs is not supposed to be used as a library.** The only exception are dependencies with other antsibull projects (currently, only [antsibull](https://github.com/ansible-community/antsibull/) itself). If you want to use a certain part of antsibull-docs as a library, please create an issue so we can discuss whether we add a stable interface for **parts** of the Python code. We do not promise that this will actually happen though.

## Running from source

Please note that to run antsibull-docs from source, you need to install some related projects adjacent to the antsibull-docs checkout.  More precisely, assuming you checked out the antsibull-docs repository in a directory `./antsibull-docs/`, you need to check out the following projects in the following locations:

- [antsibull-core](https://github.com/ansible-community/antsibull-core/) needs to be checked out in `./antsibull-core/`.

This can be done as follows:

    git clone https://github.com/ansible-community/antsibull-core.git
    git clone https://github.com/ansible-community/antsibull-docs.git
    cd antsibull-docs

Scripts are created by poetry at build time.  So if you want to run from a checkout, you'll have to run them under poetry::

    python3 -m pip install poetry
    poetry install  # Installs dependencies into a virtualenv
    poetry run antsibull-docs --help

Note: When installing a package published by poetry, it is best to use pip >= 19.0.  Installing with pip-18.1 and below could create scripts which use pkg_resources which can slow down startup time (in some environments by quite a large amount).

## Using the Sphinx extension

Include it in your Sphinx configuration ``conf.py``::

```
# Add it to 'extensions':
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'notfound.extension', 'sphinx_antsibull_ext']
```

## Updating the CSS file for the Sphinx extension

The CSS file [sphinx_antsibull_ext/antsibull-minimal.css](https://github.com/ansible-community/antsibull-docs/blob/main/sphinx_antsibull_ext/antsibull-minimal.css) is built from [sphinx_antsibull_ext/css/antsibull-minimal.scss](https://github.com/ansible-community/antsibull-docs/blob/main/sphinx_antsibull_ext/src/antsibull-minimal.scss) using [SASS](https://sass-lang.com/) and [postcss](https://postcss.org/) using [autoprefixer](https://github.com/postcss/autoprefixer) and [cssnano](https://cssnano.co/).

Use the script `build.sh` in `sphinx_antsibull_ext/css/` to build the `.css` file from the `.scss` file:

```
cd sphinx_antsibull_ext/css/
./build-css.sh
```

For this to work, you need to make sure that `sassc` and `postcss` are on your path and that the autoprefixer and nanocss modules are installed:

```
# Debian:
apt-get install sassc

# PostCSS, autoprefixer and cssnano require nodejs/npm:
npm install -g autoprefixer cssnano postcss postcss-cli
```

## Creating a new release:

If you want to create a new release::

    vim pyproject.toml  # Make sure version number is correct
    vim changelogs/fragment/$VERSION_NUMBER.yml  # create 'release_summary:' fragment
    antsibull-changelog release --version $VERSION_NUMBER
    git add CHANGELOG.rst changelogs
    git commit -m "Release $VERSION_NUMBER."
    poetry build
    poetry publish  # Uploads to pypi.  Be sure you really want to do this

    git tag $VERSION_NUMBER
    git push --tags
    vim pyproject.toml  # Bump the version number to X.Y.Z.post0
    git commit -m 'Update the version number for the next release' pyproject.toml
    git push
