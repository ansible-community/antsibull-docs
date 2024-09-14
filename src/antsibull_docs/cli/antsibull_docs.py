# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project

# PYTHON_ARGCOMPLETE_OK

"""Entrypoint to the antsibull-docs script."""

from __future__ import annotations

import argparse
import os
import os.path
import stat
import sys
from collections.abc import Callable
from importlib import import_module

from packaging.version import Version as PypiVer

try:
    import argcomplete

    HAS_ARGCOMPLETE = True
except ImportError:
    HAS_ARGCOMPLETE = False

import twiggy  # type: ignore[import]
from antsibull_core.logging import initialize_app_logging, log

initialize_app_logging()

# We have to call initialize_app_logging() before these imports so that the log object is configured
# correctly before other antisbull modules make copies of it.
# pylint: disable=wrong-import-position
from antsibull_core import app_context  # noqa: E402
from antsibull_core.args import (  # noqa: E402
    InvalidArgumentError,
    get_toplevel_parser,
    normalize_toplevel_options,
)
from antsibull_core.compat import BooleanOptionalAction  # noqa: E402
from antsibull_core.config import ConfigError, load_config  # noqa: E402
from antsibull_core.filesystem import UnableToCheck, writable_via_acls  # noqa: E402

import antsibull_docs  # noqa: E402

from ..constants import DOCUMENTABLE_PLUGINS  # noqa: E402
from ..docs_parsing.fqcn import (  # noqa: E402
    is_collection_name,
    is_fqcn,
    is_wildcard_collection_name,
)
from ..schemas.app_context import DocsAppContext  # noqa: E402

# pylint: enable=wrong-import-position


mlog = log.fields(mod=__name__)


def _create_loader(module: str, function: str) -> Callable[[], Callable[[], int]]:
    def load():
        module_obj = import_module(f"antsibull_docs.cli.doc_commands.{module}")
        return getattr(module_obj, function)

    return load


#: Mapping from command line subcommand names to functions which implement those
#: The functions need to take a single argument, the processed list of args.
ARGS_MAP: dict[str, Callable[[], Callable[[], int]]] = {
    "devel": _create_loader("devel", "generate_docs"),
    "stable": _create_loader("stable", "generate_docs"),
    "current": _create_loader("current", "generate_docs"),
    "collection": _create_loader("collection", "generate_docs"),
    "collection-plugins": _create_loader("collection_plugins", "generate_docs"),
    "plugin": _create_loader("plugin", "generate_docs"),
    "sphinx-init": _create_loader("sphinx_init", "site_init"),
    "lint-collection-docs": _create_loader("lint_docs", "lint_collection_docs"),
    "lint-core-docs": _create_loader("lint_docs", "lint_core_docs"),
}

#: The filename for the file which lists raw collection names
DEFAULT_PIECES_FILE: str = "ansible.in"


def _normalize_docs_options(args: argparse.Namespace) -> None:
    if args.command in ("lint-collection-docs", "lint-core-docs"):
        return

    args.dest_dir = os.path.abspath(os.path.realpath(args.dest_dir))

    # We're going to be writing a deep hierarchy of files into this directory so we need to make
    # sure that the user understands that this needs to be a directory which has been secured
    # against malicious usage:

    # Exists already
    try:
        stat_results = os.stat(args.dest_dir)

        if not stat.S_ISDIR(stat_results.st_mode):
            raise FileNotFoundError()
    except FileNotFoundError:
        # pylint:disable-next=raise-missing-from
        raise InvalidArgumentError(
            f"{args.dest_dir} must be an existing directory owned by you,"
            f" and only be writable by the owner"
        )

    # Owned by the user
    euid = os.geteuid()
    if stat_results[stat.ST_UID] != euid:
        raise InvalidArgumentError(
            f"{args.dest_dir} must be owned by you, and only be writable"
            f" by the owner"
        )

    # Writable only by the user
    if stat.S_IMODE(stat_results.st_mode) & (stat.S_IWOTH | stat.S_IWGRP):
        raise InvalidArgumentError(
            f"{args.dest_dir} must only be writable by the owner"
        )

    try:
        if writable_via_acls(args.dest_dir, euid):
            raise InvalidArgumentError(
                f"Filesystem acls grant write on {args.dest_dir} to additional users"
            )
    except UnableToCheck:
        # We've done our best but some systems don't even have acls on their filesystem so we can't
        # error here.
        pass


