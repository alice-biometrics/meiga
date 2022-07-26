from meiga.error import Error
from meiga.result import Result


class Success(Result):
    def __init__(self, value=True) -> None:
        Result.__init__(self, success=value)


class Failure(Result):
    def __init__(self, error=Error()) -> None:
        Result.__init__(self, failure=error)


isSuccess = Success()
isFailure = Failure()
NotImplementedMethodError = isFailure

BoolResult = Result[bool, Error]
