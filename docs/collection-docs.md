<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Creating a collection docsite

antsibull-docs can be used to create a docsite for an individual collection. For example, take a look at [the community.crypto docsite built from the latest commit to the community.crypto repository](https://ansible-collections.github.io/community.crypto/branch/main/). This document explains how you can build such a docsite with antsibull-docs, how you can lint collection documentation, and how you can use GitHub Actions to automate docsite building.

## Setting up development for a collection

While antsibull-docs can download a collection it should generate documentation for, the main mode of operation is to use collections that are made available to ansible-core.

If you just want to create documentation, you have to install ansible-core, antsibull-docs, and the collections you want to generate documentation for, or validate documentation of. To install ansible-core and antsibull-docs, you can use a [Python venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment). In short, this looks like:
```console
$ python -m venv ~/antsibull-demo-venv
$ . ~/antsibull-demo-venv/bin/activate
$ python -m pip install ansible-core antsibull-docs
```

To install collections, you can either use [`ansible-galaxy collection install`](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html), or you can provide the collection repositories in a path structure that allows ansible-core to access them. If you work on collections, the second approach is usually preferred. One way of doing this is create a directory structure `ansible_collections/<namespace>/<name>` for a collection `<namespace>.<name>` and point Ansible's [`ANSIBLE_COLLECTIONS_PATH`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths) to the directory containing `ansible_collections`. Then you can directly use the collection in Ansible.

For example, if you want to store the collection tree in `~/collections/`, and you want to work on say `community.crypto`, which is stored in the [ansible-collections/community.crypto GitHub repository](https://github.com/ansible-collections/community.crypto/), you can clone it as follows:
```console
$ mkdir -p ~/collections/ansible_collections/community
$ export ANSIBLE_COLLECTIONS_PATH=~/collections
$ git clone git@github.com:ansible-collections/community.crypto.git ~/collections/ansible_collections/community/crypto
```

With `ANSIBLE_COLLECTIONS_PATH` set up you can use modules and plugins from the collection directly:
```console
$ ansible localhost -m community.crypto.crypto_info
[WARNING]: No inventory was parsed, only implicit localhost is available
localhost | SUCCESS => {
    "changed": false,
    ...
}
```

In many cases you want to clone your fork instead of the collection's main repository itself, and only add the main repository as another remote. Please refer to your favorite Source Control Management tool/workflow on how to set up the environment. The important part is to check out the collection into the right path structure.

Using that path structure, you can also run other tools like `ansible-test`:
```console
$ cd ~/collections/ansible_collections/community/crypto
$ ansible-test sanity --docker -v
```

Finally, you can use `ansible-doc` to directly look at plugin, module, and role documentation using the command line:
```console
# List modules and filter plugins:
$ ansible-doc --type module --list community.crypto
$ ansible-doc --type filter --list community.crypto

# Show documentation of modules and filters:
$ ansible-doc --type module community.crypto.crypto_info
$ ansible-doc --type filter community.crypto.gpg_fingerprint
```
antsibull-docs internally uses `ansible-doc` and its JSON output to extract collection documentation.

## Linting collection docs

While the [`validate-modules` sanity test](https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/validate-modules.html) provided by `ansible-test` already does some validation of module and plugin documentation, it does not check filter and test plugins, for example, and does not check cross-references to other plugins, modules, and roles. antsibull-docs provides the `lint-collection-docs` subcommand that allows you to extensively validate collection documentation, including extra documentation and collection-level links (see the corresponding sections below). The basic usage is as follows:
```console
$ cd ~/collections/ansible_collections/community/crypto
$ antsibull-docs lint-collection-docs --plugin-docs .
```

This subcommand has multiple options which allow to control validation. The most important options are:

* `--plugin-docs`: whether to validate schemas and markup of modules, plugins, and roles included in the collection. By default, this is not run (for backwards compatibility). We recommend to always specify this.
* `--validate-collection-refs {self,dependent,all}`: Specify how to validate inter-plugin/module/role and inter-collection references in plugin/module/role documentation. This covers Ansible markup, like `M(foo.bar.baz)` or `O(foo.bar.baz#module:parameter=value)`, and other links such as `seealso` sections. If set to `self`, only references to the same collection are validated. If set to `dependent`, only references to the collection itself and collections it (transitively) depends on are validated, including references to ansible-core (as `ansible.builtin`). If set to `all`, all references to other collections are validated.

    If collections are referenced that are not installed and that are in scope, references to them will not be reported. Reporting these can be enabled by specifying `--disallow-unknown-collection-refs`.

* `--skip-rstcheck`: by default, when specifying `--plugin-docs`, antsibull-docs generates RST documentation for module/plugin/role docs and runs [`rstcheck`](https://rstcheck.readthedocs.io/) on these. This step is usually not necessary, since it will mostly point out errors in antsibull-docs' RST generation code, and will slow down linting especially for large collections.
* `--disallow-semantic-markup`: If you want to avoid semantic markup in Ansible markup, for example for collections whose documentation must render OK with older versions of ansible-doc or Automation Hub, you can use this parameter to make antsibull-docs report all markup that is not supported. Semantic markup is supported by ansible-doc since ansible-core 2.15.0.

The most extensive validation is achieved by running the following command:
```console
$ antsibull-docs lint-collection-docs --plugin-docs --skip-rstcheck \
                                      --validate-collection-refs=all \
                                      --disallow-unknown-collection-refs .
```

When successfully validating, the exit code will be `0`, otherwise it will be non-zero. In case it is non-zero, validation errors are shown in the format `<filename>:<line>:<column>:<message>` as follows:
```
plugins/modules/crypto_info.py:0:0: DOCUMENTATION -> description[2]: M(foo.bar.baz): a reference to the collection foo.bar is not allowed
```
This tells you that in file `plugins/modules/crypto_info.py`'s `DOCUMENTATION`, you have a broken reference `M(foo.bar.baz)` in the second paragraph of the top-level `description` key.

The same output format is also used by ansible-test.

## Building a docsite

The simplest way to set up a Sphinx docsite is to use antsibull-docs' `sphinx-init` subcommand:
```console
# Create a subdirectory which should contain the docsite:
$ mkdir built-docs

# Create a Sphinx project for the collection community.crypto in there:
$ antsibull-docs sphinx-init --use-current --squash-hierarchy community.crypto --dest-dir built-docs

# Install requirements for the docsite build
# (if you don't have an active venv, create one!)
$ cd built-docs
$ python -m pip install -r requirements.txt

# Build the docsite by:
#  1. running antsibull-docs to create the RST files for the collection,
#  2. running Sphinx to compile everything to HTML
$ ./build.sh

# Open the built HTML docsite in a browser like Firefox:
$ firefox build/html/index.html
```

The `sphinx-init` subcommand has quite a few configuration options:

* If you built a docsite for a single collection, it's a good idea to specify `--squash-hierarchy` as in the above example. This avoids the unnecessary tree structure.
* `--use-current` controls whether the collection should be assumed to be installed (if `--use-current` is specified), or whether antsibull-docs should install it itself temporarily (if `--use-current` is not specified). We recommend to install collections yourself and always specify `--use-current`.
* You can use `--lenient` (configure Sphinx to not be too strict) and `--fail-on-error` (if any parsing or schema valiation errors happen, fail instead of creating error pages) to control building. For use in CI, use `--fail-on-error` to make sure that all errors are raised early. When trying to successfully build the docsite, `--lenient` is helpful to avoid Sphinx being too strict on errors.
* `--index-rst-source` can be used to copy a provided file to `rst/index.rst` instead of generating a default `rst/index.rst` file.
* `--sphinx-theme` can be used to select a different Sphinx theme. The default is the [`sphinx-ansible-theme`](https://pypi.org/project/sphinx-ansible-theme/).
* `--intersphinx` can be used to add intersphinx config entries to allow to use RST references to more external documentation. Refer to the [intersphinx documentation](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html) for more information.
* `--project`, `--copyright`, `--title`, `--html-short-title`, `--extra-conf`, `--extra-html-context`, and `--extra-html-theme-options` can be used to add specific configuration entries to the Sphinx configuration `conf.py`.

## Configuring the docsite

Generally, configuration is done with a `docs/docsite/config.yml` YAML file. The format and options are as follows:
```yaml
---
# Whether the collection uses flatmapping to flatten subdirectories in
# `plugins/*/`.
flatmap: false

# List of environment variables that are defined by `.. envvar::` directives
# in the extra docsite RST files.
envvar_directives: []

# Changelog configuration (added in antsibull-docs 2.10.0)
changelog:
  # Whether to write the changelog (taken from changelogs/changelog.yaml, see the
  # antsibull-changelog documentation for more information) and link to it from the
  # collection's index page.
  write_changelog: false
```

Most collections should use `envvar_directives` and `changelog` only. The `flatmap` option applies to older versions of community.general and community.network and should be used for legacy collections only, not for new ones.

## Adding extra documentation

It is possible to add extra documentation in RST format to the docsite. This can for example be used to provide scenario guides. On the [community.crypto docsite](https://ansible-collections.github.io/community.crypto/branch/main/), there are for example some how-tos in the "Scenario Guides" section.

You need to provide the RST files in `docs/docsite/rst/`, and configure them in a YAML file `docs/docsite/extra-docs.yml`. See for example the [`extra-docs.yml` from community.crypto](https://github.com/ansible-collections/community.crypto/blob/main/docs/docsite/extra-docs.yml) for how this works:
```yaml
---
sections:
  # We have one section labelled "Scenario Guides"
  - title: Scenario Guides
    toctree:
      # List the filenames in docs/docsite/rst without
      # the .rst extension here in the order you want
      # them to appear:
      - guide_selfsigned
      - guide_ownca
```

Note that in the RST files, you cannot chose labels freely, but have to prefix every label with `ansible_collections.<namespace>.<name>.docsite.`. This ensures that you cannot accidentally re-use labels that are used by other parts of the Ansible docsite. This can look as follows for community.crypto:

```rst
.. _ansible_collections.community.crypto.docsite.guide_ownca:

How to create a small CA
========================

The `community.crypto collection
<https://galaxy.ansible.com/ui/repo/published/community/crypto/>`_
offers multiple modules that create private keys, certificate signing
requests, and certificates. This guide shows how to create your own
small CA and how to use it to sign certificates.

In all examples, we assume that the CA's private key is password
protected, where the password is provided in the
``secret_ca_passphrase`` variable.

Set up the CA
-------------

Any certificate can be used as a CA certificate. You can create a
self-signed certificate (see
:ref:`ansible_collections.community.crypto.docsite.guide_selfsigned`),
use another CA certificate to sign a new certificate (using the
instructions below for signing a certificate), ask (and pay) a
commercial CA to sign your CA certificate, etc.

...
```

If you want to reference modules, plugins, roles, their options and return values, see [the Ansible documentation's style guide](http://docs.testing.ansible.com/ansible/devel/dev_guide/style_guide/#adding-links-to-modules-and-plugins).

## Adding useful links to the docsite

You can add general links of interest to your collection page and the plugin pages, like for example links pointing to how to submit a bug report, how to request a feature, or where to ask for help. You can also provide links to communication channels like the Ansible Forum, Matrix rooms, IRC channels, and mailing lists.

These can be configured in `docs/docsite/links.yml`. A template showing what is available can be found below:

```yaml
---
# This will make sure that plugin and module documentation gets Edit on GitHub links
# that allow users to directly create a PR for this plugin or module in GitHub's UI.
# Remove this section if the collection repository is not on GitHub, or if you do not want this
# functionality for your collection.
edit_on_github:
  repository: ansible-collections/community.REPO_NAME
  branch: main
  # If your collection root (the directory containing galaxy.yml) does not coincide with your
  # repository's root, you have to specify the path to the collection root here. For example,
  # if the collection root is in a subdirectory ansible_collections/community/REPO_NAME
  # in your repository, you have to set path_prefix to 'ansible_collections/community/REPO_NAME'.
  path_prefix: ''

# Here you can add arbitrary extra links. Please keep the number of links down to a
# minimum! Also please keep the description short, since this will be the text put on
# a button.
#
# Also note that some links are automatically added from information in galaxy.yml.
# The following are automatically added:
#   1. A link to the issue tracker (if `issues` is specified);
#   2. A link to the homepage (if `homepage` is specified and does not equal the
#      `documentation` or `repository` link);
#   3. A link to the collection's repository (if `repository` is specified).

extra_links:
  - description: Report an issue
    url: https://github.com/ansible-collections/community.REPO_NAME/issues/new/choose

# Specify communication channels for your collection. We suggest to not specify more
# than one place for communication per communication tool to avoid confusion.
communication:
  forums:
    - topic: Ansible Forum
      # The following URL directly points to the "Get Help" section
      url: https://forum.ansible.com/c/help/6/none
  matrix_rooms:
    - topic: General usage and support questions
      room: '#users:ansible.im'
  irc_channels:
    # The IRC channels are only mentioned as examples and
    # should not be used except in very specific circumstances.
    - topic: General usage and support questions
      network: Libera
      channel: '#ansible'
  mailing_lists:
    # The mailing lists are only mentioned as examples and
    # should not be used except in very specific circumstances.
    # Please note that the ansible-project group used as an example
    # below is read-only and will soon vanish completely.
    - topic: Ansible Project List
      url: https://groups.google.com/g/ansible-project
      # You can also add a `subscribe` field with an URI that allows to subscribe
      # to the mailing list. For lists on https://groups.google.com/ a subscribe link is
      # automatically generated.
```

## Publishing a docsite with GitHub Actions

The [ansible-community/github-docs-build GitHub repository](https://github.com/ansible-community/github-docs-build) provides actions and shared workflows that can be used to:

* Build a collection docsite when pushing to the `main` branch, and uploading it for example to GitHub pages;
* Build a collection docsite during PRs, add a PR comment which shows the differences to the current documentation, and optionally push the PR docsite to GitHub pages so contributors can quickly see how their modified documentation looks like.

These are documented in detail in the [repository's Wiki](https://github.com/ansible-community/github-docs-build/wiki). Please refer to the Wiki for more information.

If you want to see this in action, you can take a look at the community.crypto collection:

* [Workflow for building documentation on push to `main` and `stable-*` branches](https://github.com/ansible-collections/community.crypto/blob/main/.github/workflows/docs-push.yml)
* [Workflow for PR documentation](https://github.com/ansible-collections/community.crypto/blob/main/.github/workflows/docs-pr.yml)

## Generating RST files for inclusion in the collection repository

Some collections include RST files for every module, plugin, and role they include in `docs/`. Traditionally, `collection_prep_add_docs` from the [ansible-network/collection_prep GitHub repository](https://github.com/ansible-network/collection_prep) was used for this, which [appears to be unmaintained](https://github.com/ansible-network/collection_prep/issues/91).

antsibull-docs now can also generate such files with the `collection-plugins` subcommand. This can be done as follows:
```console
$ cd ~/collections/ansible_collections/community/crypto
$ antsibull-docs collection-plugins --dest-dir docs/ --output-format simplified-rst --use-current --fqcn-plugin-names community.crypto
```
It is not clear to me why some collections chose to include these RST files in their repository. I would recommend not to do that, but instead provide a rendered docsite. If users want to read documentation using only the installed collection, they have a better experience using the `ansible-doc` command line tool, or building a HTML version of the docsite themselves and looking at it in a browser.
