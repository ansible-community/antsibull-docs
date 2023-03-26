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
from collections.abc import Sequence

import sh
from antsibull_core.compat import asyncio_run
from antsibull_core.venv import FakeVenvRunner

from sphinx_antsibull_ext import roles as antsibull_roles

from .augment_docs import augment_docs
from .cli.doc_commands.stable import (
    get_collection_contents,
    get_plugin_contents,
    normalize_all_plugin_info,
)
from .collection_links import load_collections_links
from .docs_parsing.ansible_doc import parse_ansible_galaxy_collection_list
from .docs_parsing.parsing import get_ansible_plugin_info
from .docs_parsing.routing import load_all_collection_routing, remove_redirect_duplicates
from .jinja2.environment import doc_environment
from .lint_helpers import load_collection_info
from .markup import dom
from .markup.parser import Context as ParserContext
from .markup.parser import parse as parse_markup
from .rstcheck import check_rst_content
from .utils.collection_name_transformer import CollectionNameTransformer
from .write_docs.plugins import create_plugin_rst, guess_relative_filename, has_broken_docs


class CollectionCopier:
    dir: t.Optional[str]

    def __init__(self):
        self.dir = None

    def __enter__(self):
        if self.dir is not None:
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


class _MarkupValidator:
    errors: t.List[str]
    context: ParserContext

    def _validate_markup_entry(self, entry: t.Union[str, t.Sequence[str]], key: str) -> None:
        parsed_paragraphs = parse_markup(
            entry,
            self.context,
            errors='message',
            only_classic_markup=False,
        )
        for paragraph in parsed_paragraphs:
            for par_elem in paragraph:
                if par_elem.type == dom.PartType.ERROR:
                    error_elem = t.cast(dom.ErrorPart, par_elem)
                    self.errors.append(f'Markup error in {key}: {error_elem.message}')

    def _validate_markup_dict_entry(self, dictionary: t.Dict[str, t.Any],
                                    key: str, key_path: str) -> None:
        value = dictionary.get(key)
        if value is None:
            return
        full_key = f'{key_path} -> {key}'
        if isinstance(value, str):
            self._validate_markup_entry(value, full_key)
        elif isinstance(value, Sequence):
            all_strings = True
            for index, entry in enumerate(value):
                if not isinstance(entry, str):
                    self.errors.append(
                        f'Expected {full_key} to be a list of strings; the {index + 1}-th'
                        f' entry is of type {type(value)} instead'
                    )
                    all_strings = False
            if all_strings:
                self._validate_markup_entry(value, full_key)
        else:
            self.errors.append(
                f'Expected {full_key} to be a string or list of strings, but got {type(value)}')

    def _validate_deprecation(self, owner: t.Dict[str, t.Any], key_path: str) -> None:
        if 'deprecated' not in owner:
            return
        key_path = f'{key_path} -> deprecated'
        deprecated = owner['deprecated']
        self._validate_markup_dict_entry(deprecated, 'why', key_path)
        self._validate_markup_dict_entry(deprecated, 'alternative', key_path)

    def _validate_options(self, options: t.Dict[str, t.Any], key_path: str) -> None:
        for opt, data in sorted(options.items()):
            opt_key = f'{key_path} -> {opt}'
            self._validate_markup_dict_entry(data, 'description', opt_key)
            self._validate_deprecation(data, opt_key)
            for sub in ('cli', 'env', 'ini', 'vars', 'keyword'):
                if sub in data:
                    for index, sub_data in enumerate(data['sub']):
                        sub_key = f'{opt_key} -> {sub}[{index + 1}]'
                        self._validate_deprecation(sub_data, sub_key)
            if 'suboptions' in data:
                self._validate_options(data['suboptions'], f'{opt_key} -> suboptions')

    def _validate_return_values(self, return_values: t.Dict[str, t.Any], key_path: str) -> None:
        for rv, data in sorted(return_values.items()):
            rv_key = f'{key_path} -> {rv}'
            self._validate_markup_dict_entry(data, 'description', rv_key)
            self._validate_markup_dict_entry(data, 'returned', rv_key)
            if 'contains' in data:
                self._validate_return_values(data['contains'], f'{rv_key} -> contains')

    def _validate_seealso(self, owner: t.Dict[str, t.Any], key_path: str) -> None:
        if 'seealso' not in owner:
            return
        key_path = f'{key_path} -> seealso'
        seealso = owner['seealso']
        for index, entry in enumerate(seealso):
            entry_path = f'{key_path}[{index + 1}]'
            self._validate_markup_dict_entry(entry, 'description', entry_path)
            self._validate_markup_dict_entry(entry, 'name', entry_path)

    def _validate_attributes(self, owner: t.Dict[str, t.Any], key_path: str) -> None:
        if 'attributes' not in owner:
            return
        key_path = f'{key_path} -> attributes'
        attributes = owner['attributes']
        for attribute, data in sorted(attributes.items()):
            attribute_path = f'{key_path} -> {attribute}'
            self._validate_markup_dict_entry(data, 'description', attribute_path)
            self._validate_markup_dict_entry(data, 'details', attribute_path)

    def _validate_main(self, main: t.Dict[str, t.Any], key_path: str) -> None:
        self._validate_deprecation(main, key_path)
        self._validate_markup_dict_entry(main, 'short_description', key_path)
        self._validate_markup_dict_entry(main, 'author', key_path)
        self._validate_markup_dict_entry(main, 'description', key_path)
        self._validate_markup_dict_entry(main, 'notes', key_path)
        self._validate_markup_dict_entry(main, 'requirements', key_path)
        self._validate_markup_dict_entry(main, 'todo', key_path)
        self._validate_seealso(main, key_path)
        self._validate_attributes(main, key_path)

    def __init__(self, plugin_record: t.Dict[str, t.Any], plugin_fqcn: str, plugin_type: str):
        self.context = ParserContext(
            current_plugin=dom.PluginIdentifier(fqcn=plugin_fqcn, type=plugin_type),
        )
        self.errors = []
        if 'doc' in plugin_record:
            self._validate_main(plugin_record['doc'], 'DOCUMENTATION')
        if 'return' in plugin_record:
            self._validate_return_values(plugin_record['return'], 'RETURN')
        if 'entry_points' in plugin_record:
            for entry_point, data in sorted(plugin_record['entry_points'].items()):
                self._validate_main(data, f'argument_specs -> {entry_point}')


