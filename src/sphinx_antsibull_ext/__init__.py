# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""
Antsibull minimal Sphinx extension which adds some features from the Ansible doc site.
"""

from __future__ import annotations

__version__ = "0.1.1"
__license__ = "BSD license"
__author__ = "Felix Fontein"
__author_email__ = "felix@fontein.de"


from .assets import setup_assets
from .roles import setup_roles


def setup(app):
    """
    Initializer for Sphinx extension API.
    See http://www.sphinx-doc.org/en/stable/extdev/index.html#dev-extensions.
    """

    # Add assets
    setup_assets(app)

    # Add roles
    setup_roles(app)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }
