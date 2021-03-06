import docutils.utils

from typing import List, Optional, Tuple, Union


def check(source: str,
          filename: Optional[str] = ...,
          report_level: Union[docutils.utils.Reporter, int] = ...,
          ignore: Union[dict, None] = ...,
          debug: bool = ...) -> List[Tuple[int, str]]: ...

def ignore_directives_and_roles(directives: List[str], roles: List[str]) -> None: ...
