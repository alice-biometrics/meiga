class Error(Exception):
    def __init__(self):
        self.message = None

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return True
        return False

    def __repr__(self) -> str:
        suffix = ""
        if self.message:
            suffix = f": {self.message}"

        return f"{self.__class__.__name__}{suffix}"
