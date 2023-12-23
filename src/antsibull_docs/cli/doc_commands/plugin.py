# Author: Toshio Kuratomi <tkuratom@redhat.com>
# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Render documentation for a single plugin."""

from __future__ import annotations

import asyncio
import json
import os
import sys
import traceback
import typing as t
from collections.abc import MutableMapping

from antsibull_core.logging import log
from antsibull_core.subprocess_util import CalledProcessError
from antsibull_core.vendored.json_utils import _filter_non_json_lines
from antsibull_core.venv import FakeVenvRunner

from ... import app_context
from ...augment_docs import augment_docs
from ...collection_links import CollectionLinks
from ...docs_parsing import AnsibleCollectionMetadata
from ...docs_parsing.fqcn import get_fqcn_parts
from ...jinja2 import FilenameGenerator, OutputFormat
from ...jinja2.environment import doc_environment
from ...process_docs import normalize_plugin_info
from ...schemas.app_context import (
    DEFAULT_COLLECTION_INSTALL_CMD,
    DEFAULT_COLLECTION_URL_TRANSFORM,
)
from ...utils.collection_name_transformer import CollectionNameTransformer
from ...write_docs.plugins import write_plugin_rst

mlog = log.fields(mod=__name__)


def generate_plugin_docs(
    plugin_type: str,
    plugin_name: str,
    collection_name: str,
    plugin: str,
    output_path: str,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,
) -> int:
    """
    Render documentation for a locally installed plugin.
    """
    flog = mlog.fields(func="generate_plugin_docs")
    flog.debug("Begin generating plugin docs")

    app_ctx = app_context.app_ctx.get()

    if app_ctx.use_html_blobs:
        print(
            "WARNING: the use of --use-html-blobs is deprecated."
            " This feature will be removed soon.",
            file=sys.stderr,
        )

    venv = FakeVenvRunner()
    try:
        ansible_doc_results = venv.log_run(
            ["ansible-doc", "-vvv", "-t", plugin_type, "--json", plugin_name]
        )
    except CalledProcessError as exc:
        err_msg = []
        formatted_exception = traceback.format_exception(None, exc, exc.__traceback__)
        err_msg.append(
            f"Exception while parsing documentation for {plugin_type} plugin:"
            f" {plugin_name}.  Will not document this plugin."
        )
        err_msg.append(f'Exception:\n{"".join(formatted_exception)}')

        err_msg.append(f"Full process stdout:\n{exc.stdout}")
        err_msg.append(f"Full process stderr:\n{exc.stderr}")

        sys.stderr.write("\n".join(err_msg))
        return 1

    plugin_data = json.loads(_filter_non_json_lines(ansible_doc_results.stdout)[0])
    try:
        plugin_info = plugin_data[plugin_name]
    except KeyError:
        print(f"Cannot find documentation for plugin {plugin_name}!")
        return 1
    flog.debug("Finished parsing info from plugin")

    try:
        plugin_info, errors = normalize_plugin_info(plugin_type, plugin_info)
    except ValueError as exc:
        print("Cannot parse documentation:")
        print(str(exc))
        return 1
    flog.debug("Finished normalizing data")

    if errors and app_ctx.extra["fail_on_error"]:
        print("Found errors:")
        for error in errors:
            print(error)
        return 1

    # The cast is needed to make pyre happy. It seems to not being able to
    # understand that
    #     dict[str, dict[str, dict[str, typing.Any]]]
    # is acceptable for
    #     MutableMapping[str, MutableMapping[str, typing.Any]].
    augment_docs(
        t.cast(
            MutableMapping[str, MutableMapping[str, t.Any]],
            {plugin_type: {plugin_name: plugin_info}},
        ),
        {},
    )

    # Setup the jinja environment
    collection_url = CollectionNameTransformer(
        app_ctx.collection_url, DEFAULT_COLLECTION_URL_TRANSFORM
    )
    collection_install = CollectionNameTransformer(
        app_ctx.collection_install,
        DEFAULT_COLLECTION_INSTALL_CMD,
    )
    env = doc_environment(
        collection_url=collection_url,
        collection_install=collection_install,
        output_format=output_format,
    )
    # Get the templates
    plugin_tmpl = env.get_template("plugin.rst.j2")
    error_tmpl = env.get_template("plugin-error.rst.j2")

    asyncio.run(
        write_plugin_rst(
            collection_name,
            AnsibleCollectionMetadata.empty(),
            CollectionLinks(),
            plugin,
            plugin_type,
            plugin_info,
            errors,
            plugin_tmpl,
            error_tmpl,
            "",
            output_format,
            filename_generator,
            path_override=output_path,
            use_html_blobs=app_ctx.use_html_blobs,
        )
    )
    flog.debug("Finished writing plugin docs")

    return 0


def generate_docs() -> int:
    """
    Create documentation for the current-plugin subcommand.

    Current plugin documentation creates documentation for one currently installed plugin.

    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func="generate_docs")
    flog.debug("Begin processing docs")

    app_ctx = app_context.app_ctx.get()
    plugin_type: str = app_ctx.extra["plugin_type"]
    plugin_name: str = app_ctx.extra["plugin"][0]
    output_format = OutputFormat.parse(app_ctx.extra["output_format"])

    output_path = os.path.join(
        app_ctx.extra["dest_dir"], f"{plugin_name}_{plugin_type}.rst"
    )

    try:
        namespace, collection, plugin = get_fqcn_parts(plugin_name)
    except ValueError:
        namespace, collection = "ansible", "builtin"
        plugin = plugin_name
    collection_name = ".".join([namespace, collection])
    plugin_name = ".".join([namespace, collection, plugin])

    filename_generator = FilenameGenerator()

    return generate_plugin_docs(
        plugin_type,
        plugin_name,
        collection_name,
        plugin,
        output_path,
        output_format,
        filename_generator,
    )
