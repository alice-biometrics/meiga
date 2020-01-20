import pytest

from meiga import Result, Error, Failure
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
def test_should_call_on_Failure_when_unwrap_or_else_with_a_result_failure():

    global called_on_failure
    called_on_failure = False

    def on_failure(failure_value):
        global called_on_failure
        called_on_failure = True
        assert isinstance(failure_value, Error)

    result = Failure(Error())

    _ = result.unwrap_or_else(on_failure)

    assert called_on_failure
