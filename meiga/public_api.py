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
from .decorators.early_return import early_return
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
    "early_return",
]
