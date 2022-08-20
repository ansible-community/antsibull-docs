# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Local app and lib context provider"""

# pylint: disable-next=unused-import
from antsibull_core.app_context import lib_ctx  # noqa
from antsibull_core.app_context import AppContextWrapper
from antsibull_docs.schemas.app_context import DocsAppContext


app_ctx: AppContextWrapper[DocsAppContext] = AppContextWrapper()
