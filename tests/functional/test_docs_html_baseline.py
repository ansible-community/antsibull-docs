# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import shutil

import pytest
from ansible_doc_caching import ansible_doc_cache
from sphinx.cmd.build import main as sphinx_main
from utils import compare_directories, scan_directories

# To regenerate the baselines, run:
# ANTSIBULL_DOCS_UPDATE_HTML_BASELINE=true nox -Re test -- tests/functional/test_docs_html_baseline.py


UPDATE_BASELINES = os.getenv("ANTSIBULL_DOCS_UPDATE_HTML_BASELINE") == "true"

TEST_CASES: list[tuple[str, str, list[str], list[str]]] = [
    (
        "baseline-default",
        "baseline-default-html",
        [
            "ansible_collections.ansible.builtin.bazbam_lookup",
            "ansible_collections.ansible.builtin.bazbam_module__return-stat/exists",
            "ansible_collections.ansible.builtin.file_module__parameter-foobarbaz",
            "ansible_collections.ansible.builtin.file_module__parameter-state",
            "ansible_collections.ansible.builtin.foobarbaz_module",
            "ansible_collections.ansible.builtin.foobarbaz_strategy",
            "ansible_collections.ansible.builtin.foobar_module",
            "ansible_collections.ansible.builtin.foobar_module__parameter-state",
            "ansible_collections.ansible.builtin.iptables_module__parameter-tcp_flags/flags",
            "ansible_collections.ansible.builtin.linear_strategy",
            "ansible_collections.ansible.builtin.pipe_lookup",
            "ansible_collections.ansible.builtin.service_module",
            "ansible_collections.ansible.builtin.ssh_connection",
            "ansible_collections.ansible.builtin.stat_module__return-baz/bam",
            "ansible_collections.ansible.builtin.stat_module__return-stat",
            "ansible_collections.ansible.builtin.stat_module__return-stat/exists",
            "ansible_collections.ext.col.bar_lookup",
            "ansible_collections.ext.col.foo_module",
            "ansible_collections.ext.col.foo_module__parameter-foo/bar",
            "ansible_collections.ext.col.foo_module__parameter-foo/notthere",
            "ansible_collections.ext.col.foo_module__parameter-notthere/bar",
            "ansible_collections.ext.col.foo_module__return-baz",
            "ansible_collections.ext.col.foo_module__return-notthere",
            "ansible_collections.ext.col.notthere_lookup",
            "ansible_collections.ext.col.notthere_module",
            "ansible_collections.ext.col.notthere_module__parameter-foo/bar",
            "ansible_collections.ext.col.notthere_module__return-baz",
            "ansible_collections.ns2.col.bar_filter__parameter-jooo",
            "ansible_collections.ns2.col.bar_test__return-booo",
            "ansible_collections.ns2.col.boo_filter__parameter-boo",
            "ansible_collections.ns2.col.boo_filter__return-boo",
            "ansible_collections.ns2.col.does_not_exist_filter",
            "ansible_collections.ns2.col.foo_asdf",
            "ansible_collections.ns2.col.foobarbaz_module",
            "ansible_collections.ns2.col.foo_filter__parameter-boo",
            "ansible_collections.ns2.col.foo_filter__return-boo",
            "ansible_collections.ns2.col.foo_filter__return-does_not_exist",
            "ansible_collections.ns2.col.foo_module__parameter-strategy",
            "ansible_collections.ns2.col.foo_redirect_module__parameter-bar",
            "ansible_collections.ns2.col.foo_redirect_module__parameter-baz",
            "ansible_collections.ns2.col.foo_role__entrypoint-boo",
            "ansible_collections.ns2.col.foo_role__parameter-boo__boo",
            "ansible_collections.ns2.col.foo_role__parameter-does_not_exist__neither",
            "ansible_collections.ns2.col.foo_role__parameter-main__does_not_exist",
            "ansible_collections.ns2.col.foo_role__return-boo__boo",
            "ansible_collections.ns2.col.foo_role__return-does_not_exist__neither",
            "ansible_collections.ns2.col.joo_filter__parameter-foo",
            "ansible_collections.ns2.col.joo_lookup",
            "ansible_collections.ns2.col.joo_module",
            "ansible_collections.ns2.col.joo_test__return-_value",
            "ansible_collections.ns2.flatcol.foobarbaz_module",
            "ansible_collections.ns2.flatcol.foobar_module__parameter-subbaz/bam",
            "ansible_collections.ns2.flatcol.foo_module__parameter-foofoofoobar",
            "ansible_collections.ns2.flatcol.foo_role__parameter-main__foo_param_1",
            "ansible_collections.ns2.flatcol.foo_role__parameter-main__foo_param_2",
            "ansible_collections.ns2.flatcol.sub.bazbam_module",
            "ansible_collections.ns2.flatcol.sub.bazbam_module__return-bar",
            "ansible_collections.ns2.flatcol.sub.foo2_module",
            "ansible_collections.ns2.flatcol.sub.foo2_module__return-bar",
            "ansible_collections.ns2.flatcol.sub.foo2_module__return-bazbarbam",
            "ansible_collections.ns.col2.foo2_module__parameter-",
            "ansible_collections.ns.col2.foo2_module__parameter-barbazbam/foo",
            "ansible_collections.ns.col2.foo2_module__parameter-broken markup",
            "ansible_collections.ns.col2.foo2_module__parameter-foobar",
            "ansible_collections.ns.col2.foo2_module__parameter-subfoo[",
            "ansible_collections.ns.col2.foo2_module__return-",
            "ansible_collections.ns.col2.foo2_module__return-bambazbar",
            "ansible_collections.ns.col2.foo2_module__return-barbaz",
            "ansible_collections.ns.col2.foo2_module__return-foobarbaz",
            "ansible_collections.ns.col2.foobarbam_filter",
            "ansible_collections.ns.col2.foobarbaz_inventory",
            "ansible_collections.ns.col2.foobarbaz_module",
            "ansible_collections.ns.col2.foofoo_lookup__return-baz",
            "ansible_collections.ns.col2.foofoo_test__parameter-subfoo/foo",
            "ansible_collections.ns.col2.foo_module__parameter-foo",
            "ansible_collections.ns.col2.foo_module__parameter-foobar",
            "ansible_collections.ns.col2.foo_module__return-bar",
            "ansible_collections.ns.col2.foo_module__return-barbaz",
            "ansible_configuration_settings",
            "asdfasdfoobarthisdoesnotexist",
            "callback_plugins",
            "common_return_values",
            "filter_plugins_in_ns.col1",
            "foo_plugins_in_ns2.col",
            "migrating_to_loop",
            "plugins_in_does.not_exist",
        ],
        [
            "/input/collections/ns/col2/foo2_module.rst:57: WARNING: undefined label: '' [ref.ref]",
            "/input/collections/ns2/col/bar_filter.rst:323: WARNING: Lexing literal_block \"{'a': 1} | ns2.col.bar({'b': 2}, baz='cde')\" as \"yaml+jinja\" resulted in an error at token: ' '. Retrying in relaxed mode. [misc.highlighting_failure]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:40: ERROR: while processing :anscollection:`ns2.col#foobar`: Invalid destination [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:50: ERROR: while processing :ansplugin:`ns2.col.foo#filter:boo`: Only roles can have entrypoints [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:58: ERROR: while processing :ansopt:`ns2.col.foo#role:does_not_exist`: Role reference is missing entrypoint [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:64: ERROR: while processing :ansretval:`ns2.col.foo#role:does_not_exist`: Role reference is missing entrypoint [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:66: ERROR: while processing :ansoptref:`no explicit title`: An explicit reference title must be provided! [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:68: ERROR: while processing :ansoptref:`title <no plugin>`: Cannot extract plugin name and type [semantic-markup]",
            '/input/collections/ns2/col/docsite/filter_guide.rst:72: ERROR: while processing :ansoptref:`entrypoint for non-role <ns2.col.foo#filter:foo:boo>`: Invalid option name "foo:boo" [semantic-markup]',
            "/input/collections/ns2/col/docsite/filter_guide.rst:74: ERROR: while processing :ansoptref:`no entrypoint for role <ns2.col.foo#role:boo>`: Role reference is missing entrypoint [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:80: ERROR: while processing :ansretvalref:`no explicit title`: An explicit reference title must be provided! [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:82: ERROR: while processing :ansretvalref:`title <no plugin>`: Cannot extract plugin name and type [semantic-markup]",
            '/input/collections/ns2/col/docsite/filter_guide.rst:86: ERROR: while processing :ansretvalref:`entrypoint for non-role <ns2.col.foo#filter:foo:boo>`: Invalid return value name "foo:boo" [semantic-markup]',
            "/input/collections/ns2/col/docsite/filter_guide.rst:88: ERROR: while processing :ansretvalref:`no entrypoint for role <ns2.col.foo#role:boo>`: Role reference is missing entrypoint [semantic-markup]",
            "/input/collections/ns2/col/foo_become.rst:210: WARNING: 'envvar' reference target not found: ANSIBLE_BECOME_EXE [ref.envvar]",
            "/input/collections/ns2/col/foo_become.rst:349: WARNING: 'envvar' reference target not found: ANSIBLE_BECOME_USER [ref.envvar]",
            "/input/collections/ns2/col/foo_cache.rst:127: WARNING: 'envvar' reference target not found: ANSIBLE_CACHE_PLUGIN_CONNECTION [ref.envvar]",
            "/input/collections/ns2/col/index.rst:71: WARNING: toctree contains reference to document 'collections/ns2/col/changelog' that doesn't have a title: no link will be generated [toc.no_title]",
        ],
    ),
    (
        "baseline-default-adl",
        "baseline-default-adl-html",
        [
            "ansible_collections.ansible.builtin.bazbam_lookup",
            "ansible_collections.ansible.builtin.bazbam_module__return-stat/exists",
            "ansible_collections.ansible.builtin.file_module__parameter-foobarbaz",
            "ansible_collections.ansible.builtin.file_module__parameter-state",
            "ansible_collections.ansible.builtin.foobarbaz_module",
            "ansible_collections.ansible.builtin.foobarbaz_strategy",
            "ansible_collections.ansible.builtin.foobar_module",
            "ansible_collections.ansible.builtin.foobar_module__parameter-state",
            "ansible_collections.ansible.builtin.iptables_module__parameter-tcp_flags/flags",
            "ansible_collections.ansible.builtin.linear_strategy",
            "ansible_collections.ansible.builtin.pipe_lookup",
            "ansible_collections.ansible.builtin.service_module",
            "ansible_collections.ansible.builtin.ssh_connection",
            "ansible_collections.ansible.builtin.stat_module__return-baz/bam",
            "ansible_collections.ansible.builtin.stat_module__return-stat",
            "ansible_collections.ansible.builtin.stat_module__return-stat/exists",
            "ansible_collections.ext.col.bar_lookup",
            "ansible_collections.ext.col.foo_module",
            "ansible_collections.ext.col.foo_module__parameter-foo/bar",
            "ansible_collections.ext.col.foo_module__parameter-foo/notthere",
            "ansible_collections.ext.col.foo_module__parameter-notthere/bar",
            "ansible_collections.ext.col.foo_module__return-baz",
            "ansible_collections.ext.col.foo_module__return-notthere",
            "ansible_collections.ext.col.notthere_lookup",
            "ansible_collections.ext.col.notthere_module",
            "ansible_collections.ext.col.notthere_module__parameter-foo/bar",
            "ansible_collections.ext.col.notthere_module__return-baz",
            "ansible_collections.ns2.col.bar_filter__parameter-jooo",
            "ansible_collections.ns2.col.bar_test__return-booo",
            "ansible_collections.ns2.col.boo_filter__parameter-boo",
            "ansible_collections.ns2.col.boo_filter__return-boo",
            "ansible_collections.ns2.col.does_not_exist_filter",
            "ansible_collections.ns2.col.foo_asdf",
            "ansible_collections.ns2.col.foobarbaz_module",
            "ansible_collections.ns2.col.foo_filter__parameter-boo",
            "ansible_collections.ns2.col.foo_filter__return-boo",
            "ansible_collections.ns2.col.foo_filter__return-does_not_exist",
            "ansible_collections.ns2.col.foo_module__parameter-strategy",
            "ansible_collections.ns2.col.foo_redirect_module__parameter-bar",
            "ansible_collections.ns2.col.foo_redirect_module__parameter-baz",
            "ansible_collections.ns2.col.foo_role__entrypoint-boo",
            "ansible_collections.ns2.col.foo_role__parameter-boo__boo",
            "ansible_collections.ns2.col.foo_role__parameter-does_not_exist__neither",
            "ansible_collections.ns2.col.foo_role__parameter-main__does_not_exist",
            "ansible_collections.ns2.col.foo_role__return-boo__boo",
            "ansible_collections.ns2.col.foo_role__return-does_not_exist__neither",
            "ansible_collections.ns2.col.joo_filter__parameter-foo",
            "ansible_collections.ns2.col.joo_lookup",
            "ansible_collections.ns2.col.joo_module",
            "ansible_collections.ns2.col.joo_test__return-_value",
            "ansible_collections.ns2.flatcol.foobarbaz_module",
            "ansible_collections.ns2.flatcol.foobar_module__parameter-subbaz/bam",
            "ansible_collections.ns2.flatcol.foo_module__parameter-foofoofoobar",
            "ansible_collections.ns2.flatcol.foo_role__parameter-main__foo_param_1",
            "ansible_collections.ns2.flatcol.foo_role__parameter-main__foo_param_2",
            "ansible_collections.ns2.flatcol.sub.bazbam_module",
            "ansible_collections.ns2.flatcol.sub.bazbam_module__return-bar",
            "ansible_collections.ns2.flatcol.sub.foo2_module",
            "ansible_collections.ns2.flatcol.sub.foo2_module__return-bar",
            "ansible_collections.ns2.flatcol.sub.foo2_module__return-bazbarbam",
            "ansible_collections.ns.col2.foo2_module__parameter-",
            "ansible_collections.ns.col2.foo2_module__parameter-barbazbam/foo",
            "ansible_collections.ns.col2.foo2_module__parameter-broken markup",
            "ansible_collections.ns.col2.foo2_module__parameter-foobar",
            "ansible_collections.ns.col2.foo2_module__parameter-subfoo[",
            "ansible_collections.ns.col2.foo2_module__return-",
            "ansible_collections.ns.col2.foo2_module__return-bambazbar",
            "ansible_collections.ns.col2.foo2_module__return-barbaz",
            "ansible_collections.ns.col2.foo2_module__return-foobarbaz",
            "ansible_collections.ns.col2.foobarbam_filter",
            "ansible_collections.ns.col2.foobarbaz_inventory",
            "ansible_collections.ns.col2.foobarbaz_module",
            "ansible_collections.ns.col2.foofoo_lookup__return-baz",
            "ansible_collections.ns.col2.foofoo_test__parameter-subfoo/foo",
            "ansible_collections.ns.col2.foo_module__parameter-foo",
            "ansible_collections.ns.col2.foo_module__parameter-foobar",
            "ansible_collections.ns.col2.foo_module__return-bar",
            "ansible_collections.ns.col2.foo_module__return-barbaz",
            "ansible_configuration_settings",
            "asdfasdfoobarthisdoesnotexist",
            "callback_plugins",
            "common_return_values",
            "filter_plugins_in_ns.col1",
            "foo_plugins_in_ns2.col",
            "migrating_to_loop",
            "plugins_in_does.not_exist",
        ],
        [
            "/input/collections/ns/col2/foo2_module.rst:57: WARNING: undefined label: '' [ref.ref]",
            "/input/collections/ns2/col/bar_filter.rst:323: WARNING: Lexing literal_block \"{'a': 1} | ns2.col.bar({'b': 2}, baz='cde')\" as \"yaml+jinja\" resulted in an error at token: ' '. Retrying in relaxed mode. [misc.highlighting_failure]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:40: ERROR: while processing :anscollection:`ns2.col#foobar`: Invalid destination [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:50: ERROR: while processing :ansplugin:`ns2.col.foo#filter:boo`: Only roles can have entrypoints [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:58: ERROR: while processing :ansopt:`ns2.col.foo#role:does_not_exist`: Role reference is missing entrypoint [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:64: ERROR: while processing :ansretval:`ns2.col.foo#role:does_not_exist`: Role reference is missing entrypoint [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:66: ERROR: while processing :ansoptref:`no explicit title`: An explicit reference title must be provided! [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:68: ERROR: while processing :ansoptref:`title <no plugin>`: Cannot extract plugin name and type [semantic-markup]",
            '/input/collections/ns2/col/docsite/filter_guide.rst:72: ERROR: while processing :ansoptref:`entrypoint for non-role <ns2.col.foo#filter:foo:boo>`: Invalid option name "foo:boo" [semantic-markup]',
            "/input/collections/ns2/col/docsite/filter_guide.rst:74: ERROR: while processing :ansoptref:`no entrypoint for role <ns2.col.foo#role:boo>`: Role reference is missing entrypoint [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:80: ERROR: while processing :ansretvalref:`no explicit title`: An explicit reference title must be provided! [semantic-markup]",
            "/input/collections/ns2/col/docsite/filter_guide.rst:82: ERROR: while processing :ansretvalref:`title <no plugin>`: Cannot extract plugin name and type [semantic-markup]",
            '/input/collections/ns2/col/docsite/filter_guide.rst:86: ERROR: while processing :ansretvalref:`entrypoint for non-role <ns2.col.foo#filter:foo:boo>`: Invalid return value name "foo:boo" [semantic-markup]',
            "/input/collections/ns2/col/docsite/filter_guide.rst:88: ERROR: while processing :ansretvalref:`no entrypoint for role <ns2.col.foo#role:boo>`: Role reference is missing entrypoint [semantic-markup]",
            "/input/collections/ns2/col/foo_become.rst:210: WARNING: 'envvar' reference target not found: ANSIBLE_BECOME_EXE [ref.envvar]",
            "/input/collections/ns2/col/foo_become.rst:349: WARNING: 'envvar' reference target not found: ANSIBLE_BECOME_USER [ref.envvar]",
            "/input/collections/ns2/col/foo_cache.rst:127: WARNING: 'envvar' reference target not found: ANSIBLE_CACHE_PLUGIN_CONNECTION [ref.envvar]",
            "/input/collections/ns2/col/index.rst:71: WARNING: toctree contains reference to document 'collections/ns2/col/changelog' that doesn't have a title: no link will be generated [toc.no_title]",
        ],
    ),
]


