import pytest

from meiga import Error, Failure, Success


@pytest.mark.unit
def test_should_transform_a_success_result_encapsulated_value():
    def transform(value):
        return f"{value} Meiga"

    result = Success("Hi")
    result.map(transform)

    assert result.value == "Hi Meiga"


@pytest.mark.unit
def test_should_transform_a_failure_result_encapsulated_value():
    def transform(domain_error):
        if isinstance(domain_error, Error):
            return "Error"
        else:
            return domain_error

    result = Failure(Error())
    result.map(transform)

    assert result.value == "Error"
