import pytest

from meiga import Result, Error
from meiga.return_error_on_failure import ReturnErrorOnFailure


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


@pytest.mark.unit
def test_should_repr_a_success_result():
    result = Result(success=2)
    assert "Result[status: success | value: 2]" == result.__repr__()


@pytest.mark.unit
def test_should_repr_a_failure_result():
    result = Result(failure=Error())
    assert "Result[status: failure | value: Error]" == result.__repr__()


@pytest.mark.unit
def test_should_eq_two_equal_success_result():
    result_1 = Result(success=2)
    result_2 = Result(success=2)

    assert result_1 == result_2


@pytest.mark.unit
def test_should_eq_two_different_success_result():
    result_1 = Result(success=2)
    result_2 = Result(success=3)

    assert result_1 != result_2


@pytest.mark.unit
def test_should_eq_two_equal_failure_result():
    result_1 = Result(failure=Error())
    result_2 = Result(failure=Error())

    assert result_1 == result_2


@pytest.mark.unit
def test_should_eq_two_different_failure_result():
    result_1 = Result(failure=Error())
    result_2 = Result(failure=Exception())

    assert result_1 != result_2


@pytest.mark.unit
def test_should_execute_success_handler():
    global called_success_handler
    called_success_handler = False

    global called_failure_handler
    called_failure_handler = False

    def success_handler():
        global called_success_handler
        called_success_handler = True

    def failure_handler():
        global called_failure_handler
        called_failure_handler = True

    result = Result(success="Hi!")
    result.handle(success_handler=success_handler, failure_handler=failure_handler)

    assert called_success_handler is True
    assert called_failure_handler is False


@pytest.mark.unit
def test_should_execute_failure_handler():
    global called_success_handler
    called_success_handler = False

    global called_failure_handler
    called_failure_handler = False

    def success_handler():
        global called_success_handler
        called_success_handler = True

    def failure_handler():
        global called_failure_handler
        called_failure_handler = True

    result = Result(failure=Error())

    with pytest.raises(ReturnErrorOnFailure):
        result.handle(success_handler=success_handler, failure_handler=failure_handler)

    assert called_success_handler is False
    assert called_failure_handler is True
