# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
Add nodes for general formatting.
"""

from docutils import nodes


# pylint: disable-next=too-many-ancestors
class link_button(nodes.reference):  # pyre-ignore[11]
    def __init__(self, *args, link_external: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.link_external = link_external


def visit_link_button_html(self, node) -> None:
    external = node.link_external
    atts = {
        "class": "ansible-link reference",
        "href": node["refuri"],
        "aria-role": "button",
        "target": "_blank",
    }
    if external:
        atts["rel"] = "noopener external"
        atts["class"] += " external"
    else:
        atts["class"] += " internal"
    self.body.append(self.starttag(node, "a", "", **atts))


def depart_link_button_html(self, node):
    self.depart_reference(node)


def setup_nodes(app):
    """
    Setup nodes for a Sphinx app object.
    """
    app.add_node(link_button, html=(visit_link_button_html, depart_link_button_html))
