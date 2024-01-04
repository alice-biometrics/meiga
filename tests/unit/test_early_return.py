import pytest

from meiga import BoolResult, Error, early_return, isFailure, isSuccess
from meiga.assertions import assert_failure, assert_success
from meiga.decorators import UnexpectedDecorationOrderError


@pytest.mark.unit
class TestEarlyReturn:
    def should_return_a_success_result_with_meiga_decorator(self):
        @early_return
        def decorated_method():
            return isSuccess

        result = decorated_method()

        assert_success(result)

    def should_return_a_failure_result_with_meiga_decorator(self):
        @early_return
        def decorated_method():
            return isFailure

        result = decorated_method()

        assert_failure(result)

    def should_return_a_failure_result_with_meiga_decorator_when_raise_an_error(self):
        @early_return
        def decorated_method():
            raise Error()

        result = decorated_method()

        assert_failure(result, value_is_instance_of=Error)

    def should_return_a_failure_result_with_meiga_decorator_when_raise_an_error_subclass(
        self,
    ):
        class MyError(Error):
            def __init__(self, message):
                self.message = message

        @early_return
        def decorated_method():
            raise MyError("message")

        result = decorated_method()

        assert_failure(result, value_is_instance_of=MyError)

    def should_return_a_failure_result_with_meiga_decorator_and_inner_function_when_raise_an_error_subclass(
        self,
    ):
        class MyError(Error):
            def __init__(self, message):
                self.message = message

        @early_return
        def decorated_method():
            def inner():
                raise MyError("message")

            inner()

        result = decorated_method()

        assert_failure(result, value_is_instance_of=MyError)

    def should_return_a_success_result_with_meiga_decorator_and_static_function_right_order(
        self,
    ):
        class MyClass:
            @staticmethod
            @early_return
            def decorated_method() -> BoolResult:
                return isSuccess

        result = MyClass.decorated_method()
        assert_success(result)

    def should_return_a_unexpected_decorator_order_failure_result_with_meiga_decorator_and_static_method(
        self,
    ):
        class MyClass:
            @early_return
            @staticmethod
            def decorated_method() -> BoolResult:
                return isSuccess

        result = MyClass.decorated_method()
        assert_failure(result, value_is_instance_of=UnexpectedDecorationOrderError)
        assert (
            result.value.message
            == "meiga decorators must be declared after a @staticmethod, @classmethod"
        )

    def should_return_a_unexpected_decorator_order_failure_result_with_meiga_decorator_and_class_method(
        self,
    ):
        class MyClass:
            @early_return
            @classmethod
            def decorated_method(cls) -> BoolResult:
                return isSuccess

        result = MyClass.decorated_method()
        assert_failure(result, value_is_instance_of=UnexpectedDecorationOrderError)
        assert (
            result.value.message
            == "meiga decorators must be declared after a @staticmethod, @classmethod"
        )
