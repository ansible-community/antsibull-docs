# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022, Ansible Project
'''
Add roles for semantic markup.
'''

from docutils import nodes


# pylint:disable-next=unused-argument,dangerous-default-value
def option_choice(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible option choice entry.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return [nodes.literal(rawtext, text, classes=['ansible-option-choices-entry'])], []


# pylint:disable-next=unused-argument,dangerous-default-value
def option_choice_default(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible option choice entry that is the default.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return [nodes.literal(rawtext, text, classes=['ansible-option-default-bold'])], []


# pylint:disable-next=unused-argument,dangerous-default-value
def option_default(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible option default value.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return [nodes.literal(rawtext, text, classes=['ansible-option-default'])], []


# pylint:disable-next=unused-argument,dangerous-default-value
def return_value_sample(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Format Ansible return value sample value.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return [nodes.literal(rawtext, text, classes=['ansible-option-sample'])], []


ROLES = {
    'ansible-option-choices-entry': option_choice,
    'ansible-option-choices-entry-default': option_choice_default,
    'ansible-option-default': option_default,
    'ansible-rv-sample-value': return_value_sample,
}


def setup_roles(app):
    '''
    Setup roles for a Sphinx app object.
    '''
    for name, role in ROLES.items():
        app.add_role(name, role)
