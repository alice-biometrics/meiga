import pytest

from meiga import Error, Failure, Success


@pytest.mark.unit
def test_should_map_a_success_result_encapsulated_value():
    def mapper(value):
        return f"{value} Meiga"

    result = Success("Hi")
    result.map(mapper)

    assert result.value == "Hi Meiga"


@pytest.mark.unit
def test_should_map_a_failure_result_encapsulated_value():
    def mapper(domain_error):
        if isinstance(domain_error, Error):
            return "Error"
        else:
            return domain_error

    result = Failure(Error())
    result.map(mapper)

    assert result.value == "Error"
