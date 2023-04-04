import pytest

from meiga import Error, Failure, Success


@pytest.mark.unit
def test_should_throw_an_exception_when_result_is_failure():
    with pytest.raises(Error):
        Failure(Error()).throw()


@pytest.mark.unit
def test_should_raise_an_exception_when_result_is_failure():
    with pytest.raises(Error):
        Failure(Error()).reraise()


@pytest.mark.unit
def test_should_throw_a_type_error_when_result_is_failure_but_type_is_not_error():
    with pytest.raises(TypeError):
        Failure("Hi").throw()


@pytest.mark.unit
def test_should_raise_a_type_error_when_result_is_failure_but_type_is_not_error():
    with pytest.raises(TypeError):
        Failure("Hi").reraise()


@pytest.mark.unit
def test_should_not_throw_an_exception_when_result_is_success():
    Success("Hi!").throw()


@pytest.mark.unit
def test_should_not_raise_an_exception_when_result_is_success():
    Success("Hi!").reraise()
