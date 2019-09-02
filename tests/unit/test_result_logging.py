import logging

import pytest

from meiga import Result, Error
from meiga.decorators import (
    log_on_start,
    log_on_end,
    return_on_failure,
    log_on_error,
    meiga,
)


@pytest.mark.unit
def test_should_sum_two_positive_values_with_log_on_start_and_end():
    class IsNegativeError(Error):
        pass

    def is_positive(value: int) -> Result[bool, Error]:
        if value >= 0:
            return Result(success=True)
        else:
            return Result(failure=IsNegativeError())

    @meiga
    @log_on_start(
        logging.INFO,
        '{{ "first_value": "{first_value:d}", "second_value": "{second_value:d}", "func": "Start sum_positive_values"}}',
    )
    @log_on_end(
        logging.INFO,
        '{{ "first_value": "{first_value:d}", "second_value": "{second_value:d}", "func": "End sum_positive_values"}}',
    )
    def sum_positive_values(first_value: int, second_value: int) -> Result[int, Error]:

        result_first_value = is_positive(first_value)
        return_on_failure(result_first_value)

        result_second_value = is_positive(second_value)
        return_on_failure(result_second_value)

        return Result(success=first_value + second_value)

    result = sum_positive_values(first_value=2, second_value=2)
    assert result.is_success and result.value == 4


@pytest.mark.unit
def test_should_sum_two_positive_values_with_log_on_error():
    class IsNegativeError(Error):
        pass

    def is_positive(value: int) -> Result[bool, Error]:
        if value >= 0:
            return Result(success=True)
        else:
            return Result(failure=IsNegativeError())

    @meiga
    @log_on_error(
        logging.INFO,
        '{{ "first_value": "{first_value}", "second_value": "{second_value}", "func": "Error on sum_positive_values"}}',
    )
    def sum_positive_values(first_value: int, second_value: int) -> Result[int, Error]:

        result_first_value = is_positive(first_value)
        return_on_failure(result_first_value)

        result_second_value = is_positive(second_value)
        return_on_failure(result_second_value)

        return Result(success=first_value + second_value)

    result = sum_positive_values(first_value=-1, second_value=2)
    assert result.is_failure and isinstance(result.value, IsNegativeError)
