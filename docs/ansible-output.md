<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Updating ansible-playbook output in RST files

One common problem with Ansible playbook examples in documentation is that while it is helpful to include the playbook's output,
it is somewhat tedious to update the playbook output, especially when changes occur to plugins or modules.

Antsibull-docs provides a tool through the `antsibull-docs ansible-output` subcommand that lets you update the `ansible-playbook` output in code blocks within RST files. The `antsibull-docs ansible-output` subcommand also lets you check whether code blocks need to be updated, which can be a useful consistency check in CI pipelines.

## Metadata and code blocks

To know which code blocks to update and what playbook and environment variables to use,
you need to provide a `ansible-output-data` directive before the actual code block:

```rst
.. ansible-output-data::

    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_NUMBER_OF_COLUMNS: "90"
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

Antsibull-docs looks for the next code block with language `ansible-output`,
and replaces its contents with the output of `ansible-playbook playbook.yml`,
where `playbook.yml` is filled with the provided playbook.

### The `ansible-output-data` directive in detail

The `ansible-output-data` directive does not generate any visible content in rendered documentation when the `sphinx_antsibull_ext` Sphinx extension is used.
The directive contains YAML configuration data that is meant for `antsibull-docs` and not for readers.
In the YAML configuration you can use the following top-level keys.
Also take a look at the example further below which demonstrates all of them.

* The playbook is provided as a multi-line YAML string `playbook`.
  Note that you can use Jinja expressions; to avoid clashes with Ansible's use of Jinja,
  you need to prepend and append `@` to template expressions, statements, and comments:

  * Expressions are of the form `@{{ expression }}@`;
  * Statements are of the form `@{% statement %}@`;
  * Comments are of the form `@{# Comment #}@`.

* The `variables` directionary allows you to define variables that can be used for templating the playbook.
  The key in the dictionary is the variable's name, and the value is a dictionary with exactly one of the following keys:

  * `value`: provide a string that defines the value of the variable.
  * `previous_code_block`: the content of the last code block before the `ansible-output-data` directive of this language will be used as the value.
    The additional key `previous_code_block_index` (integer, default `-1`) determines which of the previous code blocks of the given language is picked.
    An index of `0` uses the first one in the file; `1` the second; `-1` the last one; and `-2` the second to last before the `ansible-output-data` directive.

* The `env` dictionary allows you to set environment variables that are set when calling `ansible-playbook`.
  In the example further below, we set an explicit callback stdout plugin (using `ANSIBLE_STDOUT_CALLBACK`)
  and provide configuration for that plugin (`ANSIBLE_COLLECTIONS_TASKS_ONLY_NUMBER_OF_COLUMNS`).

* The `language` key allows to override the language for the code block that will be replaced.
  By default `antsibull-docs ansible-output` looks for code blocks of language `ansible-output`.

* The `skip_first_lines` key allows to remove a fixed number of lines from the beginning of the `ansible-playbook` output.

* The `skip_last_lines` key allows to remove a fixed number of lines from the end of the `ansible-playbook` output.

* The `prepend_lines` key allows to prepend a multi-line YAML string to the `ansible-playbook` output.

* The `postprocessors` key allows to define a list of post-processors.
  This is explained in more detail in the [Post-processing ansible-playbook output section](#post-processing-ansible-playbook-output).

* The `inventory` key allows to define a YAML inventory. See the
  [Ansible documentation on inventories](https://docs.ansible.com/projects/ansible/latest/inventory_guide/intro_inventory.html)
  for the format of a YAML inventory.

An example looks like this. The `console` code block contains the generated result:
```rst
This is an Ansible task we're going to reference in the playbook:

.. code-block:: yaml+jinja

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

.. ansible-output-data::

    ---
    # Note that the content of the 'ansible-output-data' directive
    # is hidden from the user
    # (assuming you are using the sphinx_antsibull_ext Sphinx extension)

    # Use the community.general.tasks_only callback plugin
    # and configure it to use 90 columns by setting appropriate
    # environment variables:
    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_NUMBER_OF_COLUMNS: "90"

    # Look for the next code-block with language 'console':
    language: console

    # Prepend the following lines to the output of 'ansible-playbook'.
    # In this case, we add a fake console prompt that seems to run the
    # playbook:
    prepend_lines: |
      $ ansible-playbook playbook.yml

    # Remove the first three lines at the beginning of the playbook.
    # This is the output for the 'ansible.builtin.set_fact' task:
    skip_first_lines: 3

    # Do not remove lines at the end of the playbook
    skip_last_lines: 0

    # Define variables for templating the playbook
    variables:
      hosts:
        value: localhost
      tasks:
        previous_code_block: yaml+jinja
        previous_code_block_index: -1

    # No post-processors
    postprocessors: []

    # Basic inventory with localhost
    inventory:
      ungrouped:
        localhost:
          ansible_connection: local

    # The actual playbook to run:
    playbook: |-
      @{# Use the 'hosts' variable defined above #}@
      - hosts: @{{ hosts }}@
        gather_facts: false
        tasks:
          - name: Set some value.
            ansible.builtin.set_fact:
              some_variable: some_value
      @{# Insert tasks from the previous code block #}@
      @{# (We need to indent all other lines by 4 spaces) #}@
          @{{ tasks | indent(4) }}@

The task produces the following output:

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

## Controlling code block contexts

Next to the `ansible-output-data` RST directive, antsibull-docs also provides a `ansible-output-meta` RST directive.
This meta directive allows to apply actions to the context for the next `ansible-output-data` directives.

### Reset previous code blocks

The `reset-previous-blocks` action resets the list of previous code blocks.
It can be used as follows:
```rst
.. ansible-output-meta::

  actions:
    - name: reset-previous-blocks
```

This is relevant when using `previous_code_block` variables where you specify `previous_code_block_index`.
If you want several consecutive `ansible-output-data` directives to reference the same code block,
you can reset the previous blocks directly before that code block,
and then reference that code block as the one with index `0`:
```rst
(more text with other code blocks)

.. ansible-output-meta::

  actions:
    - name: reset-previous-blocks

.. code-block:: yaml

  # This code block now has index 0, no matter how many other code blocks
  # came before the above action.
  foo: bar

Now you can have multiple ansible-output-data directives referencing the
above ``yaml`` block as the ``yaml`` block with index 0:

.. ansible-output-data::

    variables:
      content:
        previous_code_block: yaml
        previous_code_block_index: 0
    playbook: |-
      - hosts: localhost
        tasks:
          - ansible.builtin.debug:
              msg: "{{ data }}"
            vars:
              data:
                @{{ content | indent(10) }}@

.. code-block:: ansible-output

  ...
```

### Define template for `ansible-output-data`

The `set-template` action defines a template for all following `ansible-output-data` directives.
You can use all fields that you can also use for `ansible-output-data` in the template:
```rst
.. ansible-output-meta::

  actions:
    - name: set-template
      template:
        # The environment variables will be merged. If a variable is provided here,
        # you do not have to provide it again in the directive - only if you want to
        # override its value.
        env:
          ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
          ANSIBLE_COLLECTIONS_TASKS_ONLY_NUMBER_OF_COLUMNS: "90"

        # Will use this value if not specified in the directive.
        # If no language is provided in both the template and the directive,
        # 'ansible-output' will be used.
        language: console

        # Will use this value if not specified in the directive.
        prepend_lines: |
          $ ansible-playbook playbook.yml

        # Will use this value if not specified in the directive.
        skip_first_lines: 3

        # Will use this value if not specified in the directive.
        skip_last_lines: 0

        # The variables will be merged. If a varibale is provided here,
        # you can override it in the directive by specifying a variable
        # of the same name.
        variables:
          hosts:
            value: localhost
          tasks:
            previous_code_block: yaml+jinja
            previous_code_block_index: -1

        # Will use this value if not specified in the directive.
        postprocessors: []

        # Will use this value if not specified in the directive.
        inventory: {}

        # Will use this value if explicitly set to null/~ in the directive.
        playbook: |-
          (some Ansible playbook)
```

This can be useful to avoid repeating some definitions for multiple code blocks.
If another `ansible-output-meta` action sets a new template, the previous templates will be thrown away.

## Post-processing ansible-playbook output

Out of the box, you can post-process the `ansible-playbook` output in some ways:

* Skip a fixed number of lines at the top (`skip_first_lines`) or bottom (`skip_last_lines`).
* Prepend lines to the output (`prepend_lines`).

This, together with chosing an appropriate callback plugin
(like [community.general.tasks_only](https://docs.ansible.com/projects/ansible/devel/collections/community/general/tasks_only_callback.html))
gives you a lot of freedom to get the output you want.

In some cases, it is not sufficient though.
For example, if you want to extract YAML output, and present it in a way that [matches your yamllint configuration](https://docs.ansible.com/projects/antsibull-nox/config-file/#yamllint-part-of-the-yamllint-session).
The default callback's YAML output suffers from [PyYAML's list indentation issue](https://github.com/yaml/pyyaml/issues/234),
which causes problems with many yamllint configurations.
Also, the [ansible.builtin.default callback's YAML output](https://docs.ansible.com/projects/ansible/devel/collections/ansible/builtin/default_callback.html#parameter-result_format) is indented by 4 spaces,
while most YAML is expected to be indented by 2 spaces.

If you use the above settings (`skip_first_lines` / `skip_last_lines`) to extract only the YAML content of one task of the playbook's output,
you can for example use [Pretty YAML (pyaml)](https://pypi.org/project/pyaml/) to reformat it.
For that, you can use the `postprocessors` list to specify a post-processor command:
```yaml
postprocessors:
  - command:
      - python
      - "-m"
      - pyaml
```
This tells `antsibull-docs ansible-output` to feed the extracted output
(with `skip_first_lines`, `skip_last_lines`, and `prepend_lines` already processed)
through standard input into the `python -m pyaml` process,
and use its output instead.

A full example looks like this:
```rst
.. code-block:: yaml+jinja

   input:
     - k0_x0: A0
       k1_x1: B0
       k2_x2: [C0]
       k3_x3: foo
     - k0_x0: A1
       k1_x1: B1
       k2_x2: [C1]
       k3_x3: bar

   target:
     - {after: a0, before: k0_x0}
     - {after: a1, before: k1_x1}

   result: "{{ input | community.general.replace_keys(target=target) }}"

.. ansible-output-data::

    env:
      ANSIBLE_CALLBACK_RESULT_FORMAT: yaml
    variables:
      data:
        previous_code_block: yaml+jinja
    postprocessors:
      - command:
          - python
          - "-m"
          - pyaml
    language: yaml
    skip_first_lines: 4
    skip_last_lines: 3
    playbook: |-
      - hosts: localhost
        gather_facts: false
        tasks:
          - vars:
              @{{ data | indent(8) }}@
            ansible.builtin.debug:
              var: result

This results in:

.. code-block:: yaml

   result:
     - a0: A0
       a1: B0
       k2_x2:
         - C0
       k3_x3: foo
     - a0: A1
       a1: B1
       k2_x2:
         - C1
       k3_x3: bar
```

Right now there are two kind of post-processor entries in `postprocessors`:

1. Command-based post-processors:

    You can provide a list `command`.
    This command is executed,
    the input fed in through standard input,
    and its standard output is taken as the output.

    Example:
    ```yaml
    postprocessors:
      - command:
          - python
          - "-m"
          - pyaml
    ```

2. Name-reference post-processors:

    You can use `name` to reference a named globally defined post-processor.
    This is right now only possible in collections,
    since you need to define these in the collection's config file
    (`docs/docsite/config.yml` - see the [Collection usage section](#collection-usage)).

    Example:
    ```yaml
    postprocessors:
      - name: reformat-yaml
    ```

## Standalone usage

If you want to update a RST file, or all RST files in a directory, you can run antsibull-docs as follows:

```shell
$ antsibull-docs ansible-output /path/to/rst-file.rst
$ antsibull-docs ansible-output /path/to/directory-with-rst-files
```

If the provided path is a directory, it will recursively look for `.rst` files in it.

You can pass a path to a config file with `--config /path/to/config.yaml`.
You can use the keys that are described as part of `ansible_output` in [the following section](#collection-usage).

This can look as follows:
```yaml
---
# Configuration for 'antsibull-docs ansible-output'

# Insert definitions into 'env' for every ansible-output-data directive
global_env:
  ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
  ANSIBLE_COLLECTIONS_TASKS_ONLY_NUMBER_OF_COLUMNS: 80

# Global post-processors for Ansible output
global_postprocessors:
  # Keys are the names that can be referenced in ansible-output-data directives
  reformat-yaml:
    # For CLI tools, you can specify a command that accepts input on stdin
    # and outputs the result on stdout:
    command:
      - python
      - "-m"
      - pyaml
```

## Collection usage

If you run `antsibull-docs ansible-output` without a path, it assumes that you are in a collection's root directory.
(This is the directory that contains `galaxy.yml` or `MANIFEST.json`.)

It will check all `.rst` files in `docs/docsite/rst/`, if that directory exists,
and load configuration from `docs/docsite/config.yml`.
(See [more information on that configuration file](../collection-docs/#configuring-the-docsite).)
The configuration allows you to specify entries for `env` for all code blocks,
and you can define global post-processors that can be referenced in `postprocessors`:

```yaml
---
# Configuration for 'antsibull-docs ansible-output'
ansible_output:
  # Insert definitions into 'env' for every ansible-output-data directive
  global_env:
    ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
    ANSIBLE_COLLECTIONS_TASKS_ONLY_NUMBER_OF_COLUMNS: 80

  # Global post-processors for Ansible output
  global_postprocessors:
    # Keys are the names that can be referenced in ansible-output-data directives
    reformat-yaml:
      # For CLI tools, you can specify a command that accepts input on stdin
      # and outputs the result on stdout:
      command:
        - python
        - "-m"
        - pyaml
```

This is useful to standardize the callback and its settings for most code blocks in a collection's extra docs,
and set up a pre-defined set of post-processors that can be used everywhere.

## Usage in CI

If you want to run `antsibull-docs ansible-output` in CI, you might find the `--check` parameter useful.
If that parameter is specified, antsibull-docs will not update files, but instead fail if a file would be modified.
A diff of the changes that would be applied will be printed to standard output.

!!! warning
    Please note that you have to make sure that `antsibull-docs ansible-output` runs in CI with the minimum set of privileges,
    since it can run **arbitrary code**!

    Someone can add a playbook to documentation that recursively deletes all files you have access to.
    If you run `antsibull-docs ansible-output` (with or without `--check`) on such a RST file without sufficient isolation,
    all your files will be deleted.

    If you run `antsibull-docs ansible-output` in CI in a context where the code run has access to credentials,
    a playbook could send these credentials to an arbitrary location on the internet.
