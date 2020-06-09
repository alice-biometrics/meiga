from meiga.on_failure_exception import OnFailureException
from meiga.error import Error
from meiga.alias import Failure


def meiga(func):
    def _meiga(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OnFailureException as exc:
            return exc.result
        except Error as error:
            return Failure(error)

    return _meiga
