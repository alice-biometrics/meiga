from typing import Generic, cast

from meiga.error import Error
from meiga.result import TF, TS, Result


class Success(Result, Generic[TS]):
    def __init__(self, value: TS = cast(TS, True)) -> None:
        Result.__init__(self, success=value)


class Failure(Result, Generic[TF]):
    def __init__(self, error: TF = cast(TF, Error())) -> None:
        Result.__init__(self, failure=error)


isSuccess: Success = Success()
isFailure: Failure = Failure()
NotImplementedMethodError = isFailure

BoolResult = Result[bool, Error]
