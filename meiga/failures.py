import inspect
from typing import TYPE_CHECKING, Union

from meiga.error import Error

if TYPE_CHECKING:
    from meiga.alias import AnyResult


class WaitingForEarlyReturn(Error):
    result: "AnyResult"
    called_from: Union[str, None]
    called_from_coroutine: bool = False

    def __init__(self, result: "AnyResult") -> None:
        self.result = result
        try:
            stack = inspect.stack()
            parent_frame = stack[3]
            frame = stack[2]
            filename = frame.filename.split("/")[-1]
            self.called_from = f"{frame[3]} on {filename}"
            func = frame.function
            self.called_from_coroutine = inspect.iscoroutinefunction(parent_frame.frame.f_locals.get(func))
            self.is_called_from_class_coroutine(frame, func)
            # Create a descriptive string for where this was called from
            if self.called_from_coroutine:
                self.called_from = f"{func} (async) on {filename}"
            else:
                self.called_from = f"{func} on {filename}"
        except:  # noqa
            self.called_from = None
        Exception.__init__(self)

    def is_called_from_class_coroutine(self, frame, func):
        # Check if a class in the frame contains a member function with the same name as the frame function
        args, _, _, value_dict = inspect.getargvalues(frame.frame)
        # we check the first parameter for the frame function is
        # named 'self'
        if len(args) and args[0] == "self":
            # in that case, 'self' will be referenced in value_dict
            instance = value_dict.get("self", None)
            if instance:
                cls = getattr(instance, "__class__", None)
                member = getattr(cls, func)
                self.called_from_coroutine = inspect.iscoroutinefunction(member) or self.called_from_coroutine

    def __str__(self) -> str:
        function = f" ({self.called_from})" if self.called_from else ""
        return (
            f"This exception wraps the following result -> {self.result}"
            f"\nIf you want to handle this error and return a Failure, please use early_return decorator on your function{function}."
            f"\nMore info about how to use unwrap_or_return in combination with @early_return decorator on https://alice-biometrics.github.io/meiga/usage/result/#unwrap_or_return"
            f"\nUse @async_early_return if your are calling from an async function."
        )

    def __repr__(self) -> str:
        return str(self)
