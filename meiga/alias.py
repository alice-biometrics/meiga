from typing import Any, Generic, cast

from meiga.error import Error
from meiga.result import TF, TS, Result


class Success(Generic[TS], Result[TS, Any]):
    __match_args__ = ("_value_success",)

    def __init__(self, value: TS = cast(TS, True)) -> None:
        super().__init__(success=value)


class Failure(Generic[TF], Result[Any, TF]):
    __match_args__ = ("_value_failure",)

    def __init__(self, error: TF = cast(TF, Error())) -> None:
        super().__init__(failure=error)


BoolResult = Result[bool, Error]
AnyResult = Result[Any, Any]
isSuccess: AnyResult = Success()
isFailure: AnyResult = Failure()
NotImplementedMethodError: AnyResult = isFailure