def _normalize_devel_options(args: argparse.Namespace) -> None:
    if args.command != "devel":
        return

    if not os.path.isfile(args.pieces_file):
        raise InvalidArgumentError(
            f"The pieces file, {args.pieces_file}, must already exist."
            " It should contain one namespace.collection per line"
        )


def _normalize_stable_options(args: argparse.Namespace) -> None:
    if args.command != "stable":
        return

    if not os.path.isfile(args.deps_file):
        raise InvalidArgumentError(
            f"The deps file, {args.deps_file}, must already exist."
            " It should contain one namespace.collection with version"
            " per line"
        )

    if args.version is not None:
        try:
            PypiVer(args.version)
        except ValueError as exc:
            raise InvalidArgumentError(
                f"The provided version, {args.version!r}, is not a valid version: {exc}"
            ) from exc


def _normalize_collection_options(args: argparse.Namespace) -> None:
    if args.command != "collection":
        return

    if args.squash_hierarchy and len(args.collections) > 1:
        raise InvalidArgumentError(
            "The option --squash-hierarchy can only be used when"
            " only one collection is specified"
        )

    for collection_name in args.collections:
        if not is_collection_name(collection_name):
            if args.use_current and is_wildcard_collection_name(collection_name):
                continue
            raise InvalidArgumentError(
                f"The collection, {collection_name}, is not a valid collection name."
            )


def _normalize_current_options(args: argparse.Namespace) -> None:
    if args.command != "current":
        return

    if args.collection_dir is not None:
        if not os.path.isdir(os.path.join(args.collection_dir, "ansible_collections")):
            raise InvalidArgumentError(
                f"The collection directory, {args.collection_dir}, must be"
                " a directory containing a subdirectory ansible_collections"
            )


def _normalize_plugin_options(args: argparse.Namespace) -> None:
    if args.command != "plugin":
        return

    for plugin_name in args.plugin:
        if not is_fqcn(plugin_name):
            raise InvalidArgumentError(f"The plugin, {plugin_name}, must be a FQCN.")


def _normalize_sphinx_init_options(args: argparse.Namespace) -> None:
    if args.command != "sphinx-init":
        return

    if args.squash_hierarchy and len(args.collections) != 1:
        raise InvalidArgumentError(
            "The option --squash-hierarchy can only be used when"
            " exactly one collection is specified"
        )

    if not args.use_current and len(args.collections) == 0:
        raise InvalidArgumentError(
            "If no collection is provided, --use-current must be specified"
        )

    for intersphinx in args.intersphinx or []:
        if ":" not in intersphinx:
            raise InvalidArgumentError(
                "Every `--intersphinx` value must have at least one colon (:)."
            )

    if args.index_rst_source is not None and not os.path.isfile(args.index_rst_source):
        raise InvalidArgumentError(
            "The rst/index.rst replacement file,"
            f" {args.index_rst_source}, is not a file"
        )

    for key, option in [
        ("extra_conf", "--extra-conf"),
        ("extra_html_context", "--extra-html-context"),
        ("extra_html_theme_options", "--extra-html-theme-options"),
    ]:
        for entry in getattr(args, key) or []:
            if "=" not in entry:
                raise InvalidArgumentError(
                    f"Every `{option}` value must have at least one equal sign (=)."
                )


