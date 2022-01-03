import pytest

from meiga import Error, Result
from meiga.assertions import assert_failure, assert_success


@pytest.mark.unit
def test_should_assert_a_success_result():
    result = Result(success=5)
    assert_success(result)


@pytest.mark.unit
def test_should_assert_a_success_result_checking_instance():
    result = Result(success=5)
    assert_success(result, value_is_instance_of=int)


@pytest.mark.unit
def test_should_assert_a_success_result_checking_instance_and_value():
    result = Result(success=5)
    assert_success(result, value_is_instance_of=int, value_is_equal_to=5)


@pytest.mark.unit
def test_should_assert_a_failure_result():
    result = Result(failure=Error())
    assert_failure(result)


@pytest.mark.unit
def test_should_assert_a_failure_result_checking_instance():
    result = Result(failure=Error())
    assert_failure(result, value_is_instance_of=Error)


@pytest.mark.unit
def test_should_assert_a_failure_result_checking_instance_and_value():
    result = Result(failure=5)
    assert_failure(result, value_is_instance_of=int, value_is_equal_to=5)
