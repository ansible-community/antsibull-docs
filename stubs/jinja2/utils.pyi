# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import typing as t

F = t.TypeVar("F", bound=t.Callable[..., t.Any])

def pass_context(f: F) -> F: ...
def pass_eval_context(f: F) -> F: ...
def pass_environment(f: F) -> F: ...