def _validate_markup(plugin_record: t.Dict[str, t.Any],
                     plugin_fqcn: str, plugin_type: str, path: str
                     ) -> t.List[t.Tuple[str, int, int, str]]:
    validator = _MarkupValidator(plugin_record, plugin_fqcn, plugin_type)
    return [(path, 0, 0, msg) for msg in validator.errors]


def _lint_collection_plugin_docs(collections_dir: str, collection_name: str,
                                 original_path_to_collection: str,
                                 collection_url: CollectionNameTransformer,
                                 collection_install: CollectionNameTransformer,
                                 skip_rstcheck: bool,
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

    result = []
    for collection_name_, plugins_by_type in collection_to_plugin_info.items():
        for plugin_type, plugins_dict in plugins_by_type.items():
            plugin_type_tmpl = plugin_tmpl
            if plugin_type == 'role':
                plugin_type_tmpl = role_tmpl
            for plugin_short_name, dummy_ in plugins_dict.items():
                plugin_name = '.'.join((collection_name_, plugin_short_name))
                plugin_record = new_plugin_info[plugin_type].get(plugin_name) or {}
                filename = os.path.join(
                    original_path_to_collection,
                    guess_relative_filename(
                        plugin_record,
                        plugin_short_name,
                        plugin_type,
                        collection_name_,
                        collection_metadata[collection_name_]))
                path = os.path.join(
                    original_path_to_collection, 'plugins', plugin_type,
                    f'{plugin_short_name}.rst')
                if has_broken_docs(plugin_record, plugin_type):
                    result.append((filename, 0, 0, 'Did not return correct DOCUMENTATION'))
                else:
                    result.extend(_validate_markup(plugin_record, plugin_name, plugin_type, path))
                for error in nonfatal_errors[plugin_type][plugin_name]:
                    result.append((filename, 0, 0, error))
                rst_content = create_plugin_rst(
                    collection_name_,
                    collection_metadata[collection_name_],
                    link_data[collection_name_],
                    plugin_short_name,
                    plugin_type,
                    plugin_record,
                    nonfatal_errors[plugin_type][plugin_name],
                    plugin_type_tmpl, error_tmpl,
                    use_html_blobs=False,
                    log_errors=False,
                )
                if not skip_rstcheck:
                    rst_results = check_rst_content(
                        rst_content, filename=path,
                        ignore_directives=['rst-class'],
                        ignore_roles=list(antsibull_roles.ROLES),
                    )
                    result.extend([
                        (path, result[0], result[1], result[2]) for result in rst_results
                    ])
    return result


def lint_collection_plugin_docs(path_to_collection: str,
                                collection_url: CollectionNameTransformer,
                                collection_install: CollectionNameTransformer,
                                skip_rstcheck: bool = False,
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
            collection_install=collection_install,
            skip_rstcheck=skip_rstcheck))
    return result
