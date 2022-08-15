# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2019, Ansible Project
"""
Jinja2 filters for use in Ansible documentation.
"""

import json
import re

import typing as t

from jinja2.runtime import Undefined

from antsibull_core.logging import log


mlog = log.fields(mod=__name__)

_EMAIL_ADDRESS = re.compile(r"(?:<{mail}>|\({mail}\)|{mail})".format(mail=r"[\w.+-]+@[\w.-]+\.\w+"))


def documented_type(text) -> str:
    ''' Convert any python type to a type for documentation '''

    if isinstance(text, Undefined):
        return '-'
    if text == 'str':
        return 'string'
    if text == 'bool':
        return 'boolean'
    if text == 'int':
        return 'integer'
    if text == 'dict':
        return 'dictionary'
    return text


# The max filter was added in Jinja2-2.10.  Until we can require that version, use this
def do_max(seq):
    return max(seq)


def rst_fmt(text, fmt):
    ''' helper for Jinja2 to do format strings '''

    return fmt % (text)


def rst_xline(width, char="="):
    ''' return a restructured text line of a given length '''

    return char * width


def move_first(sequence, *move_to_beginning):
    ''' return a copy of sequence where the elements which are in move_to_beginning are
        moved to its beginning if they appear in the list '''

    remaining = list(sequence)
    beginning = []
    for elt in move_to_beginning:
        try:
            remaining.remove(elt)
            beginning.append(elt)
        except ValueError:
            # elt not found in remaining
            pass

    return beginning + remaining


def massage_author_name(value):
    ''' remove email addresses from the given string, and remove `(!UNKNOWN)` '''
    value = _EMAIL_ADDRESS.sub('', value)
    value = value.replace('(!UNKNOWN)', '')
    return value


def extract_options_from_list(options: t.Dict[str, t.Any],
                              options_to_extract: t.List[str],
                              options_to_ignore: t.Optional[t.List[str]] = None
                              ) -> t.List[t.Tuple[str, t.Any]]:
    ''' return list of tuples (option, option_data) with option from options_to_extract '''
    if options_to_ignore is None:
        options_to_ignore = []
    return [
        (option, options[option]) for option in options_to_extract
        if option in options and option not in options_to_ignore
    ]


def remove_options_from_list(options: t.Dict[str, t.Any],
                             options_to_remove: t.List[str]) -> t.Dict[str, t.Any]:
    ''' return copy of dictionary with the options from options_to_remove removed '''
    result = options.copy()
    for option in options_to_remove:
        result.pop(option, None)
    return result


def to_json(data: t.Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(', ', ': '))
