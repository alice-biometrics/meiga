from typing import Dict, Union

from meiga.derived_actions import OnFailureAction, OnSuccessAction


def get_on_success_handler_from_deprecated_args(
    kwargs: Dict,
) -> Union[OnSuccessAction, None]:
    on_success = kwargs.get("on_success")
    if on_success:
        return OnSuccessAction(func=on_success, args=kwargs.get("success_args"))
    return None


def get_on_failure_handler_from_deprecated_args(
    kwargs: Dict,
) -> Union[OnFailureAction, None]:
    on_failure = kwargs.get("on_failure")
    if on_failure:
        return OnFailureAction(func=on_failure, args=kwargs.get("failure_args"))
    return None
