from typing import Any, Callable, Generic, Optional, Type, TypeVar, Union, cast

from meiga.assertions import assert_failure, assert_success
from meiga.deprecation import (
    get_on_failure_handler_from_deprecated_args,
    get_on_success_handler_from_deprecated_args,
)
from meiga.handlers import OnFailureHandler, OnSuccessHandler
from meiga.no_given_value import NoGivenValue
from meiga.on_failure_exception import OnFailureException

TS = TypeVar("TS")  # Success Type
TF = TypeVar("TF")  # Failure Type
TEF = TypeVar("TEF")  # External Failure Type


class Result(Generic[TS, TF]):
    __id__ = "__meiga_result_identifier__"
    __match_args__ = ("_value_success", "_value_failure")
    __slots__ = ("_value_success", "_value_failure", "_is_success")

    def __init__(
        self,
        success: Union[TS, Type[NoGivenValue]] = NoGivenValue,
        failure: Union[TF, Type[NoGivenValue]] = NoGivenValue,
    ) -> None:
        self._value_success = success
        self._value_failure = failure
        self._assert_values()

    def __repr__(self) -> str:
        status = "failure"
        value = self.value.__repr__()
        if self._is_success:
            status = "success"
            value = self.value
        return f"Result[status: {status} | value: {value}]"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Result):
            return (
                self._value_success == other._value_success
                and self.value == other.value
            )
        return False

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        if self._is_success:
            return hash((self._is_success, self._value_success))
        else:
            return hash((self._is_success, self._value_failure))

    def _assert_values(self) -> None:
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
        return None

    def get_value(self) -> Union[TS, TF]:
        if self._is_success:
            return cast(TS, self._value_success)
        else:
            return cast(TF, self._value_failure)

    def set_value(self, value) -> None:
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

    def throw(self) -> None:
        return self.reraise()

    # cannot use raise as it is a reserved word
    def reraise(self) -> None:
        if not self._is_success:
            raise self.value
        return None

    def unwrap(self) -> Union[TS, None]:
        if not self._is_success:
            return None
        return cast(TS, self.value)

    def unwrap_or(self, failure_value: TEF) -> Union[TS, TEF]:
        if not self._is_success:
            return failure_value
        return self.value

    def unwrap_or_return(self, return_value_on_failure: Any = None) -> TS:
        if not self._is_success:
            return_value = (
                self if return_value_on_failure is None else return_value_on_failure
            )
            raise OnFailureException(return_value)
        return cast(TS, self.value)

    def unwrap_or_throw(self) -> TS:
        return self.unwrap_or_raise()

    def unwrap_or_raise(self) -> TS:
        if not self._is_success:
            self.reraise()
        return cast(TS, self.value)

    def unwrap_or_else(
        self,
        on_failure_handler: Optional[
            OnFailureHandler
        ] = None,  # Default has to be None to be compatible with deprecated signature
        failure_value: Optional[TEF] = None,
        **kwargs,  # Deprecated parameter [on_failure, failure_args]
    ) -> Union[TS, TEF]:
        if not self._is_success:
            if on_failure_handler:
                on_failure_handler.execute(self)
            else:  # Deal with deprecated parameters
                on_failure_handler = get_on_failure_handler_from_deprecated_args(kwargs)
                if on_failure_handler:
                    on_failure_handler.execute(self)
            return cast(TEF, failure_value)
        return cast(TS, self.value)

    def unwrap_and(
        self,
        on_success_handler: Optional[
            OnSuccessHandler
        ] = None,  # Default has to be None to be compatible with deprecated signature
        **kwargs,  # Deprecated parameter [on_success, success_args]
    ) -> Union[TS, None]:
        if self._is_success:
            if on_success_handler:
                on_success_handler.execute(self)
            else:  # Deal with deprecated parameters
                on_success_handler = get_on_success_handler_from_deprecated_args(kwargs)
                if on_success_handler:
                    on_success_handler.execute(self)
            return self.value
        return None

    def handle(
        self,
        on_success_handler: Optional[OnSuccessHandler] = None,
        on_failure_handler: Optional[OnFailureHandler] = None,
        **kwargs,  # Deprecated parameter [on_success, on_failure, success_args, failure_args]
    ) -> "Result":
        if on_failure_handler:
            self.unwrap_or_else(on_failure_handler)
        else:  # Deal with deprecated parameters
            on_failure_handler = get_on_failure_handler_from_deprecated_args(kwargs)
            if on_failure_handler:
                self.unwrap_or_else(on_failure_handler)

        if on_success_handler:
            self.unwrap_and(on_success_handler)
        else:  # Deal with deprecated parameters
            on_success_handler = get_on_success_handler_from_deprecated_args(kwargs)
            if on_success_handler:
                self.unwrap_and(on_success_handler)

        return self

    def map(self, transform: Callable) -> None:
        new_value = transform(self.value)
        self.set_value(new_value)

    def assert_success(
        self,
        value_is_instance_of: Optional[Type] = None,
        value_is_equal_to: Optional[Any] = None,
    ) -> None:
        assert_success(
            result=self,
            value_is_instance_of=value_is_instance_of,
            value_is_equal_to=value_is_equal_to,
        )

    def assert_failure(
        self,
        value_is_instance_of: Optional[Type] = None,
        value_is_equal_to: Optional[Any] = None,
    ) -> None:
        assert_failure(
            result=self,
            value_is_instance_of=value_is_instance_of,
            value_is_equal_to=value_is_equal_to,
        )

    value = property(get_value)
