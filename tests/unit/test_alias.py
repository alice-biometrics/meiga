import pytest

from meiga import (
    BoolResult,
    Error,
    Failure,
    NotImplementedMethodError,
    Result,
    Success,
    isFailure,
    isSuccess,
)


class MyInnerClass:
    pass


@pytest.mark.unit
class TestAlias:
    def should_be_the_same_a_result_with_true_success_with_a_success_class(self):

        result = Result(success=True)
        success = Success()
        success_with_true = Success(True)

        assert result == success
        assert result == success_with_true
        assert result == isSuccess
        assert isinstance(result, Result)
        assert isinstance(success, Result)
        assert isinstance(success_with_true, Result)

    def should_be_the_same_a_result_with_an_error_failure_with_a_failure_class(self):

        result = Result(failure=Error())
        failure = Failure()
        failure_with_error = Failure(Error())

        assert result == failure
        assert result == failure_with_error
        assert result == isFailure
        assert isinstance(result, Result)
        assert isinstance(failure, Result)
        assert isinstance(failure_with_error, Result)

    def should_be_the_same_a_failure_and_a_not_implemented_method_error(self):
        assert NotImplementedMethodError == isFailure

    def should_be_ok_use_bool_result_for_binary_return_eexpectation(self):
        def handler() -> BoolResult:
            return isSuccess

        assert handler().is_success

    @pytest.mark.parametrize("value", ["my str", 1, 2.0, MyInnerClass()])
    def should_unwrap_a_given_type_value(self, value):
        result = Result(success=value)
        success = Success(value)

        assert type(result.unwrap()) is type(value)
        assert type(success.unwrap()) is type(value)

    def should_check_bool_result_is_available_in_the_public_api(self):
        from meiga import BoolResult  # noqa

    def should_check_any_result_is_available_in_the_public_api(self):
        from meiga import AnyResult  # noqa
