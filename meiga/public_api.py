# coding=utf-8
# Copyright (C) 2021+ Alice, Vigo, Spain

"""Public API of Alice meiga package"""

# Modules
from . import decorators

modules = ["decorators"]

# Classes
from .result import Result

classes = ["Result"]

# Errors
from .error import Error

errors = ["Error"]

# Alias
from .alias import (
    BoolResult,
    Failure,
    NotImplementedMethodError,
    Success,
    isFailure,
    isSuccess,
)

alias = [
    "Success",
    "isSuccess",
    "Failure",
    "isFailure",
    "NotImplementedMethodError",
    "BoolResult",
]

__all__ = modules + classes + errors + alias
