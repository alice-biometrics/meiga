import inspect
import sys
from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar, cast

from meiga.decorators.async_decoration_error import AsyncDecorationError

if sys.version_info < (3, 10):  # pragma: no cover
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

from meiga.alias import Failure
from meiga.decorators.unexpected_decoration_order_error import (
    UnexpectedDecorationOrderError,
)
from meiga.error import Error
from meiga.failures import WaitingForEarlyReturn
from meiga.result import Result

P = ParamSpec("P")
R = TypeVar("R", bound=Result[Any, Any])


def async_early_return(
    func: Callable[..., Coroutine[Any, Any, R]],
) -> Callable[..., Coroutine[Any, Any, R]]:
    @wraps(func)
    async def _async_early_return(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            if not inspect.iscoroutinefunction(func):
                return Failure(AsyncDecorationError())
            elif isinstance(func, staticmethod):
                return Failure(UnexpectedDecorationOrderError())  # type: ignore
            elif isinstance(func, classmethod):
                return Failure(UnexpectedDecorationOrderError())  # type: ignore
            else:
                return await func(*args, **kwargs)
        except WaitingForEarlyReturn as exc:
            return cast(R, exc.result)
        except Error as error:
            return cast(R, Failure(error))

    return _async_early_return
