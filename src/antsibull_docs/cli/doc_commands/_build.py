# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Utilities for various docs build subcommands."""

from __future__ import annotations

import asyncio
import textwrap

from antsibull_core.logging import log
from antsibull_core.venv import FakeVenvRunner, VenvRunner

from ... import app_context
from ...augment_docs import augment_docs
from ...collection_links import load_collections_links
from ...docs_parsing.parsing import get_ansible_plugin_info
from ...docs_parsing.routing import (
    find_stubs,
    load_all_collection_routing,
    remove_redirect_duplicates,
)
from ...env_variables import (
    collect_referenced_environment_variables,
    load_ansible_config,
)
from ...extra_docs import load_collections_extra_docs
from ...process_docs import (
    get_callback_plugin_contents,
    get_collection_contents,
    get_collection_namespaces,
    get_plugin_contents,
    normalize_all_plugin_info,
)
from ...utils.collection_name_transformer import CollectionNameTransformer
from ...write_docs.collections import output_extra_docs, output_indexes
from ...write_docs.hierarchy import (
    output_collection_index,
    output_collection_namespace_indexes,
)
from ...write_docs.indexes import (
    output_callback_indexes,
    output_environment_variables,
    output_plugin_indexes,
)
from ...write_docs.plugin_stubs import output_all_plugin_stub_rst
from ...write_docs.plugins import output_all_plugin_rst

mlog = log.fields(mod=__name__)


