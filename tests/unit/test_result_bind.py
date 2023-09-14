import pytest

from meiga import Failure, Success


@pytest.mark.unit
def test_should_bind_a_success_result_encapsulated_value():
    result = Success("hi")

    def func(value: str):
        return value.capitalize()

    result.bind(func)

    assert result.value == "Hi"


@pytest.mark.unit
def test_should_bind_several_times_success_result():
    result = Success(0)

    def func(value: int):
        return value + 1

    result.bind(func).bind(func).bind(func).bind(func).bind(func).bind(func).bind(
        func
    ).bind(func).bind(func).bind(func)

    assert result.value == 10


@pytest.mark.unit
def test_should_bind_and_keep_same_object_when_failure():
    result = Failure("failure_value")

    def func(value: str):
        return value.capitalize()

    result.bind(func)

    assert result.value == "failure_value"
