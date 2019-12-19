import pytest

from meiga import Result, Error, isFailure, isSuccess
from meiga.decorators import meiga
from meiga.return_error_on_failure import ReturnErrorOnFailure


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


@pytest.mark.unit
def test_should_execute_success_handler_with_valid_parameters():
    given_first_parameter = 1
    given_second_parameter = 2

    global called_success_handler
    called_success_handler = False

    global called_failure_handler
    called_failure_handler = False

    def success_handler(param_1, param_2):
        global called_success_handler
        called_success_handler = True
        assert given_first_parameter == param_1
        assert given_second_parameter == param_2

    def failure_handler():
        global called_failure_handler
        called_failure_handler = True

    result = Result(success="Hi!")
    result.handle(
        success_handler=success_handler,
        failure_handler=failure_handler,
        success_args=(given_first_parameter, given_second_parameter),
    )

    assert called_success_handler is True
    assert called_failure_handler is False


@pytest.mark.unit
@pytest.mark.parametrize("result", [isSuccess, isFailure])
def test_should_execute_handler_with_additional_and_non_required_parameters(result):
    given_first_parameter = 1

    def success_handler():
        pass

    def failure_handler():
        pass

    @meiga
    def run():
        result.handle(
            success_handler=success_handler,
            failure_handler=failure_handler,
            success_args=given_first_parameter,
            failure_args=given_first_parameter,
        )

    run()
