from __future__ import annotations

from typing import Any

from meiga.handlers import OnFailureHandler, OnSuccessHandler


def get_on_success_handler_from_deprecated_args(
    kwargs: dict[Any, Any]
) -> OnSuccessHandler | None:
    on_success = kwargs.get("on_success")
    if on_success:
        return OnSuccessHandler(func=on_success, args=kwargs.get("success_args"))
    return None


def get_on_failure_handler_from_deprecated_args(
    kwargs: dict[Any, Any],
) -> OnFailureHandler | None:
    on_failure = kwargs.get("on_failure")
    if on_failure:
        return OnFailureHandler(func=on_failure, args=kwargs.get("failure_args"))
    return None
