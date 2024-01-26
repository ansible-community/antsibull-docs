# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""Schemas for collection links files."""

# Ignore Unitialized attribute errors because BaseModel works some magic
# to initialize the attributes when data is loaded into them.
# pyre-ignore-all-errors[13]

import typing as t

from antsibull_docs._pydantic_compat import v1 as p

_SENTINEL = object()

GOOGLE_GROUPS_PREFIX = "https://groups.google.com/g/"


class CollectionEditOnGitHub(p.BaseModel):
    # Repository on GitHub (example: 'ansible-collections/community.general')
    repository: str

    # Branch name (example: 'main')
    branch: str

    # Path prefix (example: '')
    # Set to 'ansible_collections/community/general/' if the collection root in the repository
    # is inside a subdirectory ansible_collections/community/general/.
    path_prefix: str = ""

    @p.validator("path_prefix", pre=True)
    # pylint:disable=no-self-argument
    def ensure_trailing_slash(cls, obj):
        if isinstance(obj, str):
            obj = obj.rstrip("/")
            if obj:
                obj += "/"
        return obj


class Link(p.BaseModel):
    description: str
    url: str


class IRCChannel(p.BaseModel):
    topic: str
    network: str
    channel: str


class MatrixRoom(p.BaseModel):
    topic: str
    room: str


class MailingList(p.BaseModel):
    topic: str
    url: str
    subscribe: t.Optional[str] = None

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument
    def add_subscribe(cls, values):
        """If 'subscribe' is not provided, try to deduce it from the URL."""

        if values.get("subscribe", _SENTINEL) is _SENTINEL:
            url = str(values.get("url"))
            if url.startswith(GOOGLE_GROUPS_PREFIX):
                name = url[len(GOOGLE_GROUPS_PREFIX) :]
                values["subscribe"] = (
                    f"{name}+subscribe@googlegroups.com?subject=subscribe"
                )

        return values


class Communication(p.BaseModel):
    irc_channels: list[IRCChannel] = []
    matrix_rooms: list[MatrixRoom] = []
    mailing_lists: list[MailingList] = []

    @property
    def empty(self):
        return (
            not self.irc_channels and not self.matrix_rooms and not self.mailing_lists
        )


class CollectionLinks(p.BaseModel):
    edit_on_github: t.Optional[CollectionEditOnGitHub] = None
    authors: list[str] = []
    description: t.Optional[str] = None
    issue_tracker: t.Optional[str] = None
    links: list[Link] = []
    extra_links: list[Link] = []
    communication: Communication = Communication()
