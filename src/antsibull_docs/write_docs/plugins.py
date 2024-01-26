# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Output plugin documentation."""

from __future__ import annotations

import asyncio
import os
import os.path
import typing as t
from collections.abc import Mapping, Sequence

import asyncio_pool  # type: ignore[import]
from antsibull_core import app_context
from antsibull_core.logging import log
from antsibull_core.utils.io import write_file
from jinja2 import Template

from ..collection_links import CollectionLinks
from ..docs_parsing import AnsibleCollectionMetadata
from ..jinja2 import FilenameGenerator, OutputFormat
from ..jinja2.environment import doc_environment, get_template_filename
from ..utils.collection_name_transformer import CollectionNameTransformer
from . import CollectionInfoT, PluginErrorsT, _render_template

mlog = log.fields(mod=__name__)


def follow_relative_links(path: str) -> str:
    """
    Resolve relative links for path.

    :arg path: Path to a file.
    """
    flog = mlog.fields(func="follow_relative_links")
    flog.fields(path=path).debug("Enter")

    original_path = path
    loop_detection: set[str] = set()
    while True:
        if path in loop_detection:
            flog.fields(path=original_path, loop=loop_detection).error(
                "{path} resulted in a loop when looking up relative symbolic links.",
                path=path,
            )
            flog.debug("Leave")
            return original_path
        loop_detection.add(path)
        if not os.path.islink(path):
            flog.fields(result=path).debug("Leave")
            return path
        flog.debug("Reading link {path}", path=path)
        link = os.readlink(path)
        if link.startswith("/"):
            flog.fields(
                original_path=original_path,
                path=path,
                link=link,
            ).error(
                "When looking up relative links for {original_path}, an absolute link"
                ' "{link}" was found for {path}.',
                original_path=original_path,
                path=path,
                link=link,
            )
            flog.debug("Leave")
            return original_path
        path = os.path.join(os.path.dirname(path), link)


def has_broken_docs(plugin_record: Mapping[str, t.Any], plugin_type: str) -> bool:
    """
    Determine whether the plugin record is completely broken or not.
    """
    expected_fields = (
        ("entry_points",) if plugin_type == "role" else ("doc", "examples", "return")
    )
    return not plugin_record or not all(
        field in plugin_record for field in expected_fields
    )


def guess_relative_filename(
    plugin_record: Mapping[str, t.Any],
    plugin_short_name: str,
    plugin_type: str,
    collection_name: str,
    collection_meta: AnsibleCollectionMetadata,
) -> str:
    """
    Make an educated guess on the documentation source file.
    """
    if (
        plugin_record
        and plugin_record.get("doc")
        and plugin_record["doc"].get("filename")
    ):
        filename = follow_relative_links(plugin_record["doc"]["filename"])
        return os.path.relpath(filename, collection_meta.path)
    if plugin_type == "role":
        return f"roles/{plugin_short_name}/meta/argument_specs.yml"
    plugin_dir = (
        # Modules in ansible-core:
        "modules"
        if plugin_type == "module" and collection_name == "ansible.builtin"
        else
        # Modules in collections:
        (
            "plugins/modules"
            if plugin_type == "module"
            else
            # Plugins in ansible-core or collections:
            "plugins/" + plugin_type
        )
    )
    # Guess path inside collection tree
    return f"{plugin_dir}/{plugin_short_name}.py"


