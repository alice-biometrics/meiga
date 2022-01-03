import pytest

from meiga import Error, Result


@pytest.mark.unit
def test_should_repr_as_expected_default_error():

    result = Result(failure=Error())

    assert "Result[status: failure | value: Error]" == result.__repr__()


@pytest.mark.unit
def test_should_repr_as_expected_an_error_with_message():
    given_any_message = "any message"

    class ErrorWithMessage(Error):
        def __init__(self, message: str):
            self.message = message

    result = Result(failure=ErrorWithMessage(given_any_message))

    assert (
        f"Result[status: failure | value: ErrorWithMessage: {given_any_message}]"
        == result.__repr__()
    )
