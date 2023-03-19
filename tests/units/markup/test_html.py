# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project

from antsibull_docs.markup import dom
from antsibull_docs.markup.html import html_escape, to_html, to_html_plain


def test_html_escape():
    assert html_escape('') == ''
    assert html_escape(' foo ') == ' foo '
    assert html_escape('<a href="a&b">&lt;&amp;&gt;</a>') == '&lt;a href="a&amp;b"&gt;&amp;lt;&amp;amp;&amp;gt;&lt;/a&gt;'

def test_to_html():
    assert to_html([]) == ''
    assert to_html([[dom.TextPart(text='test')]]) == '<p>test</p>'
    assert to_html([[dom.TextPart(text='test')]], par_start='<div>', par_end='</div>') == '<div>test</div>'
    assert to_html([[dom.CodePart(text='test')]]) == "<p><code class='docutils literal notranslate'>test</code></p>"

def test_to_html_plain():
    assert to_html_plain([]) == ''
    assert to_html_plain([[dom.TextPart(text='test')]]) == '<p>test</p>'
    assert to_html_plain([[dom.TextPart(text='test')]], par_start='<div>', par_end='</div>') == '<div>test</div>'
    assert to_html_plain([[dom.CodePart(text='test')]]) == '<p><code>test</code></p>'
