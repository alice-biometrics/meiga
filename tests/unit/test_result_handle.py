from typing import List

import pytest

from meiga import Error, OnFailureAction, OnSuccessAction, Result, isFailure, isSuccess
from meiga.decorators import meiga


@pytest.mark.unit
def test_should_execute_success_handler():
    global called_on_success
    called_on_success = False

    global called_on_failure
    called_on_failure = False

    def on_success_func(success_value):
        global called_on_success
        called_on_success = True
        assert isinstance(success_value, str)

    def on_failure_func(failure_value):
        global called_on_failure
        called_on_failure = True
        assert isinstance(failure_value, Error)

    result = Result(success="Hi!")
    new_result = result.handle(
        on_success_action=OnSuccessAction(func=on_success_func),
        on_failure_action=OnFailureAction(func=on_failure_func),
    )

    assert new_result == result
    assert called_on_success is True
    assert called_on_failure is False


@pytest.mark.unit
def test_should_execute_failure_handler():
    global called_on_success
    called_on_success = False

    global called_on_failure
    called_on_failure = False

    def on_success_func(result: Result):
        global called_on_success
        called_on_success = True

    def on_failure_func(result: Result):
        global called_on_failure
        called_on_failure = True

    result = Result(failure=Error())

    new_result = result.handle(
        on_success_action=OnSuccessAction(func=on_success_func),
        on_failure_action=OnFailureAction(func=on_failure_func),
    )

    assert new_result == result
    assert called_on_success is False
    assert called_on_failure is True


@pytest.mark.unit
def test_should_execute_success_handler_with_valid_parameters():
    given_first_parameter = 1
    given_second_parameter = 2

    global called_on_success
    called_on_success = False

    global called_on_failure
    called_on_failure = False

    def on_success_func(param_1, param_2):
        global called_on_success
        called_on_success = True
        assert given_first_parameter == param_1
        assert given_second_parameter == param_2

    def on_failure_func():
        global called_on_failure
        called_on_failure = True

    result = Result(success="Hi!")
    result.handle(
        on_success_action=OnSuccessAction(
            func=on_success_func, args=(given_first_parameter, given_second_parameter)
        ),
        on_failure_action=OnFailureAction(func=on_failure_func),
    )

    assert called_on_success is True
    assert called_on_failure is False


@pytest.mark.unit
@pytest.mark.parametrize("result", [isSuccess, isFailure])
def test_should_execute_handler_with_one_int_additional_parameters(result):
    given_first_parameter = (1,)

    def on_success_func(param_1: int):
        assert param_1 == 1

    def on_failure_func(param_1: int):
        assert param_1 == 1

    @meiga
    def run():
        result.handle(
            on_success_action=OnSuccessAction(
                func=on_success_func, args=given_first_parameter
            ),
            on_failure_action=OnFailureAction(
                func=on_failure_func, args=given_first_parameter
            ),
        )

    run()


@pytest.mark.unit
@pytest.mark.parametrize("result", [isSuccess, isFailure])
def test_should_execute_handler_with_a_list_additional_parameters(result):
    given_first_parameter = [1]

    def on_success_func(param_1: list):
        assert param_1 == [1]

    def on_failure_func(param_1: list):
        assert param_1 == [1]

    @meiga
    def run():
        result.handle(
            on_success_action=OnSuccessAction(
                func=on_success_func, args=given_first_parameter
            ),
            on_failure_action=OnFailureAction(
                func=on_failure_func, args=given_first_parameter
            ),
        )

    run()


@pytest.mark.unit
def test_should_execute_success_handler_without_any_argument():
    global called_on_success
    called_on_success = False

    global called_on_failure
    called_on_failure = False

    def on_success_func():
        global called_on_success
        called_on_success = True

    def on_failure_func():
        global called_on_failure
        called_on_failure = True

    result = Result(success="Hi!")
    result.handle(
        on_success_action=OnSuccessAction(func=on_success_func, args=()),
        on_failure_action=OnFailureAction(func=on_failure_func, args=()),
    )

    assert called_on_success is True
    assert called_on_failure is False


