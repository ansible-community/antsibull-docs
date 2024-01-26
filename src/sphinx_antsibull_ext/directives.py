# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
Add directives for general formatting.
"""

from __future__ import annotations

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx import addnodes

from .directive_helper import YAMLDirective
from .nodes import link_button
from .schemas.ansible_links import AnsibleLinks


class _OptionTypeLine(Directive):
    final_argument_whitespace = True
    has_content = True

    def run(self) -> list[nodes.Node]:
        self.assert_has_content()
        node = nodes.inline("\n".join(self.content))
        self.state.nested_parse(self.content, self.content_offset, node)
        for subnode in node.children:
            if not isinstance(subnode, nodes.paragraph):
                raise self.error(
                    f"{self.name} directive's children must all be paragraphs;"
                    f" found {type(subnode)}"
                )
            subnode.insert(
                0, nodes.raw("{\\footnotesize{}", "{\\footnotesize{}", format="latex")
            )
            subnode.append(nodes.raw("}", "}", format="latex"))
            subnode.update_basic_atts({"classes": ["ansible-option-type-line"]})
        return node.children


class _Links(YAMLDirective[AnsibleLinks]):
    wrap_as_data = True
    schema = AnsibleLinks

    def _run(self, content_str: str, content: AnsibleLinks) -> list[nodes.Node]:
        node = nodes.bullet_list(content_str, classes=["ansible-links"])
        for entry in content.data:
            refnode: link_button | addnodes.pending_xref
            if entry.url is not None:
                refnode = link_button(
                    "", entry.title, link_external=entry.external, refuri=entry.url
                )
            else:
                # Due to the way that Sphinx works, we have no chance to add
                # aria-role to the resulting ref node :(
                options = {
                    "reftype": "ref",
                    "refdomain": "std",
                    "refexplicit": True,
                    "refwarn": True,
                }
                refnode = addnodes.pending_xref(
                    "", nodes.inline("", entry.title), **options
                )
                refnode["reftarget"] = entry.ref
            item = nodes.list_item("")
            item.append(nodes.inline("", "", refnode))
            node.append(item)
        return [node]


DIRECTIVES = {
    "ansible-option-type-line": _OptionTypeLine,
    "ansible-links": _Links,
}


def setup_directives(app):
    """
    Setup directives for a Sphinx app object.
    """
    for name, directive in DIRECTIVES.items():
        app.add_directive(name, directive)
