from meiga.return_error_on_failure import ReturnErrorOnFailure


def meiga(func):
    def _meiga(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ReturnErrorOnFailure as exc:
            return exc.resurlt

    return _meiga
