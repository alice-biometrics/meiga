from meiga.on_failure_exception import OnFailureException


def meiga(func):
    def _meiga(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OnFailureException as exc:
            return exc.result

    return _meiga
