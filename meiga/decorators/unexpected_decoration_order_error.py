from meiga.error import Error


class UnexpectedDecorationOrderError(Error):
    def __init__(self):
        self.message = (
            "@meiga decorator must be declared after a @staticmethod, @classmethod"
        )
