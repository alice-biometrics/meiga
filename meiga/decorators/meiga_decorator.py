from meiga.error import Error
from meiga.result import Result


class ReturnErrorOnFailure(Error):
    def __init__(self, result: Result):
        Exception.__init__(self)
        self.result = result


def meiga(func):
    def _meiga(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ReturnErrorOnFailure as exc:
            return exc.result

    return _meiga


def return_on_failure(result: Result):
    if result.is_failure:
        raise ReturnErrorOnFailure(result)


def get_value_or_return_on_failure(result: Result):
    if result.is_failure:
        raise ReturnErrorOnFailure(result)
    else:
        return result.value
