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
        (
            "--validate-collection-refs",
            "self",
        ),
        {},
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
            "plugins/modules/foo.py:0:0: 6 validation errors for ModuleDocSchema",
            "                            doc -> short_description",
            "                              field required (type=value_error.missing)",
            "                            doc -> seealso",
            "                              value is not a valid list (type=type_error.list)",
            "                            doc -> options -> bar -> description -> 0",
            "                              str type expected (type=type_error.str)",
            "                            doc -> options -> bar -> type",
            '                              string does not match regex "^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$)',
            "                            doc -> options -> foo",
            "                              value is not a valid dict (type=type_error.dict)",
            "                            doc -> options -> subfoo -> bam",
            "                              extra fields not permitted (type=value_error.extra)",
            "plugins/modules/foo.py:0:0: Did not return correct DOCUMENTATION",
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[1]: Markup error: While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[2]: Markup error: While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter',
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[3]: O(foobar): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[4]: RV(barbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: O(ns.col2.foo#module:foo=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: RV(ns.col2.foo#module:bar=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: O(ns.col2.foo#module:foobar=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: RV(ns.col2.foo#module:barbaz=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> bar -> description[2]: O(broken markup): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> subfoo -> suboptions -> foo -> description[4]: RV(foobarbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no inventory plugin ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[2]: there is no module ns.col2.foobarbaz",
            "plugins/modules/foo3.py:0:0: Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema",
            "                             return -> bar -> type",
            '                               string does not match regex "^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$)',
            "                             return -> baz",
            "                               value is not a valid dict (type=type_error.dict)",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name 'subfoo[' cannot be parsed: Found \"[\" without closing \"]\" at position 7 of 'subfoo['",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[5]: RV(ns.col2.foo2#module:bar[]): return value name 'bar[]' refers to bar - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[19]: M(ns.col2.foobarbaz): there is no module ns.col2.foobarbaz",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[20]: P(ns.col2.foobarbam#filter): there is no filter plugin ns.col2.foobarbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[21]: O(ns.col2.foo2#module:barbazbam.foo): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[22]: RV(ns.col2.foo2#module:bambazbar): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[23]: O(ns.col2.foofoo#test:subfoo.foo): there is no test plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[24]: RV(ns.col2.foofoo#lookup:baz): there is no lookup plugin ns.col2.foofoo",
        ],
    ),
    (
        "ns",
        "col2",
        ("--validate-collection-refs", "dependent"),
        {},
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
            "plugins/modules/foo.py:0:0: 6 validation errors for ModuleDocSchema",
            "                            doc -> short_description",
            "                              field required (type=value_error.missing)",
            "                            doc -> seealso",
            "                              value is not a valid list (type=type_error.list)",
            "                            doc -> options -> bar -> description -> 0",
            "                              str type expected (type=type_error.str)",
            "                            doc -> options -> bar -> type",
            '                              string does not match regex "^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$)',
            "                            doc -> options -> foo",
            "                              value is not a valid dict (type=type_error.dict)",
            "                            doc -> options -> subfoo -> bam",
            "                              extra fields not permitted (type=value_error.extra)",
            "plugins/modules/foo.py:0:0: Did not return correct DOCUMENTATION",
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[1]: Markup error: While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[2]: Markup error: While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter',
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[3]: O(foobar): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[4]: RV(barbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: O(ns.col2.foo#module:foo=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: RV(ns.col2.foo#module:bar=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: O(ns.col2.foo#module:foobar=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: RV(ns.col2.foo#module:barbaz=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> bar -> description[2]: O(broken markup): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> subfoo -> suboptions -> foo -> description[4]: RV(foobarbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no inventory plugin ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no strategy plugin ansible.builtin.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[2]: there is no module ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[6]: there is no module ansible.builtin.foobarbaz",
            "plugins/modules/foo3.py:0:0: Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema",
            "                             return -> bar -> type",
            '                               string does not match regex "^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$)',
            "                             return -> baz",
            "                               value is not a valid dict (type=type_error.dict)",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[1]: O(ansible.builtin.file#module:state[]): option name 'state[]' refers to state - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[2]: RV(ansible.builtin.stat#module:stat[foo.bar].exists): return value name 'stat[foo.bar].exists' refers to dictionary stat with `[]`, which is only allowed for the last part",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[3]: RV(ansible.builtin.stat#module:stat.exists[]): return value name 'stat.exists[]' refers to stat.exists - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name 'subfoo[' cannot be parsed: Found \"[\" without closing \"]\" at position 7 of 'subfoo['",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[5]: RV(ns.col2.foo2#module:bar[]): return value name 'bar[]' refers to bar - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[13]: M(ns2.col.joo): there is no module ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[14]: P(ns2.col.joo#lookup): there is no lookup plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[15]: O(ns2.col.bar#filter:jooo): option name does not reference to an existing option of the filter plugin ns2.col.bar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[16]: RV(ns2.col.bar#test:booo): return value name does not reference to an existing return value of the test plugin ns2.col.bar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[17]: O(ns2.col.joo#filter:foo[-1]): there is no filter plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[18]: RV(ns2.col.joo#test:_value): there is no test plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[19]: M(ns.col2.foobarbaz): there is no module ns.col2.foobarbaz",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[1]: M(ansible.builtin.foobar): there is no module ansible.builtin.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[20]: P(ns.col2.foobarbam#filter): there is no filter plugin ns.col2.foobarbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[21]: O(ns.col2.foo2#module:barbazbam.foo): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[22]: RV(ns.col2.foo2#module:bambazbar): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[23]: O(ns.col2.foofoo#test:subfoo.foo): there is no test plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[24]: RV(ns.col2.foofoo#lookup:baz): there is no lookup plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[2]: P(ansible.builtin.bazbam#lookup): there is no lookup plugin ansible.builtin.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[3]: O(ansible.builtin.file#module:foobarbaz): option name does not reference to an existing option of the module ansible.builtin.file",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[4]: RV(ansible.builtin.stat#module:baz.bam[]): return value name does not reference to an existing return value of the module ansible.builtin.stat",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[5]: O(ansible.builtin.foobar#module:state): there is no module ansible.builtin.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[6]: RV(ansible.builtin.bazbam#module:stat.exists): there is no module ansible.builtin.bazbam",
            "roles/bar/meta/argument_specs.yml:0:0: entry_points -> main -> seealso[2]: there is no module ns2.col.foobarbaz",
        ],
    ),
    (
        "ns",
        "col2",
        ("--validate-collection-refs", "all"),
        {
            "ANSIBLE_COLLECTIONS_PATH": None,
        },
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
            "plugins/modules/foo.py:0:0: 6 validation errors for ModuleDocSchema",
            "                            doc -> short_description",
            "                              field required (type=value_error.missing)",
            "                            doc -> seealso",
            "                              value is not a valid list (type=type_error.list)",
            "                            doc -> options -> bar -> description -> 0",
            "                              str type expected (type=type_error.str)",
            "                            doc -> options -> bar -> type",
            '                              string does not match regex "^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$)',
            "                            doc -> options -> foo",
            "                              value is not a valid dict (type=type_error.dict)",
            "                            doc -> options -> subfoo -> bam",
            "                              extra fields not permitted (type=value_error.extra)",
            "plugins/modules/foo.py:0:0: Did not return correct DOCUMENTATION",
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[1]: Markup error: While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[2]: Markup error: While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter',
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[3]: O(foobar): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[4]: RV(barbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: O(ns.col2.foo#module:foo=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: RV(ns.col2.foo#module:bar=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: O(ns.col2.foo#module:foobar=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: RV(ns.col2.foo#module:barbaz=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> bar -> description[2]: O(broken markup): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> subfoo -> suboptions -> foo -> description[4]: RV(foobarbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no inventory plugin ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no strategy plugin ansible.builtin.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[2]: there is no module ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[6]: there is no module ansible.builtin.foobarbaz",
            "plugins/modules/foo3.py:0:0: Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema",
            "                             return -> bar -> type",
            '                               string does not match regex "^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$)',
            "                             return -> baz",
            "                               value is not a valid dict (type=type_error.dict)",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[1]: O(ansible.builtin.file#module:state[]): option name 'state[]' refers to state - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[2]: RV(ansible.builtin.stat#module:stat[foo.bar].exists): return value name 'stat[foo.bar].exists' refers to dictionary stat with `[]`, which is only allowed for the last part",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[3]: RV(ansible.builtin.stat#module:stat.exists[]): return value name 'stat.exists[]' refers to stat.exists - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name 'subfoo[' cannot be parsed: Found \"[\" without closing \"]\" at position 7 of 'subfoo['",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[5]: RV(ns.col2.foo2#module:bar[]): return value name 'bar[]' refers to bar - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[10]: RV(ns2.flatcol.sub.foo2#module:bazbarbam): return value name does not reference to an existing return value of the module ns2.flatcol.sub.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[11]: O(ns2.flatcol.foobar#module:subbaz.bam): there is no module ns2.flatcol.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[12]: RV(ns2.flatcol.sub.bazbam#module:bar): there is no module ns2.flatcol.sub.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[13]: M(ns2.col.joo): there is no module ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[14]: P(ns2.col.joo#lookup): there is no lookup plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[15]: O(ns2.col.bar#filter:jooo): option name does not reference to an existing option of the filter plugin ns2.col.bar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[16]: RV(ns2.col.bar#test:booo): return value name does not reference to an existing return value of the test plugin ns2.col.bar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[17]: O(ns2.col.joo#filter:foo[-1]): there is no filter plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[18]: RV(ns2.col.joo#test:_value): there is no test plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[19]: M(ns.col2.foobarbaz): there is no module ns.col2.foobarbaz",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[1]: M(ansible.builtin.foobar): there is no module ansible.builtin.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[20]: P(ns.col2.foobarbam#filter): there is no filter plugin ns.col2.foobarbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[21]: O(ns.col2.foo2#module:barbazbam.foo): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[22]: RV(ns.col2.foo2#module:bambazbar): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[23]: O(ns.col2.foofoo#test:subfoo.foo): there is no test plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[24]: RV(ns.col2.foofoo#lookup:baz): there is no lookup plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[2]: P(ansible.builtin.bazbam#lookup): there is no lookup plugin ansible.builtin.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[3]: O(ansible.builtin.file#module:foobarbaz): option name does not reference to an existing option of the module ansible.builtin.file",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[4]: RV(ansible.builtin.stat#module:baz.bam[]): return value name does not reference to an existing return value of the module ansible.builtin.stat",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[5]: O(ansible.builtin.foobar#module:state): there is no module ansible.builtin.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[6]: RV(ansible.builtin.bazbam#module:stat.exists): there is no module ansible.builtin.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[7]: M(ns2.flatcol.foobarbaz): there is no module ns2.flatcol.foobarbaz",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[8]: P(ns2.flatcol.sub.bazbam#module): there is no module ns2.flatcol.sub.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[9]: O(ns2.flatcol.foo#module:foofoofoobar): option name does not reference to an existing option of the module ns2.flatcol.foo",
            "roles/bar/meta/argument_specs.yml:0:0: entry_points -> main -> seealso[2]: there is no module ns2.col.foobarbaz",
        ],
    ),
    (
        "ns",
        "col2",
        (
            "--validate-collection-refs",
            "self",
            "--disallow-unknown-collection-refs",
        ),
        {},
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
            "plugins/modules/foo.py:0:0: 6 validation errors for ModuleDocSchema",
            "                            doc -> short_description",
            "                              field required (type=value_error.missing)",
            "                            doc -> seealso",
            "                              value is not a valid list (type=type_error.list)",
            "                            doc -> options -> bar -> description -> 0",
            "                              str type expected (type=type_error.str)",
            "                            doc -> options -> bar -> type",
            '                              string does not match regex "^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$)',
            "                            doc -> options -> foo",
            "                              value is not a valid dict (type=type_error.dict)",
            "                            doc -> options -> subfoo -> bam",
            "                              extra fields not permitted (type=value_error.extra)",
            "plugins/modules/foo.py:0:0: Did not return correct DOCUMENTATION",
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[1]: Markup error: While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[2]: Markup error: While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter',
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[3]: O(foobar): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[4]: RV(barbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: O(ns.col2.foo#module:foo=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: RV(ns.col2.foo#module:bar=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: O(ns.col2.foo#module:foobar=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: RV(ns.col2.foo#module:barbaz=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> bar -> description[2]: O(broken markup): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> subfoo -> suboptions -> foo -> description[4]: RV(foobarbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no inventory plugin ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[2]: there is no module ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[5]: a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[6]: a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo3.py:0:0: Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema",
            "                             return -> bar -> type",
            '                               string does not match regex "^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$)',
            "                             return -> baz",
            "                               value is not a valid dict (type=type_error.dict)",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[1]: O(ansible.builtin.iptables#module:tcp_flags.flags[]): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[2]: O(ns2.col.bar#filter:foo): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[3]: O(ns2.col.bar#filter:foo[]): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[4]: O(ext.col.foo#module:foo[baz].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[5]: RV(ext.col.foo#module:baz): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[6]: RV(ext.col.foo#module:baz[ ]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[7]: RV(ansible.builtin.stat#module:stat[foo.bar]): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[10]: P(ns2.col.foo#lookup): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[11]: O(ns2.col.bar#filter:foo[-1]): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[12]: RV(ns2.col.bar#test:_value): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[17]: M(ext.col.foo): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[18]: P(ext.col.bar#lookup): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[19]: O(ext.col.foo#module:foo[len(foo\\)].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[1]: M(ansible.builtin.service): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[20]: RV(ext.col.foo#module:baz[]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[2]: P(ansible.builtin.pipe#lookup): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[3]: O(ansible.builtin.file#module:state): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[4]: RV(ansible.builtin.stat#module:stat.exists): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[5]: M(ns2.flatcol.foo): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[6]: P(ns2.flatcol.sub.foo2#module): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[7]: O(ns2.flatcol.foo#module:subbaz.bam): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[8]: RV(ns2.flatcol.sub.foo2#module:bar): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[9]: M(ns2.col.foo2): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[1]: O(ansible.builtin.file#module:state[]): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[2]: RV(ansible.builtin.stat#module:stat[foo.bar].exists): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[3]: RV(ansible.builtin.stat#module:stat.exists[]): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name 'subfoo[' cannot be parsed: Found \"[\" without closing \"]\" at position 7 of 'subfoo['",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[5]: RV(ns.col2.foo2#module:bar[]): return value name 'bar[]' refers to bar - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[6]: O(ext.col.foo#module:foo.bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[10]: RV(ns2.flatcol.sub.foo2#module:bazbarbam): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[11]: O(ns2.flatcol.foobar#module:subbaz.bam): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[12]: RV(ns2.flatcol.sub.bazbam#module:bar): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[13]: M(ns2.col.joo): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[14]: P(ns2.col.joo#lookup): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[15]: O(ns2.col.bar#filter:jooo): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[16]: RV(ns2.col.bar#test:booo): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[17]: O(ns2.col.joo#filter:foo[-1]): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[18]: RV(ns2.col.joo#test:_value): a reference to the collection ns2.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[19]: M(ns.col2.foobarbaz): there is no module ns.col2.foobarbaz",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[1]: M(ansible.builtin.foobar): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[20]: P(ns.col2.foobarbam#filter): there is no filter plugin ns.col2.foobarbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[21]: O(ns.col2.foo2#module:barbazbam.foo): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[22]: RV(ns.col2.foo2#module:bambazbar): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[23]: O(ns.col2.foofoo#test:subfoo.foo): there is no test plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[24]: RV(ns.col2.foofoo#lookup:baz): there is no lookup plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[25]: M(ext.col.notthere): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[26]: P(ext.col.notthere#lookup): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[27]: O(ext.col.foo#module:foo[len(foo\\)].notthere): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[28]: O(ext.col.foo#module:notthere[len(notthere\\)].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[29]: RV(ext.col.foo#module:notthere[]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[2]: P(ansible.builtin.bazbam#lookup): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[30]: O(ext.col.notthere#module:foo[len(foo\\)].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[31]: RV(ext.col.notthere#module:baz[]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[3]: O(ansible.builtin.file#module:foobarbaz): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[4]: RV(ansible.builtin.stat#module:baz.bam[]): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[5]: O(ansible.builtin.foobar#module:state): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[6]: RV(ansible.builtin.bazbam#module:stat.exists): a reference to the collection ansible.builtin is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[7]: M(ns2.flatcol.foobarbaz): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[8]: P(ns2.flatcol.sub.bazbam#module): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[9]: O(ns2.flatcol.foo#module:foofoofoobar): a reference to the collection ns2.flatcol is not allowed",
            "roles/bar/meta/argument_specs.yml:0:0: entry_points -> main -> seealso[1]: a reference to the collection ns2.col is not allowed",
            "roles/bar/meta/argument_specs.yml:0:0: entry_points -> main -> seealso[2]: a reference to the collection ns2.col is not allowed",
        ],
    ),
    (
        "ns",
        "col2",
        (
            "--validate-collection-refs",
            "dependent",
            "--disallow-unknown-collection-refs",
        ),
        {},
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
            "plugins/modules/foo.py:0:0: 6 validation errors for ModuleDocSchema",
            "                            doc -> short_description",
            "                              field required (type=value_error.missing)",
            "                            doc -> seealso",
            "                              value is not a valid list (type=type_error.list)",
            "                            doc -> options -> bar -> description -> 0",
            "                              str type expected (type=type_error.str)",
            "                            doc -> options -> bar -> type",
            '                              string does not match regex "^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$)',
            "                            doc -> options -> foo",
            "                              value is not a valid dict (type=type_error.dict)",
            "                            doc -> options -> subfoo -> bam",
            "                              extra fields not permitted (type=value_error.extra)",
            "plugins/modules/foo.py:0:0: Did not return correct DOCUMENTATION",
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[1]: Markup error: While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[2]: Markup error: While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter',
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[3]: O(foobar): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[4]: RV(barbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: O(ns.col2.foo#module:foo=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: RV(ns.col2.foo#module:bar=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: O(ns.col2.foo#module:foobar=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: RV(ns.col2.foo#module:barbaz=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> bar -> description[2]: O(broken markup): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> subfoo -> suboptions -> foo -> description[4]: RV(foobarbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no inventory plugin ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no strategy plugin ansible.builtin.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[2]: there is no module ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[6]: there is no module ansible.builtin.foobarbaz",
            "plugins/modules/foo3.py:0:0: Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema",
            "                             return -> bar -> type",
            '                               string does not match regex "^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$)',
            "                             return -> baz",
            "                               value is not a valid dict (type=type_error.dict)",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[4]: O(ext.col.foo#module:foo[baz].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[5]: RV(ext.col.foo#module:baz): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[6]: RV(ext.col.foo#module:baz[ ]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[17]: M(ext.col.foo): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[18]: P(ext.col.bar#lookup): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[19]: O(ext.col.foo#module:foo[len(foo\\)].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[20]: RV(ext.col.foo#module:baz[]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[5]: M(ns2.flatcol.foo): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[6]: P(ns2.flatcol.sub.foo2#module): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[7]: O(ns2.flatcol.foo#module:subbaz.bam): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[8]: RV(ns2.flatcol.sub.foo2#module:bar): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[1]: O(ansible.builtin.file#module:state[]): option name 'state[]' refers to state - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[2]: RV(ansible.builtin.stat#module:stat[foo.bar].exists): return value name 'stat[foo.bar].exists' refers to dictionary stat with `[]`, which is only allowed for the last part",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[3]: RV(ansible.builtin.stat#module:stat.exists[]): return value name 'stat.exists[]' refers to stat.exists - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name 'subfoo[' cannot be parsed: Found \"[\" without closing \"]\" at position 7 of 'subfoo['",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[5]: RV(ns.col2.foo2#module:bar[]): return value name 'bar[]' refers to bar - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[6]: O(ext.col.foo#module:foo.bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[10]: RV(ns2.flatcol.sub.foo2#module:bazbarbam): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[11]: O(ns2.flatcol.foobar#module:subbaz.bam): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[12]: RV(ns2.flatcol.sub.bazbam#module:bar): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[13]: M(ns2.col.joo): there is no module ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[14]: P(ns2.col.joo#lookup): there is no lookup plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[15]: O(ns2.col.bar#filter:jooo): option name does not reference to an existing option of the filter plugin ns2.col.bar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[16]: RV(ns2.col.bar#test:booo): return value name does not reference to an existing return value of the test plugin ns2.col.bar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[17]: O(ns2.col.joo#filter:foo[-1]): there is no filter plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[18]: RV(ns2.col.joo#test:_value): there is no test plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[19]: M(ns.col2.foobarbaz): there is no module ns.col2.foobarbaz",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[1]: M(ansible.builtin.foobar): there is no module ansible.builtin.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[20]: P(ns.col2.foobarbam#filter): there is no filter plugin ns.col2.foobarbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[21]: O(ns.col2.foo2#module:barbazbam.foo): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[22]: RV(ns.col2.foo2#module:bambazbar): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[23]: O(ns.col2.foofoo#test:subfoo.foo): there is no test plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[24]: RV(ns.col2.foofoo#lookup:baz): there is no lookup plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[25]: M(ext.col.notthere): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[26]: P(ext.col.notthere#lookup): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[27]: O(ext.col.foo#module:foo[len(foo\\)].notthere): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[28]: O(ext.col.foo#module:notthere[len(notthere\\)].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[29]: RV(ext.col.foo#module:notthere[]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[2]: P(ansible.builtin.bazbam#lookup): there is no lookup plugin ansible.builtin.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[30]: O(ext.col.notthere#module:foo[len(foo\\)].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[31]: RV(ext.col.notthere#module:baz[]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[3]: O(ansible.builtin.file#module:foobarbaz): option name does not reference to an existing option of the module ansible.builtin.file",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[4]: RV(ansible.builtin.stat#module:baz.bam[]): return value name does not reference to an existing return value of the module ansible.builtin.stat",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[5]: O(ansible.builtin.foobar#module:state): there is no module ansible.builtin.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[6]: RV(ansible.builtin.bazbam#module:stat.exists): there is no module ansible.builtin.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[7]: M(ns2.flatcol.foobarbaz): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[8]: P(ns2.flatcol.sub.bazbam#module): a reference to the collection ns2.flatcol is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[9]: O(ns2.flatcol.foo#module:foofoofoobar): a reference to the collection ns2.flatcol is not allowed",
            "roles/bar/meta/argument_specs.yml:0:0: entry_points -> main -> seealso[2]: there is no module ns2.col.foobarbaz",
        ],
    ),
    (
        "ns",
        "col2",
        ("--validate-collection-refs", "all", "--disallow-unknown-collection-refs"),
        {
            "ANSIBLE_COLLECTIONS_PATH": None,
        },
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
            "plugins/modules/foo.py:0:0: 6 validation errors for ModuleDocSchema",
            "                            doc -> short_description",
            "                              field required (type=value_error.missing)",
            "                            doc -> seealso",
            "                              value is not a valid list (type=type_error.list)",
            "                            doc -> options -> bar -> description -> 0",
            "                              str type expected (type=type_error.str)",
            "                            doc -> options -> bar -> type",
            '                              string does not match regex "^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$)',
            "                            doc -> options -> foo",
            "                              value is not a valid dict (type=type_error.dict)",
            "                            doc -> options -> subfoo -> bam",
            "                              extra fields not permitted (type=value_error.extra)",
            "plugins/modules/foo.py:0:0: Did not return correct DOCUMENTATION",
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[1]: Markup error: While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[2]: Markup error: While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter',
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[3]: O(foobar): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[4]: RV(barbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: O(ns.col2.foo#module:foo=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: RV(ns.col2.foo#module:bar=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: O(ns.col2.foo#module:foobar=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: RV(ns.col2.foo#module:barbaz=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> bar -> description[2]: O(broken markup): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> subfoo -> suboptions -> foo -> description[4]: RV(foobarbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no inventory plugin ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no strategy plugin ansible.builtin.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[2]: there is no module ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[6]: there is no module ansible.builtin.foobarbaz",
            "plugins/modules/foo3.py:0:0: Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema",
            "                             return -> bar -> type",
            '                               string does not match regex "^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$)',
            "                             return -> baz",
            "                               value is not a valid dict (type=type_error.dict)",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[4]: O(ext.col.foo#module:foo[baz].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[5]: RV(ext.col.foo#module:baz): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> correct_array_stubs -> description[6]: RV(ext.col.foo#module:baz[ ]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[17]: M(ext.col.foo): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[18]: P(ext.col.bar#lookup): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[19]: O(ext.col.foo#module:foo[len(foo\\)].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> existing -> description[20]: RV(ext.col.foo#module:baz[]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[1]: O(ansible.builtin.file#module:state[]): option name 'state[]' refers to state - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[2]: RV(ansible.builtin.stat#module:stat[foo.bar].exists): return value name 'stat[foo.bar].exists' refers to dictionary stat with `[]`, which is only allowed for the last part",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[3]: RV(ansible.builtin.stat#module:stat.exists[]): return value name 'stat.exists[]' refers to stat.exists - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name 'subfoo[' cannot be parsed: Found \"[\" without closing \"]\" at position 7 of 'subfoo['",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[5]: RV(ns.col2.foo2#module:bar[]): return value name 'bar[]' refers to bar - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[6]: O(ext.col.foo#module:foo.bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[10]: RV(ns2.flatcol.sub.foo2#module:bazbarbam): return value name does not reference to an existing return value of the module ns2.flatcol.sub.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[11]: O(ns2.flatcol.foobar#module:subbaz.bam): there is no module ns2.flatcol.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[12]: RV(ns2.flatcol.sub.bazbam#module:bar): there is no module ns2.flatcol.sub.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[13]: M(ns2.col.joo): there is no module ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[14]: P(ns2.col.joo#lookup): there is no lookup plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[15]: O(ns2.col.bar#filter:jooo): option name does not reference to an existing option of the filter plugin ns2.col.bar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[16]: RV(ns2.col.bar#test:booo): return value name does not reference to an existing return value of the test plugin ns2.col.bar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[17]: O(ns2.col.joo#filter:foo[-1]): there is no filter plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[18]: RV(ns2.col.joo#test:_value): there is no test plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[19]: M(ns.col2.foobarbaz): there is no module ns.col2.foobarbaz",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[1]: M(ansible.builtin.foobar): there is no module ansible.builtin.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[20]: P(ns.col2.foobarbam#filter): there is no filter plugin ns.col2.foobarbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[21]: O(ns.col2.foo2#module:barbazbam.foo): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[22]: RV(ns.col2.foo2#module:bambazbar): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[23]: O(ns.col2.foofoo#test:subfoo.foo): there is no test plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[24]: RV(ns.col2.foofoo#lookup:baz): there is no lookup plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[25]: M(ext.col.notthere): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[26]: P(ext.col.notthere#lookup): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[27]: O(ext.col.foo#module:foo[len(foo\\)].notthere): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[28]: O(ext.col.foo#module:notthere[len(notthere\\)].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[29]: RV(ext.col.foo#module:notthere[]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[2]: P(ansible.builtin.bazbam#lookup): there is no lookup plugin ansible.builtin.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[30]: O(ext.col.notthere#module:foo[len(foo\\)].bar): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[31]: RV(ext.col.notthere#module:baz[]): a reference to the collection ext.col is not allowed",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[3]: O(ansible.builtin.file#module:foobarbaz): option name does not reference to an existing option of the module ansible.builtin.file",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[4]: RV(ansible.builtin.stat#module:baz.bam[]): return value name does not reference to an existing return value of the module ansible.builtin.stat",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[5]: O(ansible.builtin.foobar#module:state): there is no module ansible.builtin.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[6]: RV(ansible.builtin.bazbam#module:stat.exists): there is no module ansible.builtin.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[7]: M(ns2.flatcol.foobarbaz): there is no module ns2.flatcol.foobarbaz",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[8]: P(ns2.flatcol.sub.bazbam#module): there is no module ns2.flatcol.sub.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[9]: O(ns2.flatcol.foo#module:foofoofoobar): option name does not reference to an existing option of the module ns2.flatcol.foo",
            "roles/bar/meta/argument_specs.yml:0:0: entry_points -> main -> seealso[2]: there is no module ns2.col.foobarbaz",
        ],
    ),
    (
        "ns",
        "col2",
        ("--validate-collection-refs", "all", "--disallow-unknown-collection-refs"),
        {
            "ANSIBLE_COLLECTIONS_PATH": os.path.join(
                os.path.dirname(__file__), "other-collections"
            ),
        },
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
            "plugins/modules/foo.py:0:0: 6 validation errors for ModuleDocSchema",
            "                            doc -> short_description",
            "                              field required (type=value_error.missing)",
            "                            doc -> seealso",
            "                              value is not a valid list (type=type_error.list)",
            "                            doc -> options -> bar -> description -> 0",
            "                              str type expected (type=type_error.str)",
            "                            doc -> options -> bar -> type",
            '                              string does not match regex "^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|dict|float|int|json|jsonarg|list|path|raw|sid|str|tmppath|pathspec|pathlist)$)',
            "                            doc -> options -> foo",
            "                              value is not a valid dict (type=type_error.dict)",
            "                            doc -> options -> subfoo -> bam",
            "                              extra fields not permitted (type=value_error.extra)",
            "plugins/modules/foo.py:0:0: Did not return correct DOCUMENTATION",
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[1]: Markup error: While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN',
            'plugins/modules/foo2.py:0:0: DOCUMENTATION -> attributes -> platform -> details[2]: Markup error: While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter',
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[3]: O(foobar): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[4]: RV(barbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: O(ns.col2.foo#module:foo=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[5]: RV(ns.col2.foo#module:bar=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: O(ns.col2.foo#module:foobar=1): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> description[6]: RV(ns.col2.foo#module:barbaz=2): there is no module ns.col2.foo",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> bar -> description[2]: O(broken markup): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> options -> subfoo -> suboptions -> foo -> description[4]: RV(foobarbaz): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no inventory plugin ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso: there is no strategy plugin ansible.builtin.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[2]: there is no module ns.col2.foobarbaz",
            "plugins/modules/foo2.py:0:0: DOCUMENTATION -> seealso[6]: there is no module ansible.builtin.foobarbaz",
            "plugins/modules/foo3.py:0:0: Unable to normalize foo3: return due to: 2 validation errors for PluginReturnSchema",
            "                             return -> bar -> type",
            '                               string does not match regex "^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$" (type=value_error.str.regex; pattern=^(any|bits|bool|bytes|complex|dict|float|int|json|jsonarg|list|path|sid|str|pathspec|pathlist)$)',
            "                             return -> baz",
            "                               value is not a valid dict (type=type_error.dict)",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[1]: O(ansible.builtin.file#module:state[]): option name 'state[]' refers to state - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[2]: RV(ansible.builtin.stat#module:stat[foo.bar].exists): return value name 'stat[foo.bar].exists' refers to dictionary stat with `[]`, which is only allowed for the last part",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[3]: RV(ansible.builtin.stat#module:stat.exists[]): return value name 'stat.exists[]' refers to stat.exists - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name 'subfoo[' cannot be parsed: Found \"[\" without closing \"]\" at position 7 of 'subfoo['",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[4]: O(ns.col2.foo2#module:subfoo[): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[5]: RV(ns.col2.foo2#module:bar[]): return value name 'bar[]' refers to bar - which is neither list nor dictionary - with `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> incorrect_array_stubs -> description[6]: O(ext.col.foo#module:foo.bar): option name 'foo.bar' refers to list foo without `[]`",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[10]: RV(ns2.flatcol.sub.foo2#module:bazbarbam): return value name does not reference to an existing return value of the module ns2.flatcol.sub.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[11]: O(ns2.flatcol.foobar#module:subbaz.bam): there is no module ns2.flatcol.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[12]: RV(ns2.flatcol.sub.bazbam#module:bar): there is no module ns2.flatcol.sub.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[13]: M(ns2.col.joo): there is no module ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[14]: P(ns2.col.joo#lookup): there is no lookup plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[15]: O(ns2.col.bar#filter:jooo): option name does not reference to an existing option of the filter plugin ns2.col.bar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[16]: RV(ns2.col.bar#test:booo): return value name does not reference to an existing return value of the test plugin ns2.col.bar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[17]: O(ns2.col.joo#filter:foo[-1]): there is no filter plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[18]: RV(ns2.col.joo#test:_value): there is no test plugin ns2.col.joo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[19]: M(ns.col2.foobarbaz): there is no module ns.col2.foobarbaz",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[1]: M(ansible.builtin.foobar): there is no module ansible.builtin.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[20]: P(ns.col2.foobarbam#filter): there is no filter plugin ns.col2.foobarbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[21]: O(ns.col2.foo2#module:barbazbam.foo): option name does not reference to an existing option of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[22]: RV(ns.col2.foo2#module:bambazbar): return value name does not reference to an existing return value of the module ns.col2.foo2",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[23]: O(ns.col2.foofoo#test:subfoo.foo): there is no test plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[24]: RV(ns.col2.foofoo#lookup:baz): there is no lookup plugin ns.col2.foofoo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[25]: M(ext.col.notthere): there is no module ext.col.notthere",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[26]: P(ext.col.notthere#lookup): there is no lookup plugin ext.col.notthere",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[27]: O(ext.col.foo#module:foo[len(foo\\)].notthere): option name does not reference to an existing option of the module ext.col.foo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[28]: O(ext.col.foo#module:notthere[len(notthere\\)].bar): option name does not reference to an existing option of the module ext.col.foo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[29]: RV(ext.col.foo#module:notthere[]): return value name does not reference to an existing return value of the module ext.col.foo",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[2]: P(ansible.builtin.bazbam#lookup): there is no lookup plugin ansible.builtin.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[30]: O(ext.col.notthere#module:foo[len(foo\\)].bar): there is no module ext.col.notthere",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[31]: RV(ext.col.notthere#module:baz[]): there is no module ext.col.notthere",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[3]: O(ansible.builtin.file#module:foobarbaz): option name does not reference to an existing option of the module ansible.builtin.file",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[4]: RV(ansible.builtin.stat#module:baz.bam[]): return value name does not reference to an existing return value of the module ansible.builtin.stat",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[5]: O(ansible.builtin.foobar#module:state): there is no module ansible.builtin.foobar",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[6]: RV(ansible.builtin.bazbam#module:stat.exists): there is no module ansible.builtin.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[7]: M(ns2.flatcol.foobarbaz): there is no module ns2.flatcol.foobarbaz",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[8]: P(ns2.flatcol.sub.bazbam#module): there is no module ns2.flatcol.sub.bazbam",
            "plugins/modules/foo4.py:0:0: DOCUMENTATION -> options -> not_existing -> description[9]: O(ns2.flatcol.foo#module:foofoofoobar): option name does not reference to an existing option of the module ns2.flatcol.foo",
            "roles/bar/meta/argument_specs.yml:0:0: entry_points -> main -> seealso[2]: there is no module ns2.col.foobarbaz",
        ],
    ),
    (
        "ns2",
        "col",
        (),
        {},
        0,
        [],
    ),
    (
        "ns2",
        "flatcol",
        (),
        {},
        3,
        [
            "plugins/modules/sub/foo2.py:0:0: DOCUMENTATION -> description[2]: O(ns2.flatcol.foo#role:main:foo_param_1): there is no role ns2.flatcol.foo",
            "plugins/modules/sub/foo2.py:0:0: DOCUMENTATION -> description[2]: O(ns2.flatcol.foo#role:main:foo_param_2=42): there is no role ns2.flatcol.foo",
            "plugins/modules/sub/foo2.py:0:0: DOCUMENTATION -> options -> bar -> description[2]: O(ns2.flatcol.foo#role:main:foo_param_1): there is no role ns2.flatcol.foo",
            "plugins/modules/sub/foo2.py:0:0: DOCUMENTATION -> options -> bar -> description[2]: O(ns2.flatcol.foo#role:main:foo_param_2=42): there is no role ns2.flatcol.foo",
        ],
    ),
]


@contextmanager
def change_cwd(directory: str):
    old_dir = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(old_dir)


@contextmanager
def update_environment(environment: dict[str, str | None]):
    backup = {}
    for k, v in environment.items():
        if k in os.environ:
            backup[k] = os.environ[k]
        if v is not None:
            os.environ[k] = v
        elif k in os.environ:
            del os.environ[k]
    yield
    for k in environment:
        if k in backup:
            os.environ[k] = backup[k]
        elif k in os.environ:
            del os.environ[k]


@pytest.mark.parametrize(
    "namespace, name, parameters, environment, rc, errors", TEST_CASES
)
def test_lint_collection_plugin_docs(
    namespace: str,
    name: str,
    parameters: tuple[str],
    environment: dict[str, str | None],
    rc: int,
    errors: list[str],
    tmp_path,
):
    tests_root = os.path.dirname(__file__)
    collection_root = os.path.join(
        tests_root, "collections", "ansible_collections", namespace, name
    )

    config_file = tmp_path / "antsibull.cfg"
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("doc_parsing_backend = ansible-core-2.13\n")

    command = [
        "antsibull-docs",
        "--config-file",
        str(config_file),
        "lint-collection-docs",
        ".",
        "--plugin-docs",
        *parameters,
    ]

    stdout = io.StringIO()
    with change_cwd(collection_root):
        with redirect_stdout(stdout):
            with ansible_doc_cache():
                with update_environment(environment):
                    actual_rc = run(command)
    actual_errors = stdout.getvalue().splitlines()
    print("\n".join(actual_errors))
    assert actual_rc == rc
    assert actual_errors == errors
