from typing import Callable, Iterable, Optional

from meiga.misc import get_args_list


class Handler:
    def __init__(self, func: Callable[..., None], args: Optional[Iterable] = None):
        self.func = func
        self.args = args

    def execute(self, result) -> None:
        if self.args is not None:
            failure_args = get_args_list(self.args)
            if result.__id__ in failure_args:
                index_meiga_result = failure_args.index(result.__id__)
                failure_args[index_meiga_result] = result
            self.func(*tuple(failure_args))
        else:
            if self.func.__code__.co_argcount == 0:
                self.func()
            else:
                self.func(result.value)


class OnSuccessHandler(Handler):
    ...


class OnFailureHandler(Handler):
    ...
