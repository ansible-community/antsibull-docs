# coding: utf-8
# Author: Felix Fontein <felix@fontein.de>
# License: GPLv3+
# Copyright: Ansible Project, 2022
"""Lint plugin docs."""

import typing as t

from .lint_helpers import (
    load_collection_name,
)


def lint_collection_plugin_docs(path_to_collection: str) -> t.List[t.Tuple[str, int, int, str]]:
    try:
        namespace, name = load_collection_name(path_to_collection).split('.', 1)
    except Exception:  # pylint:disable=broad-except
        return [(
            path_to_collection, 0, 0,
            'Cannot identify collection with galaxy.yml or MANIFEST.json at this path')]
    result = []
    # TODO
    return result
