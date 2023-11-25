import pytest

from meiga import Error, Result
from meiga.failures import WaitingForEarlyReturn


def expected_error(value: str) -> str:
    return (
        f"This exception wraps the following result -> Result[status: failure | value: {value}]"
        f"\nIf you want to handle this error and return a Failure, please use early_return decorator on your function."
        f"\nMore info about how to use unwrap_or_return in combination with @early_return decorator on https://alice-biometrics.github.io/meiga/usage/result/#unwrap_or_return"
    )


@pytest.mark.unit
class TestWaitingForEarlyReturn:
    def should_str_as_expected_default_error(self):
        result = Result(failure=Error())

        exception = WaitingForEarlyReturn(result)

        assert expected_error("Error") == str(exception)

    def should_str_as_expected_an_exception(self):
        wrapped_exception = ValueError("Something went wrong")
        result = Result(failure=wrapped_exception)

        exception = WaitingForEarlyReturn(result)

        assert expected_error(wrapped_exception.__repr__()) == str(exception)
