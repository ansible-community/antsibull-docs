# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""Environment variable handling."""

import os
import os.path
import typing as t

from antsibull_core import yaml

from .docs_parsing import AnsibleCollectionMetadata


class EnvironmentVariableInfo:
    name: str
    description: t.Optional[t.List[str]]
    plugins: t.Dict[str, t.List[str]]  # maps plugin_type to lists of plugin FQCNs

    def __init__(self,
                 name: str,
                 description: t.Optional[t.List[str]] = None,
                 plugins: t.Optional[t.Dict[str, t.List[str]]] = None):
        self.name = name
        self.description = description
        self.plugins = plugins or {}

    def __repr__(self):
        return f'E({self.name}, description={repr(self.description)}, plugins={self.plugins})'


def load_ansible_config(ansible_builtin_metadata: AnsibleCollectionMetadata
                        ) -> t.Mapping[str, t.Mapping[str, t.Any]]:
    """
    Load Ansible base configuration (``lib/ansible/config/base.yml``).

    :arg ansible_builtin_metadata: Metadata for the ansible.builtin collection.
    :returns: A Mapping of configuration options to information on these options.
    """
    return yaml.load_yaml_file(os.path.join(ansible_builtin_metadata.path, 'config', 'base.yml'))


def _find_env_vars(options: t.Mapping[str, t.Mapping[str, t.Any]]
                   ) -> t.Generator[t.Tuple[str, t.Optional[t.List[str]]], None, None]:
    for _, option_data in options.items():
        if isinstance(option_data.get('env'), list):
            description = option_data.get('description')
            if isinstance(description, str):
                description = [description]
            if isinstance(description, list):
                description = [str(desc) for desc in description]
            else:
                description = None
            for env_var in option_data['env']:
                if isinstance(env_var.get('name'), str):
                    yield (env_var['name'], description)
        if isinstance(option_data.get('suboptions'), dict):
            yield from _find_env_vars(option_data['suboptions'])


def _collect_env_vars_and_descriptions(plugin_info: t.Mapping[str, t.Mapping[str, t.Any]],
                                       core_envs: t.Set[str],
                                       ) -> t.Tuple[t.Mapping[str, EnvironmentVariableInfo],
                                                    t.Mapping[str, t.List[t.List[str]]]]:
    other_variables: t.Dict[str, EnvironmentVariableInfo] = {}
    other_variable_description: t.Dict[str, t.List[t.List[str]]] = {}
    for plugin_type, plugins in plugin_info.items():
        for plugin_name, plugin_data in plugins.items():
            plugin_options: t.Mapping[str, t.Mapping[str, t.Any]] = (
                (plugin_data.get('doc') or {}).get('options') or {}
            )
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


def _augment_env_var_descriptions(other_variables: t.Mapping[str, EnvironmentVariableInfo],
                                  other_variable_description: t.Mapping[str, t.List[t.List[str]]],
                                  ) -> None:
    for variable, variable_info in other_variables.items():
        if other_variable_description[variable]:
            value: t.Optional[t.List[str]] = other_variable_description[variable][0]
            for other_value in other_variable_description[variable]:
                if value != other_value:
                    value = [
                        'See the documentations for the options where this environment variable'
                        ' is used.'
                    ]
                    break
            variable_info.description = value


def collect_referenced_environment_variables(plugin_info: t.Mapping[str, t.Mapping[str, t.Any]],
                                             ansible_config: t.Mapping[str, t.Mapping[str, t.Any]],
                                             ) -> t.Mapping[str, EnvironmentVariableInfo]:
    """
    Collect referenced environment variables that are not defined in the ansible-core
    configuration.

    :arg plugin_info: Mapping of plugin type to a mapping of plugin name to plugin record.
    :arg ansible_config: The Ansible base configuration (``lib/ansible/config/base.yml``).
    :returns: A Mapping of environment variable name to an environment variable infomation object.
    """
    core_envs = {'ANSIBLE_CONFIG'}
    for config in ansible_config.values():
        if config.get('env'):
            for env in config['env']:
                core_envs.add(env['name'])

    other_variables, other_variable_description = _collect_env_vars_and_descriptions(
        plugin_info, core_envs)
    _augment_env_var_descriptions(other_variables, other_variable_description)
    return other_variables
