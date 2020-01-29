from setuptools import setup, find_packages

setup(
    name="BestBuyAPI",
    version="0.1.0",
    description="Best Buy API Wrapper",
    url="https://github.com/lv10/bestbuyapi",
    author="lv10",
    author_email="luis@lv10.me",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=["requests"],
)
