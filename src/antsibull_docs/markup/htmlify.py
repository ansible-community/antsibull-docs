# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
"""
htmlify Jinja2 filter for use in Ansible documentation.
"""

import typing as t

from urllib.parse import quote

from . import dom
from ._counter import count as _count
from .parser import parse, Context
from .html import to_html
from .format import LinkProvider


class _HTMLLinkProvider(LinkProvider):
    def plugin_link(self, plugin: dom.PluginIdentifier) -> t.Optional[str]:
        name = '/'.join(plugin.fqcn.split('.', 2))
        return f'../../{name}_{plugin.type}.html'

    def plugin_option_like_link(self,
                                plugin: dom.PluginIdentifier,
                                what: "t.Union[t.Literal['option'], t.Literal['retval']]",
                                name: t.List[str], current_plugin: bool) -> t.Optional[str]:
        base = '' if current_plugin else self.plugin_link(plugin)
        w = 'parameter' if what == 'option' else 'return'
        slug = quote('/'.join(name))
        return f'{base}#{w}-{slug}'


def html_ify(text: str,
             *,
             plugin_fqcn: t.Optional[str] = None,
             plugin_type: t.Optional[str] = None) -> t.Tuple[str, t.Mapping[str, int]]:
    ''' convert symbols like I(this is in italics) to valid HTML '''
    current_plugin: t.Optional[dom.PluginIdentifier] = None
    if plugin_fqcn and plugin_type:
        current_plugin = dom.PluginIdentifier(fqcn=plugin_fqcn, type=plugin_type)
    paragraphs = parse(text, Context(current_plugin=current_plugin), errors='message')
    link_provider = _HTMLLinkProvider()
    text = to_html(
        paragraphs,
        link_provider=link_provider,
        current_plugin=current_plugin,
        par_start='',
        par_end='',
    )
    counts = _count(paragraphs)
    return text, counts
