class Error(Exception):
    def __init__(self):
        self.message = None

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return True
        return False

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        suffix = ""
        if hasattr(self, "message") and self.message is not None:
            suffix = f": {self.message}"

        return f"{self.__class__.__name__}{suffix}"

    def __hash__(self):
        return hash((self.message,))
