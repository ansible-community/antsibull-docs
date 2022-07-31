# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
'''
Antsibull minimal Sphinx extension which adds some features from the Ansible doc site.
'''

__version__ = "0.1.1"
__license__ = "BSD license"
__author__ = "Felix Fontein"
__author_email__ = "felix@fontein.de"


from .assets import setup_assets


def setup(app):
    '''
    Initializer for Sphinx extension API.
    See http://www.sphinx-doc.org/en/stable/extdev/index.html#dev-extensions.
    '''

    # Add assets
    setup_assets(app)

    return dict(
        parallel_read_safe=True,
        parallel_write_safe=True,
        version=__version__,
    )
