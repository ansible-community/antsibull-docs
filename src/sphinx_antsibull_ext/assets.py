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

from sphinx.config import ENUM
from sphinx.util.osutil import ensuredir

BUILDER_FILES = {
    "html": {
        "antsibull-minimal.css": "_static",
    },
    "latex": {
        "antsibull.sty": "",
    },
}

# A map mapping builder names to the builder they inherit (indirectly) from.
# Mainly necessary to link the myriad of HTML-derived builders to the main HTML
# builder, to make sure that the stylesheet is copied in all these cases.
_BUILDER_ALIASES = {
    "applehelp": "html",
    "devhelp": "html",
    "dirhtml": "html",
    "epub": "html",
    "htmlhelp": "html",
    "qthelp": "html",
    "singlehtml": "html",
    "websupport": "html",
}

# A list of builders which needs the static files to be presented before the
# build finishes. I only verified this for epub, since the others also provide
# similar formats my guess is that they also need it.
_BUILDER_COPY_ON_INITED = [
    "applehelp",
    "devhelp",
    "epub",
    "htmlhelp",
    "qthelp",
    "websupport",
]

for _builder_name, _alias in _BUILDER_ALIASES.items():
    if _builder_name not in BUILDER_FILES and _alias in BUILDER_FILES:
        BUILDER_FILES[_builder_name] = BUILDER_FILES[_alias]

_AVAILABLE_COLOR_SCHEMES = [
    "none",
    "default",
    "default-autodark",
    "default-dark",
]


def get_color_scheme_content(color_scheme: str) -> bytes:
    if color_scheme == "none":
        return b""

    filename = f"colors-{color_scheme}.css"
    data = pkgutil.get_data("sphinx_antsibull_ext", filename)
    if data is not None:
        return data
    raise RuntimeError(
        f"Internal error: cannot find {filename} in sphinx_antsibull_ext package"
    )


def substitue_color_scheme(data: bytes, color_scheme: str) -> bytes:
    return data.replace(
        b"/* INSERT COLOR SCHEME HERE */", get_color_scheme_content(color_scheme)
    )


def get_color_scheme(app) -> str:
    color_scheme = app.config.antsibull_ext_color_scheme
    if color_scheme not in _AVAILABLE_COLOR_SCHEMES:
        schemes = ", ".join(_AVAILABLE_COLOR_SCHEMES)
        msg = f"Color scheme {color_scheme!r} is not available. Use one of {schemes}."
        raise RuntimeError(f"Antsibull Sphinx extension: {msg}")
    return color_scheme


def _copy_asset_files(app):
    """
    Copy asset files.
    """
    for file, directory in BUILDER_FILES.get(app.builder.name, {}).items():
        data = pkgutil.get_data("sphinx_antsibull_ext", file)
        if data is None:
            raise RuntimeError(
                f"Internal error: cannot find {file} in sphinx_antsibull_ext package"
            )
        if file == "antsibull-minimal.css":
            data = substitue_color_scheme(data, color_scheme=get_color_scheme(app))

        path = os.path.join(app.outdir, directory) if directory else app.outdir
        ensuredir(path)
        destination = os.path.join(path, file)
        with open(destination, "wb") as f:
            f.write(data)


def _copy_asset_files_inited(app):
    # pylint: disable=line-too-long
    """
    Copy asset files on 'builder-inited' signal.

    While the official documentation says that stylesheets should be copied
    during the build-finished signal
    (https://www.sphinx-doc.org/en/master/development/theming.html#add-your-own-static-files-to-the-build-assets)
    this won't work for builders such as epub, since they assemble the epub
    file *before* the build finishes. Since there is no other documented
    signal when to copy over the files, I picked the 'builder-inited' signal.
    """
    # pylint: enable=line-too-long
    if app.builder.name in _BUILDER_COPY_ON_INITED:
        _copy_asset_files(app)


def _copy_asset_files_finished(app, exc):  # pylint: disable=unused-argument
    """
    Copy asset files on 'build-finished' signal.
    """
    if app.builder.name not in _BUILDER_COPY_ON_INITED:
        _copy_asset_files(app)


def setup_assets(app):
    """
    Setup assets for a Sphinx app object.
    """
    # Add CSS related options
    app.add_config_value(
        "antsibull_ext_color_scheme",
        default="default",
        rebuild="",
        types=ENUM(*_AVAILABLE_COLOR_SCHEMES),
    )

    # Copy assets
    app.connect("builder-inited", _copy_asset_files_inited)
    app.connect("build-finished", _copy_asset_files_finished)

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
