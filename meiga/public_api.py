# coding=utf-8
# Copyright (C) 2021+ Alice, Vigo, Spain

"""Public API of Alice meiga package"""

from . import decorators
from .alias import (
    AnyResult,
    BoolResult,
    Failure,
    NotImplementedMethodError,
    Success,
    isFailure,
    isSuccess,
)
from .decorators.to_result import to_result
from .error import Error
from .handlers import OnFailureHandler, OnSuccessHandler
from .result import Result

__all__ = [
    "decorators",
    "Result",
    "Error",
    "Success",
    "isSuccess",
    "Failure",
    "isFailure",
    "NotImplementedMethodError",
    "BoolResult",
    "AnyResult",
    "OnSuccessHandler",
    "OnFailureHandler",
    "to_result",
]
