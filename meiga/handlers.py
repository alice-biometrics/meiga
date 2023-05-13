from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Iterable

from meiga.misc import get_args_list

if TYPE_CHECKING:  # pragma: no cover
    from meiga.result import TF, TS, Result


class Handler:
    def __init__(
        self, func: Callable[..., None], args: Iterable[Any] | None = None
    ) -> None:
        self.func = func
        self.args = args

    def execute(self, result: Result[TS, TF]) -> None:
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
