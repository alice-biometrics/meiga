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


# def Success(value: TS = cast(TS, True)) -> Result[TS, Any]:  # type: ignore
#     return Result(success=value)
#
#
# def Failure(error: TF = cast(TF, Error())) -> Result[Any, TF]:  # type: ignore
#     return Result(failure=error)


isSuccess: Result = Success()
isFailure: Result = Failure()
NotImplementedMethodError: Result = isFailure

BoolResult = Result[bool, Error]
AnyResult = Result[Any, Error]
