# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project

import typing as t

import pytest

from antsibull_core.yaml import load_yaml_file

from antsibull_docs.markup import dom
from antsibull_docs.markup.parser import parse, Context
from antsibull_docs.markup.html import to_html
from antsibull_docs.markup.md import to_md
from antsibull_docs.markup.rst import to_rst
from antsibull_docs.markup.format import LinkProvider


class _TestLinkProvider(LinkProvider):
    _plugin_link = None
    _plugin_option_like_link = None

    def plugin_link(self, plugin: dom.PluginIdentifier) -> t.Optional[str]:
        if self._plugin_link is not None:
            return self._plugin_link(plugin)
        return None

    def plugin_option_like_link(self,
                                plugin: dom.PluginIdentifier,
                                what: "t.Union[t.Literal['option'], t.Literal['retval']]",
                                name: t.List[str], current_plugin: bool) -> t.Optional[str]:
        if self._plugin_option_like_link is not None:
            return self._plugin_option_like_link(plugin, what, name, current_plugin)
        return None

    def _update(self, config: t.Mapping[str, t.Any]):
        if 'pluginLink.py' in config:
            self._plugin_link = eval(config['pluginLink.py'])
        if 'pluginOptionLikeLink.py' in config:
            self._plugin_option_like_link = eval(config['pluginOptionLikeLink.py'])


TEST_DATA = sorted(load_yaml_file('test-vectors.yaml')['test_vectors'].items())


@pytest.mark.parametrize('test_name, test_data', TEST_DATA, ids=[test_name for test_name, test_data in TEST_DATA])
def test_vectors(test_name: str, test_data: t.Mapping[str, t.Any]) -> None:
    parse_opts = {}
    context_opts = {}
    if test_data.get('parse_opts'):
        if 'current_plugin' in test_data['parse_opts']:
            context_opts['current_plugin'] = dom.PluginIdentifier(
                fqcn=test_data['parse_opts']['current_plugin']['fqcn'],
                type=test_data['parse_opts']['current_plugin']['type'],
            )
        if 'errors' in test_data['parse_opts']:
            context_opts['errors'] = test_data['parse_opts']['errors']
        if 'onlyClassicMarkup' in test_data['parse_opts']:
            context_opts['only_classic_markup'] = test_data['parse_opts']['onlyClassicMarkup']
    parsed = parse(test_data['source'], Context(**context_opts), **parse_opts)

    html_opts = {}
    html_link_provider = _TestLinkProvider()
    if test_data.get('html_opts'):
        if 'parStart' in test_data['html_opts']:
            html_opts['par_start'] = test_data['html_opts']['parStart']
        if 'parEnd' in test_data['html_opts']:
            html_opts['par_end'] = test_data['html_opts']['parEnd']
        if 'current_plugin' in test_data['html_opts']:
            rst_opts['current_plugin'] = dom.PluginIdentifier(
                fqcn=test_data['html_opts']['current_plugin']['fqcn'],
                type=test_data['html_opts']['current_plugin']['type'],
            )
        html_link_provider._update(test_data['html_opts'])

    md_opts = {}
    md_link_provider = _TestLinkProvider()
    if test_data.get('md_opts'):
        if 'current_plugin' in test_data['md_opts']:
            rst_opts['current_plugin'] = dom.PluginIdentifier(
                fqcn=test_data['md_opts']['current_plugin']['fqcn'],
                type=test_data['md_opts']['current_plugin']['type'],
            )
        md_link_provider._update(test_data['md_opts'])

    rst_opts = {}
    if test_data.get('rst_opts'):
        if 'current_plugin' in test_data['rst_opts']:
            rst_opts['current_plugin'] = dom.PluginIdentifier(
                fqcn=test_data['rst_opts']['current_plugin']['fqcn'],
                type=test_data['rst_opts']['current_plugin']['type'],
            )

    if 'html' in test_data:
        result = to_html(parsed, link_provider=html_link_provider, **html_opts)
        assert result == test_data['html']

    if 'html_plain' in test_data:
        ...
        # TODO result = to_html(parsed, link_provider=html_link_provider, **html_opts)
        # TODO assert result == test_data['html_plain']

    if 'md' in test_data:
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        result = to_md(parsed, link_provider=md_link_provider, **md_opts)
        assert result == test_data['md']

    if 'rst' in test_data:
        result = to_rst(parsed, **rst_opts)
        assert result == test_data['rst']
