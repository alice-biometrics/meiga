from setuptools import setup

VERSION = "0.0.1"

setup(
    name="meiga",
    version=VERSION,
    description="Alice Onboarding Python SDK",
    url="https://github.com/alicebiometrics/meiga",
    author="ALiCE Biometrics",
    author_email="support@alicebiometrics.com",
    license="ALiCE Copyright",
    packages=["meiga", "meiga/assertions", "meiga/decorators"],
    zip_safe=False,
)