def parse_args(program_name: str, args: list[str]) -> argparse.Namespace:
    """
    Parse and coerce the command line arguments.

    :arg program_name: The name of the program
    :arg args: A list of the command line arguments
    :returns: A :python:obj:`argparse.Namespace`
    :raises InvalidArgumentError: Whenever there's something wrong with the arguments.
    """
    flog = mlog.fields(func="parse_args")
    flog.fields(program_name=program_name, raw_args=args).info("Enter")

    # Overview of parsers:
    # * docs_parser is an abstract parser.  Contains options that all of the antisbull-docs
    #   subcommands use.
    # * template_parser is a mixin for subcommands which template HTML
    # * cache_parser is a mixin for subcommands which operate on the ansible-core sources and
    #   therefore they can use a preinstalled version of the code instead of downloading it
    #   themselves.
    # * whole_site_parser is a mixin for subcommands which can choose to build a structure
    #   for integration into a comprehensive website.
    # * devel, stable, current, collection, file: These parsers contain all of the options for those
    #   respective subcommands.
    docs_parser = argparse.ArgumentParser(add_help=False)
    docs_parser.add_argument(
        "--dest-dir", default=".", help="Directory to write the output to"
    )
    docs_parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="If any parsing or schema valiation errors happen, fail instead"
        " of creating error pages. For use in CI.",
    )

    template_parser = argparse.ArgumentParser(add_help=False)
    template_parser.add_argument(
        "--use-html-blobs",
        dest="use_html_blobs",
        action=BooleanOptionalAction,
        default=argparse.SUPPRESS,
        help="Determines whether to use HTML blobs for option and return"
        " value tables. Using HTML blobs reduces memory and CPU time"
        " usage significantly so you can enable this if necessary."
        " (default: False)",
    )

    insert_version_parser = argparse.ArgumentParser(add_help=False)
    insert_version_parser.add_argument(
        "--add-antsibull-docs-version",
        dest="add_antsibull_docs_version",
        action=BooleanOptionalAction,
        default=argparse.SUPPRESS,
        help="Determines whether the antsibull-docs version is inserted"
        " in the generated files. (default: True)",
    )

    cache_parser = argparse.ArgumentParser(add_help=False)
    # TODO: Remove --ansible-base-cache once the ansible/ansible docs-build test is updated
    # TODO: Eventually remove --ansible-base-source
    cache_parser.add_argument(
        "--ansible-core-source",
        "--ansible-base-source",
        "--ansible-base-cache",
        default=None,
        help="Checkout or expanded tarball of the ansible-core package.  If"
        " this is a git checkout it must be the HEAD of the branch you are"
        " building for. If it is an expanded tarball, the __version__ will"
        " be checked to make sure it is compatible with and the same or"
        " later version than requested by the deps file.",
    )
    cache_parser.add_argument(
        "--collection-cache",
        default=argparse.SUPPRESS,
        help="Directory of collection tarballs.  These will be used instead"
        " of downloading fresh versions provided that they meet the criteria"
        " (Latest version of the collections known to galaxy).",
    )

    output_format_parser = argparse.ArgumentParser(add_help=False)
    output_format_parser.add_argument(
        "--output-format",
        default="ansible-docsite",
        choices=["ansible-docsite", "simplified-rst"],
        help="What kind of output format to use. Note that simplified-rst is"
        " *EXPERIMENTAL*; the output format will likely change considerably"
        " over the next few versions, and these changes will not be considered"
        " breaking changes.",
    )

    whole_site_parser = argparse.ArgumentParser(add_help=False)
    whole_site_parser.add_argument(
        "--breadcrumbs",
        "--gretel",
        dest="breadcrumbs",
        action=BooleanOptionalAction,
        default=argparse.SUPPRESS,
        help="Determines whether to add breadcrumbs to plugin docs via"
        " hidden sphinx toctrees. This can take up a significant"
        " amount of memory if there are a large number of plugins so"
        " you can disable this if necessary. (default: True)",
    )
    whole_site_parser.add_argument(
        "--indexes",
        dest="indexes",
        action=BooleanOptionalAction,
        default=argparse.SUPPRESS,
        help="Determines whether to create the collection index and"
        " plugin indexes. They may not be needed if you have"
        " a different structure for your website. (default: True)",
    )
    # --skip-indexes is for backwards compat.  We want all negations to be --no-* in the future.
    whole_site_parser.add_argument(
        "--skip-indexes",
        dest="indexes",
        action="store_false",
        default=argparse.SUPPRESS,
        help="Do not create the collection index and plugin indexes."
        " This option is deprecated in favor of --no-indexes",
    )

    cleanup_parser = argparse.ArgumentParser(add_help=False)
    cleanup_parser.add_argument(
        "--cleanup",
        dest="cleanup",
        choices=[
            "no",
            "similar-files",
            "similar-files-and-dirs",
            "everything",
        ],
        default="no",
        help="Whether to clean-up the output directory after writing the own"
        " files and directories. Generally this only affects the collections/"
        " subdirectory of the output directly, unless no hierarchy is emitted."
        # no:
        " 'no' means that no cleanup is done."
        # similar-files:
        " 'similar-files' removes similar files in directories that"
        " antsibull-docs writes to, for example files like 'foo_module.rst';"
        # similar-files-and-dirs:
        " 'similar-files-and-dirs' also removes directories that are not"
        " written by antsibull-docs inside the directory structure, for"
        " example other collections;"
        # everything:
        " 'everything' ensures that only what antsibull-docs has written stays"
        " inside the output directory. (default: no)",
    )

    parser = get_toplevel_parser(
        prog=program_name,
        package="antsibull_docs",
        package_version=antsibull_docs.__version__,
        program_name="antsibull-docs",
        description="Script to manage generated documentation for ansible",
    )
    subparsers = parser.add_subparsers(
        title="Subcommands", dest="command", help="for help use: `SUBCOMMANDS -h`"
    )
    subparsers.required = True

    #
    # Document the next version of ansible
    #
    devel_parser = subparsers.add_parser(
        "devel",
        parents=[
            docs_parser,
            cache_parser,
            whole_site_parser,
            template_parser,
            insert_version_parser,
            cleanup_parser,
        ],
        description="Generate documentation for the next major release of Ansible",
    )
    devel_parser.add_argument(
        "--pieces-file",
        default=DEFAULT_PIECES_FILE,
        help="File containing a list of collections to include",
    )
    devel_parser.add_argument(
        "--use-installed-ansible-core",
        action="store_true",
        help="Assumes that ansible-core is already installed and can be"
        " used by calling `ansible`, `ansible-doc`, and `ansible-galaxy`"
        " from $PATH. By default, antsibull-docs installs ansible-core"
        " into a temporary venv.",
    )
    devel_parser.add_argument(
        "--major-version",
        type=int,
        help="Provide the major Ansible version for the devel build.",
    )

    #
    # Document a released version of ansible
    #
    stable_parser = subparsers.add_parser(
        "stable",
        parents=[
            docs_parser,
            cache_parser,
            whole_site_parser,
            template_parser,
            insert_version_parser,
            cleanup_parser,
        ],
        description="Generate documentation for a current version of ansible",
    )
    stable_parser.add_argument(
        "--deps-file",
        required=True,
        help="File which contains the list of collections and"
        " versions which were included in this version of Ansible",
    )
    stable_parser.add_argument(
        "--use-installed-ansible-core",
        action="store_true",
        help="Assumes that ansible-core is already installed and can be"
        " used by calling `ansible`, `ansible-doc`, and `ansible-galaxy`"
        " from $PATH. By default, antsibull-docs installs ansible-core"
        " into a temporary venv.",
    )
    stable_parser.add_argument("--version", help="Provide the Ansible version.")

    #
    # Document the currently installed version of ansible
    #
    current_parser = subparsers.add_parser(
        "current",
        parents=[
            docs_parser,
            whole_site_parser,
            template_parser,
            insert_version_parser,
            output_format_parser,
            cleanup_parser,
        ],
        description="Generate documentation for the current"
        " installed version of ansible and the current installed"
        " collections",
    )
    current_parser.add_argument(
        "--collection-dir",
        help="Path to the directory containing ansible_collections. If not"
        " specified, all collections in the currently configured ansible"
        " search paths will be used",
    )
    current_parser.add_argument(
        "--skip-ansible-builtin",
        action="store_true",
        help="Do not generate documentation for ansible.builtin, the synthetic"
        " collection consisting of all modules and plugins bundled with ansible-core.",
    )

    #
    # Document one or more specified collections
    #
    collection_parser = subparsers.add_parser(
        "collection",
        parents=[
            docs_parser,
            whole_site_parser,
            template_parser,
            insert_version_parser,
            output_format_parser,
            cleanup_parser,
        ],
        description="Generate documentation for specified collections",
    )
    collection_parser.add_argument(
        "--collection-version",
        default="@latest",
        help="The version of the collection to document.  The special"
        ' version, "@latest" can be used to download and document the'
        " latest version from galaxy.",
    )
    collection_parser.add_argument(
        "--use-current",
        action="store_true",
        help="Assumes that all arguments are collection names, and"
        " these collections have been installed with the current"
        " version of ansible. Specified --collection-version will be"
        " ignored.",
    )
    collection_parser.add_argument(
        "--squash-hierarchy",
        action="store_true",
        help="Do not use the full hierarchy collections/namespace/name/"
        " in the destination directory. Only valid if there is only"
        " one collection specified.  Implies --no-indexes.",
    )
    collection_parser.add_argument(
        nargs="+",
        dest="collections",
        help="One or more collections to document. No paths or URLs are"
        " supported. Collections are assumed to exist on Galaxy, or be"
        " installed locally when --use-current is used. When --use-current"
        " is used, the wildcard '*' can be used for the namespace, the"
        " collection name, or both ('foo.*', '*.bar', '*.*').",
    )

    #
    # Document a specifically named plugin
    #
    plugin_parser = subparsers.add_parser(
        "plugin",
        parents=[
            docs_parser,
            template_parser,
            insert_version_parser,
            output_format_parser,
        ],
        description="Generate documentation for a single plugin",
    )
    plugin_parser.add_argument(
        nargs=1,
        dest="plugin",
        action="store",
        help="A single file to document. Must be a FQCN. The plugin is assumed"
        " to be installed for the current ansible-core version.",
    )
    plugin_parser.add_argument(
        "--plugin-type",
        action="store",
        default="module",
        choices=DOCUMENTABLE_PLUGINS,
        help="The type of the plugin",
    )

    #
    # Document one or more specified collections
    #
    collection_plugins_parser = subparsers.add_parser(
        "collection-plugins",
        parents=[
            docs_parser,
            template_parser,
            insert_version_parser,
            output_format_parser,
            cleanup_parser,
        ],
        description="Generate documentation for all plugins of a specified collection",
    )
    collection_plugins_parser.add_argument(
        "--collection-version",
        default="@latest",
        help="The version of the collection to document.  The special"
        ' version, "@latest" can be used to download and document the'
        " latest version from galaxy.",
    )
    collection_plugins_parser.add_argument(
        "--use-current",
        action="store_true",
        default=False,
        help="Assumes that the argument is a collection name, and"
        " that collection has been installed with the current"
        " version of ansible. Specified --collection-version will be"
        " ignored.",
    )
    collection_plugins_parser.add_argument(
        "--fqcn-plugin-names",
        action="store_true",
        default=False,
        help="Include the collection name in the plugin file names.",
    )
    collection_plugins_parser.add_argument(
        nargs=1,
        dest="collection",
        help="A collection whose plugins to document.  It will be"
        " downloaded from Galaxy or is assumed to be installed,"
        " depending on whether --use-current is specified.",
    )

    #
    # Create a Sphinx site template
    #
    sphinx_init_parser = subparsers.add_parser(
        "sphinx-init",
        parents=[
            docs_parser,
            template_parser,
            whole_site_parser,
            insert_version_parser,
            output_format_parser,
        ],
        description="Generate a Sphinx site template for a collection docsite",
    )

    sphinx_init_parser.add_argument(
        "--collection-version",
        default="@latest",
        help="The version of the collection to document.  The special"
        ' version, "@latest" can be used to download and document the'
        " latest version from galaxy.",
    )
    sphinx_init_parser.add_argument(
        "--use-current",
        action="store_true",
        help="Assumes that all arguments are collection names, and"
        " these collections have been installed with the current"
        " version of ansible. Specified --collection-version will be"
        " ignored.",
    )
    sphinx_init_parser.add_argument(
        "--squash-hierarchy",
        action="store_true",
        help="Do not use the full hierarchy collections/namespace/name/"
        " in the destination directory. Only valid if there is exactly"
        " one collection specified.",
    )
    sphinx_init_parser.add_argument(
        "--lenient", action="store_true", help="Configure Sphinx to not be too strict."
    )
    sphinx_init_parser.add_argument(
        "--sphinx-theme",
        default="sphinx-ansible-theme",
        help="Configure the Sphinx theme to use.",
    )
    sphinx_init_parser.add_argument(
        nargs="*",
        dest="collections",
        help="One or more collections to document.  If the names are"
        " directories on disk, they will be parsed as expanded"
        " collections. Otherwise, if they could be collection"
        " names, they will be downloaded from galaxy.  If no names are"
        " provided, --use-current must be supplied and docs are built"
        " for all collections found.",
    )
    sphinx_init_parser.add_argument(
        "--intersphinx",
        action="append",
        help="Add entries to intersphinx_mapping in the generated"
        " conf.py. Use the syntax `identifier:https://server/path` to"
        " add the identifier `identifier` with URL"
        " `https://server/path`. The inventory is always `None`.",
    )
    sphinx_init_parser.add_argument(
        "--index-rst-source",
        help="Copy the provided file to rst/index.rst intead of"
        " templating a default one.",
    )
    sphinx_init_parser.add_argument(
        "--project",
        default="Ansible collections",
        help='Sets the "project" value in the Sphinx configuration.',
    )
    sphinx_init_parser.add_argument(
        "--copyright",
        default="Ansible contributors",
        help='Sets the "copyright" value in the Sphinx configuration.',
    )
    sphinx_init_parser.add_argument(
        "--title",
        default="Ansible Collections Documentation",
        help='Sets the "title" and "html_short_title" values in the'
        " Sphinx configuration. If --html-short-title is also"
        ' specified, only "title" will be set to the value specified'
        " here.",
    )
    sphinx_init_parser.add_argument(
        "--html-short-title",
        help='Sets the "html_short_title" value in the Sphinx'
        " configuration. If not specified, the value of --title will"
        " be used.",
    )
    sphinx_init_parser.add_argument(
        "--extra-conf",
        action="append",
        help="Add additional configuration entries to the generated"
        " conf.py. Use the syntax `key=value` to add an entry"
        ' `key = "value"`.',
    )
    sphinx_init_parser.add_argument(
        "--extra-html-context",
        action="append",
        help="Add additional configuration entries to the generated"
        " conf.py in `html_context`. Use the syntax `key=value` to add"
        ' an entry `"key": "value",`.',
    )
    sphinx_init_parser.add_argument(
        "--extra-html-theme-options",
        action="append",
        help="Add additional configuration entries to the generated"
        " conf.py in `html_theme_options`. Use the syntax `key=value`"
        ' to add an entry `"key": "value",`.',
    )

    #
    # Lint collection docs
    #
    lint_collection_docs_parser = subparsers.add_parser(
        "lint-collection-docs",
        parents=[output_format_parser],
        description="Collection extra docs linter for inclusion in docsite",
    )

    lint_collection_docs_parser.add_argument(
        "collection_root_path",
        metavar="/path/to/collection",
        help="path to collection (directory that includes galaxy.yml)",
    )
    lint_collection_docs_parser.add_argument(
        "--plugin-docs",
        dest="plugin_docs",
        action=BooleanOptionalAction,
        default=False,
        help="Determine whether to also check RST file"
        " generation and schema and markup validation for"
        " plugins and roles in this collection.",
    )
    lint_collection_docs_parser.add_argument(
        "--validate-collection-refs",
        dest="validate_collections_refs",
        choices=["self", "dependent", "all"],
        default="dependent",
        help="When --plugin-docs is specified, determine references to which"
        " collections to validate.  'self' means only validate references to"
        " this collection.  'dependent' means validating references to"
        " collections this collection (transitively) depends on, including"
        " references to ansible.builtin.  'all' means validating references"
        " to all collections the linter can find.",
    )
    lint_collection_docs_parser.add_argument(
        "--disallow-unknown-collection-refs",
        dest="disallow_unknown_collection_refs",
        action=BooleanOptionalAction,
        default=False,
        help="When --plugin-docs is specified, determine whether to accept"
        " references to unknown collections that are not covered by "
        "--validate-collection-refs.",
    )
    lint_collection_docs_parser.add_argument(
        "--skip-rstcheck",
        dest="skip_rstcheck",
        action=BooleanOptionalAction,
        default=False,
        help="When --plugin-docs is specified, do not run"
        " rstcheck on the generated RST files. This speeds"
        " up testing for large collections.",
    )
    lint_collection_docs_parser.add_argument(
        "--disallow-semantic-markup",
        dest="disallow_semantic_markup",
        action=BooleanOptionalAction,
        default=False,
        help="When --plugin-docs is specified, check that"
        " there is no semantic markup used. This can be used"
        " by collections to ensure that semantic markup is"
        " not yet used.",
    )

    #
    # Lint core docs
    #
    lint_core_docs_parser = subparsers.add_parser(
        "lint-core-docs",
        description="Collection extra docs linter for inclusion in docsite",
    )

    lint_core_docs_parser.add_argument(
        "--validate-collection-refs",
        dest="validate_collections_refs",
        choices=["self", "all"],
        default="self",
        help="Determine references to which collections to validate.  'self'"
        " means only validate references to ansible.builtin.  'all' means"
        " validating references to all collections the linter can find.",
    )
    lint_core_docs_parser.add_argument(
        "--disallow-unknown-collection-refs",
        dest="disallow_unknown_collection_refs",
        action=BooleanOptionalAction,
        default=False,
        help="Determine whether to accept references to unknown collections"
        " that are not covered by --validate-collection-refs.",
    )

    # This must come after all parser setup
    if HAS_ARGCOMPLETE:
        argcomplete.autocomplete(parser)

    flog.debug("Argument parser setup")

    if "--ansible-base-cache" in args:
        flog.warning(
            "The CLI parameter, `--ansible-base-cache` has been renamed to"
            " `--ansible-core-source`.  Please use that instead"
        )
    if "--ansible-base-source" in args:
        flog.warning(
            "The CLI parameter, `--ansible-base-source` has been renamed to"
            " `--ansible-core-source`.  Please use that instead"
        )

    if "--skip-indexes" in args:
        flog.warning(
            "The CLI parameter, `--skip-indexes` has been renamed to"
            " `--no-indexes`.  Please use that instead"
        )
        if "--indexes" in args or "--no-indexes" in args:
            raise InvalidArgumentError(
                "You cannot use `--indexes`/`--no-indexes` with"
                " `--skip-indexes`. Please remove `--skip-indexes`"
                " and try again."
            )

    parsed_args: argparse.Namespace = parser.parse_args(args)
    flog.fields(args=parsed_args).debug("Arguments parsed")

    # Validation and coercion
    normalize_toplevel_options(parsed_args)
    _normalize_docs_options(parsed_args)
    _normalize_devel_options(parsed_args)
    _normalize_stable_options(parsed_args)
    _normalize_current_options(parsed_args)
    _normalize_collection_options(parsed_args)
    _normalize_plugin_options(parsed_args)
    _normalize_sphinx_init_options(parsed_args)
    flog.fields(args=parsed_args).debug("Arguments normalized")

    # Note: collections aren't validated as existing files or collection names here because talking
    # to galaxy to validate the collection names goes beyond the scope of what parsing and
    # validating the command line should do.

    return parsed_args


