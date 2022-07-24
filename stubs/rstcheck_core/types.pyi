# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import enum
import pathlib

from typing import Literal, Union


class LintError:
    source_origin: Union[pathlib.Path, Literal["<string>"], Literal["<stdin>"]]
    line_number: int
    message: str
