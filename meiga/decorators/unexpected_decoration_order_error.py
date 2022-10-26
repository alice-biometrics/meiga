from meiga.error import Error


class UnexpectedDecorationOrderError(Error):
    def __init__(self) -> None:
        self.message = (
            "meiga decorators must be declared after a @staticmethod, @classmethod"
        )
