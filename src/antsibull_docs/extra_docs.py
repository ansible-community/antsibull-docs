# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""Code for handling extra collection documentation in docs/docsite/."""

from __future__ import annotations

import asyncio
import os
import os.path
import re
import typing as t
from collections.abc import Mapping

import asyncio_pool  # type: ignore[import]
from antsibull_core import app_context
from antsibull_core.logging import log
from antsibull_fileutils.io import read_file
from antsibull_fileutils.yaml import load_yaml_file

mlog = log.fields(mod=__name__)

_RST_LABEL_DEFINITION = re.compile(r"""^\.\. _([^:]+):""")


class ExtraDocsIndexError(Exception):
    pass


class TocTreeEntry:
    ref: str
    title: str | None

    def __init__(self, ref: str, title: str | None = None):
        self.ref = ref
        self.title = title


class Section:
    title: str
    toctree: list[TocTreeEntry]

    def __init__(self, title: str, toctree: list[TocTreeEntry]):
        self.title = title
        self.toctree = toctree


#: A tuple consisting of a list of sections and a list of RST documents as tuples
#: (absolute path to source file, relative path in collection's docs directory).
CollectionExtraDocsInfoT = tuple[list[Section], list[tuple[str, str]]]


def find_extra_docs(path_to_collection: str) -> list[tuple[str, str]]:
    """Enumerate all extra docs RST files for a collection path.

    :arg path_to_collection: Path to a collection.
    :arg collection_name: Dotted collection name.
    :returns: A list of tuples (absolute path, relative path in docs/docsite/rst)
    """
    docs_dir = os.path.join(path_to_collection, "docs", "docsite", "rst")
    if not os.path.isdir(docs_dir):
        return []
    result = []
    for dirname, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".rst"):
                path = os.path.join(dirname, file)
                result.append((path, os.path.normpath(os.path.relpath(path, docs_dir))))
    return result


def get_label_prefix(collection_name: str) -> str:
    """Create RST label prefix for the given collection name.

    :arg collection_name: Dotted collection name.
    :returns: A RST label prefix
    """
    return f"ansible_collections.{collection_name}.docsite."


def lint_required_conditions(
    content: str, collection_name: str
) -> tuple[list[str], list[tuple[int, int, str]]]:
    """Check a extra docs RST file's content for whether it satisfied the required conditions.

    :arg content: Content of a RST document.
    :arg collection_name: Dotted collection name.
    :returns: A tuple consisting of a list of RST labels and a list of error messages
              (with line and column numbers).
    """
    labels: set[str] = set()
    errors: list[tuple[int, int, str]] = []
    label_prefix = get_label_prefix(collection_name)
    # Check label definitions
    for row, line in enumerate(content.splitlines()):
        m = _RST_LABEL_DEFINITION.match(line)
        if m:
            label = m.group(1)
            if not label.startswith(label_prefix):
                errors.append(
                    (
                        row + 1,
                        0,
                        f'Label "{label}" does not start with expected prefix "{label_prefix}"',
                    )
                )
            else:
                labels.add(label)
    return sorted(labels), errors


def _parse_toctree_entry(
    entry: dict[t.Any, t.Any], toctree_index: int, section_index: int
) -> tuple[TocTreeEntry | None, list[str]]:
    errors: list[str] = []
    toctree_entry: TocTreeEntry | None = None
    for key in ("ref",):
        if key not in entry:
            errors.append(
                f"Toctree entry #{toctree_index} in section #{section_index}"
                f' does not have a "{key}" entry'
            )
    for key, value in entry.items():
        if not isinstance(key, str) or not isinstance(value, str):
            errors.append(
                f"Toctree entry #{toctree_index} in section #{section_index}"
                f" must have strings for keys and values for all entries"
            )
    if not errors:
        toctree_entry = TocTreeEntry(entry["ref"], title=entry.get("title"))
    return toctree_entry, errors


def load_toctree(
    yaml_section: dict[str, t.Any], section_index: int = 0
) -> tuple[list[TocTreeEntry], list[str]]:
    errors: list[str] = []
    toctree: list[TocTreeEntry] = []
    if "toctree" in yaml_section:
        if not isinstance(yaml_section["toctree"], list):
            errors.append(f"Toctree entry in section #{section_index} is not a list")
            return toctree, errors

        for toctree_index, toctree_entry in enumerate(yaml_section["toctree"]):
            if isinstance(toctree_entry, str):
                toctree.append(TocTreeEntry(toctree_entry))
                continue
            if isinstance(toctree_entry, dict):
                toctree_entry_obj, toctree_entry_errors = _parse_toctree_entry(
                    toctree_entry, toctree_index, section_index
                )
                errors.extend(toctree_entry_errors)
                if toctree_entry_obj:
                    toctree.append(toctree_entry_obj)
                continue
            errors.append(
                f"Toctree entry #{toctree_index} in section #{section_index}"
                f" is neither a string nor a dictionary"
            )
            continue
    return toctree, errors


