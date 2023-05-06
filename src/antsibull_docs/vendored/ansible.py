# Vendored from various module_utils in
# https://github.com/ansible/ansible/tree/2218b63aefc558ff967a8597a1dc9c4c5f88e27c/lib/ansible/module_utils
#
# Copyright 2017, Ansible Project
# Copyright (c) 2019 Ansible Project
# Copyright (c) 2016 Toshio Kuratomi <tkuratomi@ansible.com>
# Simplified BSD License (see LICENSES/BSD-2-Clause.txt or
# https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

import codecs
import datetime
import json
import os
import re
from ast import literal_eval
from collections.abc import Set

try:
    codecs.lookup_error("surrogateescape")
    HAS_SURROGATEESCAPE = True
except LookupError:
    HAS_SURROGATEESCAPE = False


SIZE_RANGES = {
    "Y": 1 << 80,
    "Z": 1 << 70,
    "E": 1 << 60,
    "P": 1 << 50,
    "T": 1 << 40,
    "G": 1 << 30,
    "M": 1 << 20,
    "K": 1 << 10,
    "B": 1,
}


def human_to_bytes(number, isbits=False):  # noqa: C901
    """Convert number in string format into bytes (ex: '2K' => 2048) or using unit argument.

    example: human_to_bytes('10M') <=> human_to_bytes(10, 'M').

    When isbits is False (default), converts bytes from a human-readable format to integer.
        example: human_to_bytes('1MB') returns 1048576 (int).
        The function expects 'B' (uppercase) as a byte identifier passed
        as a part of 'name' param string or 'unit', e.g. 'MB'/'KB'/etc.
        (except when the identifier is single 'b', it is perceived as a byte identifier too).
        if 'Mb'/'Kb'/... is passed, the ValueError will be rased.

    When isbits is True, converts bits from a human-readable format to integer.
        example: human_to_bytes('1Mb', isbits=True) returns 8388608 (int) -
        string bits representation was passed and return as a number or bits.
        The function expects 'b' (lowercase) as a bit identifier, e.g. 'Mb'/'Kb'/etc.
        if 'MB'/'KB'/... is passed, the ValueError will be rased.
    """
    m = re.search(r"^\s*(\d*\.?\d*)\s*([A-Za-z]+)?", str(number), flags=re.IGNORECASE)
    if m is None:
        raise ValueError(
            "human_to_bytes() can't interpret following string: %s" % str(number)
        )
    try:
        num = float(m.group(1))
    except Exception:
        raise ValueError(
            "human_to_bytes() can't interpret following number: %s (original input string: %s)"
            % (m.group(1), number)
        )

    unit = m.group(2)

    if unit is None:
        """No unit given, returning raw number"""
        return int(round(num))
    range_key = unit[0].upper()
    try:
        limit = SIZE_RANGES[range_key]
    except Exception:
        raise ValueError(
            "human_to_bytes() failed to convert %s (unit = %s). The suffix must be one of %s"
            % (number, unit, ", ".join(SIZE_RANGES.keys()))
        )

    # default value
    unit_class = "B"
    unit_class_name = "byte"
    # handling bits case
    if isbits:
        unit_class = "b"
        unit_class_name = "bit"
    # check unit value if more than one character (KB, MB)
    if len(unit) > 1:
        expect_message = "expect %s%s or %s" % (range_key, unit_class, range_key)
        if range_key == "B":
            expect_message = "expect %s or %s" % (unit_class, unit_class_name)

        if unit_class_name in unit.lower():
            pass
        elif unit[1] != unit_class:
            raise ValueError(
                "human_to_bytes() failed to convert %s. Value is not a valid string (%s)"
                % (number, expect_message)
            )

    return int(round(num * limit))


_COMPOSED_ERROR_HANDLERS = frozenset(
    (None, "surrogate_or_replace", "surrogate_or_strict", "surrogate_then_replace")
)


