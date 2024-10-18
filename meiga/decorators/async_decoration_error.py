from meiga.error import Error


class AsyncDecorationError(Error):
    def __init__(self) -> None:
        self.message = "meiga async decorators must be declared on async functions"
