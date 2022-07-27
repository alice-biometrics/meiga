from typing import Any, cast

from meiga.error import Error
from meiga.result import Result


# TODO: exploring solutions
class Success(Result):
    def __new__(self, value: Any = True) -> "Success":
        return cast(Success, Result[type(value), Error](success=value))


# TODO: exploring solutions
# class Failure(Result):
#     def __new__(self, error: Error = Error()) -> "Failure":
#         return cast(Failure, Result[..., Error](failure=error))


class Failure(Result):
    def __init__(self, error=Error()) -> None:
        Result.__init__(self, failure=error)


isSuccess = Success()
isFailure = Failure()
NotImplementedMethodError = isFailure

BoolResult = Result[bool, Error]
