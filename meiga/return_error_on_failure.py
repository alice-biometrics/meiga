from meiga.error import Error


class ReturnErrorOnFailure(Error):
    def __init__(self, result):
        Exception.__init__(self)
        self.result = result
