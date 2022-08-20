# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Entrypoint to the antsibull-docs script."""

from antsibull_core.logging import log

from ... import app_context
from ...collection_links import lint_collection_links
from ...lint_extra_docs import lint_collection_extra_docs_files
from ...lint_plugin_docs import lint_collection_plugin_docs
from ...utils.collection_name_transformer import CollectionNameTransformer


mlog = log.fields(mod=__name__)


def lint_collection_docs() -> int:
    """
    Lint collection documentation for inclusion into the collection's docsite.

    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func='lint_collection_docs')
    flog.notice('Begin collection docs linting')

    app_ctx = app_context.app_ctx.get()

    collection_root = app_ctx.extra['collection_root_path']
    plugin_docs = app_ctx.extra['plugin_docs']

    flog.notice('Linting extra docs files')
    errors = lint_collection_extra_docs_files(collection_root)

    flog.notice('Linting collection links')
    errors.extend(lint_collection_links(collection_root))

    if plugin_docs:
        flog.notice('Linting plugin docs')
        collection_url = CollectionNameTransformer(
            app_ctx.collection_url, 'https://galaxy.ansible.com/{namespace}/{name}')
        collection_install = CollectionNameTransformer(
            app_ctx.collection_install, 'ansible-galaxy collection install {namespace}.{name}')
        errors.extend(lint_collection_plugin_docs(
            collection_root, collection_url=collection_url, collection_install=collection_install))

    messages = sorted(set(f'{error[0]}:{error[1]}:{error[2]}: {error[3]}' for error in errors))

    for message in messages:
        print(message)

    return 3 if messages else 0
