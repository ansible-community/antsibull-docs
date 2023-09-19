# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
Add domains.
"""

from __future__ import annotations

import typing as t

from docutils.nodes import Element
from sphinx import addnodes, domains
from sphinx.builders import Builder
from sphinx.environment import BuildEnvironment
from sphinx.locale import _
from sphinx.util import logging

logger = logging.getLogger(__name__)


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


def setup_domains(app):
    """
    Setup domains for a Sphinx app object.
    """
    app.add_domain(AnsibleDomain)
