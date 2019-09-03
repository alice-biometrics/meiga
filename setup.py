from setuptools import setup

VERSION = "0.0.1"

setup(
    name="meiga",
    version=VERSION,
    description="A simple, typed and monad-based Result type for Python",
    keywords=["Result", "Monad", "Typed", "Typing"],
    url="https://github.com/alice-biometrics/meiga",
    author="ALiCE Biometrics",
    author_email="support@alicebiometrics.com",
    license="ALiCE Copyright",
    packages=["meiga", "meiga/assertions", "meiga/decorators"],
    zip_safe=False,
)