def load_section(
    yaml_section: dict[str, t.Any], section_index: int = 0
) -> tuple[Section | None, list[str]]:
    errors: list[str] = []
    missing = False
    for required_key in ("title",):
        if required_key not in yaml_section:
            errors.append(f'Section #{section_index} has no "{required_key}" entry')
            missing = True
    if missing:
        return None, errors
    toctree, toctree_errors = load_toctree(yaml_section, section_index)
    errors.extend(toctree_errors)
    if not toctree:
        errors.append(f"Section #{section_index} has no content")
        return None, errors
    return Section(yaml_section["title"], toctree), errors


def load_extra_docs_index(index_path: str) -> tuple[list[Section], list[str]]:
    """Load a collection's extra-docs.yml file.

    :arg index_path: Path to extra-docs.yml (does not need to exist).
    :returns: A tuple consisting of a list of sections and a list of error messages.
    :raises: ExtraDocsIndexError if extra-docs.yml does not exist
    """
    sections: list[Section] = []
    errors: list[str] = []

    if not os.path.isfile(index_path):
        raise ExtraDocsIndexError("extra-docs.yml does not exist")

    try:
        index = load_yaml_file(index_path)
        if index.get("sections"):
            for section_index, yaml_section in enumerate(index["sections"]):
                if not isinstance(yaml_section, dict):
                    errors.append(f"Section #{section_index} must be a mapping")
                    continue
                section, section_errors = load_section(yaml_section, section_index)
                if section is not None:
                    sections.append(section)
                errors.extend(section_errors)
    except Exception as exc:  # pylint:disable=broad-except
        errors.append(str(exc))

    return sections, errors


async def load_collection_extra_docs(
    collection_name: str, collection_path: str, path_prefix: str = "docsite"
) -> CollectionExtraDocsInfoT:
    """Given a collection name and collection metadata, load extra docs data.

    :arg collection_name: Dotted collection name.
    :arg collection_path: Path to the collection.
    :arg path_prefix: Prefix to add to relative paths, and toctree entries.
    :returns: A tuple consisting of a list of sections and a list of RST documents as tuples
              (relative path in docs/docsite/rst, content).
    """
    flog = mlog.fields(func="load_collection_extra_docs")
    flog.debug("Enter")

    index_path = os.path.join(collection_path, "docs", "docsite", "extra-docs.yml")
    try:
        sections, dummy = load_extra_docs_index(index_path)
    except ExtraDocsIndexError:
        sections = []

    for section in sections:
        for toctree in section.toctree:
            toctree.ref = f"{path_prefix}/{toctree.ref}"
    documents = []
    for abs_path, rel_path in find_extra_docs(collection_path):
        try:
            # Load content
            content = await read_file(abs_path, encoding="utf-8")

            # Lint content
            dummy, errors = lint_required_conditions(content, collection_name)

            # When no errors were found, add to output
            if not errors:
                documents.append((abs_path, os.path.join(path_prefix, rel_path)))
        except Exception:  # pylint:disable=broad-except
            pass

    flog.debug("Leave")
    return sections, documents


async def load_collections_extra_docs(
    collection_paths: Mapping[str, str],
) -> Mapping[str, CollectionExtraDocsInfoT]:
    """Load extra docs data.

    :arg collection_paths: Mapping of collection_name to the collection's path.
    :returns: A mapping of collection_name to CollectionExtraDocsInfoT.
    """
    flog = mlog.fields(func="load_collections_extra_docs")
    flog.debug("Enter")

    loaders = {}
    lib_ctx = app_context.lib_ctx.get()

    async with asyncio_pool.AioPool(size=lib_ctx.thread_max) as pool:
        for collection_name, collection_path in collection_paths.items():
            loaders[collection_name] = await pool.spawn(
                load_collection_extra_docs(collection_name, collection_path)
            )

        responses = await asyncio.gather(*loaders.values())

    # Note: Python dicts have always had a stable order as long as you don't modify the dict.
    # So loaders (implicitly, the keys) and responses have a matching order here.
    result = dict(zip(loaders, responses))

    flog.debug("Leave")
    return result
