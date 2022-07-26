import pytest
from hypothesis import given
from hypothesis.strategies import (
    booleans,
    composite,
    dictionaries,
    floats,
    integers,
    lists,
    none,
    one_of,
    text,
    times,
    tuples,
    uuids,
)

from meiga import Result


@composite
def all_types(draw):
    return draw(
        one_of(
            text(),
            integers(),
            none(),
            booleans(),
            floats(),
            tuples(),
            times(),
            uuids(),
            lists(integers()),
            dictionaries(text(), text()),
        )
    )


@pytest.mark.property
@given(given_value=all_types())
def test_property_should_works_with_any_type_on_success(given_value):

    result = Result(success=given_value)

    assert result.is_success


@pytest.mark.property
@given(given_value=all_types())
def test_property_should_works_with_any_type_on_failure(given_value):

    result = Result(failure=given_value)

    assert result.is_failure
