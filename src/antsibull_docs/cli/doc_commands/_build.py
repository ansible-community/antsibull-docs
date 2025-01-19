# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Utilities for various docs build subcommands."""

from __future__ import annotations

import asyncio
import os
import sys
import textwrap
import typing as t
from collections.abc import Mapping, MutableMapping

from antsibull_core.logging import log
from antsibull_core.schemas.collection_meta import (
    CollectionMetadata,
    CollectionsMetadata,
    RemovalInformation,
)
from antsibull_core.venv import FakeVenvRunner, VenvRunner
from packaging.version import Version as PypiVer

from ... import app_context
from ...augment_docs import augment_docs
from ...collection_links import load_collections_links
from ...constants import DOCUMENTABLE_PLUGINS
from ...docs_parsing import AnsibleCollectionMetadata
from ...docs_parsing.parsing import get_ansible_plugin_info
from ...docs_parsing.routing import (
    find_stubs,
    load_all_collection_routing,
    remove_redirect_duplicates,
)
from ...env_variables import (
    collect_referable_envvars,
    collect_referenced_environment_variables,
    load_ansible_config,
)
from ...extra_docs import CollectionExtraDocsInfoT, load_collections_extra_docs
from ...jinja2 import FilenameGenerator, OutputFormat
from ...process_docs import (
    get_callback_plugin_contents,
    get_collection_contents,
    get_collection_namespaces,
    get_plugin_contents,
    normalize_all_plugin_info,
)
from ...schemas.app_context import (
    DEFAULT_COLLECTION_INSTALL_CMD,
    DEFAULT_COLLECTION_URL_TRANSFORM,
)
from ...utils.collection_name_transformer import CollectionNameTransformer
from ...write_docs import CollectionInfoT, _get_collection_dir
from ...write_docs.changelog import output_changelogs
from ...write_docs.collections import (
    output_collection_indexes,
    output_collection_tombstones,
    output_extra_docs,
)
from ...write_docs.hierarchy import (
    output_collection_index,
    output_collection_namespace_indexes,
)
from ...write_docs.indexes import (
    output_callback_indexes,
    output_environment_variables,
    output_plugin_indexes,
)
from ...write_docs.io import TrackingOutput
from ...write_docs.plugin_stubs import output_all_plugin_stub_rst
from ...write_docs.plugins import output_all_plugin_rst

mlog = log.fields(mod=__name__)


def _remove_collections_from_mapping(
    mapping: MutableMapping[str, t.Any],
    exclude_collection_names: list[str],
) -> None:
    for collection_name in exclude_collection_names:
        mapping.pop(collection_name, None)


def _remove_collections(
    plugin_info: MutableMapping[str, MutableMapping[str, t.Any]],
    collection_metadata: MutableMapping[str, AnsibleCollectionMetadata],
    exclude_collection_names: list[str],
) -> None:
    if not exclude_collection_names:
        return

    _remove_collections_from_mapping(collection_metadata, exclude_collection_names)

    prefixes = tuple(
        f"{collection_name}." for collection_name in exclude_collection_names
    )
    for _, plugin_data in plugin_info.items():
        plugins_to_remove = [
            plugin_name
            for plugin_name in plugin_data
            if plugin_name.startswith(prefixes)
        ]
        for plugin_name in plugins_to_remove:
            del plugin_data[plugin_name]


def _validate_options(
    collection_names: list[str] | None,
    exclude_collection_names: list[str] | None,
    use_html_blobs: bool,
    for_official_docsite: bool = False,
    ansible_version: PypiVer | None = None,
) -> None:
    if collection_names is not None and exclude_collection_names is not None:
        raise ValueError(
            "Cannot specify both collection_names and exclude_collection_names"
        )

    if use_html_blobs:
        print(
            "WARNING: the use of --use-html-blobs is deprecated."
            " This feature will be removed soon.",
            file=sys.stderr,
        )

    if ansible_version is not None and not for_official_docsite:
        raise AssertionError(
            "Ansible version cannot be provided if this is not for the official docsite"
        )


