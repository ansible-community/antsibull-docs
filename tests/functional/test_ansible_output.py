# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import io
from contextlib import contextmanager, redirect_stdout
from pathlib import Path
from unittest import mock

import pytest
from utils import change_cwd

from antsibull_docs.cli.antsibull_docs import run


@contextmanager
def patch_ansible_playbook(
    *,
    expected_cmd: list[str],
    expected_env: dict[str, str | None],
    stdout: str = "",
    stderr: str = "",
) -> None:
    class Result:
        def __init__(self) -> None:
            self.returncode = 0
            self.stdout = stdout
            self.stderr = stderr

    def subprocess_run(
        command,
        *,
        capture_output: bool,
        cwd: str | Path,
        env: dict[str, str],
        check: bool,
        encoding: str,
    ) -> Result:
        assert capture_output == True
        assert cwd is not None
        assert check is True
        assert encoding == "utf-8"
        for key, value in expected_env.items():
            if value is None:
                assert key not in env
            else:
                assert env[key] == value
        assert command == expected_cmd
        return Result()

    with mock.patch(
        "antsibull_docs.cli.doc_commands.ansible_output.subprocess.run",
        subprocess_run,
    ):
        yield


EXPECTED_CHECK_RESULTS: list[
    tuple[str, str, list[str], dict[str, str | None], str, int, str]
] = [
    (
        "no-code-block.rst",
        """
Working with versions
---------------------

Foo.
""",
        [],
        {},
        "",
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
        [],
        {},
        "",
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
        ["ansible-playbook", "playbook.yml"],
        {
            "NO_COLOR": "true",
            "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
            "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "90",
        },
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
        0,
        "",
    ),
    (
        "modified-test.rst",
        """
.. ansible-output-data::

    env:
      ANSIBLE_STDOUT_CALLBACK: community.general.tasks_only
      ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH: "80"
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
        ["ansible-playbook", "playbook.yml"],
        {
            "NO_COLOR": "true",
            "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
            "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "80",
        },
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
        ["ansible-playbook", "playbook.yml"],
        {
            "NO_COLOR": "true",
            "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
            "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "90",
        },
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
        3,
        r"""
Found 1 error:
missing-test.rst:24:5: Output would differ:
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
        [],
        {},
        "",
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
        [],
        {},
        "",
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
        ["ansible-playbook", "playbook.yml"],
        {},
        "foo\n",
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
        ["ansible-playbook", "playbook.yml"],
        {},
        """


foo


""",
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
        ["ansible-playbook", "playbook.yml"],
        {},
        """
bar
""",
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
        ["ansible-playbook", "playbook.yml"],
        {
            "NO_COLOR": "true",
            "ANSIBLE_STDOUT_CALLBACK": "community.general.tasks_only",
            "ANSIBLE_COLLECTIONS_TASKS_ONLY_COLUMN_WIDTH": "90",
        },
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
        ["ansible-playbook", "playbook.yml"],
        {},
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
]


@pytest.mark.parametrize(
    "rst_filename, rst_content, ansible_playbook_expected_cmd, ansible_playbook_expected_env, ansible_playbook_output, expected_rc, expected_stdout",
    EXPECTED_CHECK_RESULTS,
    ids=[entry[0] for entry in EXPECTED_CHECK_RESULTS],
)
def test_ansible_output_check(
    rst_filename: str,
    rst_content: str,
    ansible_playbook_expected_cmd: list[str],
    ansible_playbook_expected_env: dict[str, str | None],
    ansible_playbook_output: str,
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
                expected_cmd=ansible_playbook_expected_cmd,
                expected_env=ansible_playbook_expected_env,
                stdout=ansible_playbook_output,
            ):
                actual_rc = run(command)
    print(f"RC: {actual_rc}")
    print("Stdout:")
    print(stdout.getvalue())
    assert actual_rc == expected_rc
    assert stdout.getvalue() == expected_stdout
