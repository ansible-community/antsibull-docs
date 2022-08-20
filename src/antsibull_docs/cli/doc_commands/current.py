# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Entrypoint to the antsibull-docs script."""

from antsibull_core.logging import log
from antsibull_core.venv import FakeVenvRunner

from .stable import generate_docs_for_all_collections
from ... import app_context


mlog = log.fields(mod=__name__)


def generate_docs() -> int:
    """
    Create documentation for the current subcommand.

    Current documentation creates documentation for the currently installed version of Ansible,
    as well as the currently installed collections.

    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func='generate_docs')
    flog.debug('Begin processing docs')

    app_ctx = app_context.app_ctx.get()

    venv = FakeVenvRunner()

    return generate_docs_for_all_collections(
        venv, app_ctx.extra['collection_dir'], app_ctx.extra['dest_dir'],
        breadcrumbs=app_ctx.breadcrumbs,
        use_html_blobs=app_ctx.use_html_blobs,
        fail_on_error=app_ctx.extra['fail_on_error'])
