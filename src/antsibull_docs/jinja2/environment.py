# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2019-2020, Ansible Project
"""Create Jinja2 environment for rendering Ansible documentation."""

from __future__ import annotations

import os.path
import typing as t
from collections.abc import Mapping

from jinja2 import BaseLoader, Environment, FileSystemLoader, PackageLoader

from ..markup.rstify import rst_code, rst_escape
from ..utils.collection_name_transformer import CollectionNameTransformer
from . import FilenameGenerator, OutputFormat
from .filters import (
    collection_name,
    column_width,
    documented_type,
    extract_options_from_list,
    html_ify,
    make_rst_ify,
    massage_author_name,
    move_first,
    plugin_shortname,
    remove_options_from_list,
    rst_fmt,
    rst_format,
    rst_xline,
    suboption_depth,
    to_ini_value,
    to_json,
)
from .tests import still_relevant, test_list


def reference_plugin_rst(plugin_name: str, plugin_type: str) -> str:
    fqcn = f"{plugin_name}"
    return f"\\ :ref:`{rst_escape(fqcn)} <ansible_collections.{fqcn}_{plugin_type}>`\\ "


def reference_plugin_rst_simplified(plugin_name: str, plugin_type: str) -> str:
    fqcn = f"{plugin_name}"
    # TODO: return f"\\ {fqcn}\\ " for other collections
    name = plugin_name.split(".", 2)[2]
    return f"\\ `{rst_escape(fqcn)} <{name}_{plugin_type}.rst>`__\\ "


def make_reference_plugin_rst(output_format: OutputFormat):
    if output_format == OutputFormat.SIMPLIFIED_RST:
        return reference_plugin_rst_simplified
    return reference_plugin_rst


def get_template_location(output_format: OutputFormat) -> tuple[str, str]:
    """
    Return template location given the output format.
    """
    return ("antsibull_docs.data", f"docsite/{output_format.output_format}")


def get_template_filename(filename_base: str, output_format: OutputFormat) -> str:
    """
    Return template filename given the filename base and the output format.
    """
    return f"{filename_base}{output_format.template_extension}"


def _get_loader(
    template_location: str | tuple[str, str] | None, output_format: OutputFormat | None
) -> BaseLoader:
    if template_location is None:
        if output_format is None:
            raise ValueError(
                "Either template_location or output_format must be provided"
            )
        template_location = get_template_location(output_format)

    if isinstance(template_location, str) and os.path.exists(template_location):
        return FileSystemLoader(template_location)

    if isinstance(template_location, str):
        template_pkg = template_location
        template_path = "templates"
    else:
        template_pkg = template_location[0]
        template_path = template_location[1]

    return PackageLoader(template_pkg, template_path)


def _create_filename_functions(
    filename_generator: FilenameGenerator,
    output_format: OutputFormat,
) -> Mapping[str, t.Callable]:
    def get_plugin_basename(plugin_fqcn: str, plugin_type: str) -> str:
        return filename_generator.plugin_basename(plugin_fqcn, plugin_type)

    def get_plugin_filename(plugin_fqcn: str, plugin_type: str) -> str:
        return filename_generator.plugin_filename(
            plugin_fqcn, plugin_type, output_format
        )

    return {
        "get_plugin_basename": get_plugin_basename,
        "get_plugin_filename": get_plugin_filename,
    }


def doc_environment(
    template_location: str | tuple[str, str] | None = None,
    *,
    extra_filters: Mapping[str, t.Callable] | None = None,
    extra_tests: Mapping[str, t.Callable] | None = None,
    collection_url: CollectionNameTransformer | None = None,
    collection_install: CollectionNameTransformer | None = None,
    referable_envvars: set[str] | None = None,
    output_format: OutputFormat | None = None,
    filename_generator: FilenameGenerator | None = None,
) -> Environment:
    loader = _get_loader(template_location, output_format)
    if output_format is None:
        output_format = OutputFormat.ANSIBLE_DOCSITE

    env = Environment(
        loader=loader,
        variable_start_string="@{",
        variable_end_string="}@",
        trim_blocks=True,
    )
    env.globals["xline"] = rst_xline

    if filename_generator:
        env.globals.update(
            _create_filename_functions(filename_generator, output_format)
        )

    env.globals["reference_plugin_rst"] = make_reference_plugin_rst(output_format)
    env.globals["referable_envvars"] = referable_envvars
    env.filters["rst_ify"] = make_rst_ify(output_format)
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
    env.filters["collection_name"] = collection_name
    env.filters["column_width"] = column_width
    env.filters["plugin_shortname"] = plugin_shortname
    env.filters["suboption_depth"] = suboption_depth
    env.filters["rst_format"] = rst_format
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
