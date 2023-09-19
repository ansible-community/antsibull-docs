# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
Add directives for general formatting.
"""

from __future__ import annotations

import typing as t
from urllib.parse import quote as _urllib_quote

from docutils import nodes
from docutils.nodes import Element
from sphinx import addnodes, domains
from sphinx.builders import Builder
from sphinx.domains.std import StandardDomain
from sphinx.environment import BuildEnvironment
from sphinx.locale import _
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import make_id

from antsibull_docs.utils.rst import massage_rst_label

from .directive_helper import YAMLDirective
from .nodes import ansible_attribute, ansible_option, ansible_return_value, link_button
from .schemas.ansible_links import AnsibleLinks
from .schemas.ansible_plugin import (
    AnsibleAttribute,
    AnsibleOption,
    AnsiblePlugin,
    AnsibleRequirementsAnchor,
    AnsibleReturnValue,
    AnsibleRoleEntrypoint,
)

logger = logging.getLogger(__name__)


class _OptionTypeLine(SphinxDirective):
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


class AnsibleDomain(domains.Domain):
    name = "ansible"

    object_types: dict[str, domains.ObjType] = {
        "plugin": domains.ObjType(_("plugin"), "plugin", searchprio=-1),
        "role_entrypoint": domains.ObjType(
            _("role entrypoint"), "role_entrypoint", searchprio=-1
        ),
    }

    @property
    def objects(self) -> dict[tuple[str, str], tuple[str, str]]:
        return self.data.setdefault(
            "objects", {}
        )  # (objtype, name) -> docname, labelid

    def note_object(
        self, objtype: str, name: str, labelid: str, location: t.Any = None
    ) -> None:
        if (objtype, name) in self.objects:
            docname = self.objects[objtype, name][0]
            logger.warning(
                f"Duplicate {objtype} description of {name}, other instance in {docname}",
                location=location,
            )
        self.objects[objtype, name] = (self.env.docname, labelid)

    def merge_domaindata(self, docnames: list[str], otherdata: dict) -> None:
        """Merge in data regarding *docnames* from a different domaindata
        inventory (coming from a subprocess in parallel builds).
        """

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: addnodes.pending_xref,
        contnode: Element,
    ) -> list[tuple[str, Element]]:
        """Resolve the pending_xref *node* with the given *target*."""
        return []


class _Plugin(YAMLDirective[AnsiblePlugin]):
    schema = AnsiblePlugin

    def _run(self, content_str: str, content: AnsiblePlugin) -> list[nodes.Node]:
        section = self.state.parent
        titles = [child for child in section.children if isinstance(child, nodes.title)]
        if len(titles) != 1:
            raise self.error(
                f"Cannot find single title for section {section} - found {titles}"
            )
        title = titles[0]

        if content.plugin_type == "role":
            # just add index nodes for the entrypoints
            return []

        indexnode = addnodes.index(entries=[])
        node_id = make_id(
            self.env,
            self.state.document,
            "plugin",
            f"{content.fqcn}_{content.plugin_type}",
        )
        title["ids"].append(node_id)
        self.state.document.note_explicit_target(title)
        index_category = content.plugin_type
        if content.plugin_type not in ("role", "module"):
            index_category = f"{index_category} plugin"
        indexnode["entries"].append(
            ("single", f"{index_category}; {content.fqcn}", node_id, "", None)
        )
        ansible = t.cast(AnsibleDomain, self.env.get_domain("ansible"))
        ansible.note_object(
            "plugin", f"{content.fqcn}_{content.plugin_type}", node_id, location=title
        )

        return [indexnode]


class _RoleEntrypoint(YAMLDirective[AnsibleRoleEntrypoint]):
    schema = AnsibleRoleEntrypoint

    def _run(
        self, content_str: str, content: AnsibleRoleEntrypoint
    ) -> list[nodes.Node]:
        section = self.state.parent
        titles = [child for child in section.children if isinstance(child, nodes.title)]
        if len(titles) != 1:
            raise self.error(
                f"Cannot find single title for section {section} - found {titles}"
            )
        title = titles[0]

        indexnode = addnodes.index(entries=[])
        node_id = make_id(
            self.env,
            self.state.document,
            "role_entrypoint",
            f"{content.fqcn}#{content.entrypoint}",
        )
        title["ids"].append(node_id)
        self.state.document.note_explicit_target(title)
        indexnode["entries"].append(
            (
                "single",
                f"role; {content.fqcn}; {content.entrypoint} entrypoint",
                node_id,
                "",
                None,
            )
        )
        ansible = t.cast(AnsibleDomain, self.env.get_domain("ansible"))
        ansible.note_object(
            "role_entrypoint",
            f"{content.fqcn}#{content.entrypoint}",
            node_id,
            location=title,
        )

        return [indexnode]


def _plugin_name(fqcn: str, plugin_type: str) -> str:
    if plugin_type in ("module", "role"):
        return f"{fqcn} {plugin_type}"
    return f"{fqcn} {plugin_type} plugin"


class _RequirementsAnchor(YAMLDirective[AnsibleRequirementsAnchor]):
    schema = AnsibleRequirementsAnchor

    def _run(
        self, content_str: str, content: AnsibleRequirementsAnchor
    ) -> list[nodes.Node]:
        section = self.state.parent
        titles = [child for child in section.children if isinstance(child, nodes.title)]
        if len(titles) != 1:
            raise self.error(
                f"Cannot find single title for section {section} - found {titles}"
            )
        title = titles[0]
        self.state.document.note_explicit_target(title)
        std = t.cast(StandardDomain, self.env.get_domain("std"))
        rst_id = (
            f"ansible_collections.{content.fqcn}_{content.plugin_type}_requirements"
        )
        ref_title = (
            f"Requirements of the {_plugin_name(content.fqcn, content.plugin_type)}"
        )
        if content.role_entrypoint is not None and content.plugin_type == "role":
            rst_id = (
                f"ansible_collections.{content.fqcn}_role"
                f"-{content.role_entrypoint}_requirements"
            )
            ref_title = f"{ref_title}, {content.role_entrypoint} entrypoint"
        std.note_hyperlink_target(
            rst_id,
            self.env.docname,
            title["ids"][0],
            ref_title,
        )
        return []


def _percent_encode(s):
    return _urllib_quote(s, safe="")


class _Attribute(YAMLDirective[AnsibleAttribute]):
    schema = AnsibleAttribute

    def _run(self, content_str: str, content: AnsibleAttribute) -> list[nodes.Node]:
        html_id = f"attribute-{_percent_encode(content.name)}"
        rst_id = (
            f"ansible_collections.{content.fqcn}_{content.plugin_type}"
            f"__attribute-{content.name}"
        )
        node = ansible_attribute(
            "", content.name, classes=["ansible-option-title"], ids=[html_id]
        )
        self.state.document.note_explicit_target(node)
        std = t.cast(StandardDomain, self.env.get_domain("std"))
        std.note_hyperlink_target(
            rst_id,
            self.env.docname,
            html_id,
            f"{content.name} attribute of {_plugin_name(content.fqcn, content.plugin_type)}",
        )
        permalink = nodes.raw(
            "",
            f' <a class="ansibleOptionLink" href="#{html_id}"'
            ' title="Permalink to this attribute"></a>',
            format="html",
        )
        return [node, permalink]


def _make_unique(ids: list[str]) -> list[str]:
    result = sorted(set(ids))
    if ids:
        result.remove(ids[0])
        result.insert(0, ids[0])
    return result


def _compile_ids(
    fqcn: str,
    plugin_type: str,
    role_entrypoint: str | None,
    full_keys: list[list[str]],
    prefix_type: str,
) -> tuple[dict[str, tuple[str, str]], list[str]]:
    rst_id_prefix = f"ansible_collections.{fqcn}_{plugin_type}__{prefix_type}-"
    html_id_prefix = f"{prefix_type}-"
    if role_entrypoint is not None:
        rst_id_prefix += f"{role_entrypoint}__"
        html_id_prefix += f"{role_entrypoint}--"
    rst_ids = {}
    html_ids = []
    for full_key in full_keys:
        html_id = html_id_prefix + "/".join([_percent_encode(k) for k in full_key])
        rst_id = rst_id_prefix + "/".join([massage_rst_label(k) for k in full_key])
        html_ids.append(html_id)
        rst_ids[rst_id] = (html_id, ".".join(full_key))
    return rst_ids, _make_unique(html_ids)


class _Option(YAMLDirective[AnsibleOption]):
    schema = AnsibleOption

    def _run(self, content_str: str, content: AnsibleOption) -> list[nodes.Node]:
        rst_ids, html_ids = _compile_ids(
            content.fqcn,
            content.plugin_type,
            content.role_entrypoint,
            content.full_keys,
            "parameter",
        )
        node = ansible_option(
            "",
            content.name,
            classes=["ansible-option-title"],
            ids=html_ids,
        )
        self.state.document.note_explicit_target(node)
        std = t.cast(StandardDomain, self.env.get_domain("std"))
        for rst_id, (html_id, key) in rst_ids.items():
            std.note_hyperlink_target(
                rst_id,
                self.env.docname,
                html_id,
                f"{key} option of {_plugin_name(content.fqcn, content.plugin_type)}",
            )
        permalink = nodes.raw(
            "",
            f' <a class="ansibleOptionLink" href="#{html_ids[0]}"'
            ' title="Permalink to this option"></a>',
            format="html",
        )
        return [node, permalink]


class _ReturnValue(YAMLDirective[AnsibleReturnValue]):
    schema = AnsibleReturnValue

    def _run(self, content_str: str, content: AnsibleReturnValue) -> list[nodes.Node]:
        rst_ids, html_ids = _compile_ids(
            content.fqcn,
            content.plugin_type,
            content.role_entrypoint,
            content.full_keys,
            "return",
        )
        node = ansible_return_value(
            "",
            content.name,
            classes=["ansible-option-title"],
            ids=html_ids,
        )
        self.state.document.note_explicit_target(node)
        std = t.cast(StandardDomain, self.env.get_domain("std"))
        for rst_id, (html_id, key) in rst_ids.items():
            std.note_hyperlink_target(
                rst_id,
                self.env.docname,
                html_id,
                f"{key} return value of {_plugin_name(content.fqcn, content.plugin_type)}",
            )
        permalink = nodes.raw(
            "",
            f' <a class="ansibleOptionLink" href="#{html_ids[0]}"'
            ' title="Permalink to this return value"></a>',
            format="html",
        )
        return [node, permalink]


DIRECTIVES = {
    "ansible-option-type-line": _OptionTypeLine,
    "ansible-links": _Links,
    "ansible-plugin": _Plugin,
    "ansible-role-entrypoint": _RoleEntrypoint,
    "ansible-requirements-anchor": _RequirementsAnchor,
    "ansible-attribute": _Attribute,
    "ansible-option": _Option,
    "ansible-return-value": _ReturnValue,
}


def setup_directives(app):
    """
    Setup directives for a Sphinx app object.
    """
    app.add_domain(AnsibleDomain)
    for name, directive in DIRECTIVES.items():
        app.add_directive(name, directive)