def to_text(obj, encoding="utf-8", errors=None, nonstring="simplerepr"):  # noqa: C901
    """Make sure that a string is a text string

    :arg obj: An object to make sure is a text string.  In most cases this
        will be either a text string or a byte string.  However, with
        ``nonstring='simplerepr'``, this can be used as a traceback-free
        version of ``str(obj)``.
    :kwarg encoding: The encoding to use to transform from a byte string to
        a text string.  Defaults to using 'utf-8'.
    :kwarg errors: The error handler to use if the byte string is not
        decodable using the specified encoding.  Any valid `codecs error
        handler <https://docs.python.org/3/library/codecs.html#codec-base-classes>`_
        may be specified.   We support three additional error strategies
        specifically aimed at helping people to port code:

            :surrogate_or_strict: Will use surrogateescape if it is a valid
                handler, otherwise it will use strict
            :surrogate_or_replace: Will use surrogateescape if it is a valid
                handler, otherwise it will use replace.
            :surrogate_then_replace: Does the same as surrogate_or_replace but
                `was added for symmetry with the error handlers in
                :func:`ansible.module_utils._text.to_bytes` (Added in Ansible 2.3)

        Because surrogateescape was added in Python3 this usually means that
        Python3 will use `surrogateescape` and Python2 will use the fallback
        error handler. Note that the code checks for surrogateescape when the
        module is imported.  If you have a backport of `surrogateescape` for
        python2, be sure to register the error handler prior to importing this
        module.

        The default until Ansible-2.2 was `surrogate_or_replace`
        In Ansible-2.3 this defaults to `surrogate_then_replace` for symmetry
        with :func:`ansible.module_utils._text.to_bytes` .
    :kwarg nonstring: The strategy to use if a nonstring is specified in
        ``obj``.  Default is 'simplerepr'.  Valid values are:

        :simplerepr: The default.  This takes the ``str`` of the object and
            then returns the text version of that string.
        :empty: Return an empty text string
        :passthru: Return the object passed in
        :strict: Raise a :exc:`TypeError`

    :returns: Typically this returns a text string.  If a nonstring object is
        passed in this may be a different type depending on the strategy
        specified by nonstring.  This will never return a byte string.
        From Ansible-2.3 onwards, the default is `surrogate_then_replace`.

    .. version_changed:: 2.3

        Added the surrogate_then_replace error handler and made it the default error handler.
    """
    if isinstance(obj, str):
        return obj

    if errors in _COMPOSED_ERROR_HANDLERS:
        if HAS_SURROGATEESCAPE:
            errors = "surrogateescape"
        elif errors == "surrogate_or_strict":
            errors = "strict"
        else:
            errors = "replace"

    if isinstance(obj, bytes):
        # Note: We don't need special handling for surrogate_then_replace
        # because all bytes will either be made into surrogates or are valid
        # to decode.
        return obj.decode(encoding, errors)

    # Note: We do these last even though we have to call to_text again on the
    # value because we're optimizing the common case
    if nonstring == "simplerepr":
        try:
            value = str(obj)
        except UnicodeError:
            try:
                value = repr(obj)
            except UnicodeError:
                # Giving up
                return ""
    elif nonstring == "passthru":
        return obj
    elif nonstring == "empty":
        return ""
    elif nonstring == "strict":
        raise TypeError("obj must be a string type")
    else:
        raise TypeError(
            "Invalid value %s for to_text's nonstring parameter" % nonstring
        )

    return to_text(value, encoding, errors)


def _json_encode_fallback(obj):
    if isinstance(obj, Set):
        return list(obj)
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Cannot json serialize %s" % to_text(obj))


def container_to_text(d, encoding="utf-8", errors="surrogate_or_strict"):
    """Recursively convert dict keys and values to text str

    Specialized for json return because this only handles, lists, tuples,
    and dict container types (the containers that the json module returns)
    """

    if isinstance(d, bytes):
        # Warning, can traceback
        return to_text(d, encoding=encoding, errors=errors)
    elif isinstance(d, dict):
        return dict(container_to_text(o, encoding, errors) for o in d.items())
    elif isinstance(d, list):
        return [container_to_text(o, encoding, errors) for o in d]
    elif isinstance(d, tuple):
        return tuple(container_to_text(o, encoding, errors) for o in d)
    else:
        return d


