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
from meiga.result import Result

P = ParamSpec("P")
R = TypeVar("R", bound=Result[Any, Any])


def to_result(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def _to_result(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            if isinstance(func, staticmethod):
                return Failure(UnexpectedDecorationOrderError())
            elif isinstance(func, classmethod):
                return Failure(UnexpectedDecorationOrderError())
            else:
                return func(*args, **kwargs)
        except Exception as exc:
            return cast(R, Failure(exc))

    return _to_result
