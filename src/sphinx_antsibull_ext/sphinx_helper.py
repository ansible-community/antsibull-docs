# Author: Sphinx team
# two clause BSD licence (see LICENSES/BSD-2-Clause.txt or
# https://github.com/sphinx-doc/sphinx/blob/master/LICENSE)
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2007-2023, Sphinx team (see Sphinx's AUTHORS file)
#
# The code in here has been extracted and adjusted from
# https://github.com/sphinx-doc/sphinx/blob/d3c91f951255c6729a53e38c895ddc0af036b5b9/sphinx/util/docutils.py#L520-L537
"""
Helpers vendored from Sphinx.
"""

from __future__ import annotations

import re

from docutils.utils import unescape

# \x00 means the "<" was backslash-escaped
_EXPLICIT_TITLE_RE = re.compile(r"^(.+?)\s*(?<!\x00)<(.*?)>$", re.DOTALL)


def extract_explicit_title(text: str) -> tuple[str, str | None]:
    """
    Given the parameter to a reference role, extract the unescaped target and
    the optional unescaped title.
    """
    m = _EXPLICIT_TITLE_RE.match(text)
    if not m:
        return unescape(text), None
    return unescape(m.group(2)), unescape(m.group(1))
