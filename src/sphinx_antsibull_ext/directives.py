# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
Add directives for general formatting.
"""

from docutils import nodes
from docutils.parsers.rst import Directive


class _OptionTypeLine(Directive):
    final_argument_whitespace = True
    has_content = True

    def run(self):
        self.assert_has_content()
        node = nodes.inline("\n".join(self.content))
        self.state.nested_parse(self.content, self.content_offset, node)
        for subnode in node.children:
            if not isinstance(subnode, nodes.paragraph):
                raise ValueError(
                    f"{self.name} directive's children must all be paragraphs;"
                    f" found {type(subnode)}"
                )
            subnode.insert(
                0, nodes.raw("{\\footnotesize{}", "{\\footnotesize{}", format="latex")
            )
            subnode.append(nodes.raw("}", "}", format="latex"))
            subnode.update_basic_atts({"classes": ["ansible-option-type-line"]})
        return node.children


DIRECTIVES = {
    "ansible-option-type-line": _OptionTypeLine,
}


def setup_directives(app):
    """
    Setup directives for a Sphinx app object.
    """
    for name, directive in DIRECTIVES.items():
        app.add_directive(name, directive)
