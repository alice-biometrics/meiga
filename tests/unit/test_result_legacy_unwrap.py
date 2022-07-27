import pytest

from meiga import Error, Failure, Success


@pytest.mark.unit
def test_should_call_legacy_on_failure_when_unwrap_or_else_with_a_result_failure():

    global called_on_failure
    called_on_failure = False

    def on_failure(failure_value):
        global called_on_failure
        called_on_failure = True
        assert isinstance(failure_value, Error)

    result = Failure(Error())

    _ = result.unwrap_or_else(on_failure=on_failure)

    assert called_on_failure


@pytest.mark.unit
def test_should_call_legacy_on_failure_when_unwrap_or_else_with_a_result_failure_without_passing_arguments():

    global called_on_failure
    called_on_failure = False

    def on_failure():
        global called_on_failure
        called_on_failure = True

    result = Failure(Error())

    _ = result.unwrap_or_else(on_failure=on_failure)

    assert called_on_failure


@pytest.mark.unit
def test_should_call_legacy_on_failure_when_unwrap_or_else_with_failure_result_and_custom_args():
    param1 = 1
    param2 = "param2"

    global called_on_failure
    called_on_failure = False

    def on_failure(param1, param2):
        global called_on_failure
        called_on_failure = True
        assert isinstance(param1, int)
        assert isinstance(param2, str)

    result = Failure(Error())

    _ = result.unwrap_or_else(on_failure=on_failure, failure_args=(param1, param2))

    assert called_on_failure


@pytest.mark.unit
def test_should_legacy_call_on_success_when_unwrap_and_with_a_result_success():

    global called_on_success
    called_on_success = False

    def on_success(success_value):
        global called_on_success
        called_on_success = True
        assert isinstance(success_value, str)

    result = Success("Hi!")

    _ = result.unwrap_and(on_success=on_success)

    assert called_on_success


@pytest.mark.unit
def test_should_call_legacy_on_success_when_unwrap_and_with_a_result_success_without_passing_arguments():

    global called_on_success
    called_on_success = False

    def on_success():
        global called_on_success
        called_on_success = True

    result = Success("Hi!")

    _ = result.unwrap_and(on_success=on_success)

    assert called_on_success


@pytest.mark.unit
def test_should_call_legacy_on_success_when_unwrap_and_with_a_result_success_and_custom_args():
    param1 = 1
    param2 = "param2"

    global called_on_success
    called_on_success = False

    def on_success(param1, param2):
        global called_on_success
        called_on_success = True
        assert isinstance(param1, int)
        assert isinstance(param2, str)

    result = Success("Hi!")

    _ = result.unwrap_and(on_success=on_success, success_args=(param1, param2))

    assert called_on_success
