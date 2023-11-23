from typing import TYPE_CHECKING

from meiga.error import Error

if TYPE_CHECKING:
    from meiga.alias import AnyResult


class OnFailureException(Error):
    result: "AnyResult"

    def __init__(self, result: "AnyResult") -> None:
        self.result = result
        Exception.__init__(self)

    def __str__(self) -> str:
        return f"OnFailureException: {self.result}"

    def __repr__(self) -> str:
        return f"OnFailureException: {self.result}"
