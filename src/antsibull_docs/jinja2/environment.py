# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2019-2020, Ansible Project
"""Create Jinja2 environment for rendering Ansible documentation."""

from __future__ import annotations

import json
import os.path
import typing as t
from collections.abc import Mapping

from jinja2 import BaseLoader, Environment, FileSystemLoader, PackageLoader

from ..markup.rstify import rst_code, rst_escape
from ..utils.collection_name_transformer import CollectionNameTransformer
from .filters import (
    do_max,
    documented_type,
    extract_options_from_list,
    html_ify,
    massage_author_name,
    move_first,
    remove_options_from_list,
    rst_fmt,
    rst_ify,
    rst_xline,
    to_ini_value,
    to_json,
)
from .tests import still_relevant, test_list

# kludge_ns gives us a kludgey way to set variables inside of loops that need to be visible outside
# the loop.  We can get rid of this when we no longer need to build docs with less than Jinja-2.10
# http://jinja.pocoo.org/docs/2.10/templates/#assignments
# With Jinja-2.10 we can use jinja2's namespace feature, restoring the namespace template portion
# of: fa5c0282a4816c4dd48e80b983ffc1e14506a1f5
NS_MAP = {}


def to_kludge_ns(key, value):
    NS_MAP[key] = value
    return ""


def from_kludge_ns(key):
    return NS_MAP[key]


def reference_plugin_rst(plugin_name: str, plugin_type: str) -> str:
    fqcn = f"{plugin_name}"
    return f"\\ :ref:`{rst_escape(fqcn)} <ansible_collections.{fqcn}_{plugin_type}>`\\ "


def doc_environment(
    template_location: str | tuple[str, str],
    *,
    extra_filters: Mapping[str, t.Callable] | None = None,
    extra_tests: Mapping[str, t.Callable] | None = None,
    collection_url: CollectionNameTransformer | None = None,
    collection_install: CollectionNameTransformer | None = None,
) -> Environment:
    loader: BaseLoader
    if isinstance(template_location, str) and os.path.exists(template_location):
        loader = FileSystemLoader(template_location)
    else:
        if isinstance(template_location, str):
            template_pkg = template_location
            template_path = "templates"
        else:
            template_pkg = template_location[0]
            template_path = template_location[1]

        loader = PackageLoader(template_pkg, template_path)

    env = Environment(
        loader=loader,
        variable_start_string="@{",
        variable_end_string="}@",
        trim_blocks=True,
    )
    env.globals["xline"] = rst_xline

    # Can be removed (and template switched to use namespace) when we no longer need to build
    # with <Jinja-2.10
    env.globals["to_kludge_ns"] = to_kludge_ns
    env.globals["from_kludge_ns"] = from_kludge_ns
    env.globals["reference_plugin_rst"] = reference_plugin_rst
    if "max" not in env.filters:
        # Jinja < 2.10
        env.filters["max"] = do_max

    if "tojson" not in env.filters:
        # Jinja < 2.9
        env.filters["tojson"] = json.dumps

    env.filters["rst_ify"] = rst_ify
    env.filters["html_ify"] = html_ify
    env.filters["fmt"] = rst_fmt
    env.filters["rst_code"] = rst_code
    env.filters["rst_escape"] = rst_escape
    env.filters["xline"] = rst_xline
    env.filters["documented_type"] = documented_type
    env.filters["move_first"] = move_first
    env.filters["massage_author_name"] = massage_author_name
    env.filters["extract_options_from_list"] = extract_options_from_list
    env.filters["remove_options_from_list"] = remove_options_from_list
    env.filters["antsibull_to_json"] = to_json
    env.filters["antsibull_to_ini_value"] = to_ini_value
    if collection_url is not None:
        env.filters["collection_url"] = collection_url
    if collection_install is not None:
        env.filters["collection_install"] = collection_install
    if extra_filters:
        env.filters.update(extra_filters)

    env.tests["list"] = test_list
    env.tests["still_relevant"] = still_relevant
    if extra_tests:
        env.tests.update(extra_tests)

    return env