def _register_plugin_patterns(
    output: TrackingOutput,
    collection_to_plugin_info: CollectionInfoT,
    /,
    *,
    filename_generator: FilenameGenerator,
    output_format: OutputFormat,
    squash_hierarchy: bool,
) -> None:
    for collection_name in collection_to_plugin_info:
        namespace, collection = collection_name.split(".")
        collection_dir = _get_collection_dir(
            output,
            namespace,
            collection,
            squash_hierarchy=squash_hierarchy,
            create_if_not_exists=False,
        )
        for plugin_type in DOCUMENTABLE_PLUGINS:
            output.register_pattern(
                collection_dir,
                filename_generator.plugin_filename(
                    f"{collection_name}.*", plugin_type, output_format
                ),
            )


def _register_extra_docs(
    output: TrackingOutput,
    extra_docs_data: Mapping[str, CollectionExtraDocsInfoT],
    /,
    *,
    squash_hierarchy: bool,
) -> None:
    for collection_name, (dummy, documents) in extra_docs_data.items():
        namespace, collection = collection_name.split(".", 1)
        collection_dir = _get_collection_dir(
            output,
            namespace,
            collection,
            squash_hierarchy=squash_hierarchy,
            create_if_not_exists=False,
        )
        directories = {os.path.join(collection_dir, "docsite")}
        for _, rel_path in documents:
            directories.add(os.path.dirname(os.path.join(collection_dir, rel_path)))
        for directory in sorted(directories):
            output.register_pattern(directory, "*")


def _compose_redirect_sentence(
    collection: str,
    new_name: str,
    redirect_replacement_major_version: int,
    current_major_version: int | None,
) -> str:
    if (
        current_major_version is not None
        and current_major_version == redirect_replacement_major_version
    ):
        return (
            f"The content of {collection} has been replaced"
            f" by redirects to {new_name}"
            f" in this major release of Ansible."
        )
    if (
        current_major_version is not None
        and current_major_version > redirect_replacement_major_version
    ):
        return (
            f"The content of {collection} has been replaced"
            f" by redirects to {new_name}"
            f" in Ansible {redirect_replacement_major_version}."
        )
    return (
        f"The content of {collection} will be replaced"
        f" by redirects to {new_name}"
        f" in Ansible {redirect_replacement_major_version}."
    )


def _collect_removal_sentences(
    collection: str,
    removal: RemovalInformation,
    /,
    ansible_version: PypiVer | None,
    discussion_override: str | None = None,
    reason_override: str | None = None,
    reason_text_override: str | None = None,
) -> list[str]:
    sentences = []
    removed_text = (
        "will eventually be removed from Ansible"
        if removal.major_version == "TBD"
        else f"will be removed from Ansible {removal.major_version}"
    )

    discussion = discussion_override or removal.discussion
    reason = reason_override or removal.reason
    reason_text = reason_text_override or removal.reason_text

    if reason == "deprecated":
        sentences.append(
            f"The {collection} collection has been deprecated and {removed_text}."
        )
    if reason == "considered-unmaintained":
        sentences.append(
            f"The {collection} collection is considered unmaintained and {removed_text}."
        )
    if reason == "renamed":
        sentences.append(
            f"The {collection} collection has been renamed to"
            f" R({removal.new_name}, plugins_in_{removal.new_name})"
            f" and {removed_text}."
        )
        if removal.redirect_replacement_major_version is not None:
            sentences.append(
                _compose_redirect_sentence(
                    collection,
                    removal.new_name or "",
                    removal.redirect_replacement_major_version,
                    ansible_version.major if ansible_version is not None else None,
                )
            )
        sentences.append(
            f"If you use content from {collection},"
            " please update FQCNs in your playbooks and roles!"
        )
        sentences.append(
            "When creating new playbooks or roles,"
            f" directly use content from {removal.new_name} instead."
        )
    if reason == "guidelines-violation":
        sentences.append(
            f"The {collection} collection {removed_text}"
            " due to violations of the Ansible inclusion requirements."
        )
    if reason == "other":
        sentences.append(f"The {collection} collection {removed_text}.")

    if reason_text:
        sentences.append(reason_text)

    if reason not in ("renamed", "deprecated"):
        sentences.append(
            "Once removed, you can still install the collection manually"
            f" with C(ansible-galaxy collection install {collection})."
        )

    if sentences and discussion:
        sentences.append(
            f"See the L(discussion thread, {discussion}) for more information."
        )

    return sentences


