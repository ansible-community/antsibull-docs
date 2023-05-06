# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import io
import os
from contextlib import contextmanager, redirect_stdout

import pytest
from ansible_doc_caching import ansible_doc_cache

from antsibull_docs.cli.antsibull_docs import run


def write_file(path, content):
    with open(path, "wb") as f:
        f.write(content)


def test_docsite_linting_success(tmp_path_factory):
    dir = tmp_path_factory.mktemp("foobar")
    write_file(
        dir / "galaxy.yml",
        b"""
namespace: foo
name: bar
""",
    )
    docsite_dir = dir / "docs" / "docsite"
    docsite_rst_dir = docsite_dir / "rst"
    os.makedirs(docsite_rst_dir)
    write_file(
        docsite_dir / "extra-docs.yml",
        b"""
sections:
  - title: Foo
    toctree:
      - foo

""",
    )
    write_file(
        docsite_dir / "links.yml",
        b"""
edit_on_github:
  repository: ansible-collections/foo.bar
  branch: main
  path_prefix: ''

extra_links:
  - description: Submit an issue
    url: https://github.com/ansible-collections/foo.bar/issues/new

communication:
  matrix_rooms:
    - topic: General usage and support questions
      room: '#users:ansible.im'
  irc_channels:
    - topic: General usage and support questions
      network: Libera
      channel: '#ansible'
  mailing_lists:
    - topic: Ansible Project List
      url: https://groups.google.com/g/ansible-project
""",
    )
    write_file(
        docsite_rst_dir / "foo.rst",
        b"""
.. _ansible_collections.foo.bar.docsite.bla:

Foo bar
=======

Baz bam :ref:`myself <ansible_collections.foo.bar.docsite.bla>`.
""",
    )

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        rc = run(["antsibull-docs", "lint-collection-docs", str(dir)])
    stdout = stdout.getvalue().splitlines()
    print("\n".join(stdout))
    assert rc == 0
    assert stdout == []


def test_docsite_linting_failure(tmp_path_factory):
    dir = tmp_path_factory.mktemp("foo.bar")
    write_file(
        dir / "galaxy.yml",
        b"""
namespace: foo
name: bar
""",
    )
    docsite_dir = dir / "docs" / "docsite"
    docsite_rst_dir = docsite_dir / "rst"
    os.makedirs(docsite_rst_dir)
    extra_docs = docsite_dir / "extra-docs.yml"
    write_file(
        extra_docs,
        b"""
sections:
  - title: Foo
    toctree:
      - foo
      - fooooo
  - foo: bar
    toctree:
      baz: bam
""",
    )
    links = docsite_dir / "links.yml"
    write_file(
        links,
        b"""
foo: bar

edit_on_github:
  repository: ansible-collections/foo.bar
  path_prefix: 1

extra_links:
  - description: Submit an issue
    url: https://github.com/ansible-collections/foo.bar/issues/new
  - url: bar

communication:
  matrix_rooms:
    - topic: General usage and support questions
      room: '#users:ansible.im'
  irc_channel:
    - topic: General usage and support questions
      network: Libera
      channel: '#ansible'
  mailing_lists:
    - topic: Ansible Project List
      url: https://groups.google.com/g/ansible-project
""",
    )
    foo_rst = docsite_rst_dir / "foo.rst"
    write_file(
        foo_rst,
        b"""
.. _ansible_collections.foo.bar.docsite.bla:

Foo bar
=======

Baz bam :ref:`myself <ansible_collections.foo.bar.docsite.bla>`.

.. _ansible_collections.foo.bar.bad_label:

Bad section
-----------

Foo ``bar`.
""",
    )

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        rc = run(["antsibull-docs", "lint-collection-docs", str(dir)])
    stdout = stdout.getvalue().splitlines()
    print("\n".join(stdout))
    assert rc == 3
    assert stdout == [
        f'{extra_docs}:0:0: Section #1 has no "title" entry',
        f"{links}:0:0: communication -> irc_channel: extra fields not permitted (type=value_error.extra)",
        f"{links}:0:0: edit_on_github -> branch: field required (type=value_error.missing)",
        f"{links}:0:0: extra_links -> 1 -> description: field required (type=value_error.missing)",
        f"{links}:0:0: foo: extra fields not permitted (type=value_error.extra)",
        f'{foo_rst}:9:0: Label "ansible_collections.foo.bar.bad_label" does not start with expected prefix "ansible_collections.foo.bar.docsite."',
        f"{foo_rst}:14:0: (WARNING/2) Inline literal start-string without end-string.",
    ]


