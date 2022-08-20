# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Helper to transform collection names based on a dictionary."""

import typing as t


class CollectionNameTransformer:
    """Helper to transform collection names based on a dictionary."""

    def __init__(self, data: t.Mapping[str, str], default_transform: str):
        """Create a collection name transformer.

        :arg data: Maps collection names (with wildcards) to transformation strings.
        :arg default_transform: If no entry in ``data`` is found for some collection name,
            this transormation is used as a fallback.

        Transformation strings must be regular `Python format strings
        <https://docs.python.org/3.8/library/string.html#formatstrings>`_ and are passed
        the parameters ``namespace`` and ``name`` extracted from the collection name.

        The keys of ``data`` are colletion names of the form ``<namespace>.<name>``.
        One of ``<namespace>`` and ``<name>`` can be replaced by ``*`` to match all
        collections with that name respectively namespace. The special key ``*`` matches
        all collections that are not covered by other rules. If a collection name is matched
        both by a wildcard for the namespace and a wildcard for the name, the transform for
        the wildcard in the name is preferred.
        """
        self._data = data
        self._default_transform = default_transform

    def __call__(self, collection_name: str) -> str:
        """Transform the given collection name."""
        parts = collection_name.split('.', 1)
        if len(parts) < 2:
            raise Exception(
                f'Collection name must have at least one period; {collection_name!r} has not')
        namespace, name = parts
        if collection_name in self._data:
            transform = self._data[collection_name]
        elif f'{namespace}.*' in self._data:
            transform = self._data[f'{namespace}.*']
        elif f'*.{name}' in self._data:
            transform = self._data[f'*.{name}']
        elif '*' in self._data:
            transform = self._data['*']
        else:
            transform = self._default_transform
        return transform.format(namespace=namespace, name=name)
