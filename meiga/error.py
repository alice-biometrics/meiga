class Error(Exception):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return True
        return False

    def __repr__(self):
        suffix = ""
        if hasattr(self, "message"):
            suffix = f": {self.message}"

        return f"{self.__class__.__name__}{suffix}"
