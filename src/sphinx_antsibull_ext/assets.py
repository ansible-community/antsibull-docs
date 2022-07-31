# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
'''
Handling assets.
'''

import os
import pkgutil

from sphinx.util.osutil import ensuredir


CSS_FILES = [
    'antsibull-minimal.css',
]


def _copy_asset_files(app, exc):  # pylint: disable=unused-argument
    '''
    Copy asset files.
    '''
    # Copy CSS files
    for file in CSS_FILES:
        data = pkgutil.get_data('sphinx_antsibull_ext', file)
        if data is None:
            raise Exception(f'Internal error: cannot find {file} in sphinx_antsibull_ext package')
        ensuredir(os.path.join(app.outdir, '_static'))
        destination = os.path.join(app.outdir, '_static', file)
        with open(destination, 'wb') as f:
            f.write(data)


def setup_assets(app):
    '''
    Setup assets for a Sphinx app object.
    '''
    # Copy assets
    app.connect('build-finished', _copy_asset_files)

    # Add CSS files
    for file in CSS_FILES:
        try:
            app.add_css_file(file)
        except AttributeError:
            # Compat for Sphinx < 1.8
            app.add_stylesheet(file)
