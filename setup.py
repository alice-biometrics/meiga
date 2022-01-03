import os

from setuptools import setup

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = "meiga"
VERSION = open("meiga/VERSION", "r").read()

# The text of the README file
with open(os.path.join(CURRENT_DIR, "README.md")) as fid:
    README = fid.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="A simple, typed and monad-based Result type for Python",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["Result", "Monad", "Typed", "Typing"],
    url="https://github.com/alice-biometrics/meiga",
    author="Alice Biometrics",
    author_email="support@alicebiometrics.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["meiga", "meiga/assertions", "meiga/decorators"],
    include_package_data=True,
    zip_safe=False,
)
