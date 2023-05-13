from __future__ import annotations

from typing import Any, List, cast


def get_args_list(args: Any) -> list[Any]:
    if isinstance(args, tuple):
        list_args = list(args)
    else:
        list_args = [args]
    return cast(List[Any], list_args)