@pytest.mark.parametrize(
    "source_dir, dest_dir, broken_refs, expected_warnings_and_errors", TEST_CASES
)
def test_baseline(
    source_dir: str,
    dest_dir: str,
    broken_refs: list[str],
    expected_warnings_and_errors: list[str],
    tmp_path,
) -> None:
    tests_root = os.path.join("tests", "functional")
    theme_path = os.path.abspath(os.path.join(tests_root, "sphinx-themes"))

    input_dir = tmp_path / "input"
    shutil.copytree(os.path.join(tests_root, source_dir), input_dir)
    (input_dir / "conf.py").write_text("""
project = 'Ansible collections'
copyright = 'Ansible contributors'
title = 'Ansible Collections Documentation'
html_short_title = 'Ansible Collections Documentation'
extensions = ['sphinx_antsibull_ext']
pygments_style = 'ansible'
highlight_language = 'YAML+Jinja'
html_theme = 'empty'
html_theme_path = [<THEME_PATH>]
html_show_sphinx = False
display_version = False
html_use_smartypants = True
html_use_modindex = False
html_use_index = False
html_copy_source = False
nitpicky = True
""".replace("<THEME_PATH>", repr(str(theme_path))))

    (input_dir / "index.rst").write_text("""
====================
Some Ansible Docsite
====================

.. toctree::
   :glob:

   collections/*
""")

    (input_dir / "broken-refs.rst").write_text(""":orphan:

<LABELS>

Dead reference
==============

All dead references should link to this section.
""".replace("<LABELS>", "\n".join(f".. _{ref}:" for ref in broken_refs)))

    output_dir = tmp_path / "output"

    warning_file = tmp_path / "warnings.txt"

    command = [
        "--builder",
        "html",
        str(input_dir),
        str(output_dir),
        "--keep-going",
        "--warning-file",
        str(warning_file),
        # "--fail-on-warning",
    ]
    with ansible_doc_cache():
        rc = sphinx_main(command)

    tmp_path_str = str(tmp_path)
    warnings = sorted(
        [
            line.replace(tmp_path_str, "")
            for line in warning_file.read_text(encoding="utf-8").splitlines()
        ]
    )
    print("Warnings and errors:")
    for warning in warnings:
        print(warning)

    assert rc == 0
    assert expected_warnings_and_errors == warnings

    html_dir = output_dir
    for filename in ["objects.inv", "searchindex.js", "search.html", ".buildinfo"]:
        file = html_dir / filename
        if file.exists():
            file.unlink()
    for directory in ["_static", "_sources", ".doctrees"]:
        file = html_dir / directory
        if file.exists():
            shutil.rmtree(file)

    comparsion_dir = os.path.join(tests_root, dest_dir)

    if UPDATE_BASELINES:
        print(f"Copying {html_dir} to {comparsion_dir}...")
        if os.path.exists(comparsion_dir):
            shutil.rmtree(comparsion_dir)
        shutil.copytree(html_dir, comparsion_dir)

    # Compare baseline to expected result
    source = scan_directories(comparsion_dir)
    dest = scan_directories(html_dir)
    compare_directories(source, dest)
