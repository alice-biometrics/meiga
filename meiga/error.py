class Error(Exception):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return True
        return False
