# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023, Ansible Project
"""
Helpers for directives
"""

from __future__ import annotations

import abc
import typing as t

import pydantic as p
from antsibull_fileutils.yaml import load_yaml_bytes
from docutils import nodes
from docutils.parsers.rst import Directive

SchemaT = t.TypeVar("SchemaT", bound=p.BaseModel)


class YAMLDirective(Directive, t.Generic[SchemaT], metaclass=abc.ABCMeta):
    has_content = True

    wrap_as_data = False
    schema: type[SchemaT]

    @abc.abstractmethod
    def _run(self, content_str: str, content: SchemaT) -> list[nodes.Node]:
        pass

    def _handle_error(self, message: str, from_exc: Exception) -> list[nodes.Node]:
        raise self.error(message) from from_exc

    def run(self) -> list[nodes.Node]:
        self.assert_has_content()
        content_str = "\n".join(self.content)
        try:
            content = load_yaml_bytes(content_str.encode("utf-8"))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return self._handle_error(
                f"Error while parsing content of {self.name} as YAML: {exc}", exc
            )
        if self.wrap_as_data:
            content = {
                "data": content,
            }
        try:
            content_obj = self.schema.model_validate(content)
        except p.ValidationError as exc:
            return self._handle_error(
                f"Error while parsing content of {self.name}: {exc}", exc
            )
        return self._run(content_str, content_obj)
