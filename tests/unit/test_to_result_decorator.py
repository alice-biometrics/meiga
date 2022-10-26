import pytest

from meiga import BoolResult, Error, isFailure, isSuccess, to_result
from meiga.decorators import UnexpectedDecorationOrderError


@pytest.mark.unit
class TestToResultDecorator:
    def should_return_a_success_result_when_is_success_is_returned(self):
        @to_result
        def decorated_method():
            return isSuccess

        result = decorated_method()

        result.assert_success()

    def should_return_a_failure_when_is_failure_is_returned(self):
        @to_result
        def decorated_method():
            return isFailure

        result = decorated_method()

        result.assert_failure()

    def should_return_a_failure_result_when_raise_an_error(self):
        @to_result
        def decorated_method():
            raise Error()

        result = decorated_method()

        result.assert_failure(value_is_instance_of=Error)

    def should_return_a_failure_result_when_raise_an_error_subclass(self):
        class MyError(Error):
            def __init__(self, message):
                self.message = message

        @to_result
        def decorated_method():
            raise MyError("message")

        result = decorated_method()

        result.assert_failure(value_is_instance_of=MyError)

    def should_return_a_failure_result_and_inner_function_when_raise_an_error_subclass(
        self,
    ):
        class MyError(Error):
            def __init__(self, message):
                self.message = message

        @to_result
        def decorated_method():
            def inner():
                raise MyError("message")

            inner()

        result = decorated_method()

        result.assert_failure(value_is_instance_of=MyError)

    def should_return_a_success_result_and_static_function_right_order(self):
        class MyClass:
            @staticmethod
            @to_result
            def decorated_method() -> BoolResult:
                return isSuccess

        result = MyClass.decorated_method()
        result.assert_success()

    def should_return_a_unexpected_decorator_order_failure_result_and_static_method(
        self,
    ):
        class MyClass:
            @to_result
            @staticmethod
            def decorated_method() -> BoolResult:
                return isSuccess

        result = MyClass.decorated_method()
        result.assert_failure(value_is_instance_of=UnexpectedDecorationOrderError)
        assert (
            result.value.message
            == "meiga decorators must be declared after a @staticmethod, @classmethod"
        )

    def should_return_a_unexpected_decorator_order_failure_result_and_class_method(
        self,
    ):
        class MyClass:
            @to_result
            @classmethod
            def decorated_method(cls) -> BoolResult:
                return isSuccess

        result = MyClass.decorated_method()
        result.assert_failure(value_is_instance_of=UnexpectedDecorationOrderError)
        assert (
            result.value.message
            == "meiga decorators must be declared after a @staticmethod, @classmethod"
        )

    def should_transform_a_function_with_one_liner_when_raise_an_error(self):
        def decorated_method():
            raise Error()

        result = to_result(decorated_method)()

        result.assert_failure(value_is_instance_of=Error)
