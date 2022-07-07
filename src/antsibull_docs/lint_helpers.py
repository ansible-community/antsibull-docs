# coding: utf-8
# Author: Felix Fontein <felix@fontein.de>
# License: GPLv3+
# Copyright: Ansible Project, 2022
"""Lint plugin docs."""

import json
import os
import os.path
import typing as t

from antsibull_core.yaml import load_yaml_file


def load_collection_info(path_to_collection: str) -> t.Dict[str, t.Any]:
    '''Load collection name (namespace.name) from collection's galaxy.yml.'''
    manifest_json_path = os.path.join(path_to_collection, 'MANIFEST.json')
    if os.path.isfile(manifest_json_path):
        with open(manifest_json_path, 'rb') as f:
            manifest_json = json.load(f)
        return manifest_json['collection_info']

    galaxy_yml_path = os.path.join(path_to_collection, 'galaxy.yml')
    if os.path.isfile(galaxy_yml_path):
        galaxy_yml = load_yaml_file(galaxy_yml_path)
        return galaxy_yml

    raise Exception(f'Cannot find files {manifest_json_path} and {galaxy_yml_path}')


def load_collection_name(path_to_collection: str) -> str:
    '''Load collection name (namespace.name) from collection's galaxy.yml.'''
    info = load_collection_info(path_to_collection)
    # pylint:disable-next=consider-using-f-string
    collection_name = '{namespace}.{name}'.format(**info)
    return collection_name
