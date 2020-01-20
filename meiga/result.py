from typing import TypeVar, Generic, Any, Callable

from meiga.no_given_value import NoGivenValue, NoGivenValueClass
from meiga.on_failure_exception import OnFailureException

TS = TypeVar("TS")  # Success Type
TF = TypeVar("TF")  # Failure Type


class Result(Generic[TS, TF]):
    _is_success: bool = False

    def __init__(self, success: TS = NoGivenValue, failure: TF = NoGivenValue) -> None:
        self._value_success = success
        self._value_failure = failure
        self._assert_values()

    def __repr__(self):
        status = "failure"
        value = self.value.__repr__()
        if self._is_success:
            status = "success"
            value = self.value
        return f"Result[status: {status} | value: {value}]"

    def __eq__(self, other):
        if isinstance(other, Result):
            return (
                self._value_success == other._value_success
                and self.value == other.value
            )
        return False

    def _assert_values(self):
        if isinstance(self._value_success, NoGivenValueClass) and isinstance(
            self._value_failure, NoGivenValueClass
        ):
            raise TypeError(
                "Result is a monad, it must be a success or a failure. "
                "Please model your result selecting only one type [success or failure]."
            )
        elif not isinstance(self._value_success, NoGivenValueClass) and not isinstance(
            self._value_failure, NoGivenValueClass
        ):
            raise TypeError(
                "Result is a monad, it cannot be success and failure at the same time. "
                "Please model your result selecting only one type [success or failure]."
            )
        elif not isinstance(self._value_success, NoGivenValueClass):
            self._is_success = True

    def get_value(self):
        if self._is_success:
            return self._value_success
        else:
            return self._value_failure

    def set_value(self, value):
        if self._is_success:
            self._value_success = value
        else:
            self._value_failure = value

    def is_success(self):
        return self._is_success

    def is_failure(self):
        return not self._is_success

    def unwrap(self):
        if not self._is_success:
            return None
        else:
            return self.value

    def unwrap_or(self, failure_value: Any):
        if not self._is_success:
            return failure_value
        else:
            return self.value

    def unwrap_or_throw(self):
        if not self._is_success:
            raise OnFailureException(self)
        else:
            return self.value

    def unwrap_or_else(self, on_failure: Callable):
        if not self._is_success:
            on_failure(self.value)
        else:
            return self.value

    def handle(
        self,
        on_success: Callable = None,
        on_failure: Callable = None,
        success_args=None,
        failure_args=None,
    ) -> Any:
        if not self._is_success:
            if on_failure:
                if failure_args:
                    on_failure(*failure_args)
                else:
                    if on_failure.__code__.co_argcount == 0:
                        on_failure()
                    else:
                        on_failure(self.value)
            raise OnFailureException(self)
        else:
            if on_success:
                if success_args:
                    on_success(*success_args)
                else:
                    if on_success.__code__.co_argcount == 0:
                        on_success()
                    else:
                        on_success(self.value)
            return self.value

    def map(self, transform: Callable):
        new_value = transform(self.value)
        self.set_value(new_value)

    value = property(get_value)
    is_success = property(is_success)
    is_failure = property(is_failure)
