# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2019, Ansible Project
"""
Jinja2 filters for use in Ansible documentation.
"""

from __future__ import annotations

import json
import re
import typing as t
from collections.abc import Mapping, Sequence

from antsibull_core.logging import log
from docutils.utils import column_width as _column_width  # pyre-ignore[21]
from jinja2.runtime import Context, Undefined
from jinja2.utils import pass_context

from ..markup.htmlify import html_ify as html_ify_impl
from ..markup.rstify import get_rst_formatter_link_provider
from ..markup.rstify import rst_ify as rst_ify_impl
from . import OutputFormat

mlog = log.fields(mod=__name__)

_EMAIL_ADDRESS = re.compile(
    r"(?:<{mail}>|\({mail}\)|{mail})".format(mail=r"[\w.+-]+@[\w.-]+\.\w+")
)


def extract_plugin_data(
    context: Context, plugin_fqcn: str | None = None, plugin_type: str | None = None
) -> tuple[str | None, str | None, str | None, str | None]:
    # The doc plugin is determined by the current page
    doc_plugin_fqcn = context.get("plugin_name")
    doc_plugin_type = context.get("plugin_type")
    if doc_plugin_fqcn is None or doc_plugin_type is None:
        doc_plugin_fqcn = doc_plugin_type = None

    # The current plugin for this markup is determined by the parameters,
    # with fallback to the doc plugin
    plugin_fqcn = doc_plugin_fqcn if plugin_fqcn is None else plugin_fqcn
    plugin_type = doc_plugin_type if plugin_type is None else plugin_type
    if plugin_fqcn is None or plugin_type is None:
        plugin_fqcn = plugin_type = None

    return doc_plugin_fqcn, doc_plugin_type, plugin_fqcn, plugin_type


def documented_type(text) -> str:
    """Convert any python type to a type for documentation"""

    if isinstance(text, Undefined):
        return "-"
    if text == "str":
        return "string"
    if text == "bool":
        return "boolean"
    if text == "int":
        return "integer"
    if text == "dict":
        return "dictionary"
    return text


def rst_fmt(text, fmt):
    """helper for Jinja2 to do format strings"""

    return fmt % (text)


def rst_xline(width, char="="):
    """return a restructured text line of a given length"""

    return char * width


def move_first(sequence, *move_to_beginning):
    """return a copy of sequence where the elements which are in move_to_beginning are
    moved to its beginning if they appear in the list"""

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
    """remove email addresses from the given string, and remove `(!UNKNOWN)`"""
    value = _EMAIL_ADDRESS.sub("", value)
    value = value.replace("(!UNKNOWN)", "")
    return value


def extract_options_from_list(
    options: dict[str, t.Any],
    options_to_extract: list[str],
    options_to_ignore: list[str] | None = None,
) -> list[tuple[str, t.Any]]:
    """return list of tuples (option, option_data) with option from options_to_extract"""
    if options_to_ignore is None:
        options_to_ignore = []
    return [
        (option, options[option])
        for option in options_to_extract
        if option in options and option not in options_to_ignore
    ]


def remove_options_from_list(
    options: dict[str, t.Any], options_to_remove: list[str]
) -> dict[str, t.Any]:
    """return copy of dictionary with the options from options_to_remove removed"""
    result = options.copy()
    for option in options_to_remove:
        result.pop(option, None)
    return result


def to_json(data: t.Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(", ", ": "))


def to_ini_value(data: t.Any) -> str:
    if isinstance(data, (str, bytes)):
        if not data:
            return '""'
        return str(data)
    if isinstance(data, Sequence):
        return ", ".join(to_ini_value(v) for v in data)
    if isinstance(data, Mapping):
        return "MAPPINGS ARE NOT SUPPORTED"
    # Handle other values (booleans, integers, floats) as JSON
    return json.dumps(data)


def make_rst_ify(output_format: OutputFormat):
    @pass_context
    def rst_ify(
        context: Context,
        text: str,
        *,
        plugin_fqcn: str | None = None,
        plugin_type: str | None = None,
        role_entrypoint: str | None = None,
    ) -> str:
        """convert symbols like I(this is in italics) to valid restructured text"""
        flog = mlog.fields(func="rst_ify")
        flog.fields(text=text).debug("Enter")

        (
            doc_plugin_fqcn,
            doc_plugin_type,
            plugin_fqcn,
            plugin_type,
        ) = extract_plugin_data(
            context,
            plugin_fqcn=plugin_fqcn,
            plugin_type=plugin_type,
        )

        formatter, link_provider = get_rst_formatter_link_provider(
            output_format, context.get("referable_envvars")
        )
        text, counts = rst_ify_impl(
            text,
            plugin_fqcn=plugin_fqcn,
            plugin_type=plugin_type,
            role_entrypoint=role_entrypoint,
            doc_plugin_fqcn=doc_plugin_fqcn,
            doc_plugin_type=doc_plugin_type,
            formatter=formatter,
            link_provider=link_provider,
        )

        flog.fields(counts=counts).info("Number of macros converted to rst equivalents")
        flog.debug("Leave")
        return text

    return rst_ify


@pass_context
def html_ify(
    context: Context,
    text: str,
    *,
    plugin_fqcn: str | None = None,
    plugin_type: str | None = None,
    role_entrypoint: str | None = None,
) -> str:
    """convert symbols like I(this is in italics) to valid HTML"""
    flog = mlog.fields(func="html_ify")
    flog.fields(text=text).debug("Enter")

    doc_plugin_fqcn, doc_plugin_type, plugin_fqcn, plugin_type = extract_plugin_data(
        context,
        plugin_fqcn=plugin_fqcn,
        plugin_type=plugin_type,
    )

    text, counts = html_ify_impl(
        text,
        plugin_fqcn=plugin_fqcn,
        plugin_type=plugin_type,
        role_entrypoint=role_entrypoint,
        doc_plugin_fqcn=doc_plugin_fqcn,
        doc_plugin_type=doc_plugin_type,
    )

    flog.fields(counts=counts).info("Number of macros converted to html equivalents")
    flog.debug("Leave")
    return text


def collection_name(fqcn: str) -> str:
    return ".".join(fqcn.split(".", 2)[:2])


def plugin_shortname(fqcn: str) -> str:
    return fqcn.split(".", 2)[2]


def suboption_depth(
    data: Sequence[tuple[t.Any, t.Any]] | t.ItemsView[t.Any, t.Any], subkey: str
) -> int:
    subdepth = 0
    for _, option in data:
        subdata = option.get(subkey)
        if subdata and isinstance(subdata, Mapping):
            subdepth = max(subdepth, suboption_depth(subdata.items(), subkey))
    return subdepth + 1


def rst_format(fmt: str, for_sphinx: bool = False) -> str:
    if fmt == "ini":
        return "ini"
    if fmt == "toml":
        return "toml"
    if fmt == "yaml":
        return "yaml+jinja" if for_sphinx else "yaml"
    if fmt == "json":
        return "json"
    # Unknown format: no syntax highlighting
    return "text"


def column_width(string: str) -> int:
    return _column_width(string)
