from meiga.result import Result
from meiga.error import Error


class Success(Result):
    def __init__(self, value=True):
        Result.__init__(self, success=value)


class Failure(Result):
    def __init__(self, error=Error()):
        Result.__init__(self, failure=error)


isSuccess = Success()
isFailure = Failure()
NotImplementedMethodError = isFailure
