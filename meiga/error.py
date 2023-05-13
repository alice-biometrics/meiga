from __future__ import annotations

from typing import Any


class Error(Exception):
    message: str | None

    def __init__(self) -> None:
        self.message = None

    def __eq__(self, other: Any) -> bool:
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

    def __hash__(self) -> int:
        return hash((self.message,))
