import pytest

from meiga import isSuccess, isFailure, Error
from meiga.assertions import assert_success, assert_failure
from meiga.decorators import meiga


@pytest.mark.unit
def test_should_return_a_success_result_with_meiga_decorator():
    @meiga
    def decorated_method():
        return isSuccess

    result = decorated_method()

    assert_success(result)


@pytest.mark.unit
def test_should_return_a_failure_result_with_meiga_decorator():
    @meiga
    def decorated_method():
        return isFailure

    result = decorated_method()

    assert_failure(result)


@pytest.mark.unit
def test_should_return_a_failure_result_with_meiga_decorator_when_raise_an_error():
    @meiga
    def decorated_method():
        raise Error()

    result = decorated_method()

    assert_failure(result, value_is_instance_of=Error)


@pytest.mark.unit
def test_should_return_a_failure_result_with_meiga_decorator_when_raise_an_error_subclass():
    class MyError(Error):
        def __init__(self, message):
            self.message = message

    @meiga
    def decorated_method():
        raise MyError("message")

    result = decorated_method()

    assert_failure(result, value_is_instance_of=MyError)


@pytest.mark.unit
def test_should_return_a_failure_result_with_meiga_decorator_and_inner_function_when_raise_an_error_subclass():
    class MyError(Error):
        def __init__(self, message):
            self.message = message

    @meiga
    def decorated_method():
        def inner():
            raise MyError("message")

        inner()

    result = decorated_method()

    assert_failure(result, value_is_instance_of=MyError)
