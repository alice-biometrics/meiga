from typing import Any

from meiga.result import Result


def assert_failure(
    result: Result, value_is_instance_of: Any = None, value_is_equal_to: Any = None
):
    assert (
        result.is_failure
    ), f"result is not failure as expected. Given failure value is {result.value}"
    if value_is_instance_of:
        assert isinstance(result.value, value_is_instance_of), (
            f"Value is not instance of {value_is_instance_of}. "
            f"Given value is {result.value}"
        )
    if value_is_equal_to:
        assert result.value == value_is_equal_to, (
            f"Value is not equal to {value_is_equal_to}. "
            f"Given value is {result.value}"
        )
