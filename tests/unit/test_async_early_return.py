import pytest

from meiga import BoolResult, Error, async_early_return, isFailure, isSuccess
from meiga.assertions import assert_failure, assert_success
from meiga.decorators import UnexpectedDecorationOrderError


@pytest.mark.unit
@pytest.mark.asyncio
class TestAsyncEarlyReturn:
    async def should_return_a_success_result_with_async_early_return(self):
        @async_early_return
        async def decorated_method():
            return isSuccess

        result = await decorated_method()

        assert_success(result)

    async def should_return_a_failure_result_with_async_early_return(self):
        @async_early_return
        async def decorated_method():
            return isFailure

        result = await decorated_method()

        assert_failure(result)

    async def should_return_a_failure_result_with_async_early_return_when_raise_an_error(
        self,
    ):
        @async_early_return
        async def decorated_method():
            raise Error()

        result = await decorated_method()

        assert_failure(result, value_is_instance_of=Error)

    async def should_return_a_failure_result_with_async_early_return_when_raise_an_error_subclass(
        self,
    ):
        class MyError(Error):
            def __init__(self, message):
                self.message = message

        @async_early_return
        async def decorated_method():
            raise MyError("message")

        result = await decorated_method()

        assert_failure(result, value_is_instance_of=MyError)

    async def should_return_a_failure_result_with_async_early_return_and_inner_function_when_raise_an_error_subclass(
        self,
    ):
        class MyError(Error):
            def __init__(self, message):
                self.message = message

        @async_early_return
        async def decorated_method():
            def inner():
                raise MyError("message")

            inner()

        result = await decorated_method()

        assert_failure(result, value_is_instance_of=MyError)

    async def should_return_a_success_result_with_async_early_return_and_static_function_right_order(
        self,
    ):
        class MyClass:
            @staticmethod
            @async_early_return
            async def decorated_method() -> BoolResult:
                return isSuccess

        result = await MyClass.decorated_method()
        assert_success(result)

    async def should_return_a_unexpected_decorator_order_failure_result_with_async_early_return_and_static_method(
        self,
    ):
        class MyClass:
            @async_early_return
            @staticmethod
            async def decorated_method() -> BoolResult:
                return isSuccess

        result = await MyClass.decorated_method()
        assert_failure(result, value_is_instance_of=UnexpectedDecorationOrderError)
        assert (
            result.value.message
            == "meiga decorators must be declared after a @staticmethod, @classmethod"
        )

    async def should_return_a_unexpected_decorator_order_failure_result_with_async_early_return_and_class_method(
        self,
    ):
        class MyClass:
            @async_early_return
            @classmethod
            async def decorated_method(cls) -> BoolResult:
                return isSuccess

        result = await MyClass.decorated_method()
        assert_failure(result, value_is_instance_of=UnexpectedDecorationOrderError)
        assert (
            result.value.message
            == "meiga decorators must be declared after a @staticmethod, @classmethod"
        )
