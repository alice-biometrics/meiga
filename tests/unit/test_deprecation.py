import pytest

from meiga import OnFailureHandler, OnSuccessHandler
from meiga.deprecation import (
    get_on_failure_handler_from_deprecated_args,
    get_on_success_handler_from_deprecated_args,
)


@pytest.mark.unit
class TestDeprecation:
    success_deprecated_params: dict
    failure_deprecated_params: dict

    def setup(self):
        def func(param_1: int):
            pass

        self.success_deprecated_params = dict(on_success=func, arg=(1,))
        self.failure_deprecated_params = dict(on_failure=func, arg=(1,))

    def should_get_on_success_handler_from_older_parameters(self):
        on_success_handler = get_on_success_handler_from_deprecated_args(
            self.success_deprecated_params
        )
        assert isinstance(on_success_handler, OnSuccessHandler)

    def should_get_on_failure_handler_from_older_parameters(self):
        on_failure_handler = get_on_failure_handler_from_deprecated_args(
            self.failure_deprecated_params
        )
        assert isinstance(on_failure_handler, OnFailureHandler)

    def should_get_none_asking_for_on_success_handler_from_empty_parameters(self):
        on_success_handler = get_on_success_handler_from_deprecated_args(dict())
        assert on_success_handler is None

    def should_get_none_asking_for_on_failure_handler_from_empty_parameters(self):
        on_failure_handler = get_on_failure_handler_from_deprecated_args(dict())
        assert on_failure_handler is None
