# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project

from antsibull_docs.markup import dom
from antsibull_docs.markup.md import md_escape, to_md


def test_md_escape():
    assert md_escape('') == ''
    assert md_escape('  foo  ') == '  foo  '
    assert md_escape(r'[]!.()-\@<>?[]!.()-\@<>?') == r'\[\]\!.\(\)\-\\\@\<\>\?\[\]\!.\(\)\-\\\@\<\>\?'

def test_to_rst():
    assert to_md([]) == ''
    assert to_md([[dom.TextPart(text='test')]]) == 'test'
