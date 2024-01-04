import re
from typing import Union

import pytest

from meiga import AnyResult, Error, Failure, Result, WaitingForEarlyReturn, isSuccess
from meiga.on_failure_exception import OnFailureException


def expected_error(
    value: str, called_from: Union[str, None] = None, escape: bool = False
) -> str:
    called_from = f" ({called_from})" if called_from else ""

    text = (
        f"This exception wraps the following result -> Result[status: failure | value: {value}]"
        f"\nIf you want to handle this error and return a Failure, please use early_return decorator on your function{called_from}."
        f"\nMore info about how to use unwrap_or_return in combination with @early_return decorator on https://alice-biometrics.github.io/meiga/usage/result/#unwrap_or_return"
    )
    if escape:
        return re.escape(text)  # necessary to match on pytest.raises contextmanager

    return text


@pytest.mark.unit
class TestWaitingForEarlyReturn:
    def should_str_as_expected_default_error(self):
        result = Result(failure=Error())

        exception = WaitingForEarlyReturn(result)

        assert expected_error(
            "Error", called_from="pytest_pyfunc_call on python.py"
        ) == str(exception)

    def should_str_as_expected_an_exception(self):
        wrapped_exception = ValueError("Something went wrong")
        result = Result(failure=wrapped_exception)

        exception = WaitingForEarlyReturn(result)

        assert expected_error(
            wrapped_exception.__repr__(), called_from="pytest_pyfunc_call on python.py"
        ) == str(exception)

    def should_be_compatible_with_older_version_and_expect_st_as_expected_an_exception(
        self,
    ):
        wrapped_exception = ValueError("Something went wrong")
        result = Result(failure=wrapped_exception)

        exception = OnFailureException(result)

        assert expected_error(
            wrapped_exception.__repr__(), called_from="pytest_pyfunc_call on python.py"
        ) == str(exception)

    def should_log_hint_when_called_from_function_and_not_early_return(self):
        def inner_function() -> AnyResult:
            result = Failure(Error())
            result.unwrap_or_return()
            return isSuccess

        with pytest.raises(
            WaitingForEarlyReturn,
            match=expected_error(
                "Error",
                called_from="inner_function on test_waiting_for_early_return.py",
                escape=True,
            ),
        ):
            inner_function()

    def should_log_hint_when_called_from_class_function_and_not_early_return(self):
        class MyClass:
            def execute(self) -> AnyResult:
                result = Failure(Error())
                result.unwrap_or_return()
                return isSuccess

        with pytest.raises(
            WaitingForEarlyReturn,
            match=expected_error(
                "Error",
                called_from="execute on test_waiting_for_early_return.py",
                escape=True,
            ),
        ):
            MyClass().execute()
