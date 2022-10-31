import os

from meiga import public_api
from meiga.public_api import *

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

with open(f"{ROOT_PATH}/VERSION") as f:
    __version__ = f.read().rstrip()

__all__ = public_api.__all__
