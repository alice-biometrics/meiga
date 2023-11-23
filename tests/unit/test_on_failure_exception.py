import pytest

from meiga import Error, Result
from meiga.on_failure_exception import OnFailureException


@pytest.mark.unit
def test_should_str_as_expected_default_error():
    result = Result(failure=Error())

    exception = OnFailureException(result)

    assert "OnFailureException: Result[status: failure | value: Error]" == str(
        exception
    )


@pytest.mark.unit
def test_should_str_as_expected_an_exception():
    wrapped_exception = ValueError("Something went wrong")
    result = Result(failure=wrapped_exception)

    exception = OnFailureException(result)

    assert (
        f"OnFailureException: Result[status: failure | value: {wrapped_exception.__repr__()}]"
        == str(exception)
    )
