from typing import Any

from meiga.result import Result


def assert_failure(result: Result, value_is_instance_of: Any = None):
    assert (
        result.is_failure
    ), f"result is failure as expected. Given failure value is {result.value}"
    if value_is_instance_of:
        assert isinstance(result.value, value_is_instance_of), (
            f"Value is not instance of {value_is_instance_of}. "
            f"Given value is {result.value}"
        )