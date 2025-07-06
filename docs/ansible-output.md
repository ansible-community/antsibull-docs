<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Updating ansible-playbook output in RST files

One common problem with Ansible playbook examples in documentation is that while it is helpful to include the playbook's output,
it is somewhat tedious to update the playbook output, especially when the used plugins or modules change.

Antsibull-docs has a tool, its `antsibull-docs ansible-output` subcommand, that lets you update the `ansible-playbook` output
in code blocks in RST files, and check whether they need to be updated (for example useful for CI).

## Metadata and code blocks

To know which code blocks to update and what playbook and environment variables to use, you need to provide a `ansible-output-data` directive before the actual code block:

```rst
.. ansible-output-data::

    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "90"
    playbook: |-
      - hosts: localhost
        gather_facts: false
        tasks:
          - name: Sort list by version number
            debug:
              var: ansible_versions | community.general.version_sort
            vars:
              ansible_versions:
                - '2.8.0'
                - '2.11.0'
                - '2.7.0'
                - '2.10.0'
                - '2.9.0'

.. code-block:: ansible-output

    TASK [Sort list by version number] ********************************************************
    ok: [localhost] => {
        "ansible_versions | community.general.version_sort": [
            "2.7.0",
            "2.8.0",
            "2.9.0",
            "2.10.0",
            "2.11.0"
        ]
    }
```

The `ansible-output-data` directive results in no output when the `sphinx_antsibull_ext` Sphinx extension is used, and contains YAML data.
The `env` dictionary allows to set environment variables that are set when calling `ansible-playbook`.
In this example, we set an explicit callback stdout plugin (using `ANSIBLE_STDOUT_CALLBACK`),
and provide configuration for that plugin (`ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH`).

The playbook is provided as a multi-line YAML string.
Antsibull-docs looks for the next code block with language `ansible-output`, and replaces its contents with the output of `ansible-playbook playbook.yml`,
where `playbook.yml` is filled with the provided playbook.

Note that the lanuage for the code block can be overridden by providing `language`.
Also you can prepend lines to the output using `prepend_lines`:

```rst
.. ansible-output-data::

    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "90"
    language: console
    prepend_lines: |
      $ ansible-playbook playbook.yml
    playbook: |-
      - hosts: localhost
        gather_facts: false
        tasks:
          - name: Sort list by version number
            debug:
              var: ansible_versions | community.general.version_sort
            vars:
              ansible_versions:
                - '2.8.0'
                - '2.11.0'
                - '2.7.0'
                - '2.10.0'
                - '2.9.0'

.. code-block:: console

    $ ansible-playbook playbook.yml

    TASK [Sort list by version number] ********************************************************
    ok: [localhost] => {
        "ansible_versions | community.general.version_sort": [
            "2.7.0",
            "2.8.0",
            "2.9.0",
            "2.10.0",
            "2.11.0"
        ]
    }
```

## Standalone usage

If you want to update a RST file, or all RST files in a directory, you can run antsibull-docs as follows:

```shell
$ antsibull-docs ansible-output /path/to/rst-file.rst
$ antsibull-docs ansible-output /path/to/directory-with-rst-files
```

If the provided path is a directory, it will recursively look for `.rst` files in it.

## Collection usage

If you run `antsibull-docs ansible-output` without a path, it assumes that you are in a collection's root directory.
(This is the directory that contains `galaxy.yml` or `MANIFEST.json`.)

It will check all `.rst` files in `docs/docsite/rst/`, if that directory exists,
and load configuration from `docs/docsite/config.yml`.
(See [more information on that configuration file](../collection-docs/#configuring-the-docsite).)
The configuration allows you to specify entries for `env` for all code blocks:

```yaml
---
# Configuration for 'antsibull-docs ansible-output'
ansible_output:
  # Insert definitions into 'env' for every ansible-output-data directive
  global_env:
    ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
    ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: 80
```

This is useful to standardize the callback and its settings for most code blocks in a collection's extra docs.
