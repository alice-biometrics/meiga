import pytest

from meiga import Error, Failure, Result, Success


@pytest.mark.unit
class TestResultAttributesOfObjectType:
    def should_repr_a_success_result(self):
        result = Result(success=2)
        assert "Result[status: success | value: 2]" == result.__repr__()

    def should_repr_a_success(self):
        result = Success(2)
        assert "Result[status: success | value: 2]" == result.__repr__()

    def should_repr_a_failure_result(self):
        result = Result(failure=Error())
        assert "Result[status: failure | value: Error]" == result.__repr__()

    def should_repr_a_failure(self):
        result = Failure(Error())
        assert "Result[status: failure | value: Error]" == result.__repr__()

    def should_eq_two_equal_success_result(self):
        result_1 = Result(success=2)
        result_2 = Result(success=2)

        assert result_1 == result_2

    def should_eq_two_different_success_result(self):
        result_1 = Result(success=2)
        result_2 = Result(success=3)

        assert result_1 != result_2

    def should_eq_a_result_with_another_type(self):
        result_1 = Result(success=2)
        result_2 = "no_result_value"

        assert result_1 != result_2

    def should_eq_two_equal_failure_result(self):
        result_1 = Result(failure=Error())
        result_2 = Result(failure=Error())

        assert result_1 == result_2

    def should_eq_two_different_failure_result(self):
        result_1 = Result(failure=Error())
        result_2 = Result(failure=Exception())

        assert result_1 != result_2

    @pytest.mark.parametrize(
        "result",
        [
            Result(success="hello"),
            Result(failure=Exception()),
            Result(failure=Error()),
            Success("hello"),
            Failure(Exception()),
            Failure(Error()),
        ],
    )
    def should_hashes_are_equal(self, result: Result):
        assert hash(result) == hash(result)
