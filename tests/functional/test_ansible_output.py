# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import io
import os
import subprocess
from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from unittest import mock

import pytest
from utils import change_cwd

from antsibull_docs.ansible_output.process import _compose_error
from antsibull_docs.cli.antsibull_docs import run


@dataclass
class FileContent:
    filename: str
    content: str


@dataclass
class AnsiblePlaybookSuccess:
    expected_cmd: list[str]
    expected_env: dict[str, str | None]
    file_contents: list[FileContent]
    stdout: str
    stderr: str = ""


@dataclass
class AnsiblePlaybookFailure:
    expected_cmd: list[str]
    expected_env: dict[str, str | None]
    file_contents: list[FileContent]
    rc: int
    stdout: str
    stderr: str


@contextmanager
def patch_ansible_playbook(
    *,
    ansible_playbook_command: AnsiblePlaybookSuccess | AnsiblePlaybookFailure | None,
) -> None:
    async def execute(
        command: list[str],
        *,
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
        stdin: str | None = None,
    ) -> str:
        if ansible_playbook_command is None:
            raise AssertionError("ansible-playbook should never have been called!")

        assert cwd is not None
        assert stdin is None
        assert env is not None
        for key, value in ansible_playbook_command.expected_env.items():
            if value is None:
                assert key not in env
            else:
                assert env[key] == value
        assert command == ansible_playbook_command.expected_cmd

        for file_content in ansible_playbook_command.file_contents:
            with open(
                os.path.join(cwd, file_content.filename), "rt", encoding="utf-8"
            ) as f:
                read_content = f.read()
            assert read_content == file_content.content

        if isinstance(ansible_playbook_command, AnsiblePlaybookSuccess):
            return ansible_playbook_command.stdout

        if isinstance(ansible_playbook_command, AnsiblePlaybookFailure):
            raise ValueError(
                _compose_error(
                    command=command,
                    returncode=ansible_playbook_command.rc,
                    stdout=ansible_playbook_command.stdout,
                    stderr=ansible_playbook_command.stderr,
                )
            )

        raise AssertionError("should not happen")  # pragma: no cover

    with mock.patch(
        "antsibull_docs.ansible_output.process._execute",
        execute,
    ):
        yield


