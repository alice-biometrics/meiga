import pytest

from meiga import Error, Failure, Result, Success


@pytest.mark.unit
class TestMatch:
    @pytest.mark.parametrize(
        "result, expected_success, expected_failure",
        [
            (Success(), True, False),
            (Success("hello"), True, False),
            (Failure(), False, True),
            (Failure(Error()), False, True),
        ],
    )
    def should_match_simple(
        self, result: Result, expected_success: bool, expected_failure: bool
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

    def should_match_specific_success(self):
        called_success = False
        result = Success("hello")

        match result:
            case Success("hello"):
                called_success = True

        assert called_success is True

    def should_match_specific_failure(self):
        called_failure = False
        result = Failure(Error())

        match result:
            case Failure(Error()):
                called_failure = True

        assert called_failure is True

    def should_match_when_user_result_success(self):
        called_success = False
        result = Result(success=True)

        match result:
            case Result(_):
                called_success = True

        assert called_success is True

    def test_should_match_when_user_result_failure(self):
        called_failure = False
        result = Result(failure=Error())

        match result:
            case Result(_, Error()):
                called_failure = True

        assert called_failure is True
