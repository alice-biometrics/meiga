import pytest

from meiga import Error, Result


@pytest.mark.unit
def test_should_create_a_success_result_with_a_true_bool():
    result = Result(success=True)

    assert result.is_success
    assert result.value is True


@pytest.mark.unit
def test_should_create_a_success_result_with_a_false_bool():
    result = Result(success=False)

    assert result.is_success
    assert result.value is False


@pytest.mark.unit
def test_should_create_a_success_result_with_a_none_value():
    result = Result(success=None)

    assert result.is_success
    assert result.value is None


@pytest.mark.unit
def test_should_create_a_failure_result_with_a_generic_error():
    result = Result(failure=Error())

    assert result.is_failure
    assert isinstance(result.value, Error)


@pytest.mark.unit
def test_should_create_a_failure_result_with_any_error():
    class AnyError(Error):
        pass

    result = Result(failure=AnyError())

    assert result.is_failure
    assert isinstance(result.value, AnyError)
    assert issubclass(result.value.__class__, Error)


@pytest.mark.unit
def test_should_raise_a_type_error_when_result_is_constructed_with_success_and_failure_at_the_same_time():
    with pytest.raises(TypeError) as excinfo:
        _ = Result(success="Success", failure="Failure")
        assert (
            "Result is a monad, it cannot be success and failure at the same time."
            in str(excinfo.value)
        )


@pytest.mark.unit
def test_should_raise_a_type_error_when_result_is_constructed_without_any_success_or_failure_value():
    with pytest.raises(TypeError) as excinfo:
        _ = Result()
        assert "Result is a monad, it must be a success or a failure." in str(
            excinfo.value
        )