def jsonify(data, **kwargs):
    for encoding in ("utf-8", "latin-1"):
        try:
            return json.dumps(
                data, encoding=encoding, default=_json_encode_fallback, **kwargs
            )
        # Old systems using old simplejson module does not support encoding keyword.
        except TypeError:
            try:
                new_data = container_to_text(data, encoding=encoding)
            except UnicodeDecodeError:
                continue
            return json.dumps(new_data, default=_json_encode_fallback, **kwargs)
        except UnicodeDecodeError:
            continue
    raise UnicodeError("Invalid unicode encoding encountered")


BOOLEANS_TRUE = frozenset(("y", "yes", "on", "1", "true", "t", 1, 1.0, True))
BOOLEANS_FALSE = frozenset(("n", "no", "off", "0", "false", "f", 0, 0.0, False))
BOOLEANS = BOOLEANS_TRUE.union(BOOLEANS_FALSE)


def boolean(value, strict=True):
    if isinstance(value, bool):
        return value

    normalized_value = value
    if isinstance(value, (str, bytes)):
        normalized_value = to_text(value, errors="surrogate_or_strict").lower().strip()

    if normalized_value in BOOLEANS_TRUE:
        return True
    elif normalized_value in BOOLEANS_FALSE or not strict:
        return False

    raise TypeError(
        "The value '%s' is not a valid boolean.  Valid booleans include: %s"
        % (to_text(value), ", ".join(repr(i) for i in BOOLEANS))
    )


def safe_eval(value, locals=None):
    # do not allow method calls to modules
    if not isinstance(value, (str, bytes)):
        # already templated to a datavaluestructure, perhaps?
        return (value, None)
    if re.search(r"\w\.\w+\(", value):
        return (value, None)
    # do not allow imports
    if re.search(r"import \w+", value):
        return (value, None)
    try:
        result = literal_eval(value)
        return (result, None)
    except Exception as e:
        return (value, e)


# FIXME: The param and prefix parameters here are coming from AnsibleModule._check_type_string()
#        which is using those for the warning messaged based on string conversion warning settings.
#        Not sure how to deal with that here since we don't have config state to query.
def check_type_str(value, allow_conversion=True, param=None, prefix=""):
    """Verify that the value is a string or convert to a string.

    Since unexpected changes can sometimes happen when converting to a string,
    ``allow_conversion`` controls whether or not the value will be converted or a
    TypeError will be raised if the value is not a string and would be converted

    :arg value: Value to validate or convert to a string
    :arg allow_conversion: Whether to convert the string and return it or raise
        a TypeError

    :returns: Original value if it is a string, the value converted to a string
        if allow_conversion=True, or raises a TypeError if allow_conversion=False.
    """
    if isinstance(value, (str, bytes)):
        return value

    if allow_conversion:
        return to_text(value, errors="surrogate_or_strict")

    msg = "'{0!r}' is not a string and conversion is not allowed".format(value)
    raise TypeError(to_text(msg))


def check_type_list(value):
    """Verify that the value is a list or convert to a list

    A comma separated string will be split into a list. Raises a :class:`TypeError`
    if unable to convert to a list.

    :arg value: Value to validate or convert to a list

    :returns: Original value if it is already a list, single item list if a
        float, int, or string without commas, or a multi-item list if a
        comma-delimited string.
    """
    if isinstance(value, list):
        return value

    if isinstance(value, (str, bytes)):
        return value.split(",")
    elif isinstance(value, int) or isinstance(value, float):
        return [str(value)]

    raise TypeError("%s cannot be converted to a list" % type(value))


