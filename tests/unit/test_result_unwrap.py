import pytest

from meiga import Result, Error, Failure, Success
from meiga.on_failure_exception import OnFailureException


@pytest.mark.unit
def test_should_return_the_value_when_unwrap_a_success_result():

    result = Result(success="Hi!")
    value = result.unwrap()

    assert value == "Hi!"


@pytest.mark.unit
def test_should_return_none_when_unwrap_a_failure_result():

    result = Failure(Error())
    value = result.unwrap()

    assert value is None


@pytest.mark.unit
def test_should_return_default_none_when_unwrap_or_a_failure_result():

    result = Failure(Error())
    value = result.unwrap_or("Error")

    assert value == "Error"


@pytest.mark.unit
def test_should_raise_an_exception_when_unwrap_or_throw_with_a_failure_result():

    result = Failure(Error())

    with pytest.raises(OnFailureException):
        _ = result.unwrap_or_throw()


@pytest.mark.unit
def test_should_call_on_failure_when_unwrap_or_else_with_a_result_failure():

    global called_on_failure
    called_on_failure = False

    def on_failure(failure_value):
        global called_on_failure
        called_on_failure = True
        assert isinstance(failure_value, Error)

    result = Failure(Error())

    _ = result.unwrap_or_else(on_failure)

    assert called_on_failure


@pytest.mark.unit
def test_should_call_on_failure_when_unwrap_or_else_with_failure_result_and_custom_args():
    param1 = 1
    param2 = "param2"

    global called_on_failure
    called_on_failure = False

    def on_failure(param1, param2):
        global called_on_failure
        called_on_failure = True
        assert isinstance(param1, int)
        assert isinstance(param2, str)

    result = Failure(Error())

    _ = result.unwrap_or_else(on_failure, failure_args=(param1, param2))

    assert called_on_failure


@pytest.mark.unit
def test_should_call_on_success_when_unwrap_and_with_a_result_success():

    global called_on_success
    called_on_success = False

    def on_success(success_value):
        global called_on_success
        called_on_success = True
        assert isinstance(success_value, str)

    result = Success("Hi!")

    _ = result.unwrap_and(on_success)

    assert called_on_success


@pytest.mark.unit
def test_should_call_on_success_when_unwrap_and_with_a_result_success_and_custom_args():
    param1 = 1
    param2 = "param2"

    global called_on_success
    called_on_success = False

    def on_success(param1, param2):
        global called_on_success
        called_on_success = True
        assert isinstance(param1, int)
        assert isinstance(param2, str)

    result = Success("Hi!")

    _ = result.unwrap_and(on_success, success_args=(param1, param2))

    assert called_on_success