def _compose_deprecation_info(
    collection: str,
    metadata: CollectionMetadata,
    ansible_version: PypiVer | None,
) -> str | None:
    removal = metadata.removal
    if removal is None or not removal.is_deprecated():
        return None

    discussion_override = None
    reason_override = None
    reason_text_override = None
    if removal.updates and (
        removal.updates[-1].deprecated_version
        or removal.updates[-1].redeprecated_version
    ):
        discussion_override = removal.updates[-1].discussion
        reason_override = removal.updates[-1].reason
        reason_text_override = removal.updates[-1].reason_text

    sentences = _collect_removal_sentences(
        collection,
        removal,
        ansible_version=ansible_version,
        discussion_override=discussion_override,
        reason_override=reason_override,
        reason_text_override=reason_text_override,
    )
    if not sentences:
        return None

    return "\n".join(sentences)


def _add_deprecation_info(
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
    collection_meta: CollectionsMetadata | None,
    ansible_version: PypiVer | None,
) -> None:
    if collection_meta is None:
        return

    for collection, metadata in collection_metadata.items():
        meta = collection_meta.get_meta(collection)
        metadata.deprecation_info = _compose_deprecation_info(
            collection, meta, ansible_version
        )
        if (
            meta.removal
            and meta.removal.is_deprecated()
            and meta.removal.major_version != "TBD"
        ):
            metadata.removal_ansible_major_version = meta.removal.major_version