def create_plugin_rst(
    collection_name: str,
    collection_meta: AnsibleCollectionMetadata,
    collection_links: CollectionLinks,
    plugin_short_name: str,
    plugin_type: str,
    plugin_record: dict[str, t.Any],
    nonfatal_errors: Sequence[str],
    plugin_tmpl: Template,
    error_tmpl: Template,
    use_html_blobs: bool = False,
    for_official_docsite: bool = False,
    log_errors: bool = True,
) -> str:
    """
    Create the rst page for one plugin.

    :arg collection_name: Dotted colection name.
    :arg collection_meta: Collection metadata object.
    :arg collection_links: Collection links object.
    :arg plugin_short_name: short name for the plugin.
    :arg plugin_type: The type of the plugin.  (module, inventory, etc)
    :arg plugin_record: The record for the plugin.  doc, examples, and return are the
        toplevel fields.
    :arg nonfatal_errors: Mapping of plugin to any nonfatal errors that will be displayed in place
        of some or all of the docs
    :arg plugin_tmpl: Template for the plugin.
    :arg error_tmpl: Template to use when there wasn't enough documentation for the plugin.
    :arg use_html_blobs: If set to ``True``, will use HTML blobs for parameter and return value
                         tables instead of using RST tables.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg log_errors: Default True.  Set to False to avoid errors to be logged.
    """
    flog = mlog.fields(func="create_plugin_rst")
    flog.debug("Enter")

    plugin_name = ".".join((collection_name, plugin_short_name))

    edit_on_github_url = None
    eog = collection_links.edit_on_github
    if eog:
        # Compose Edit on GitHub URL
        gh_path = guess_relative_filename(
            plugin_record,
            plugin_short_name,
            plugin_type,
            collection_name,
            collection_meta,
        )
        edit_on_github_url = (
            f"https://github.com/{eog.repository}/"
            f"edit/{eog.branch}/{eog.path_prefix}{gh_path}"
        )

    if has_broken_docs(plugin_record, plugin_type):
        if log_errors:
            flog.fields(
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                nonfatal_errors=nonfatal_errors,
            ).error(
                "{plugin_name} did not return correct DOCUMENTATION.  An error"
                " page will be generated.",
                plugin_name=plugin_name,
            )
        plugin_contents = _render_template(
            error_tmpl,
            plugin_name + "_" + plugin_type,
            plugin_type=plugin_type,
            plugin_name=plugin_name,
            collection=collection_name,
            collection_version=collection_meta.version,
            nonfatal_errors=nonfatal_errors,
            edit_on_github_url=edit_on_github_url,
            collection_links=collection_links.links,
            collection_communication=collection_links.communication,
            collection_issue_tracker=collection_links.issue_tracker,
            for_official_docsite=for_official_docsite,
        )
    else:
        if log_errors and nonfatal_errors:
            flog.fields(
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                nonfatal_errors=nonfatal_errors,
            ).error(
                "{plugin_name} did not return correct RETURN or EXAMPLES.",
                plugin_name=plugin_name,
            )
        if plugin_type == "role":
            plugin_contents = _render_template(
                plugin_tmpl,
                plugin_name + "_" + plugin_type,
                use_html_blobs=use_html_blobs,
                collection=collection_name,
                collection_version=collection_meta.version,
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                entry_points=plugin_record["entry_points"],
                nonfatal_errors=nonfatal_errors,
                edit_on_github_url=edit_on_github_url,
                collection_links=collection_links.links,
                collection_communication=collection_links.communication,
                collection_issue_tracker=collection_links.issue_tracker,
                for_official_docsite=for_official_docsite,
            )
        else:
            plugin_contents = _render_template(
                plugin_tmpl,
                plugin_name + "_" + plugin_type,
                use_html_blobs=use_html_blobs,
                collection=collection_name,
                collection_version=collection_meta.version,
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                doc=plugin_record["doc"],
                examples=plugin_record["examples"],
                examples_format=plugin_record["examples_format"],
                returndocs=plugin_record["return"],
                nonfatal_errors=nonfatal_errors,
                edit_on_github_url=edit_on_github_url,
                collection_links=collection_links.links,
                collection_communication=collection_links.communication,
                collection_issue_tracker=collection_links.issue_tracker,
                for_official_docsite=for_official_docsite,
            )

    flog.debug("Leave")
    return plugin_contents


async def write_plugin_rst(
    collection_name: str,
    collection_meta: AnsibleCollectionMetadata,
    collection_links: CollectionLinks,
    plugin_short_name: str,
    plugin_type: str,
    plugin_record: dict[str, t.Any],
    nonfatal_errors: Sequence[str],
    plugin_tmpl: Template,
    error_tmpl: Template,
    dest_dir: str,
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,
    path_override: str | None = None,
    squash_hierarchy: bool = False,
    use_html_blobs: bool = False,
    for_official_docsite: bool = False,
) -> None:
    """
    Write the rst page for one plugin.

    :arg collection_name: Dotted colection name.
    :arg collection_meta: Collection metadata object.
    :arg collection_links: Collection links object.
    :arg plugin_short_name: short name for the plugin.
    :arg plugin_type: The type of the plugin.  (module, inventory, etc)
    :arg plugin_record: The record for the plugin.  doc, examples, and return are the
        toplevel fields.
    :arg nonfatal_errors: Mapping of plugin to any nonfatal errors that will be displayed in place
        of some or all of the docs
    :arg plugin_tmpl: Template for the plugin.
    :arg error_tmpl: Template to use when there wasn't enough documentation for the plugin.
    :arg dest_dir: Destination directory for the plugin data.  For instance,
        :file:`ansible-checkout/docs/docsite/rst/`.  The directory structure underneath this
        directory will be created if needed.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    :arg use_html_blobs: If set to ``True``, will use HTML blobs for parameter and return value
                         tables instead of using RST tables.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    """
    flog = mlog.fields(func="write_plugin_rst")
    flog.debug("Enter")

    namespace, collection = collection_name.split(".")

    plugin_contents = create_plugin_rst(
        collection_name=collection_name,
        collection_meta=collection_meta,
        collection_links=collection_links,
        plugin_short_name=plugin_short_name,
        plugin_type=plugin_type,
        plugin_record=plugin_record,
        nonfatal_errors=nonfatal_errors,
        plugin_tmpl=plugin_tmpl,
        error_tmpl=error_tmpl,
        use_html_blobs=use_html_blobs,
        for_official_docsite=for_official_docsite,
    )

    if path_override is not None:
        plugin_file = path_override
    else:
        if squash_hierarchy:
            collection_dir = dest_dir
        else:
            collection_dir = os.path.join(
                dest_dir, "collections", namespace, collection
            )
            # This is dangerous but the code that takes dest_dir from the user checks
            # permissions on it to make it as safe as possible.
            os.makedirs(collection_dir, mode=0o755, exist_ok=True)

        plugin_file = os.path.join(
            collection_dir,
            filename_generator.plugin_filename(
                f"{collection_name}.{plugin_short_name}", plugin_type, output_format
            ),
        )

    await write_file(plugin_file, plugin_contents)

    flog.debug("Leave")