EXPECTED_CHECK_RESULTS: list[
    tuple[str, str, AnsiblePlaybookSuccess | AnsiblePlaybookFailure | None, int, str]
] = [
    (
        "no-code-block.rst",
        """
Working with versions
---------------------

Foo.
""",
        None,
        0,
        "",
    ),
    (
        "no-data.rst",
        """
Working with versions
---------------------

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

.. versionadded: 2.2.0
""",
        None,
        0,
        "",
    ),
    (
        "working-test.rst",
        """
Working with versions
---------------------

If you need to sort a list of version numbers, the Jinja ``sort`` filter is problematic. Since it sorts lexicographically, ``2.10`` will come before ``2.9``. To treat version numbers correctly, you can use the :ansplugin:`community.general.version_sort filter <community.general.version_sort#filter>`:

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

This produces:

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

.. versionadded: 2.2.0
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
                "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
                "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "90",
            },
            [],
            """

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

""",
        ),
        0,
        "",
    ),
    (
        "modified-test.rst",
        """
.. ansible-output-data::

    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: 80
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

.. versionadded: 2.2.0
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
                "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
                "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "80",
            },
            [],
            """TASK [Sort list by version number] **********************************************
ok: [localhost] => {
    "ansible_versions | community.general.version_sort": [
        "2.7.0",
        "2.8.0",
        "2.10.0",
        "2.11.0"
    ]
}
""",
        ),
        3,
        r"""
Found 1 error:
modified-test.rst:23:5: Output would differ:
   - TASK [Sort list by version number] ********************************************************
   ?                                                                                  ----------
   + TASK [Sort list by version number] **********************************************
     ok: [localhost] => {
         "ansible_versions | community.general.version_sort": [
             "2.7.0",
             "2.8.0",
   -         "2.9.0",
             "2.10.0",
             "2.11.0"
   [... 2 lines skipped ...]
""",
    ),
    (
        "missing-test.rst",
        """
.. ansible-output-data::

    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "90"
    skip_first_lines: 1
    skip_last_lines: 1
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

    ...
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
                "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
                "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "90",
            },
            [],
            """should not be there
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
this neither
""",
        ),
        3,
        r"""
Found 1 error:
missing-test.rst:26:5: Output would differ:
   - ...
   + TASK [Sort list by version number] ********************************************************
   + ok: [localhost] => {
   +     "ansible_versions | community.general.version_sort": [
   +         "2.7.0",
   +         "2.8.0",
   +         "2.9.0",
   +         "2.10.0",
   +         "2.11.0"
   +     ]
   + }
""",
    ),
    (
        "broken-meta-yaml.rst",
        """
.. ansible-output-data::

    env: {
    playbook: |-
      foo
""",
        None,
        3,
        r"""
Found 1 error:
broken-meta-yaml.rst:5:15: Error while parsing content of ansible-output-data as YAML: while scanning for the next token
   found character that cannot start any token
     in "<byte string>", line 2, column 11
""",
    ),
    (
        "broken-meta-schema.rst",
        """
.. ansible-output-data::

    env: 123
    playbook: []
""",
        None,
        3,
        r"""
Found 1 error:
broken-meta-schema.rst:4:5: Error while validating ansible-output-data directive's contents:
   playbook: Input should be a valid string
   env: Input should be a valid dictionary
""",
    ),
    (
        "unused-ansible-output-data.rst",
        """
.. ansible-output-data::

    playbook: ""

.. ansible-output-data::

    playbook: ""

.. code-block:: ansible-output

    foo

.. ansible-output-data::

    playbook: ""

""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {},
            [],
            "foo\n",
        ),
        3,
        r"""
Found 2 errors:
unused-ansible-output-data.rst:4:5: ansible-output-data directive not used
unused-ansible-output-data.rst:16:5: ansible-output-data directive not used
""",
    ),
    (
        "multiple-empty-lines.rst",
        """
.. ansible-output-data::

    playbook: foo

.. code-block:: ansible-output

    foo
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {},
            [],
            """


foo


""",
        ),
        0,
        "",
    ),
    (
        "language-and-prepend.rst",
        """
.. ansible-output-data::

    playbook: ""
    prepend_lines: |-
      Hello
      World!
    language: bar

.. code-block:: foo

    foo

.. code-block:: bar

    Hello
    World!
    bar

.. code-block:: baz

    baz
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {},
            [],
            """
bar
""",
        ),
        0,
        "",
    ),
    (
        "working-test.rst",
        """
Working with versions
---------------------

If you need to sort a list of version numbers, the Jinja ``sort`` filter is problematic. Since it sorts lexicographically, ``2.10`` will come before ``2.9``. To treat version numbers correctly, you can use the :ansplugin:`community.general.version_sort filter <community.general.version_sort#filter>`:

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

This produces:

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

.. versionadded: 2.2.0
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
                "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
                "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "90",
            },
            [],
            """TASK [Sort list by version number] ********************************************************
ok: [localhost] => {
    "ansible_versions | community.general.version_sort": [
        "2.7.0",
        "2.8.0",
        "2.9.0",
        "2.10.0",
        "2.11.0"
    ]
}
""",
        ),
        0,
        "",
    ),
    (
        "complex-diff.rst",
        """
.. ansible-output-data::

    playbook: ""

.. code-block:: ansible-output

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    11 again
    12
    13
    14
    15
    16
    17
    18
    19
    20
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {},
            [],
            """
2
4
5
6
7
8
9
10
11
12
13
14
15
16
17
eighteen
nineteen
20
""",
        ),
        3,
        r"""
Found 1 error:
complex-diff.rst:8:5: Output would differ:
   - 1
     2
   - 3
     4
     5
   [... 4 lines skipped ...]
     10
     11
   - 11 again
     12
     13
   [... 2 lines skipped ...]
     16
     17
   - 18
   - 19
   + eighteen
   + nineteen
     20
""",
    ),
    (
        "working-test-in-table.rst",
        """
+----------------------------------------------------------------------+----------------------------------------------------------------+
| .. ansible-output-data::                                             | .. code-block:: ansible-output                                 |
|                                                                      |                                                                |
|     env:                                                             |     TASK [Sort list by version number] *********************** |
|       ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only          |     ok: [localhost] => {                                       |
|       ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "57"              |         "ansible_versions | community.general.version_sort": [ |
|     playbook: |-                                                     |             "2.7.0",                                           |
|       - hosts: localhost                                             |             "2.8.0",                                           |
|         gather_facts: false                                          |             "2.9.0",                                           |
|         tasks:                                                       |             "2.10.0",                                          |
|           - name: Sort list by version number                        |             "2.11.0"                                           |
|             debug:                                                   |         ]                                                      |
|               var: ansible_versions | community.general.version_sort |     }                                                          |
|             vars:                                                    |                                                                |
|               ansible_versions:                                      | .. versionadded: 2.2.0                                         |
|                 - '2.8.0'                                            |                                                                |
|                 - '2.11.0'                                           |                                                                |
|                 - '2.7.0'                                            |                                                                |
|                 - '2.10.0'                                           |                                                                |
|                 - '2.9.0'                                            |                                                                |
+----------------------------------------------------------------------+----------------------------------------------------------------+
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
                "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
                "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "57",
            },
            [],
            """TASK [Sort list by version number] ***********************
ok: [localhost] => {
    "ansible_versions | community.general.version_sort": [
        "2.7.0",
        "2.8.0",
        "2.9.0",
        "2.10.0",
        "2.11.0"
    ]
}
""",
        ),
        0,
        "",
    ),
    (
        "ansible-playbook-failure.rst",
        """
.. ansible-output-data::

    playbook: |-
      foo

.. code-block:: ansible-output

    bar
""",
        AnsiblePlaybookFailure(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
            },
            [],
            1,
            "Nothing to see here...",
            r"""Something bad happened.
Some traceback maybe?
Or just some blabla?
""",
        ),
        3,
        r"""
Found 1 error:
ansible-playbook-failure.rst:4:5: Error while computing code block's expected contents:
   Command ['ansible-playbook', 'playbook.yml'] returned non-zero exit status 1.
   Error output:
   Something bad happened.
   Some traceback maybe?
   Or just some blabla?


   Standard output:
   Nothing to see here...
""",
    ),
    (
        "ansible-playbook-failure-empty.rst",
        """
.. ansible-output-data::

    playbook: |-
      foo

.. code-block:: ansible-output

    bar
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
            },
            [],
            "\n\n  \n    \n",
        ),
        3,
        r"""
Found 1 error:
ansible-playbook-failure-empty.rst:4:5: Error while computing code block's expected contents:
   Output is empty
""",
    ),
    (
        "ansible-playbook-failure-variables-empty.rst",
        """
.. ansible-output-data::

    variables:
      foo: {}
    playbook: |-
      foo

.. code-block:: ansible-output

    bar
""",
        None,
        3,
        r"""
Found 1 error:
ansible-playbook-failure-variables-empty.rst:4:5: Error while validating ansible-output-data directive's contents:
   variables -> foo -> VariableSourceCodeBlock -> previous_code_block: Field required
   variables -> foo -> VariableSourceValue -> value: Field required
""",
    ),
    (
        "ansible-playbook-failure-variables-too-many.rst",
        """
.. ansible-output-data::

    variables:
      foo:
        previous_code_block: foo
        value: bar
    playbook: |-
      foo

.. code-block:: ansible-output

    bar
""",
        None,
        3,
        r"""
Found 1 error:
ansible-playbook-failure-variables-too-many.rst:4:5: Error while validating ansible-output-data directive's contents:
   variables -> foo -> VariableSourceCodeBlock -> value: Extra inputs are not permitted
   variables -> foo -> VariableSourceValue -> previous_code_block: Extra inputs are not permitted
""",
    ),
    (
        "ansible-playbook-failure-variables-does-exist.rst",
        """
.. code-block:: yaml

    foo: foo!

.. code-block:: yaml

    foo: bar

.. ansible-output-data::

    variables:
      foo:
        previous_code_block: yaml
        previous_code_block_index: 1
    playbook: |-
      foo @{{ foo }}@

.. code-block:: ansible-output

    bar
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {},
            [
                FileContent(
                    "playbook.yml",
                    "foo foo: bar\n",
                ),
            ],
            "meh",
        ),
        3,
        r"""
Found 1 error:
ansible-playbook-failure-variables-does-exist.rst:21:5: Output would differ:
   - bar
   + meh
""",
    ),
    (
        "ansible-playbook-failure-variables-does-not-exist.rst",
        """
.. code-block:: yaml

    foo: foo!

.. ansible-output-meta::

    actions:
      - name: reset-previous-blocks

.. code-block:: yaml

    foo: bar

.. ansible-output-data::

    variables:
      foo:
        previous_code_block: yaml
        previous_code_block_index: 1
    playbook: |-
      foo @{{ foo }}@

.. code-block:: ansible-output

    bar
""",
        None,
        3,
        r"""
Found 1 error:
ansible-playbook-failure-variables-does-not-exist.rst:17:5: Error while computing code block's expected contents:
   Found 1 previous code block(s) of language 'yaml' for variable 'foo', which does not allow index 1
""",
    ),
    (
        "ansible-playbook-failure-variables-reset.rst",
        """
.. code-block:: yaml

    foo: foo!

.. ansible-output-meta::

    actions:
      - name: reset-previous-blocks

.. code-block:: yaml

    foo: bar

.. ansible-output-data::

    variables:
      foo:
        previous_code_block: yaml
    playbook: |-
      foo @{{ foo }}@

.. code-block:: ansible-output

    bar
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {},
            [
                FileContent(
                    "playbook.yml",
                    "foo foo: bar\n",
                ),
            ],
            "meh",
        ),
        3,
        r"""
Found 1 error:
ansible-playbook-failure-variables-reset.rst:25:5: Output would differ:
   - bar
   + meh
""",
    ),
    (
        "ansible-playbook-bad-template.rst",
        """
.. ansible-output-data::

    playbook: |-
      foo @{{

.. code-block:: ansible-output

    bar
""",
        None,
        3,
        r"""
Found 1 error:
ansible-playbook-bad-template.rst:4:5: Error while computing code block's expected contents:
   Error while templating playbook:
   unexpected 'end of template'
""",
    ),
]


