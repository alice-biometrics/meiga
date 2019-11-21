# coding=utf-8
# Copyright (C) 2019+ Alice, Vigo, Spain

"""Public API of ALiCE meiga package"""

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
from .alias import Success, isSuccess, Failure, isFailure, NotImplementedMethodError

alias = ["Success", "isSuccess", "Failure", "isFailure", "NotImplementedMethodError"]

__all__ = modules + classes + errors + alias
