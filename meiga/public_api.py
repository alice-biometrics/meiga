# coding=utf-8
# Copyright (C) 2021+ Alice, Vigo, Spain

"""Public API of Alice meiga package"""

from . import decorators
from .alias import (
    BoolResult,
    Failure,
    NotImplementedMethodError,
    Success,
    isFailure,
    isSuccess,
)
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
    "OnSuccessHandler",
    "OnFailureHandler",
]
