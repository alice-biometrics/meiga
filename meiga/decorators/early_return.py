import sys
from functools import wraps
from typing import Any, Callable, TypeVar, cast

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


def early_return(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def _early_return(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            if isinstance(func, staticmethod):
                return Failure(UnexpectedDecorationOrderError())  # type: ignore
            elif isinstance(func, classmethod):
                return Failure(UnexpectedDecorationOrderError())  # type: ignore
            else:
                return func(*args, **kwargs)
        except WaitingForEarlyReturn as exc:
            return cast(R, exc.result)
        except Error as error:
            return cast(R, Failure(error))

    return _early_return


meiga = early_return  # To keep compatibility (Now this is deprecated)
