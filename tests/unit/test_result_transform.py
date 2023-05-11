import pytest

from meiga import Result, Success


def transformer(result: Result):
    return result.value


@pytest.mark.unit
def test_should_set_transformer_an_return_transformed_value():
    result = Success("Hi")
    result.set_transformer(transformer)

    recast_result = result.transform()

    assert recast_result == "Hi"


@pytest.mark.unit
def test_should_set_transformer_an_return_transformed_value_with_expected_type():
    result = Success("Hi")
    result.set_transformer(transformer)

    recast_result = result.transform(expected_type=str)

    assert recast_result == "Hi"


@pytest.mark.unit
def test_should_raise_an_error_when_transform_method_is_not_set():
    result = Success("Hi")

    with pytest.raises(RuntimeError):
        result.transform()
