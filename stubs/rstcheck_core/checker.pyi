# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import enum
import pathlib

from typing import List, Optional, Tuple, Union

from . import config, types


def check_file(
    source_file: pathlib.Path,
    rstcheck_config: config.RstcheckConfig,
    overwrite_with_file_config: bool = True,
) -> List[types.LintError]: ...
