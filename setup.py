import sys
from setuptools import setup, find_packages

ERROR_UNSUPPORTED_PYTHON = f'BestBuyApi only supports Python 3.6 or later'
PY36_OR_OLDER = sys.version_info < (3, 6)
if PY37_OR_LATER:
    raise Exception(UNSUPPORTED_PYTHON)

setup(
    name="BestBuyAPI",
    version="1.0.0",
    description="Best Buy API Wrapper",
    url="https://github.com/lv10/bestbuyapi",
    author="lv10",
    author_email="luis@lv10.me",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=["requests"],
)