def _check_type_dict_part(value):
    fields = []
    field_buffer = []
    in_quote = False
    in_escape = False
    for c in value.strip():
        if in_escape:
            field_buffer.append(c)
            in_escape = False
        elif c == "\\":
            in_escape = True
        elif not in_quote and c in ("'", '"'):
            in_quote = c
        elif in_quote and in_quote == c:
            in_quote = False
        elif not in_quote and c in (",", " "):
            field = "".join(field_buffer)
            if field:
                fields.append(field)
            field_buffer = []
        else:
            field_buffer.append(c)

    field = "".join(field_buffer)
    if field:
        fields.append(field)
    return dict(x.split("=", 1) for x in fields)


def check_type_dict(value):
    """Verify that value is a dict or convert it to a dict and return it.

    Raises :class:`TypeError` if unable to convert to a dict

    :arg value: Dict or string to convert to a dict. Accepts ``k1=v2, k2=v2``.

    :returns: value converted to a dictionary
    """
    if isinstance(value, dict):
        return value

    if isinstance(value, (str, bytes)):
        if value.startswith("{"):
            try:
                return json.loads(value)
            except Exception:
                (result, exc) = safe_eval(value, dict())
                if exc is not None:
                    raise TypeError("unable to evaluate string as dictionary")
                return result
        elif "=" in value:
            return _check_type_dict_part(value)
        else:
            raise TypeError("dictionary requested, could not parse JSON or key=value")

    raise TypeError("%s cannot be converted to a dict" % type(value))


def check_type_bool(value):
    """Verify that the value is a bool or convert it to a bool and return it.

    Raises :class:`TypeError` if unable to convert to a bool

    :arg value: String, int, or float to convert to bool. Valid booleans include:
         '1', 'on', 1, '0', 0, 'n', 'f', 'false', 'true', 'y', 't', 'yes', 'no', 'off'

    :returns: Boolean True or False
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, (str, bytes)) or isinstance(value, (int, float)):
        return boolean(value)

    raise TypeError("%s cannot be converted to a bool" % type(value))


def check_type_int(value):
    """Verify that the value is an integer and return it or convert the value
    to an integer and return it

    Raises :class:`TypeError` if unable to convert to an int

    :arg value: String or int to convert of verify

    :return: int of given value
    """
    if isinstance(value, int):
        return value

    if isinstance(value, (str, bytes)):
        try:
            return int(value)
        except ValueError:
            pass

    raise TypeError("%s cannot be converted to an int" % type(value))


def check_type_float(value):
    """Verify that value is a float or convert it to a float and return it

    Raises :class:`TypeError` if unable to convert to a float

    :arg value: float, int, str, or bytes to verify or convert and return.

    :returns: float of given value.
    """
    if isinstance(value, float):
        return value

    if isinstance(value, (bytes, str, int)):
        try:
            return float(value)
        except ValueError:
            pass

    raise TypeError("%s cannot be converted to a float" % type(value))


def check_type_path(
    value,
):
    """Verify the provided value is a string or convert it to a string,
    then return the expanded path
    """
    value = check_type_str(value)
    return os.path.expanduser(os.path.expandvars(value))


def check_type_raw(value):
    """Returns the raw value"""
    return value


def check_type_bytes(value):
    """Convert a human-readable string value to bytes

    Raises :class:`TypeError` if unable to covert the value
    """
    try:
        return human_to_bytes(value)
    except ValueError:
        raise TypeError("%s cannot be converted to a Byte value" % type(value))


def check_type_bits(value):
    """Convert a human-readable string bits value to bits in integer.

    Example: ``check_type_bits('1Mb')`` returns integer 1048576.

    Raises :class:`TypeError` if unable to covert the value.
    """
    try:
        return human_to_bytes(value, isbits=True)
    except ValueError:
        raise TypeError("%s cannot be converted to a Bit value" % type(value))


def check_type_jsonarg(value):
    """Return a jsonified string. Sometimes the controller turns a json string
    into a dict/list so transform it back into json here

    Raises :class:`TypeError` if unable to covert the value

    """
    if isinstance(value, (str, bytes)):
        return value.strip()
    elif isinstance(value, (list, tuple, dict)):
        return jsonify(value)
    raise TypeError("%s cannot be converted to a json string" % type(value))
