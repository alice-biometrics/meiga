from meiga.error import Error


class OnFailureException(Error):
    def __init__(self, result):
        Exception.__init__(self)
        self.result = result
