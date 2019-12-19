from typing import TypeVar, Generic, Any, Callable

from meiga.no_given_value import NoGivenValue, NoGivenValueClass
from meiga.return_error_on_failure import ReturnErrorOnFailure

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

    def is_success(self):
        return self._is_success

    def is_failure(self):
        return not self._is_success

    def handle(
        self,
        success_handler: Callable = None,
        failure_handler: Callable = None,
        success_args=None,
        failure_args=None,
    ) -> Any:
        if not self._is_success:
            if failure_handler:
                failure_handler(
                    *failure_args
                ) if failure_handler.__code__.co_argcount > 0 else failure_handler()
            raise ReturnErrorOnFailure(self)
        else:
            if success_handler:
                success_handler(
                    *success_args
                ) if success_handler.__code__.co_argcount > 0 else success_handler()
            return self._value_success

    value = property(get_value)
    is_success = property(is_success)
    is_failure = property(is_failure)
