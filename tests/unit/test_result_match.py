import sys

import pytest

from meiga import Result, Success


@pytest.mark.unit
@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10")
def test_should_match():
    called_success = False
    result = Result(success="Hi!")
    match result:
        case Success("Hi!"):
            called_success = True
        case (_, "Hi!"):
            print("failure")
        case _:
            print("default")

    assert called_success is True