def generate_docs_for_all_collections(  # noqa: C901
    venv: VenvRunner | FakeVenvRunner,
    collection_dir: str | None,
    dest_dir: str,
    output_format: OutputFormat,
    *,
    collection_names: list[str] | None = None,
    exclude_collection_names: list[str] | None = None,
    create_indexes: bool = True,
    create_collection_indexes: bool = True,
    add_extra_docs: bool = True,
    add_redirect_stubs: bool = True,
    squash_hierarchy: bool = False,
    breadcrumbs: bool = True,
    use_html_blobs: bool = False,
    fail_on_error: bool = False,
    for_official_docsite: bool = False,
    include_collection_name_in_plugins: bool = False,
    add_antsibull_docs_version: bool = True,
    cleanup: t.Literal[
        "no", "similar-files", "similar-files-and-dirs", "everything"
    ] = "no",
    collection_meta: CollectionsMetadata | None = None,
    ansible_version: PypiVer | None = None,
) -> int:
    """
    Create documentation for a set of installed collections.

    :arg venv: The venv in which ansible-core is installed.
    :arg collection_dir: The directory in which the collections have been installed.
                         If ``None``, the collections are assumed to be in the current
                         search path for Ansible.
    :arg dest_dir: The directory into which the documentation is written.
    :arg output_format: The output format.
    :kwarg collection_names: Optional list of collection names. If specified, only documentation
                             for these collections will be collected and generated.
    :kwarg exclude_collection_names: Optional list of collection names to skip. Mutually exclusive
                                     with ``collection_names``.
    :kwarg create_indexes: Whether to create the collection, namespace, and plugin indexes. By
                           default, they are created.
    :kwarg create_collection_indexes: Whether to create the per-collection plugin index and other
                                      global docs.
    :kwarg add_extra_docs: Whether to add extra docs.
    :kwarg add_redirect_stubs: Whether to create redirect stub files.
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
    :kwarg include_collection_name_in_plugins: Default False.  Set to True to use the FQCN for
        plugin files instead of only the part without the collection name.
    :kwarg add_antsibull_docs_version: Default True.  Set to False to not insert antsibull-docs'
        version into generated files.
    :kwarg collection_meta: Metadata on collections, if available.
    :kwarg ansible_version: The version of the Ansible build, if available.
    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func="generate_docs_for_all_collections")
    flog.notice("Begin")

    _validate_options(
        collection_names,
        exclude_collection_names,
        use_html_blobs,
        for_official_docsite,
        ansible_version,
    )

    if collection_names is not None and all(
        ab not in collection_names
        for ab in ("ansible.builtin", "ansible.*", "*.builtin", "*.*")
    ):
        exclude_collection_names = ["ansible.builtin"]

    app_ctx = app_context.app_ctx.get()

    # Get the info from the plugins
    plugin_info, full_collection_metadata = asyncio.run(
        get_ansible_plugin_info(venv, collection_dir, collection_names=collection_names)
    )
    flog.notice("Finished parsing info from plugins and collections")
    # flog.fields(plugin_info=plugin_info).debug('Plugin data')
    # flog.fields(
    #     collection_metadata=full_collection_metadata).debug('Collection metadata')

    _add_deprecation_info(full_collection_metadata, collection_meta, ansible_version)

    collection_metadata = dict(full_collection_metadata)
    _remove_collections(
        plugin_info, collection_metadata, exclude_collection_names or []
    )

    # Load collection routing information
    collection_routing = asyncio.run(load_all_collection_routing(collection_metadata))
    flog.notice("Finished loading collection routing information")
    # flog.fields(collection_routing=collection_routing).debug('Collection routing infos')

    remove_redirect_duplicates(plugin_info, collection_routing)
    stubs_info = find_stubs(plugin_info, collection_routing)
    _remove_collections_from_mapping(stubs_info, exclude_collection_names or [])
    # flog.fields(stubs_info=stubs_info).debug('Stubs info')

    new_plugin_info, nonfatal_errors = asyncio.run(
        normalize_all_plugin_info(plugin_info)
    )
    flog.fields(errors=len(nonfatal_errors)).notice("Finished data validation")
    augment_docs(new_plugin_info, collection_routing)
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
    referenced_env_vars, core_env_vars = collect_referenced_environment_variables(
        new_plugin_info, ansible_config
    )
    referable_envvars = collect_referable_envvars(
        referenced_env_vars, core_env_vars, collection_metadata
    )

    collection_namespaces = get_collection_namespaces(
        collection_to_plugin_info.keys(), collection_meta=collection_meta
    )

    collection_url = CollectionNameTransformer(
        app_ctx.collection_url, DEFAULT_COLLECTION_URL_TRANSFORM
    )
    collection_install = CollectionNameTransformer(
        app_ctx.collection_install,
        DEFAULT_COLLECTION_INSTALL_CMD,
    )

    filename_generator = FilenameGenerator(
        include_collection_name_in_plugins=include_collection_name_in_plugins
    )

    output = TrackingOutput(dest_dir)

    # Only build top-level index if requested
    if create_indexes:
        asyncio.run(
            output_collection_index(
                collection_to_plugin_info,
                collection_namespaces,
                collection_metadata,
                output,
                collection_url=collection_url,
                collection_install=collection_install,
                output_format=output_format,
                filename_generator=filename_generator,
                breadcrumbs=breadcrumbs,
                for_official_docsite=for_official_docsite,
                referable_envvars=referable_envvars,
                add_version=add_antsibull_docs_version,
            )
        )
        flog.notice("Finished writing collection index")
        asyncio.run(
            output_collection_namespace_indexes(
                collection_namespaces,
                collection_metadata,
                output,
                collection_url=collection_url,
                collection_install=collection_install,
                output_format=output_format,
                filename_generator=filename_generator,
                breadcrumbs=breadcrumbs,
                for_official_docsite=for_official_docsite,
                referable_envvars=referable_envvars,
                add_version=add_antsibull_docs_version,
            )
        )
        flog.notice("Finished writing collection namespace index")
        asyncio.run(
            output_plugin_indexes(
                plugin_contents,
                collection_metadata,
                output,
                collection_url=collection_url,
                collection_install=collection_install,
                output_format=output_format,
                filename_generator=filename_generator,
                for_official_docsite=for_official_docsite,
                referable_envvars=referable_envvars,
                add_version=add_antsibull_docs_version,
            )
        )
        output.register_pattern(
            "collections", f"index_*{output_format.output_extension}"
        )
        flog.notice("Finished writing plugin indexes")
        asyncio.run(
            output_callback_indexes(
                callback_plugin_contents,
                output,
                collection_url=collection_url,
                collection_install=collection_install,
                output_format=output_format,
                filename_generator=filename_generator,
                for_official_docsite=for_official_docsite,
                referable_envvars=referable_envvars,
                add_version=add_antsibull_docs_version,
            )
        )
        flog.notice("Finished writing callback plugin indexes")

    if create_collection_indexes:
        asyncio.run(
            output_collection_indexes(
                collection_to_plugin_info,
                output,
                collection_url=collection_url,
                collection_install=collection_install,
                collection_metadata=collection_metadata,
                squash_hierarchy=squash_hierarchy,
                extra_docs_data=extra_docs_data,
                link_data=link_data,
                output_format=output_format,
                filename_generator=filename_generator,
                breadcrumbs=breadcrumbs,
                for_official_docsite=for_official_docsite,
                referable_envvars=referable_envvars,
                add_version=add_antsibull_docs_version,
            )
        )
        flog.notice("Finished writing collection indexes")

        asyncio.run(
            output_collection_tombstones(
                collection_meta,
                output,
                collection_url=collection_url,
                collection_install=collection_install,
                squash_hierarchy=squash_hierarchy,
                output_format=output_format,
                filename_generator=filename_generator,
                breadcrumbs=breadcrumbs,
                for_official_docsite=for_official_docsite,
                add_version=add_antsibull_docs_version,
            )
        )
        flog.notice("Finished writing collection tombstones")

        asyncio.run(
            output_changelogs(
                collection_to_plugin_info,
                output,
                collection_metadata=collection_metadata,
                squash_hierarchy=squash_hierarchy,
                output_format=output_format,
            )
        )
        flog.notice("Finished writing indexes")

    if add_redirect_stubs:
        asyncio.run(
            output_all_plugin_stub_rst(
                stubs_info,
                output,
                collection_url=collection_url,
                collection_install=collection_install,
                collection_metadata=collection_metadata,
                link_data=link_data,
                output_format=output_format,
                filename_generator=filename_generator,
                squash_hierarchy=squash_hierarchy,
                for_official_docsite=for_official_docsite,
                referable_envvars=referable_envvars,
                add_version=add_antsibull_docs_version,
            )
        )
        flog.debug("Finished writing plugin stubs")

    asyncio.run(
        output_all_plugin_rst(
            collection_to_plugin_info,
            new_plugin_info,
            nonfatal_errors,
            output,
            collection_url=collection_url,
            collection_install=collection_install,
            collection_metadata=collection_metadata,
            link_data=link_data,
            output_format=output_format,
            filename_generator=filename_generator,
            squash_hierarchy=squash_hierarchy,
            use_html_blobs=use_html_blobs,
            for_official_docsite=for_official_docsite,
            referable_envvars=referable_envvars,
            add_version=add_antsibull_docs_version,
        )
    )
    flog.debug("Finished writing plugin docs")

    _register_plugin_patterns(
        output,
        collection_to_plugin_info,
        filename_generator=filename_generator,
        output_format=output_format,
        squash_hierarchy=squash_hierarchy,
    )

    if add_extra_docs:
        asyncio.run(
            output_extra_docs(
                output, extra_docs_data, squash_hierarchy=squash_hierarchy
            )
        )
        flog.debug("Finished writing extra docs")

        _register_extra_docs(output, extra_docs_data, squash_hierarchy=squash_hierarchy)

    if output_format == OutputFormat.ANSIBLE_DOCSITE:
        asyncio.run(
            output_environment_variables(
                output,
                referenced_env_vars,
                output_format=output_format,
                filename_generator=filename_generator,
                squash_hierarchy=squash_hierarchy,
                referable_envvars=referable_envvars,
                add_version=add_antsibull_docs_version,
            )
        )
        flog.debug("Finished writing environment variables")

    # Cleanup
    if cleanup != "no":
        output.cleanup("." if squash_hierarchy else "collections", cleanup)

    return 0