@pytest.mark.parametrize(
    "rst_filename, rst_content, ansible_playbook_command, expected_rc, expected_stdout",
    EXPECTED_CHECK_RESULTS,
    ids=[entry[0] for entry in EXPECTED_CHECK_RESULTS],
)
def test_ansible_output_check(
    rst_filename: str,
    rst_content: str,
    ansible_playbook_command: AnsiblePlaybookSuccess | AnsiblePlaybookFailure | None,
    expected_rc: int,
    expected_stdout: str,
    tmp_path: Path,
):
    command = [
        "antsibull-docs",
        "ansible-output",
        "--check",
        "--no-force-color",
        rst_filename,
    ]

    (tmp_path / rst_filename).write_text(rst_content)

    stdout = io.StringIO()
    with change_cwd(tmp_path):
        with redirect_stdout(stdout):
            with patch_ansible_playbook(
                ansible_playbook_command=ansible_playbook_command
            ):
                actual_rc = run(command)
    print(f"RC: {actual_rc}")
    print("Stdout:")
    print(stdout.getvalue())
    assert actual_rc == expected_rc
    assert stdout.getvalue() == expected_stdout


EXPECTED_REPLACE_RESULTS: list[
    tuple[
        str,
        str,
        AnsiblePlaybookSuccess | AnsiblePlaybookFailure | None,
        int,
        str,
        bool,
        str,
    ]
] = [
    (
        "no-code-block.rst",
        """
Working with versions
---------------------

Foo.
""",
        None,
        0,
        "",
        False,
        """
Working with versions
---------------------

Foo.
""",
    ),
    (
        "working-test.rst",
        """
Working with versions
---------------------

This produces:

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

.. versionadded: 2.2.0
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
                "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
                "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "90",
            },
            [],
            """TASK [Sort list by version number] ********************************************************
ok: [localhost] => {
    "ansible_versions | community.general.version_sort": [
        "2.7.0",
        "2.8.0",
        "2.9.0",
        "2.10.0",
        "2.11.0"
    ]
}
""",
        ),
        0,
        "",
        False,
        """
Working with versions
---------------------

This produces:

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

.. versionadded: 2.2.0
""",
    ),
    (
        "working-test-variables.rst",
        """
Working with versions
---------------------

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

This produces:

.. ansible-output-data::

    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "90"
    variables:
      host:
        value: localhost
      task:
        previous_code_block: yaml+jinja
    playbook: |-
      - hosts: @{{ host }}@
        gather_facts: false
        tasks:
          @{{ task | indent(4) }}@

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

.. versionadded: 2.2.0
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
                "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
                "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "90",
            },
            [
                FileContent(
                    "playbook.yml",
                    r"""- hosts: localhost
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
""",
                ),
            ],
            """TASK [Sort list by version number] ********************************************************
ok: [localhost] => {
    "ansible_versions | community.general.version_sort": [
        "2.7.0",
        "2.8.0",
        "2.9.0",
        "2.10.0",
        "2.11.0"
    ]
}
""",
        ),
        0,
        "",
        False,
        """
Working with versions
---------------------

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

This produces:

.. ansible-output-data::

    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "90"
    variables:
      host:
        value: localhost
      task:
        previous_code_block: yaml+jinja
    playbook: |-
      - hosts: @{{ host }}@
        gather_facts: false
        tasks:
          @{{ task | indent(4) }}@

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

.. versionadded: 2.2.0
""",
    ),
    (
        "modified-test.rst",
        """
.. ansible-output-data::

    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: 80
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

.. versionadded: 2.2.0
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
                "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
                "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "80",
            },
            [],
            """TASK [Sort list by version number] **********************************************
ok: [localhost] => {
    "ansible_versions | community.general.version_sort": [
        "2.7.0",
        "2.8.0",
        "2.10.0",
        "2.11.0"
    ]
}
""",
        ),
        0,
        "Write modified-test.rst...\n",
        True,
        """
.. ansible-output-data::

    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: 80
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

.. code-block:: ansible-output

    TASK [Sort list by version number] **********************************************
    ok: [localhost] => {
        "ansible_versions | community.general.version_sort": [
            "2.7.0",
            "2.8.0",
            "2.10.0",
            "2.11.0"
        ]
    }

.. versionadded: 2.2.0
""",
    ),
    (
        "working-test-in-table.rst",
        """
+----------------------------------------------------------------------+----------------------------------------------------------------+
| .. ansible-output-data::                                             | .. code-block:: ansible-output                                 |
|                                                                      |                                                                |
|     env:                                                             |     TASK [Sort list by version number] *********************** |
|       ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only          |     ok: [localhost] => {                                       |
|       ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "57"              |         "ansible_versions | community.general.version_sort": [ |
|     playbook: |-                                                     |             "2.7.0",                                           |
|       - hosts: localhost                                             |             "2.8.0",                                           |
|         gather_facts: false                                          |             "2.9.0",                                           |
|         tasks:                                                       |             "2.10.0",                                          |
|           - name: Sort list by version number                        |             "2.11.0"                                           |
|             debug:                                                   |         ]                                                      |
|               var: ansible_versions | community.general.version_sort |     }                                                          |
|             vars:                                                    |                                                                |
|               ansible_versions:                                      | .. versionadded: 2.2.0                                         |
|                 - '2.8.0'                                            |                                                                |
|                 - '2.11.0'                                           |                                                                |
|                 - '2.7.0'                                            |                                                                |
|                 - '2.10.0'                                           |                                                                |
|                 - '2.9.0'                                            |                                                                |
+----------------------------------------------------------------------+----------------------------------------------------------------+
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
                "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
                "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "57",
            },
            [],
            """TASK [Sort list by version number] ***********************
ok: [localhost] => {
    "ansible_versions | community.general.version_sort": [
        "2.7.0",
        "2.8.0",
        "2.9.0",
        "2.10.0",
        "2.11.0"
    ]
}
""",
        ),
        0,
        "",
        False,
        """
+----------------------------------------------------------------------+----------------------------------------------------------------+
| .. ansible-output-data::                                             | .. code-block:: ansible-output                                 |
|                                                                      |                                                                |
|     env:                                                             |     TASK [Sort list by version number] *********************** |
|       ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only          |     ok: [localhost] => {                                       |
|       ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "57"              |         "ansible_versions | community.general.version_sort": [ |
|     playbook: |-                                                     |             "2.7.0",                                           |
|       - hosts: localhost                                             |             "2.8.0",                                           |
|         gather_facts: false                                          |             "2.9.0",                                           |
|         tasks:                                                       |             "2.10.0",                                          |
|           - name: Sort list by version number                        |             "2.11.0"                                           |
|             debug:                                                   |         ]                                                      |
|               var: ansible_versions | community.general.version_sort |     }                                                          |
|             vars:                                                    |                                                                |
|               ansible_versions:                                      | .. versionadded: 2.2.0                                         |
|                 - '2.8.0'                                            |                                                                |
|                 - '2.11.0'                                           |                                                                |
|                 - '2.7.0'                                            |                                                                |
|                 - '2.10.0'                                           |                                                                |
|                 - '2.9.0'                                            |                                                                |
+----------------------------------------------------------------------+----------------------------------------------------------------+
""",
    ),
    (
        "failing-test-in-table.rst",
        """
+----------------------------------------------------------------------+----------------------------------------------------------------+
| .. ansible-output-data::                                             | .. code-block:: ansible-output                                 |
|                                                                      |                                                                |
|     env:                                                             |     TASK [Sort list by version number] *********************** |
|       ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only          |     ok: [localhost] => {                                       |
|       ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "57"              |         "ansible_versions | community.general.version_sort": [ |
|     playbook: |-                                                     |             "2.7.0",                                           |
|       - hosts: localhost                                             |             "2.8.0",                                           |
|         gather_facts: false                                          |             "2.9.0",                                           |
|         tasks:                                                       |             "2.10.0",                                          |
|           - name: Sort list by version number                        |             "2.11.0"                                           |
|             debug:                                                   |         ]                                                      |
|               var: ansible_versions | community.general.version_sort |     }                                                          |
|             vars:                                                    |                                                                |
|               ansible_versions:                                      | .. versionadded: 2.2.0                                         |
|                 - '2.8.0'                                            |                                                                |
|                 - '2.11.0'                                           |                                                                |
|                 - '2.7.0'                                            |                                                                |
|                 - '2.10.0'                                           |                                                                |
|                 - '2.9.0'                                            |                                                                |
+----------------------------------------------------------------------+----------------------------------------------------------------+
""",
        AnsiblePlaybookSuccess(
            ["ansible-playbook", "playbook.yml"],
            {
                "NO_COLOR": "true",
                "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
                "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "57",
            },
            [],
            """TASK [Sort list by version number] ***********************
ok: [localhost] => {
    "ansible_versions | community.general.version_sort": [
        "2.8.0",
        "2.9.0",
        "2.10.0",
        "2.11.0"
    ]
}
""",
        ),
        3,
        r"""
Found 1 error:
failing-test-in-table.rst:6:1: Code block is not replacable
""",
        False,
        """
+----------------------------------------------------------------------+----------------------------------------------------------------+
| .. ansible-output-data::                                             | .. code-block:: ansible-output                                 |
|                                                                      |                                                                |
|     env:                                                             |     TASK [Sort list by version number] *********************** |
|       ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only          |     ok: [localhost] => {                                       |
|       ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "57"              |         "ansible_versions | community.general.version_sort": [ |
|     playbook: |-                                                     |             "2.7.0",                                           |
|       - hosts: localhost                                             |             "2.8.0",                                           |
|         gather_facts: false                                          |             "2.9.0",                                           |
|         tasks:                                                       |             "2.10.0",                                          |
|           - name: Sort list by version number                        |             "2.11.0"                                           |
|             debug:                                                   |         ]                                                      |
|               var: ansible_versions | community.general.version_sort |     }                                                          |
|             vars:                                                    |                                                                |
|               ansible_versions:                                      | .. versionadded: 2.2.0                                         |
|                 - '2.8.0'                                            |                                                                |
|                 - '2.11.0'                                           |                                                                |
|                 - '2.7.0'                                            |                                                                |
|                 - '2.10.0'                                           |                                                                |
|                 - '2.9.0'                                            |                                                                |
+----------------------------------------------------------------------+----------------------------------------------------------------+
""",
    ),
]


