# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
Add directives for general formatting.
"""

from collections.abc import Mapping, Sequence

from antsibull_core.yaml import load_yaml_bytes
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx import addnodes

from .nodes import link_button


class _OptionTypeLine(Directive):
    final_argument_whitespace = True
    has_content = True

    def run(self):
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


class _Links(Directive):
    has_content = True

    def _get_string(
        self, entry: Mapping, index: int, key: str, exp_type, optional: bool = False
    ):
        value = entry.get(key)
        if value is None and optional:
            return value
        if isinstance(value, exp_type):
            return value
        raise self.error(
            f"{index + 1}th entry in {self.name}:"
            f" entry '{key}' must be {exp_type}, but found {value!r}"
        )

    def run(self):
        self.assert_has_content()
        node = nodes.bullet_list("\n".join(self.content), classes=["ansible-links"])
        content = "\n".join(self.content)
        try:
            data = load_yaml_bytes(content.encode("utf-8"))
        except Exception as exc:
            raise self.error(
                f"Error while parsing content of {self.name} as YAML: {exc}"
            ) from exc
        if not isinstance(data, Sequence):
            raise self.error(
                f"Content of {self.name} must be a YAML list, got {data!r} - {content!r}"
            )
        for index, entry in enumerate(data):
            if not isinstance(entry, Mapping):
                raise self.error(
                    f"Content of {self.name} must be a YAML list of mappings:"
                    " item {index + 1} is not a mapping, got {entry!r}"
                )
            title = self._get_string(entry, index, "title", str)
            url = self._get_string(entry, index, "url", str, optional=True)
            ref = self._get_string(entry, index, "ref", str, optional=True)
            external = (
                self._get_string(entry, index, "external", bool, optional=True) or False
            )
            if (url is None) == (ref is None):
                raise self.error(
                    f"{index + 1}th entry in {self.name}:"
                    " exactly one of 'url' and 'ref' must be provided"
                )
            if url is not None:
                refnode = link_button("", title, link_external=external, refuri=url)
            else:
                # Due to the way that Sphinx works, we have no chance to add
                # aria-role to the resulting ref node :(
                options = {
                    "reftype": "ref",
                    "refdomain": "std",
                    "refexplicit": True,
                    "refwarn": True,
                }
                refnode = addnodes.pending_xref("", nodes.inline("", title), **options)
                refnode["reftarget"] = ref
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
