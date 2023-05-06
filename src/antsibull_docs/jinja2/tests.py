# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2019, Ansible Project
"""Jinja2 tests for use in Ansible documentation."""

from __future__ import annotations

import typing as t
import warnings
from functools import partial

from antsibull_core.vendored.collections import is_sequence
from packaging.version import Version as PypiVer
from semantic_version import Version as SemVer

# The following dictionary maps collection names to cut-off versions. If a version of such a
# collection is mentioned as when a feature was added that is older than the cut-off version,
# we do not print the version.
TOO_OLD_TO_BE_NOTABLE = {
    "ansible.builtin": "2.7",
}

test_list: t.Callable[[t.Any], bool] = partial(is_sequence, include_strings=False)


def still_relevant(version, collection=None):
    """
    Calculates whether the given version is older than a cutoff value

    :arg version: Version to check
    :returns: False if the `version` is older than the cutoff version, otherwise True.

    .. note:: This is similar to the ansible `version_compare` test but needs to handle the
        `historical` version and empty version.
    """
    # Note: This was the opposite in previous code but then the version_added was stripped out by
    # other things
    if not version:
        return False

    if version == "historical":
        return False

    cutoff = TOO_OLD_TO_BE_NOTABLE.get(collection)
    if cutoff is None:
        # If we do not have a cut-off version for the collection, we simply declare it to be
        # still relevant
        return True

    if collection == "ansible.builtin":
        Version = PypiVer
    else:
        Version = SemVer

    try:
        version = Version(version)
    except ValueError as e:
        warnings.warn(f"Could not parse {version}: {e}")
        return True
    try:
        return version >= Version(cutoff)
    except Exception as e:  # pylint:disable=broad-except
        warnings.warn(f"Could not compare {version}: {e}")
        return True