def is_stat_equal(first: os.stat_result, second: os.stat_result) -> bool:
    return first.st_mtime_ns == second.st_mtime_ns and first.st_size == second.st_size


@pytest.mark.parametrize(
    "rst_filename, rst_content, ansible_playbook_command, expected_rc, expected_stdout, rst_updated, rst_new_content",
    EXPECTED_REPLACE_RESULTS,
    ids=[entry[0] for entry in EXPECTED_REPLACE_RESULTS],
)
def test_ansible_output_replace(
    rst_filename: str,
    rst_content: str,
    ansible_playbook_command: AnsiblePlaybookSuccess | AnsiblePlaybookFailure | None,
    expected_rc: int,
    expected_stdout: str,
    rst_updated: bool,
    rst_new_content: str,
    tmp_path: Path,
):
    command = [
        "antsibull-docs",
        "ansible-output",
        "--no-force-color",
        rst_filename,
    ]

    rst_path = tmp_path / rst_filename
    rst_path.write_text(rst_content)
    old_stat = rst_path.stat()

    stdout = io.StringIO()
    with change_cwd(tmp_path):
        with redirect_stdout(stdout):
            with patch_ansible_playbook(
                ansible_playbook_command=ansible_playbook_command
            ):
                actual_rc = run(command)
    print(f"RC: {actual_rc}")
    print("Stdout:")
    print(stdout.getvalue())
    assert actual_rc == expected_rc
    assert stdout.getvalue() == expected_stdout

    new_stat = rst_path.stat()
    if rst_updated:
        assert not is_stat_equal(old_stat, new_stat)
    else:
        assert is_stat_equal(old_stat, new_stat)
    assert rst_path.read_text() == rst_new_content