@pytest.mark.parametrize("result", [isSuccess, isFailure])
def test_should_execute_handler_with_additional_and_non_required_parameters_result_first(
    result,
):
    given_first_parameter = (Result.__id__, 1)

    def on_success_func(result: Result, param_1: int):
        assert isinstance(result, Result)
        assert result.value is True
        assert param_1 == 1

    def on_failure_func(result: Result, param_1: int):
        assert isinstance(result, Result)
        assert result.value == Error()
        assert param_1 == 1

    @meiga
    def run():
        result.handle(
            on_success_action=OnSuccessAction(
                func=on_success_func, args=given_first_parameter
            ),
            on_failure_action=OnFailureAction(
                func=on_failure_func, args=given_first_parameter
            ),
        )

    run()


@pytest.mark.parametrize("result", [isSuccess, isFailure])
def test_should_execute_handler_with_additional_and_non_required_parameters_result_last(
    result,
):
    given_first_parameter = (1, Result.__id__)

    def on_success_func(param_1: int, result: Result):
        assert param_1 == 1
        assert isinstance(result, Result)
        assert result.value is True

    def on_failure_func(param_1: int, result: Result):
        assert param_1 == 1
        assert isinstance(result, Result)
        assert result.value == Error()

    @meiga
    def run():
        result.handle(
            on_success_action=OnSuccessAction(
                func=on_success_func, args=given_first_parameter
            ),
            on_failure_action=OnFailureAction(
                func=on_failure_func, args=given_first_parameter
            ),
        )

    run()


@pytest.mark.parametrize("result", [isSuccess, isFailure])
def test_should_execute_handler_with_additional_and_non_required_parameters_result_middle(
    result,
):
    given_first_parameter = (1, Result.__id__, 2)

    def on_success_func(param_1: int, result: Result, param_2: int):
        assert param_1 == 1
        assert isinstance(result, Result)
        assert result.value is True
        assert param_2 == 2

    def on_failure_func(param_1: int, result: Result, param_2: int):
        assert param_1 == 1
        assert isinstance(result, Result)
        assert result.value == Error()
        assert param_2 == 2

    @meiga
    def run():
        result.handle(
            on_success_action=OnSuccessAction(
                func=on_success_func, args=given_first_parameter
            ),
            on_failure_action=OnFailureAction(
                func=on_failure_func, args=given_first_parameter
            ),
        )

    run()


# TODO To be reviewed...
#  As we are typing args to Tuple, we get
# Expected type 'Optional[Iterable]', got 'int' instead
@pytest.mark.parametrize("result", [isSuccess, isFailure])
def test_should_execute_handler_with_only_one_parameter(result):
    given_first_parameter = 1

    def on_success_func(param_1: int):
        assert param_1 == 1

    def on_failure_func(param_1: int):
        assert param_1 == 1

    @meiga
    def run():
        result.handle(
            on_success_action=OnSuccessAction(
                func=on_success_func, args=given_first_parameter
            ),
            on_failure_action=OnFailureAction(
                func=on_failure_func, args=given_first_parameter
            ),
        )

    run()


@pytest.mark.parametrize("result", [isSuccess, isFailure])
def test_should_execute_handler_with_an_empty_list(result):
    given_first_parameter = []

    def on_success_func(param_1: List):
        assert isinstance(param_1, list)
        assert len(param_1) == 0

    def on_failure_func(param_1: List):
        assert isinstance(param_1, list)
        assert len(param_1) == 0

    @meiga
    def run():
        result.handle(
            on_success_action=OnSuccessAction(
                func=on_success_func, args=given_first_parameter
            ),
            on_failure_action=OnFailureAction(
                func=on_failure_func, args=given_first_parameter
            ),
        )

    run()
