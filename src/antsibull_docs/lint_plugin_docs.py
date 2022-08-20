# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Lint plugin docs."""

import os
import shutil
import tempfile
import typing as t

import sh

from antsibull_core.compat import asyncio_run
from antsibull_core.venv import FakeVenvRunner

from .lint_helpers import (
    load_collection_info,
)

from .docs_parsing.ansible_doc import (
    parse_ansible_galaxy_collection_list,
)

from .augment_docs import augment_docs
from .cli.doc_commands.stable import (
    normalize_all_plugin_info,
    get_plugin_contents,
    get_collection_contents,
)
from .collection_links import load_collections_links
from .docs_parsing.parsing import get_ansible_plugin_info
from .docs_parsing.routing import (
    load_all_collection_routing,
    remove_redirect_duplicates,
)
from .jinja2.environment import doc_environment
from .utils.collection_name_transformer import CollectionNameTransformer
from .write_docs import create_plugin_rst
from .rstcheck import check_rst_content


class CollectionCopier:
    dir: t.Optional[str]

    def __init__(self):
        self.dir = None

    def __enter__(self):
        if self.dir is None:
            raise AssertionError('Collection copier already initialized')
        self.dir = os.path.realpath(tempfile.mkdtemp(prefix='antsibull-docs-'))
        return self

    def add_collection(self, collecion_source_path: str, namespace: str, name: str) -> None:
        self_dir = self.dir
        if self_dir is None:
            raise AssertionError('Collection copier not initialized')
        collection_container_dir = os.path.join(
            self_dir, 'ansible_collections', namespace)
        os.makedirs(collection_container_dir, exist_ok=True)

        collection_dir = os.path.join(collection_container_dir, name)
        shutil.copytree(collecion_source_path, collection_dir, symlinks=True)

    def __exit__(self, type_, value, traceback_):
        self_dir = self.dir
        if self_dir is None:
            raise AssertionError('Collection copier not initialized')
        shutil.rmtree(self_dir, ignore_errors=True)
        self.dir = None


class CollectionFinder:
    def __init__(self):
        self.collections = {}
        stdout = sh.Command('ansible-galaxy')('collection', 'list').stdout
        raw_output = stdout.decode('utf-8', errors='surrogateescape')
        for namespace, name, path, _ in reversed(parse_ansible_galaxy_collection_list(raw_output)):
            self.collections[f'{namespace}.{name}'] = path

    def find(self, namespace, name):
        return self.collections.get(f'{namespace}.{name}')


def _lint_collection_plugin_docs(collections_dir: str, collection_name: str,
                                 original_path_to_collection: str,
                                 collection_url: CollectionNameTransformer,
                                 collection_install: CollectionNameTransformer,
                                 ) -> t.List[t.Tuple[str, int, int, str]]:
    # Load collection docs
    venv = FakeVenvRunner()
    plugin_info, collection_metadata = asyncio_run(get_ansible_plugin_info(
        venv, collections_dir, collection_names=[collection_name]))
    # Load routing information
    collection_routing = asyncio_run(load_all_collection_routing(collection_metadata))
    # Process data
    remove_redirect_duplicates(plugin_info, collection_routing)
    new_plugin_info, nonfatal_errors = asyncio_run(normalize_all_plugin_info(plugin_info))
    augment_docs(new_plugin_info)
    # Load link data
    link_data = asyncio_run(load_collections_links(
        {name: data.path for name, data in collection_metadata.items()}))
    # More processing
    plugin_contents = get_plugin_contents(new_plugin_info, nonfatal_errors)
    collection_to_plugin_info = get_collection_contents(plugin_contents)
    for collection in collection_metadata:
        collection_to_plugin_info[collection]  # pylint:disable=pointless-statement
    # Collect non-fatal errors
    result = []
    for plugin_type, plugins in sorted(nonfatal_errors.items()):
        for plugin_name, errors in sorted(plugins.items()):
            for error in errors:
                result.append((
                    os.path.join(original_path_to_collection, 'plugins', plugin_type, plugin_name),
                    0,
                    0,
                    error,
                ))
    # Compose RST files and check for errors
    # Setup the jinja environment
    env = doc_environment(
        ('antsibull_docs.data', 'docsite'),
        collection_url=collection_url,
        collection_install=collection_install)
    # Get the templates
    plugin_tmpl = env.get_template('plugin.rst.j2')
    role_tmpl = env.get_template('role.rst.j2')
    error_tmpl = env.get_template('plugin-error.rst.j2')

    for collection_name_, plugins_by_type in collection_to_plugin_info.items():
        for plugin_type, plugins_dict in plugins_by_type.items():
            plugin_type_tmpl = plugin_tmpl
            if plugin_type == 'role':
                plugin_type_tmpl = role_tmpl
            for plugin_short_name, dummy_ in plugins_dict.items():
                plugin_name = '.'.join((collection_name_, plugin_short_name))
                rst_content = create_plugin_rst(
                    collection_name_, collection_metadata[collection_name_],
                    link_data[collection_name_],
                    plugin_short_name, plugin_type,
                    new_plugin_info[plugin_type].get(plugin_name) or {},
                    nonfatal_errors[plugin_type][plugin_name],
                    plugin_type_tmpl, error_tmpl,
                    use_html_blobs=False,
                )
                path = os.path.join(
                    original_path_to_collection, 'plugins', plugin_type,
                    f'{plugin_short_name}.rst')
                rst_results = check_rst_content(
                    rst_content, filename=path,
                    ignore_directives=['rst-class'],
                )
                result.extend([(path, result[0], result[1], result[2]) for result in rst_results])
    return result


def lint_collection_plugin_docs(path_to_collection: str,
                                collection_url: CollectionNameTransformer,
                                collection_install: CollectionNameTransformer,
                                ) -> t.List[t.Tuple[str, int, int, str]]:
    try:
        info = load_collection_info(path_to_collection)
        namespace = info['namespace']
        name = info['name']
        dependencies = info.get('dependencies') or {}
    except Exception:  # pylint:disable=broad-except
        return [(
            path_to_collection, 0, 0,
            'Cannot identify collection with galaxy.yml or MANIFEST.json at this path')]
    result = []
    collection_name = f'{namespace}.{name}'
    done_dependencies = {collection_name}
    dependencies = sorted(dependencies)
    with CollectionCopier() as copier:
        # Copy collection
        copier.add_collection(path_to_collection, namespace, name)
        # Copy all dependencies
        if dependencies:
            collection_finder = CollectionFinder()
            while dependencies:
                dependency = dependencies.pop(0)
                if dependency in done_dependencies:
                    continue
                dep_namespace, dep_name = dependency.split('.', 2)
                dep_collection_path = collection_finder.find(dep_namespace, dep_name)
                if dep_collection_path:
                    copier.add_collection(dep_collection_path, dep_namespace, dep_name)
                    try:
                        info = load_collection_info(dep_collection_path)
                        dependencies.extend(sorted(info.get('dependencies') or {}))
                    except Exception:  # pylint:disable=broad-except
                        result.append((
                            dep_collection_path, 0, 0,
                            'Cannot identify collection with galaxy.yml or MANIFEST.json'
                            ' at this path'))
        # Load docs
        result.extend(_lint_collection_plugin_docs(
            copier.dir, collection_name, path_to_collection,
            collection_url=collection_url,
            collection_install=collection_install))
    return result
