# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Test the set of Schemas altogether to see that they will parse information correctly.
"""

from __future__ import annotations

import json
import os.path

import pytest

from antsibull_docs.schemas.docs import ansible_doc as ad

# To generate the data in the one_*.json files, run::
#   ansible-doc --json -t $PLUGIN_TYPE $PLUGIN_NAME > \
#       tests/functional/schema/good_data/one_$PLUGINTYPE.json
#
# The matching one_$PLUGINTYPE_results.json file is created by running the schema over the
# input, dumping that to one_$PLUGINTYPE_results.json, and then manually inspecting it to
# make sure it is correct.  Due to the manual inspection, these might be considered better
# at catching regressions than at detecting errors in fresh code.  Some sample python code for
# dumping the file::
#
#   import json
#   from antsibull_docs.schemas.docs.ansible_doc import ConnectionPluginSchema
#   raw = open('one_connection.json').read()
#   normalized = ConnectionPluginSchema.model_validate_json(raw)
#   out = json.dumps(normalized.model_dump(), indent=4, sort_keys=True)
#   open('one_connection_results.json', 'w').write(out)
#
# To re-generate the EDA schemas, run::
#
#   python3 tests/functional/schema/test_schema.py

SINGLE_TESTS = {
    "one_become.json": ad.BecomePluginSchema,
    "one_cache.json": ad.CachePluginSchema,
    "one_callback.json": ad.CallbackPluginSchema,
    "one_cliconf.json": ad.CliConfPluginSchema,
    "one_connection.json": ad.ConnectionPluginSchema,
    # The ssh connection plugin is the only one which can take values directly from
    # dedicated command line arguments in ansible and ansible-playbook.  Make sure that
    # we can deal with its documentation to test that the cli field they use for that works.
    "ssh_connection.json": ad.ConnectionPluginSchema,
    "one_eda_event_filter.json": ad.EdaEventFilterPluginSchema,
    "one_eda_event_source.json": ad.EdaEventSourcePluginSchema,
    "one_filter.json": ad.FilterPluginSchema,
    "one_httpapi.json": ad.HttpApiPluginSchema,
    "one_inventory.json": ad.InventoryPluginSchema,
    "one_lookup.json": ad.LookupPluginSchema,
    "one_module.json": ad.ModulePluginSchema,
    "one_netconf.json": ad.NetConfPluginSchema,
    "one_role.json": ad.RolePluginSchema,
    "one_shell.json": ad.ShellPluginSchema,
    "one_strategy.json": ad.StrategyPluginSchema,
    "one_test.json": ad.TestPluginSchema,
    "one_vars.json": ad.VarsPluginSchema,
}


@pytest.mark.parametrize("test_file, test_schema", SINGLE_TESTS.items())
def test_plugin_schemas(test_file, test_schema):
    base_name, extension = os.path.splitext(os.path.basename(test_file))

    test_dir = os.path.dirname(__file__)
    result_file = os.path.join(test_dir, "good_data", f"{base_name}_results{extension}")
    full_path = os.path.join(test_dir, "good_data", test_file)

    with open(result_file) as f:
        results = json.load(f)

    with open(full_path) as f:
        ansible_doc_output = f.read()

    model = test_schema.model_validate_json(ansible_doc_output)

    model_dict = {"__root__": model.model_dump()}
    if model_dict != results:
        print(json.dumps(model_dict, indent=4))
    assert model_dict == results


def create_eda_schemas() -> None:
    import asyncio

    from antsibull_core.venv import FakeVenvRunner

    from antsibull_docs.docs_parsing.antsibull_docs_loader import (
        get_ansible_plugin_info,
    )

    test_dir = os.path.dirname(__file__)
    plugin_map = asyncio.run(
        get_ansible_plugin_info(
            FakeVenvRunner(), os.path.join(test_dir, "..", "collections"), ["ns.col2"]
        )
    )[0]

    schema_dir = os.path.join(test_dir, "good_data")
    for basename, schema, docs, fqcn in [
        (
            "one_eda_event_filter",
            ad.EdaEventFilterPluginSchema,
            plugin_map["eda_event_filter"],
            "ns.col2.foo",
        ),
        (
            "one_eda_event_source",
            ad.EdaEventSourcePluginSchema,
            plugin_map["eda_event_source"],
            "ns.col2.foo",
        ),
    ]:
        ansible_doc_output = {fqcn: docs[fqcn]}
        with open(
            os.path.join(schema_dir, f"{basename}.json"), "wt", encoding="utf-8"
        ) as f:
            f.write(json.dumps(ansible_doc_output, sort_keys=True, indent=4))
        model = schema.model_validate(ansible_doc_output)
        model_dict = {"__root__": model.model_dump()}
        with open(
            os.path.join(schema_dir, f"{basename}_results.json"), "wt", encoding="utf-8"
        ) as f:
            f.write(json.dumps(model_dict, sort_keys=True, indent=4))


if __name__ == "__main__":
    create_eda_schemas()
