<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# antsibull-docs -- Ansible Documentation Build Scripts
[![Discuss on Matrix at #docs:ansible.com](https://img.shields.io/matrix/docs:ansible.com.svg?server_fqdn=ansible-accounts.ems.host&label=Discuss%20on%20Matrix%20at%20%23docs:ansible.com&logo=matrix)](https://matrix.to/#/#docs:ansible.com)
[![Nox badge](https://github.com/ansible-community/antsibull-docs/actions/workflows/nox.yml/badge.svg)](https://github.com/ansible-community/antsibull-docs/actions/workflows/nox.yml)
[![Build docs testing badge](https://github.com/ansible-community/antsibull-docs/workflows/antsibull-docs%20tests/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull-docs/actions?query=workflow%3A%22antsibull-docs+tests%22+branch%3Amain)
[![Build CSS testing badge](https://github.com/ansible-community/antsibull-docs/workflows/Build%20CSS/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull-docs/actions?query=workflow%3A%22Build+CSS%22+branch%3Amain)
[![Codecov badge](https://img.shields.io/codecov/c/github/ansible-community/antsibull-docs)](https://codecov.io/gh/ansible-community/antsibull-docs)

Tooling for building Ansible documentation. This is mainly the `antsibull-docs` command and the [Sphinx extension](https://www.sphinx-doc.org/en/master/), ``sphinx_antsibull_ext``. Please check out the [documentation](https://ansible.readthedocs.io/projects/antsibull-docs/) for more information.

You can find a list of changes in [the antsibull-docs changelog](https://github.com/ansible-community/antsibull-docs/blob/main/CHANGELOG.md).

antsibull-docs is covered by the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).

## Versioning and compatibility

From version 1.0.0 on, antsibull-docs sticks to semantic versioning and aims at providing no backwards compatibility breaking changes **to the command line API (antsibull-docs)** during a major release cycle. We might make exceptions from this in case of security fixes for vulnerabilities that are severe enough.

The current major version is 2.x.y. Development for 2.x.y occurs on the `main` branch. 2.x.y mainly differs from 1.x.y by dropping support for Python 3.6, 3.7, and 3.8, and by dropping support for older Ansible/ansible-base/ansible-core versions. See the changelog for details. 1.x.y is still developed on the `stable-1` branch, but only security fixes, major bugfixes, and other absolutely necessary changes will be backported.

We explicitly exclude code compatibility. **antsibull-docs is not supposed to be used as a library.** The only exception are potential dependencies with other antsibull projects (currently there are none). If you want to use a certain part of antsibull-docs as a library, please create an issue so we can discuss whether we add a stable interface for **parts** of the Python code. We do not promise that this will actually happen though.

If you are interested in library support for interpreting Ansible markup, please take a look at [the antsibull-docs-parser project](https://github.com/ansible-community/antsibull-docs-parser).

## Development

Install and run `nox` to run all tests. That's it for simple contributions!
`nox` will create virtual environments in `.nox` inside the checked out project
and install the requirements needed to run the tests there.


---

antsibull-docs depends on the sister antsibull-core and antsibull-docs-parser projects.
By default, `nox` will install a development version of these projects from
Github.
If you're hacking on antsibull-core and/or antsibull-docs-parser alongside antsibull-docs,
nox will automatically install the projects from `../antsibull-core` and
`../antsibull-docs-parser` when running tests if those paths exist.
You can change this behavior through the `OTHER_ANTSIBULL_MODE` env var:

- `OTHER_ANTSIBULL_MODE=auto` — the default behavior described above
- `OTHER_ANTSIBULL_MODE=local` — install the projects from `../antsibull-core`
  and `../antsibull-docs-parser`. Fail if those paths don't exist.
- `OTHER_ANTSIBULL_MODE=git` — install the projects from the Github main branch
- `OTHER_ANTSIBULL_MODE=pypi` — install the latest versions from PyPI


To run specific tests:

1. `nox -e test` to only run unit tests;
2. `nox -e lint` to run all linters and formatter;
3. `nox -e codeqa` to run `flake8`, `pylint`, `reuse lint`, and `antsibull-changelog lint`;
4. `nox -e formatters` to run `isort` and `black`;
5. `nox -e typing` to run `mypy` and `pyre`.

To create a more complete local development env:

```console
git clone https://github.com/ansible-community/antsibull-core.git
git clone https://github.com/ansible-community/antsibull-docs-parser.git
git clone https://github.com/ansible-community/antsibull-docs.git
cd antsibull-docs
python3 -m venv venv
. ./venv/bin/activate
pip install -e '.[dev]' -e ../antsibull-core -e ../antsibull-docs-parser
[...]
nox
```

## Updating the CSS file for the Sphinx extension

The CSS file [sphinx_antsibull_ext/antsibull-minimal.css](https://github.com/ansible-community/antsibull-docs/blob/main/sphinx_antsibull_ext/antsibull-minimal.css) is built from [sphinx_antsibull_ext/css/antsibull-minimal.scss](https://github.com/ansible-community/antsibull-docs/blob/main/sphinx_antsibull_ext/src/antsibull-minimal.scss) using [SASS](https://sass-lang.com/) and [postcss](https://postcss.org/) using [autoprefixer](https://github.com/postcss/autoprefixer) and [cssnano](https://cssnano.co/).

Use the script `build.sh` in `sphinx_antsibull_ext/css/` to build the `.css` file from the `.scss` file:

```console
cd sphinx_antsibull_ext/css/
./build-css.sh
```

For this to work, you need to install some Node.js dependencies:

```console
npm clean-install
```

## Creating a new release:

1. Run `nox -e bump -- <version> <release_summary_message>`. This:
   * Bumps the package version in `src/antsibull_docs/__init__.py`.
   * Creates `changelogs/fragments/<version>.yml` with a `release_summary` section.
   * Runs `antsibull-changelog release --version <version>` and adds the changed files to git.
   * Commits with message `Release <version>.` and runs `git tag -a -m 'antsibull-docs <version>' <version>`.
   * Runs `hatch build --clean`.
2. Run `git push` to the appropriate remotes.
3. Once CI passes on GitHub, run `nox -e publish`. This:
   * Runs `hatch publish`;
   * Bumps the version to `<version>.post0`;
   * Adds the changed file to git and run `git commit -m 'Post-release version bump.'`;
4. Run `git push --follow-tags` to the appropriate remotes and create a GitHub release.

## License

Unless otherwise noted in the code, it is licensed under the terms of the GNU
General Public License v3 or, at your option, later. See
[LICENSES/GPL-3.0-or-later.txt](https://github.com/ansible-community/antsibull-docs/tree/main/LICENSE)
for a copy of the license.

The repository follows the [REUSE Specification](https://reuse.software/spec/) for declaring copyright and
licensing information. The only exception are changelog fragments in ``changelog/fragments/``.
