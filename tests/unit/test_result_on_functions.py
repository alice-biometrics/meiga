import pytest

from meiga import Result, Error
from meiga.decorators import meiga, return_on_failure, get_value_or_return_on_failure


@pytest.mark.unit
def test_should_create_a_success_result_with_a_true_bool():
    def func(value: bool) -> Result[bool, Error]:
        if value:
            return Result(success=True)
        else:
            return Result(failure=Error())

    result_success = func(value=True)
    result_failure = func(value=False)

    assert result_success.is_success
    assert result_failure.is_failure


@pytest.mark.unit
def test_should_sum_two_positive_values():
    class IsNegativeError(Error):
        pass

    def is_positive(value: int) -> Result[bool, Error]:
        if value >= 0:
            return Result(success=True)
        else:
            return Result(failure=IsNegativeError())

    def sum_positive_values(first_value: int, second_value: int) -> Result[int, Error]:

        result_first_value = is_positive(first_value)
        if result_first_value.is_failure:
            return Result(failure=result_first_value.value)

        result_second_value = is_positive(second_value)
        if result_second_value.is_failure:
            return Result(failure=result_second_value.value)

        return Result(success=first_value + second_value)

    result = sum_positive_values(first_value=2, second_value=2)
    assert result.is_success and result.value == 4

    result = sum_positive_values(first_value=-1, second_value=2)
    assert result.is_failure and isinstance(result.value, IsNegativeError)

    result = sum_positive_values(first_value=2, second_value=-1)
    assert result.is_failure and isinstance(result.value, IsNegativeError)


@pytest.mark.unit
def test_should_sum_two_positive_values_with_decorator_and_return_on_failure():
    class IsNegativeError(Error):
        pass

    def is_positive(value: int) -> Result[bool, Error]:
        if value >= 0:
            return Result(success=True)
        else:
            return Result(failure=IsNegativeError())

    @meiga
    def sum_positive_values(first_value: int, second_value: int) -> Result[int, Error]:

        result_first_value = is_positive(first_value)
        return_on_failure(result_first_value)

        result_second_value = is_positive(second_value)
        return_on_failure(result_second_value)

        return Result(success=first_value + second_value)

    result = sum_positive_values(first_value=2, second_value=2)
    assert result.is_success and result.value == 4

    result = sum_positive_values(first_value=-1, second_value=2)
    assert result.is_failure and isinstance(result.value, IsNegativeError)

    result = sum_positive_values(first_value=2, second_value=-1)
    assert result.is_failure and isinstance(result.value, IsNegativeError)


@pytest.mark.unit
def test_should_sum_two_positive_values_with_decorator_and_get_value_or_return_on_failure():
    class IsNegativeError(Error):
        pass

    def is_positive(value: int) -> Result[bool, Error]:
        if value >= 0:
            return Result(success=True)
        else:
            return Result(failure=IsNegativeError())

    @meiga
    def sum_positive_values(first_value: int, second_value: int) -> Result[int, Error]:

        result_first_value = is_positive(first_value)
        _ = get_value_or_return_on_failure(result_first_value)

        result_second_value = is_positive(second_value)
        _ = get_value_or_return_on_failure(result_second_value)

        return Result(success=first_value + second_value)

    result = sum_positive_values(first_value=2, second_value=2)
    assert result.is_success and result.value == 4

    result = sum_positive_values(first_value=-1, second_value=2)
    assert result.is_failure and isinstance(result.value, IsNegativeError)

    result = sum_positive_values(first_value=2, second_value=-1)
    assert result.is_failure and isinstance(result.value, IsNegativeError)
