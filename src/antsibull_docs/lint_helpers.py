# coding: utf-8
# Author: Felix Fontein <felix@fontein.de>
# License: GPLv3+
# Copyright: Ansible Project, 2022
"""Lint plugin docs."""

import json
import os
import os.path

from antsibull_core.yaml import load_yaml_file


def load_collection_name(path_to_collection: str) -> str:
    '''Load collection name (namespace.name) from collection's galaxy.yml.'''
    manifest_json_path = os.path.join(path_to_collection, 'MANIFEST.json')
    if os.path.isfile(manifest_json_path):
        with open(manifest_json_path, 'rb') as f:
            manifest_json = json.load(f)
        # pylint:disable-next=consider-using-f-string
        collection_name = '{namespace}.{name}'.format(**manifest_json['collection_info'])
        return collection_name

    galaxy_yml_path = os.path.join(path_to_collection, 'galaxy.yml')
    if os.path.isfile(galaxy_yml_path):
        galaxy_yml = load_yaml_file(galaxy_yml_path)
        # pylint:disable-next=consider-using-f-string
        collection_name = '{namespace}.{name}'.format(**galaxy_yml)
        return collection_name

    raise Exception(f'Cannot find files {manifest_json_path} and {galaxy_yml_path}')
