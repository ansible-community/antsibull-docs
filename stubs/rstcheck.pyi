# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import docutils.utils

from typing import List, Optional, Tuple, Union


def check(source: str,
          filename: Optional[str] = ...,
          report_level: Union[docutils.utils.Reporter, int] = ...,
          ignore: Union[dict, None] = ...,
          debug: bool = ...) -> List[Tuple[int, str]]: ...

def ignore_directives_and_roles(directives: List[str], roles: List[str]) -> None: ...
