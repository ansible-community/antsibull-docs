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
SINGLE_TESTS = {
    "one_become.json": ad.BecomePluginSchema,
    "one_cache.json": ad.CachePluginSchema,
    "one_callback.json": ad.CallbackPluginSchema,
    "one_cliconf.json": ad.CliConfPluginSchema,
    "one_connection.json": ad.ConnectionPluginSchema,
    "one_filter.json": ad.FilterPluginSchema,
    "one_httpapi.json": ad.HttpApiPluginSchema,
    "one_inventory.json": ad.InventoryPluginSchema,
    "one_lookup.json": ad.LookupPluginSchema,
    "one_module.json": ad.ModulePluginSchema,
    "one_netconf.json": ad.NetConfPluginSchema,
    "one_shell.json": ad.ShellPluginSchema,
    "one_strategy.json": ad.StrategyPluginSchema,
    "one_test.json": ad.TestPluginSchema,
    "one_vars.json": ad.VarsPluginSchema,
}


@pytest.mark.parametrize("test_file, test_schema", SINGLE_TESTS.items())
def test_one_plugin_of_each_type(test_file, test_schema):
    plugin_type = os.path.splitext(os.path.basename(test_file))[0]
    plugin_type = plugin_type[len("one_") :]

    test_dir = os.path.dirname(__file__)
    result_file = os.path.join(
        test_dir, "good_data", "one_%s_results.json" % plugin_type
    )
    full_path = os.path.join(test_dir, "good_data", test_file)

    with open(result_file) as f:
        results = json.load(f)

    with open(full_path) as f:
        ansible_doc_output = f.read()

    model = test_schema.model_validate_json(ansible_doc_output)

    model_dict = {"__root__": model.model_dump()}
    assert model_dict == results


def test_ssh_connection():
    """Test using the cli field with the ssh connection."""

    # The ssh connection plugin is the only one which can take values directly from
    # dedicated command line arguments in ansible and ansible-playbook.  Make sure that
    # we can deal with its documentation to test that the cli field they use for that works.

    test_file = "ssh_connection.json"
    test_schema = ad.ConnectionPluginSchema

    test_dir = os.path.dirname(__file__)
    result_file = os.path.join(test_dir, "good_data", "ssh_connection_results.json")
    full_path = os.path.join(test_dir, "good_data", test_file)

    with open(result_file) as f:
        results = json.load(f)

    with open(full_path) as f:
        ansible_doc_output = f.read()

    model = test_schema.model_validate_json(ansible_doc_output)

    model_dict = {"__root__": model.model_dump()}
    assert model_dict == results