def generate_docs_for_all_collections(
    venv: VenvRunner | FakeVenvRunner,
    collection_dir: str | None,
    dest_dir: str,
    collection_names: list[str] | None = None,
    create_indexes: bool = True,
    squash_hierarchy: bool = False,
    breadcrumbs: bool = True,
    use_html_blobs: bool = False,
    fail_on_error: bool = False,
    for_official_docsite: bool = False,
) -> int:
    """
    Create documentation for a set of installed collections.

    :arg venv: The venv in which ansible-core is installed.
    :arg collection_dir: The directory in which the collections have been installed.
                         If ``None``, the collections are assumed to be in the current
                         search path for Ansible.
    :arg dest_dir: The directory into which the documentation is written.
    :kwarg collection_names: Optional list of collection names. If specified, only documentation
                             for these collections will be collected and generated.
    :kwarg create_indexes: Whether to create the collection, namespace, and plugin indexes. By
                           default, they are created.
    :kwarg squash_hierarchy: If set to ``True``, no directory hierarchy will be used.
                             Undefined behavior if documentation for multiple collections are
                             created.
    :kwarg breadcrumbs: Default True.  Set to False if breadcrumbs for collections should be
        disabled.  This will disable breadcrumbs but save on memory usage.
    :kwarg use_html_blobs: Default False.  Set to True if HTML blobs should be used instead of
        RST tables for parameter and return value tables.
    :kwarg fail_on_error: Default False.  Set to True to fail on loading or schema validation
        errors, instead of generating error pages.
    :kwarg for_official_docsite: Default False.  Set to True to use wording specific for the
        official docsite on docs.ansible.com.
    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func="generate_docs_for_all_collections")
    flog.notice("Begin")

    app_ctx = app_context.app_ctx.get()

    # Get the info from the plugins
    plugin_info, full_collection_metadata = asyncio.run(
        get_ansible_plugin_info(venv, collection_dir, collection_names=collection_names)
    )
    flog.notice("Finished parsing info from plugins and collections")
    # flog.fields(plugin_info=plugin_info).debug('Plugin data')
    # flog.fields(
    #     collection_metadata=full_collection_metadata).debug('Collection metadata')

    collection_metadata = dict(full_collection_metadata)
    if collection_names is not None and "ansible.builtin" not in collection_names:
        del collection_metadata["ansible.builtin"]

    # Load collection routing information
    collection_routing = asyncio.run(load_all_collection_routing(collection_metadata))
    flog.notice("Finished loading collection routing information")
    # flog.fields(collection_routing=collection_routing).debug('Collection routing infos')

    remove_redirect_duplicates(plugin_info, collection_routing)
    stubs_info = find_stubs(plugin_info, collection_routing)
    # flog.fields(stubs_info=stubs_info).debug('Stubs info')

    new_plugin_info, nonfatal_errors = asyncio.run(
        normalize_all_plugin_info(plugin_info)
    )
    flog.fields(errors=len(nonfatal_errors)).notice("Finished data validation")
    augment_docs(new_plugin_info)
    flog.notice("Finished calculating new data")

    # Load collection extra docs data
    extra_docs_data = asyncio.run(
        load_collections_extra_docs(
            {name: data.path for name, data in collection_metadata.items()}
        )
    )
    flog.debug("Finished getting collection extra docs data")

    # Load collection links data
    link_data = asyncio.run(
        load_collections_links(
            {name: data.path for name, data in collection_metadata.items()}
        )
    )
    flog.debug("Finished getting collection link data")

    plugin_contents = get_plugin_contents(new_plugin_info, nonfatal_errors)
    callback_plugin_contents = get_callback_plugin_contents(new_plugin_info)
    collection_to_plugin_info = get_collection_contents(plugin_contents)
    # Make sure collections without documentable plugins are mentioned
    for collection in collection_metadata:
        collection_to_plugin_info[collection]  # pylint:disable=pointless-statement
    flog.debug("Finished getting collection data")

    # Fail on errors
    if fail_on_error and nonfatal_errors:
        print("Found errors in some modules or plugins:")
        for plugin_type, plugins in sorted(nonfatal_errors.items()):
            for plugin_name, errors in sorted(plugins.items()):
                for error in errors:
                    print(
                        f"{plugin_name} {plugin_type}: {textwrap.indent(error, '    ').lstrip()}"
                    )
        return 1

    # Handle environment variables
    ansible_config = load_ansible_config(full_collection_metadata["ansible.builtin"])
    referenced_env_vars = collect_referenced_environment_variables(
        new_plugin_info, ansible_config
    )

    collection_namespaces = get_collection_namespaces(collection_to_plugin_info.keys())

    collection_url = CollectionNameTransformer(
        app_ctx.collection_url, "https://galaxy.ansible.com/{namespace}/{name}"
    )
    collection_install = CollectionNameTransformer(
        app_ctx.collection_install,
        "ansible-galaxy collection install {namespace}.{name}",
    )

    # Only build top-level index if requested
    if create_indexes:
        asyncio.run(
            output_collection_index(
                collection_to_plugin_info,
                collection_namespaces,
                dest_dir,
                collection_url=collection_url,
                collection_install=collection_install,
                breadcrumbs=breadcrumbs,
                for_official_docsite=for_official_docsite,
            )
        )
        flog.notice("Finished writing collection index")
        asyncio.run(
            output_collection_namespace_indexes(
                collection_namespaces,
                dest_dir,
                collection_url=collection_url,
                collection_install=collection_install,
                breadcrumbs=breadcrumbs,
                for_official_docsite=for_official_docsite,
            )
        )
        flog.notice("Finished writing collection namespace index")
        asyncio.run(
            output_plugin_indexes(
                plugin_contents,
                collection_metadata,
                dest_dir,
                collection_url=collection_url,
                collection_install=collection_install,
                for_official_docsite=for_official_docsite,
            )
        )
        flog.notice("Finished writing plugin indexes")
        asyncio.run(
            output_callback_indexes(
                callback_plugin_contents,
                dest_dir,
                collection_url=collection_url,
                collection_install=collection_install,
                for_official_docsite=for_official_docsite,
            )
        )
        flog.notice("Finished writing callback plugin indexes")

    asyncio.run(
        output_indexes(
            collection_to_plugin_info,
            dest_dir,
            collection_url=collection_url,
            collection_install=collection_install,
            collection_metadata=collection_metadata,
            squash_hierarchy=squash_hierarchy,
            extra_docs_data=extra_docs_data,
            link_data=link_data,
            breadcrumbs=breadcrumbs,
            for_official_docsite=for_official_docsite,
        )
    )
    flog.notice("Finished writing indexes")

    asyncio.run(
        output_all_plugin_stub_rst(
            stubs_info,
            dest_dir,
            collection_url=collection_url,
            collection_install=collection_install,
            collection_metadata=collection_metadata,
            link_data=link_data,
            squash_hierarchy=squash_hierarchy,
            for_official_docsite=for_official_docsite,
        )
    )
    flog.debug("Finished writing plugin stubs")

    asyncio.run(
        output_all_plugin_rst(
            collection_to_plugin_info,
            new_plugin_info,
            nonfatal_errors,
            dest_dir,
            collection_url=collection_url,
            collection_install=collection_install,
            collection_metadata=collection_metadata,
            link_data=link_data,
            squash_hierarchy=squash_hierarchy,
            use_html_blobs=use_html_blobs,
            for_official_docsite=for_official_docsite,
        )
    )
    flog.debug("Finished writing plugin docs")

    asyncio.run(
        output_extra_docs(dest_dir, extra_docs_data, squash_hierarchy=squash_hierarchy)
    )
    flog.debug("Finished writing extra docs")

    asyncio.run(
        output_environment_variables(
            dest_dir, referenced_env_vars, squash_hierarchy=squash_hierarchy
        )
    )
    flog.debug("Finished writing environment variables")
    return 0