async def output_all_plugin_rst(
    collection_to_plugin_info: CollectionInfoT,
    plugin_info: dict[str, t.Any],
    nonfatal_errors: PluginErrorsT,
    dest_dir: str,
    collection_url: CollectionNameTransformer,
    collection_install: CollectionNameTransformer,
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    link_data: Mapping[str, CollectionLinks],
    output_format: OutputFormat,
    filename_generator: FilenameGenerator,
    squash_hierarchy: bool = False,
    use_html_blobs: bool = False,
    for_official_docsite: bool = False,
    referable_envvars: set[str] | None = None,
) -> None:
    """
    Output rst files for each plugin.

    :arg collection_to_plugin_info: Mapping of collection_name to Mapping of plugin_type to Mapping
        of plugin_name to short_description.
    :arg plugin_info: Documentation information for all of the plugins.
    :arg nonfatal_errors: Mapping of plugins to nonfatal errors.  Using this to note on the docs
        pages when documentation wasn't formatted such that we could use it.
    :arg dest_dir: The directory to place the documentation in.
    :arg collection_metadata: Dictionary mapping collection names to collection metadata objects.
    :arg link_data: Dictionary mapping collection names to CollectionLinks.
    :arg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                           Undefined behavior if documentation for multiple collections are
                           created.
    :arg use_html_blobs: If set to ``True``, will use HTML blobs for parameter and return value
                         tables instead of using RST tables.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :kwarg referable_envvars: Optional set of environment variables that can be referenced.
    :kwarg output_format: The output format to use.
    """
    # Setup the jinja environment
    env = doc_environment(
        collection_url=collection_url,
        collection_install=collection_install,
        referable_envvars=referable_envvars,
        output_format=output_format,
        filename_generator=filename_generator,
    )
    # Get the templates
    plugin_tmpl = env.get_template(get_template_filename("plugin", output_format))
    role_tmpl = env.get_template(get_template_filename("role", output_format))
    error_tmpl = env.get_template(get_template_filename("plugin-error", output_format))

    writers = []
    lib_ctx = app_context.lib_ctx.get()
    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name, plugins_by_type in collection_to_plugin_info.items():
            for plugin_type, plugins in plugins_by_type.items():
                plugin_type_tmpl = plugin_tmpl
                if plugin_type == "role":
                    plugin_type_tmpl = role_tmpl
                for plugin_short_name, dummy_ in plugins.items():
                    plugin_name = ".".join((collection_name, plugin_short_name))
                    writers.append(
                        await pool.spawn(
                            write_plugin_rst(
                                collection_name,
                                collection_metadata[collection_name],
                                link_data[collection_name],
                                plugin_short_name,
                                plugin_type,
                                plugin_info[plugin_type].get(plugin_name),
                                nonfatal_errors[plugin_type][plugin_name],
                                plugin_type_tmpl,
                                error_tmpl,
                                dest_dir,
                                output_format,
                                filename_generator,
                                squash_hierarchy=squash_hierarchy,
                                use_html_blobs=use_html_blobs,
                                for_official_docsite=for_official_docsite,
                            )
                        )
                    )

        # Write docs for each plugin
        await asyncio.gather(*writers)
