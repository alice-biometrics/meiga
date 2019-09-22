class Error(Exception):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return True
        return False

    def __repr__(self):
        return f"Error: {self.__class__.__name__}"
