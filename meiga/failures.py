from typing import TYPE_CHECKING

from meiga.error import Error

if TYPE_CHECKING:
    from meiga.alias import AnyResult


class WaitingForEarlyReturn(Error):
    result: "AnyResult"

    def __init__(self, result: "AnyResult") -> None:
        self.result = result
        Exception.__init__(self)

    def __str__(self) -> str:
        return (
            f"This exception wraps the following result -> {self.result}"
            f"\nIf you want to handle this error and return a Failure, please use early_return decorator on your function."
            f"\nMore info about how to use unwrap_or_return in combination with @early_return decorator on https://alice-biometrics.github.io/meiga/usage/result/#unwrap_or_return"
        )

    def __repr__(self) -> str:
        return str(self)