def run(args: list[str]) -> int:
    """
    Run the program.

    :arg args: A list of command line arguments.  Typically :python:`sys.argv`.
    :returns: A program return code.  0 for success, integers for any errors.  These are documented
        in :func:`main`.
    """
    flog = mlog.fields(func="run")
    flog.fields(raw_args=args).info("Enter")

    program_name = os.path.basename(args[0])
    try:
        parsed_args: argparse.Namespace = parse_args(program_name, args[1:])
    except InvalidArgumentError as e:
        print(e)
        return 2
    flog.fields(args=parsed_args).info("Arguments parsed")

    try:
        cfg = load_config(parsed_args.config_file, app_context_model=DocsAppContext)
        flog.fields(config=cfg).info("Config loaded")
    except ConfigError as e:
        print(e)
        return 2

    context_data = app_context.create_contexts(
        args=parsed_args, cfg=cfg, app_context_model=DocsAppContext
    )
    with app_context.app_and_lib_context(context_data) as (app_ctx, dummy_):
        twiggy.dict_config(app_ctx.logging_cfg.model_dump())
        flog.debug("Set logging config")

        flog.fields(command=parsed_args.command).info("Action")
        return ARGS_MAP[parsed_args.command]()()


def main() -> int:
    """
    Entrypoint called from the script.

    console_scripts call functions which take no parameters.  However, it's hard to test a function
    which takes no parameters so this function lightly wraps :func:`run`, which actually does the
    heavy lifting.

    :returns: A program return code.

    Return codes:
        :0: Success
        :1: Unhandled error.  See the Traceback for more information.
        :2: There was a problem with the command line arguments
        :3: Unexpected problem downloading ansible-core
    """
    return run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
