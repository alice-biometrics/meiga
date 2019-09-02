# coding=utf-8
# Copyright (C) 2019+ Alice, Vigo, Spain

"""Public API of ALiCE Onboarding Python SDK"""

# Modules
from . import decorators

modules = ["decorators"]

# Classes
from .result import Result

classes = ["Result"]

# Errors
from .error import Error

errors = ["Error"]

__all__ = modules + classes + errors
