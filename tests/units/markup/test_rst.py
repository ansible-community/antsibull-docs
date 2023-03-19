# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project

from antsibull_docs.markup import dom
from antsibull_docs.markup.rst import rst_escape, to_rst


def test_rst_escape():
    assert rst_escape('') == ''
    assert rst_escape('  foo  ') == '  foo  '
    assert rst_escape('  foo  ', True) == '\\   foo  \\ '
    assert rst_escape('\\<_>`*<_>*`\\') == '\\\\\\<\\_\\>\\`\\*\\<\\_\\>\\*\\`\\\\'

def test_to_rst():
    assert to_rst([]) == ''
    assert to_rst([[dom.TextPart(text='test')]]) == 'test'
