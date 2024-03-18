from typing import Any

import pytest

from meiga import Error, Result


class MyError(Error):
    pass


@pytest.mark.unit
class TestResultAssertion:
    def should_assert_a_success(self):
        result = Result(success=5)
        result.assert_success()

    def should_assert_a_success_checking_instance(self):
        result = Result(success=5)
        result.assert_success(value_is_instance_of=int)

    def should_assert_a_success_checking_instance_and_value(self):
        result = Result(success=5)
        result.assert_success(value_is_instance_of=int, value_is_equal_to=5)

    def should_assert_a_failure(self):
        result = Result(failure=Error())
        result.assert_failure()

    def should_assert_a_failure_checking_instance(self):
        result = Result(failure=Error())
        result.assert_failure(value_is_instance_of=Error)

    def should_assert_a_failure_result_checking_instance_and_value(self):
        result = Result(failure=5)
        result.assert_failure(value_is_instance_of=int, value_is_equal_to=5)

    @pytest.mark.parametrize("error", [Error(), MyError(), Exception()])
    def should_raise_an_assertion_error_when_instance_is_not_correct(self, error: Any):
        result = Result(failure=error)
        with pytest.raises(AssertionError):
            result.assert_failure(value_is_instance_of=bool)
