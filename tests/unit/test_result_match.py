import sys

import pytest

from meiga import Error, Failure, Result, Success

version_less_than_3_10 = sys.version_info < (3, 10)


@pytest.mark.unit
@pytest.mark.skipif(version_less_than_3_10, reason="requires python3.10")
@pytest.mark.parametrize(
    "result, expected_success, expected_failure",
    [
        (Success(), True, False),
        (Success("hello"), True, False),
        (Failure(), False, True),
        (Failure(Error()), False, True),
    ],
)
def test_should_match_simple(
    result: Result, expected_success: bool, expected_failure: bool
):
    called_success = False
    called_failure = False

    match result:
        case Success(_):
            called_success = True
        case Failure(_):
            called_failure = True

    assert called_success is expected_success
    assert called_failure is expected_failure


@pytest.mark.unit
@pytest.mark.skipif(version_less_than_3_10, reason="requires python3.10")
def test_should_match_specific_success():
    called_success = False
    result = Success("hello")

    match result:
        case Success("hello"):
            called_success = True

    assert called_success is True


@pytest.mark.unit
@pytest.mark.skipif(version_less_than_3_10, reason="requires python3.10")
def test_should_match_specific_failure():
    called_failure = False
    result = Failure(Error())

    match result:
        case Failure(Error()):
            called_failure = True

    assert called_failure is True


@pytest.mark.unit
@pytest.mark.skipif(version_less_than_3_10, reason="requires python3.10")
def test_should_match_when_user_result_success():
    called_success = False
    result = Result(success=True)

    match result:
        case Result(_):
            called_success = True

    assert called_success is True


@pytest.mark.unit
@pytest.mark.skipif(version_less_than_3_10, reason="requires python3.10")
def test_should_match_when_user_result_failure():
    called_failure = False
    result = Result(failure=Error())

    match result:
        case Result(_, Error()):
            called_failure = True

    assert called_failure is True
