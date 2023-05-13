from typing import TYPE_CHECKING, Any, Type, Union

if TYPE_CHECKING:  # pragma: no cover
    from meiga.result import TF, TS, Result


def assert_success(
    result: "Result[TS, TF]",
    value_is_instance_of: Union[Type[Any], None] = None,
    value_is_equal_to: Union[Any, None] = None,
) -> None:
    assert (
        result.is_success
    ), f"result is not success as expected. Given failure value is {result.value}"
    if value_is_instance_of:
        assert isinstance(result.value, value_is_instance_of), (
            f"Value is not instance of {value_is_instance_of}. "
            f"Given value is {result.value} of {type({result.value})}"
        )
    if value_is_equal_to:
        assert result.value == value_is_equal_to, (
            f"Value is not equal to {value_is_equal_to}. "
            f"Given value is {result.value}"
        )
