# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""
Schemas for the plugin DOCUMENTATION data.

This is a highlevel interface.  The hope is that developers can use either this or
antsibull.schemas.docs to handle all of their validation needs.
"""

from __future__ import annotations

import pydantic as p

from .base import BaseModel
from .callback import CallbackSchema
from .module import ModuleSchema
from .plugin import PluginSchema
from .positional import PositionalSchema
from .role import RoleSchema

__all__ = (
    "ANSIBLE_DOC_SCHEMAS",
    "AnsibleDocSchema",
    "BecomePluginSchema",
    "CachePluginSchema",
    "CallbackPluginSchema",
    "CliConfPluginSchema",
    "ConnectionPluginSchema",
    "HttpApiPluginSchema",
    "InventoryPluginSchema",
    "LookupPluginSchema",
    "ModulePluginSchema",
    "NetConfPluginSchema",
    "ShellPluginSchema",
    "StrategyPluginSchema",
    "VarsPluginSchema",
    "TestPluginSchema",
    "FilterPluginSchema",
)


class AnsibleDocSchema(BaseModel):
    """
    Document the output that comes back from ansible-doc.

    This schema is a constructed schema.  It imagines that the user has accumulated the output from
    repeated runs of ansible-doc in a dict layed out roughly like this:

    .. code-block:: yaml

        plugin_type:
            plugin_name:
                # json.loads(ansible-doc -t plugin_type --json plugin_name)

    Pass the dict above to :meth:`AnsibleDocSchema.model_validate` to build the models from the
    schema.

    If you want to use the Schema to validate and normalize the data but need a :python:obj:`dict`
    afterwards, call :meth:`AnsibleDocSchema.dict` on the populated model to get
    a :python:obj:`dict` back out.
    """

    become: dict[str, PluginSchema]
    cache: dict[str, PluginSchema]
    callback: dict[str, CallbackSchema]
    cliconf: dict[str, PluginSchema]
    connection: dict[str, PluginSchema]
    filter: dict[str, PositionalSchema]
    httpapi: dict[str, PluginSchema]
    inventory: dict[str, PluginSchema]
    lookup: dict[str, PositionalSchema]
    module: dict[str, ModuleSchema]
    netconf: dict[str, PluginSchema]
    shell: dict[str, PluginSchema]
    strategy: dict[str, PluginSchema]
    test: dict[str, PositionalSchema]
    vars: dict[str, PluginSchema]
    role: dict[str, RoleSchema]


GenericPluginSchema = p.RootModel[dict[str, PluginSchema]]
"""
Document the output of ``ansible-doc -t PLUGIN_TYPE PLUGIN_NAME``.
"""


CallbackPluginSchema = p.RootModel[dict[str, CallbackSchema]]
"""
Document the output of ``ansible-doc -t callback CALLBACK_NAME``.
"""


PositionalPluginSchema = p.RootModel[dict[str, PositionalSchema]]
"""
Document the output of ``ansible-doc -t lookup CALLBACK_NAME``, or ``-t filter``, ``-t test``.
"""


ModulePluginSchema = p.RootModel[dict[str, ModuleSchema]]
"""
Document the output of ``ansible-doc -t module MODULE_NAME``.
"""


RolePluginSchema = p.RootModel[dict[str, RoleSchema]]
"""
Document the output of ``ansible-doc -t role ROLE_NAME``.
"""


#: Make sure users can access plugins using the plugin type rather than having to guess that
#: these types use the GenericPluginSchema
BecomePluginSchema = GenericPluginSchema
CachePluginSchema = GenericPluginSchema
CliConfPluginSchema = GenericPluginSchema
ConnectionPluginSchema = GenericPluginSchema
HttpApiPluginSchema = GenericPluginSchema
InventoryPluginSchema = GenericPluginSchema
LookupPluginSchema = PositionalPluginSchema
NetConfPluginSchema = GenericPluginSchema
ShellPluginSchema = GenericPluginSchema
StrategyPluginSchema = GenericPluginSchema
VarsPluginSchema = GenericPluginSchema
TestPluginSchema = PositionalPluginSchema
FilterPluginSchema = PositionalPluginSchema


#: A mapping from plugin type to the Schema to use for them.  Use this to more easily get
#: the Schema programmatically.
ANSIBLE_DOC_SCHEMAS = {
    "become": BecomePluginSchema,
    "cache": CachePluginSchema,
    "callback": CallbackPluginSchema,
    "cliconf": CliConfPluginSchema,
    "connection": ConnectionPluginSchema,
    "filter": FilterPluginSchema,
    "httpapi": HttpApiPluginSchema,
    "inventory": InventoryPluginSchema,
    "lookup": LookupPluginSchema,
    "module": ModulePluginSchema,
    "netconf": NetConfPluginSchema,
    "role": RolePluginSchema,
    "shell": ShellPluginSchema,
    "strategy": StrategyPluginSchema,
    "test": TestPluginSchema,
    "vars": VarsPluginSchema,
}