TEST_CASES = [
    (
        "ns",
        "col2",
        3,
        [
            "docs/docsite/config.yml:0:0: bla: extra fields not permitted (type=value_error.extra)",
            "docs/docsite/config.yml:0:0: flatmap: value could not be parsed to a boolean (type=type_error.bool)",
            "docs/docsite/extra-docs.yml:0:0: Section #0 has no content",
            'docs/docsite/extra-docs.yml:0:0: Section #1 has no "title" entry',
            "docs/docsite/extra-docs.yml:0:0: Toctree entry in section #0 is not a list",
            "docs/docsite/links.yml:0:0: bla: extra fields not permitted (type=value_error.extra)",
            "docs/docsite/links.yml:0:0: communication -> irc_channels -> 0 -> channel: field required (type=value_error.missing)",
            "docs/docsite/links.yml:0:0: communication -> mailing_lists -> 0: value is not a valid dict (type=type_error.dict)",
            "docs/docsite/links.yml:0:0: communication -> matrix_rooms: value is not a valid list (type=type_error.list)",
            "docs/docsite/links.yml:0:0: edit_on_github -> path_prefi: extra fields not permitted (type=value_error.extra)",
            "docs/docsite/links.yml:0:0: edit_on_github -> repository: field required (type=value_error.missing)",
            "docs/docsite/links.yml:0:0: extra_link: extra fields not permitted (type=value_error.extra)",
            "docs/docsite/links.yml:0:0: extra_links: value is not a valid list (type=type_error.list)",
            'docs/docsite/rst/filter_guide.rst:6:0: Label "bad_label" does not start with expected prefix "ansible_collections.ns.col2.docsite."',
            "plugins/modules/foo.py:0:0: 5 validation errors for ModuleDocSchema",
            "                            doc -> short_description",
            "                              field required (type=value_error.missing)",
            "                            doc -> options -> bar -> description -> 0",
            "                              str type expected (type=type_error.str)",
            "                            doc -> options -> bar -> type",
            '                              string does not match regex "^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$)',
            "                            doc -> options -> foo",
            "                              value is not a valid dict (type=type_error.dict)",
            "                            doc -> options -> subfoo -> bam",
            "                              extra fields not permitted (type=value_error.extra)",
            "plugins/modules/foo.py:0:0: Did not return correct DOCUMENTATION",
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details: Markup error: While parsing "B(broken." at index 25 of paragraph 2: Cannot find closing ")" after last parameter',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details: Markup error: While parsing "M(boo)" at index 12 of paragraph 1: Module name "boo" is not a FQCN',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> description: option name reference "foobar" does not reference to an existing option of the module ns.col2.foo2',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> description: return value name reference "barbaz" does not reference to an existing return value of the module ns.col2.foo2',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> bar -> description: option name reference "broken markup" does not reference to an existing option of the module ns.col2.foo2',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> subfoo -> suboptions -> foo -> description: return value name reference "foobarbaz" does not reference to an existing return value of the module ns.col2.foo2',
            "plugins/modules/foo3.py:0:0: Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema",
            "                             return -> bar -> type",
            '                               string does not match regex "^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$)',
            "                             return -> baz",
            "                               value is not a valid dict (type=type_error.dict)",
        ],
    ),
    (
        "ns2",
        "col",
        0,
        [],
    ),
    (
        "ns2",
        "flatcol",
        0,
        [],
    ),
]


@contextmanager
def change_cwd(directory):
    old_dir = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(old_dir)


@pytest.mark.parametrize("namespace, name, rc, errors", TEST_CASES)
def test_lint_collection_plugin_docs(namespace, name, rc, errors, tmp_path):
    tests_root = os.path.join("tests", "functional")
    collection_root = os.path.join(
        tests_root, "collections", "ansible_collections", namespace, name
    )

    config_file = tmp_path / "antsibull.cfg"
    print(config_file)
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("doc_parsing_backend = ansible-core-2.13\n")

    command = [
        "antsibull-docs",
        "--config-file",
        str(config_file),
        "lint-collection-docs",
        ".",
        "--plugin-docs",
    ]

    stdout = io.StringIO()
    with change_cwd(collection_root):
        with redirect_stdout(stdout):
            with ansible_doc_cache():
                actual_rc = run(command)
    actual_errors = stdout.getvalue().splitlines()
    print("\n".join(actual_errors))
    assert actual_rc == rc
    assert actual_errors == errors
