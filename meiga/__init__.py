import os

from meiga import public_api
from meiga.public_api import *

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

__version__ = open(f"{ROOT_PATH}/VERSION", "r").read()[:-1]

__all__ = public_api.__all__
