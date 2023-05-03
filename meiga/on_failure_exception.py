from meiga import AnyResult
from meiga.error import Error


class OnFailureException(Error):
    result: AnyResult

    def __init__(self, result: AnyResult) -> None:
        self.result = result
        Exception.__init__(self)
