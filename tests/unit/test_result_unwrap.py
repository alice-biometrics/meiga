import pytest

from meiga import Result, Error, Failure


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
