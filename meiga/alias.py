from typing import Any, cast

from meiga.error import Error
from meiga.result import TF, TS, Result


def Success(value: TS = cast(TS, True)) -> Result[TS, Any]:  # type: ignore
    return Result(success=value)


def Failure(error: TF = cast(TF, Error())) -> Result[Any, TF]:  # type: ignore
    return Result(failure=error)


isSuccess: Result = Success()
isFailure: Result = Failure()
NotImplementedMethodError: Result = isFailure

BoolResult = Result[bool, Error]
AnyResult = Result[Any, Error]
