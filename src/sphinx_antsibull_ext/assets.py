# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""
Handling assets.
"""

from __future__ import annotations

import os
import pkgutil

from sphinx.util.osutil import ensuredir

BUILDER_FILES = {
    "html": {
        "antsibull-minimal.css": "_static",
    },
    "latex": {
        "antsibull.sty": "",
    },
}


def _copy_asset_files(app, exc):  # pylint: disable=unused-argument
    """
    Copy asset files.
    """
    for file, directory in BUILDER_FILES.get(app.builder.name, {}).items():
        data = pkgutil.get_data("sphinx_antsibull_ext", file)
        if data is None:
            raise RuntimeError(
                f"Internal error: cannot find {file} in sphinx_antsibull_ext package"
            )
        path = os.path.join(app.outdir, directory) if directory else app.outdir
        ensuredir(path)
        destination = os.path.join(path, file)
        with open(destination, "wb") as f:
            f.write(data)


def setup_assets(app):
    """
    Setup assets for a Sphinx app object.
    """
    # Copy assets
    app.connect("build-finished", _copy_asset_files)

    # Add CSS files
    for file in BUILDER_FILES.get("html", {}):
        if file.endswith(".css"):
            try:
                app.add_css_file(file)
            except AttributeError:
                # Compat for Sphinx < 1.8
                app.add_stylesheet(file)

    # Add LaTeX packages
    for file in BUILDER_FILES.get("latex", {}):
        if file.endswith(".sty"):
            app.add_latex_package(file[:-4])
