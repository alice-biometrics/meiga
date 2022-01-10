from typing import Any, Callable, Generic, Optional, Type, TypeVar, Union

from meiga.misc import get_args_list
from meiga.no_given_value import NoGivenValue
from meiga.on_failure_exception import OnFailureException

TS = TypeVar("TS")  # Success Type
TF = TypeVar("TF")  # Failure Type


class Result(Generic[TS, TF]):
    __id__ = "__meiga_result_identifier__"

    def __init__(
        self,
        success: Union[TS, Type[NoGivenValue]] = NoGivenValue,
        failure: Union[TF, Type[NoGivenValue]] = NoGivenValue,
    ) -> None:
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
        self._is_success = False
        if isinstance(self._value_success, type(NoGivenValue)) and isinstance(
            self._value_failure, type(NoGivenValue)
        ):
            raise TypeError(
                "Result is a monad, it must be a success or a failure. "
                "Please model your result selecting only one type [success or failure]."
            )
        elif not isinstance(self._value_success, type(NoGivenValue)) and not isinstance(
            self._value_failure, type(NoGivenValue)
        ):
            raise TypeError(
                "Result is a monad, it cannot be success and failure at the same time. "
                "Please model your result selecting only one type [success or failure]."
            )
        elif not isinstance(self._value_success, type(NoGivenValue)):
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

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def is_failure(self) -> bool:
        return not self._is_success

    def throw(self):
        if not self._is_success:
            raise self.value

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

    def unwrap_or_return(self, return_value_on_failure: Any = None):
        if not self._is_success:
            return_value = (
                self if return_value_on_failure is None else return_value_on_failure
            )
            raise OnFailureException(return_value)
        else:
            return self.value

    def unwrap_or_throw(self):
        if self._is_success:
            return self.value
        else:
            self.throw()

    def unwrap_or_else(
        self,
        on_failure: Optional[Callable],
        failure_args: Optional[Any] = None,
        failure_value: Optional[Any] = None,
    ):
        if not self._is_success:
            if on_failure:
                if failure_args is not None:
                    failure_args = get_args_list(failure_args)
                    if Result.__id__ in failure_args:
                        index_meiga_result = failure_args.index(Result.__id__)
                        failure_args[index_meiga_result] = self
                    on_failure(*tuple(failure_args))
                else:
                    if on_failure.__code__.co_argcount == 0:
                        on_failure()
                    else:
                        on_failure(self.value)
            return failure_value
        else:
            return self.value

    def unwrap_and(
        self, on_success: Optional[Callable], success_args: Optional[Any] = None
    ):
        if self._is_success:
            if on_success:
                if success_args is not None:
                    success_args = get_args_list(success_args)
                    if Result.__id__ in success_args:
                        index_meiga_result = success_args.index(Result.__id__)
                        success_args[index_meiga_result] = self
                    on_success(*tuple(success_args))
                else:
                    if on_success.__code__.co_argcount == 0:
                        on_success()
                    else:
                        on_success(self.value)
            return self.value
        else:
            return None

    def handle(
        self,
        on_success: Optional[Callable] = None,
        on_failure: Optional[Callable] = None,
        success_args: Optional[Any] = None,
        failure_args: Optional[Any] = None,
    ):
        self.unwrap_or_else(on_failure, failure_args)
        self.unwrap_and(on_success, success_args)
        return self

    def map(self, transform: Callable):
        new_value = transform(self.value)
        self.set_value(new_value)

    value = property(get_value)
