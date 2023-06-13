# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Environment variable handling."""

from __future__ import annotations

import os
import os.path
import typing as t
from collections.abc import Generator, Mapping

from antsibull_core import yaml

from .docs_parsing import AnsibleCollectionMetadata


class EnvironmentVariableInfo:
    name: str
    description: list[str] | None
    plugins: dict[str, list[str]]  # maps plugin_type to lists of plugin FQCNs

    def __init__(
        self,
        name: str,
        description: list[str] | None = None,
        plugins: dict[str, list[str]] | None = None,
    ):
        self.name = name
        self.description = description
        self.plugins = plugins or {}

    def __repr__(self):
        return f"E({self.name}, description={repr(self.description)}, plugins={self.plugins})"


def load_ansible_config(
    ansible_builtin_metadata: AnsibleCollectionMetadata,
) -> Mapping[str, Mapping[str, t.Any]]:
    """
    Load Ansible base configuration (``lib/ansible/config/base.yml``).

    :arg ansible_builtin_metadata: Metadata for the ansible.builtin collection.
    :returns: A Mapping of configuration options to information on these options.
    """
    return yaml.load_yaml_file(
        os.path.join(ansible_builtin_metadata.path, "config", "base.yml")
    )


def _find_env_vars(
    options: Mapping[str, Mapping[str, t.Any]]
) -> Generator[tuple[str, list[str] | None], None, None]:
    for _, option_data in options.items():
        if isinstance(option_data.get("env"), list):
            description = option_data.get("description")
            if isinstance(description, str):
                description = [description]
            if isinstance(description, list):
                description = [str(desc) for desc in description]
            else:
                description = None
            for env_var in option_data["env"]:
                if isinstance(env_var.get("name"), str):
                    yield (env_var["name"], description)
        if isinstance(option_data.get("suboptions"), dict):
            yield from _find_env_vars(option_data["suboptions"])


def _collect_env_vars_and_descriptions(
    plugin_info: Mapping[str, Mapping[str, t.Any]],
    core_envs: set[str],
) -> tuple[Mapping[str, EnvironmentVariableInfo], Mapping[str, list[list[str]]]]:
    other_variables: dict[str, EnvironmentVariableInfo] = {}
    other_variable_description: dict[str, list[list[str]]] = {}
    for plugin_type, plugins in plugin_info.items():
        for plugin_name, plugin_data in plugins.items():
            plugin_options: Mapping[str, Mapping[str, t.Any]] = (
                plugin_data.get("doc") or {}
            ).get("options") or {}
            for env_var, env_var_description in _find_env_vars(plugin_options):
                if env_var in core_envs:
                    continue
                if env_var not in other_variables:
                    other_variables[env_var] = EnvironmentVariableInfo(env_var)
                    other_variable_description[env_var] = []
                if plugin_type not in other_variables[env_var].plugins:
                    other_variables[env_var].plugins[plugin_type] = []
                other_variables[env_var].plugins[plugin_type].append(plugin_name)
                if env_var_description is not None:
                    other_variable_description[env_var].append(env_var_description)
    return other_variables, other_variable_description


def _augment_env_var_descriptions(
    other_variables: Mapping[str, EnvironmentVariableInfo],
    other_variable_description: Mapping[str, list[list[str]]],
) -> None:
    for variable, variable_info in other_variables.items():
        if other_variable_description[variable]:
            value: list[str] | None = other_variable_description[variable][0]
            for other_value in other_variable_description[variable]:
                if value != other_value:
                    value = [
                        "See the documentations for the options where this environment variable"
                        " is used."
                    ]
                    break
            variable_info.description = value


def collect_referenced_environment_variables(
    plugin_info: Mapping[str, Mapping[str, t.Any]],
    ansible_config: Mapping[str, Mapping[str, t.Any]],
) -> tuple[Mapping[str, EnvironmentVariableInfo], set[str]]:
    """
    Collect referenced environment variables that are not defined in the ansible-core
    configuration.

    :arg plugin_info: Mapping of plugin type to a mapping of plugin name to plugin record.
    :arg ansible_config: The Ansible base configuration (``lib/ansible/config/base.yml``).
    :returns: A tuple consisting of a
        Mapping of environment variable name to an environment variable infomation object,
        and a set of environment variable names that are part of the ansible-core
        configuration.
    """
    core_envs = {"ANSIBLE_CONFIG"}
    for config in ansible_config.values():
        if config.get("env"):
            for env in config["env"]:
                core_envs.add(env["name"])

    other_variables, other_variable_description = _collect_env_vars_and_descriptions(
        plugin_info, core_envs
    )
    _augment_env_var_descriptions(other_variables, other_variable_description)
    return other_variables, core_envs


def collect_referable_envvars(
    referenced_env_vars: Mapping[str, EnvironmentVariableInfo],
    core_env_vars: set[str],
    collection_metadata: Mapping[str, AnsibleCollectionMetadata],
) -> set[str]:
    """
    :arg referenced_env_vars: A Mapping of environment variable name to an
        environment variable infomation object.
    :arg core_env_vars: Set of environment variable names that are part of the
        ansible-core configuration.
    :arg collection_metadata: A Mapping of collection names to collection metadata
        objects.
    :returns: A set of environment variables that can be referenced via the
        ``:envvar:`` role.
    """
    referable_envvars = set(referenced_env_vars)
    referable_envvars.update(core_env_vars)
    for collection_meta in collection_metadata.values():
        referable_envvars.update(collection_meta.docs_config.envvar_directives)
    return referable_envvars
