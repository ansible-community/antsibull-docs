# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""Entrypoint to the antsibull-docs script."""

from __future__ import annotations

import os
import os.path
import sys
import typing as t

from antsibull_core.logging import log

import antsibull_docs

from ... import app_context
from ...jinja2.environment import doc_environment

mlog = log.fields(mod=__name__)


RST_INDEX_RST = "rst/index.rst"

TEMPLATES = [
    ".gitignore",
    "antsibull-docs.cfg",
    "build.sh",
    "conf.py",
    "requirements.txt",
    RST_INDEX_RST,
]


def write_file(filename: str, content: str) -> None:
    """
    Write content into a file.
    """
    if os.path.exists(filename):
        with open(filename, encoding="utf-8") as f:
            existing_content = f.read()
        if existing_content == content:
            print(f"Skipping {filename}")
            return

    print(f"Writing {filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def write_binary_file(filename: str, content: bytes) -> None:
    """
    Write binary content into a file.
    """
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            existing_content = f.read()
        if existing_content == content:
            print(f"Skipping {filename}")
            return

    print(f"Writing {filename}...")
    with open(filename, "wb") as f:
        f.write(content)


def toperky(value: t.Any) -> str:
    if isinstance(value, str):
        value = value.replace("\\", "\\\\")
        value = value.replace("\n", "\\n")
        value = value.replace("\r", "\\r")
        value = value.replace('"', '\\"')
        if all(ch not in value for ch in "\\={}[]") and value.strip() == value:
            return value
        return f'"{value}"'
    raise RuntimeError(f"toperky filter cannot handle type {type(value)}")


def python_repr(value: t.Any) -> str:
    return repr(value)


def split_kv(entries: list[str] | None) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for entry in entries or []:
        key, value = entry.split("=", 1)
        result.append((key, value))
    return result


def site_init() -> int:
    """
    Initialize a Sphinx site template for a collection docsite.

    Creates a Sphinx configuration file, requirements.txt and a bash script which uses
    antsibull-docs to build the RST files for the specified collections.

    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func="site_init")
    flog.notice("Begin site init")

    app_ctx = app_context.app_ctx.get()

    dest_dir = app_ctx.extra["dest_dir"]
    collections = app_ctx.extra["collections"]
    collection_version = app_ctx.extra["collection_version"]
    use_current = app_ctx.extra["use_current"]
    squash_hierarchy = app_ctx.extra["squash_hierarchy"]
    lenient = app_ctx.extra["lenient"]
    fail_on_error = app_ctx.extra["fail_on_error"]
    use_html_blobs = app_ctx.use_html_blobs
    breadcrumbs = app_ctx.breadcrumbs
    indexes = app_ctx.indexes
    collection_url = app_ctx.collection_url
    collection_install = app_ctx.collection_install
    intersphinx_parts = []
    for intersphinx in app_ctx.extra["intersphinx"] or []:
        inventory, url = intersphinx.split(":", 1)
        intersphinx_parts.append((inventory.rstrip(" "), url.lstrip(" ")))
    index_rst_source: str | None = app_ctx.extra["index_rst_source"]
    project: str = app_ctx.extra["project"]
    conf_copyright: str = app_ctx.extra["copyright"]
    title: str = app_ctx.extra["title"]
    html_short_title: str | None = app_ctx.extra["html_short_title"]
    if html_short_title is None:
        html_short_title = title
    extra_conf = split_kv(app_ctx.extra["extra_conf"])
    extra_html_context = split_kv(app_ctx.extra["extra_html_context"])
    extra_html_theme_options = split_kv(app_ctx.extra["extra_html_theme_options"])
    output_format = app_ctx.extra["output_format"]

    if use_html_blobs:
        print(
            "WARNING: the use of --use-html-blobs is deprecated."
            " This feature will be removed soon.",
            file=sys.stderr,
        )

    sphinx_theme = "sphinx_ansible_theme"
    sphinx_theme_package = "sphinx-ansible-theme >= 0.9.0"
    if app_ctx.extra["sphinx_theme"] != "sphinx-ansible-theme":
        sphinx_theme = app_ctx.extra["sphinx_theme"]
        sphinx_theme_package = app_ctx.extra["sphinx_theme"]

    env = doc_environment(
        ("antsibull_docs.data", "sphinx_init"),
        extra_filters={
            "toperky": toperky,
            "python_repr": python_repr,
        },
    )

    for filename in TEMPLATES:
        if filename == RST_INDEX_RST and index_rst_source is not None:
            continue

        source = filename.replace(".", "_").replace("/", "_") + ".j2"
        template = env.get_template(source)

        content = (
            template.render(
                dest_dir=dest_dir,
                collection_version=collection_version,
                use_current=use_current,
                squash_hierarchy=squash_hierarchy,
                collections=collections,
                lenient=lenient,
                fail_on_error=fail_on_error,
                use_html_blobs=use_html_blobs,
                breadcrumbs=breadcrumbs,
                indexes=indexes,
                sphinx_theme=sphinx_theme,
                sphinx_theme_package=sphinx_theme_package,
                collection_url=collection_url,
                collection_install=collection_install,
                intersphinx=intersphinx_parts,
                project=project,
                conf_copyright=conf_copyright,
                title=title,
                html_short_title=html_short_title,
                extra_conf=extra_conf,
                extra_html_context=extra_html_context,
                extra_html_theme_options=extra_html_theme_options,
                output_format=output_format,
                antsibull_docs_version=antsibull_docs.__version__,
            )
            + "\n"
        )

        destination = os.path.join(dest_dir, filename)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        write_file(destination, content)

        # Make scripts executable
        if filename.endswith(".sh"):
            os.chmod(destination, 0o755)

    if index_rst_source is not None:
        with open(index_rst_source, "rb") as f:
            binary_content = f.read()

        destination = os.path.join(dest_dir, RST_INDEX_RST)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        write_binary_file(destination, binary_content)

    print(f"To build the docsite, go into {dest_dir} and run:")
    print("    pip install -r requirements.txt  # possibly use a venv")
    print("    ./build.sh")
    return 0
