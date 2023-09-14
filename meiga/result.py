from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar, Union, cast

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
R = TypeVar("R")  # Recast expected type


class Result(Generic[TS, TF]):
    """
    A discriminated union that encapsulates successful outcome with a value of type T or a failure with an arbitrary Error exception.
    """

    __id__ = "__meiga_result_identifier__"
    __match_args__ = ("_value_success", "_value_failure")
    __slots__ = (
        "_value_success",
        "_value_failure",
        "_is_success",
        "_inner_transformer",
    )

    def __init__(
        self,
        success: TS | type[NoGivenValue] = NoGivenValue,
        failure: TF | type[NoGivenValue] = NoGivenValue,
    ) -> None:
        self._value_success = success
        self._value_failure = failure
        self._assert_values()
        self._inner_transformer: Callable[[Result[TS, TF]], Any] | None = None

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
        if self._value_success is NoGivenValue and self._value_failure is NoGivenValue:
            raise TypeError(
                "Result is a monad, it must be a success or a failure. "
                "Please model your result selecting only one type [success or failure]."
            )
        elif (
            self._value_success is not NoGivenValue
            and self._value_failure is not NoGivenValue
        ):
            raise TypeError(
                "Result is a monad, it cannot be success and failure at the same time. "
                "Please model your result selecting only one type [success or failure]."
            )
        else:
            self._is_success = self._value_success is not NoGivenValue

    def get_value(self) -> TS | TF:
        if self._is_success:
            return cast(TS, self._value_success)
        else:
            return cast(TF, self._value_failure)

    def set_value(self, value: Any) -> None:
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
        """
        Deprecated. Use `reraise`
        """
        return self.reraise()

    # cannot use raise as it is a reserved word
    def reraise(self) -> None:
        """
        Raise an exception with the failure value
        """
        if not self._is_success:
            raise self.value
        return None

    def unwrap(self) -> TS | None:
        """
        Returns the encapsulated value if this instance is a success or None if it is failure.
        """
        if not self._is_success:
            return None
        return cast(TS, self.value)

    def unwrap_or(self, failure_value: TEF) -> TS | TEF:
        """
        Returns the encapsulated value if this instance is a success or the selected failure_value if it is failure.
        """
        if not self._is_success:
            return failure_value

        return cast(Union[TS, TEF], self.value)

    def unwrap_or_return(self, return_value_on_failure: Any = None) -> TS:
        """
        Returns the encapsulated value if this instance is a success or return Result as long as @early_return decorator wraps the function.
        """
        if not self._is_success:
            return_value = (
                self if return_value_on_failure is None else return_value_on_failure
            )
            raise OnFailureException(return_value)
        return cast(TS, self.value)

    def unwrap_or_throw(self) -> TS:
        """
        Deprecated. Use unwrap_or_raise instead.
        """
        return self.unwrap_or_raise()

    def unwrap_or_raise(self) -> TS:
        """
        Returns the encapsulated value if this instance is a success or raise the encapsulated exception if it is failure.
        """
        if not self._is_success:
            self.reraise()
        return cast(TS, self.value)

    def unwrap_or_else(
        self,
        on_failure_handler: (
            OnFailureHandler | None
        ) = None,  # Default has to be None to be compatible with deprecated signature
        failure_value: TEF | None = None,
        **kwargs: dict[Any, Any],  # Deprecated parameter [on_failure, failure_args]
    ) -> TS | TEF:
        """
        Returns the encapsulated value if this instance is a success or execute the `on_failure_handler` when it is failure.
        """
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
        on_success_handler: (
            OnSuccessHandler | None
        ) = None,  # Default has to be None to be compatible with deprecated signature
        **kwargs: dict[Any, Any],  # Deprecated parameter [on_success, success_args]
    ) -> TS | None:
        """
        Returns the encapsulated value if this instance is a success and execute the `on_success_handler` when it is success.
        """
        if self._is_success:
            if on_success_handler:
                on_success_handler.execute(self)
            else:  # Deal with deprecated parameters
                on_success_handler = get_on_success_handler_from_deprecated_args(kwargs)
                if on_success_handler:
                    on_success_handler.execute(self)
            return cast(TS, self.value)
        return None

    def handle(
        self,
        on_success_handler: OnSuccessHandler | None = None,
        on_failure_handler: OnFailureHandler | None = None,
        **kwargs: dict[
            Any, Any
        ],  # Deprecated parameter [on_success, on_failure, success_args, failure_args]
    ) -> Result[TS, TF]:
        """
        Returns itself and execute the `on_success_handler` when the instance is a success and the `on_failure_handler` when it is failure.
        """
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

    def bind(self, func: Callable[..., None]) -> Result[TS, TF]:
        """
        Returns itself binding success value with input func
        """
        value = self.unwrap()
        if value is None:
            return self

        new_value = func(value)
        self.set_value(new_value)

        return self

    def map(self, mapper: Callable[[TS | TF], Any]) -> None:
        """
        Modifies encapsulate value applying a mapper function.
        """
        new_value = mapper(self.value)
        self.set_value(new_value)

    def assert_success(
        self,
        value_is_instance_of: type[Any] | None = None,
        value_is_equal_to: Any | None = None,
    ) -> None:
        """
        Assert if result is a Success
        """
        assert_success(
            result=self,
            value_is_instance_of=value_is_instance_of,
            value_is_equal_to=value_is_equal_to,
        )

    def assert_failure(
        self,
        value_is_instance_of: type[Any] | None = None,
        value_is_equal_to: Any | None = None,
    ) -> None:
        """
        Assert if result is a Failure
        """
        assert_failure(
            result=self,
            value_is_instance_of=value_is_instance_of,
            value_is_equal_to=value_is_equal_to,
        )

    value = property(get_value)

    def set_transformer(self, transformer: Callable[[Result[TS, TF]], Any]) -> None:
        """
        Set a Callable transformer to be used with the `transform` method
        """
        self._inner_transformer = transformer

    def transform(
        self,
        transformer: Callable[[Result[TS, TF]], Any] | None = None,
        expected_type: type[R] | None = None,  # noqa
    ) -> R:
        """
        Transform the result with a transformer function. You can give the transformer callable or use the set_transformer function to pre-set the callable to be used.
        """
        if not transformer:
            if not self._inner_transformer:
                raise RuntimeError(
                    "Result object cannot be transformed as no transformer have been given or set. "
                    "Use result.set_transformer(callable) to add your transformer callable method"
                )
            transformer = self._inner_transformer

        return cast(R, transformer(self))
