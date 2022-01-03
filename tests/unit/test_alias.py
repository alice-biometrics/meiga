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


@pytest.mark.unit
def test_should_be_the_same_a_result_with_true_success_with_a_success_class():

    result = Result(success=True)
    success = Success()
    success_with_true = Success(True)

    assert result == success
    assert result == success_with_true
    assert result == isSuccess


@pytest.mark.unit
def test_should_be_the_same_a_result_with_an_error_failure_with_a_failure_class():

    result = Result(failure=Error())
    failure = Failure()
    failure_with_error = Failure(Error())

    assert result == failure
    assert result == failure_with_error
    assert result == isFailure


@pytest.mark.unit
def test_should_be_the_same_a_failure_and_a_not_implemented_method_error():

    assert NotImplementedMethodError == isFailure


@pytest.mark.unit
def test_should_be_ok_use_bool_result_for_binary_return_eexpectation():
    def handler() -> BoolResult:
        return isSuccess

    assert handler().is_success
