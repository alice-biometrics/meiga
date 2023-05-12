from typing import Any, List, cast


def get_args_list(args: Any) -> List[str]:
    if isinstance(args, tuple):
        list_args = list(args)
    else:
        list_args = [args]
    return cast(List[str], list_args)
