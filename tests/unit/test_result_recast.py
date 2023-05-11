import pytest

from meiga import Result, Success


def recast_method(result: Result):
    return result.value


@pytest.mark.unit
def test_should_set_recast_an_return_recast_value():
    result = Success("Hi")
    result.set_recast(recast_method)

    recast_result = result.recast()

    assert recast_result == "Hi"


@pytest.mark.unit
def test_should_set_recast_an_return_recast_value_with_expected_type():
    result = Success("Hi")
    result.set_recast(recast_method)

    recast_result = result.recast(expected_type=str)

    assert recast_result == "Hi"


@pytest.mark.unit
def test_should_raise_an_error_when_recast_method_is_not_set():
    result = Success("Hi")

    with pytest.raises(RuntimeError):
        result.recast()
