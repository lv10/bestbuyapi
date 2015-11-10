from setuptools import setup, find_packages

setup(
    name="BestBuyAPI",
    version="0.0.46",
    description="Best Buy API Wrapper",
    url="https://github.com/lv10/bestbuyapi",
    author="lv10",
    author_email="luis@lv10.me",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7"
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "argparse==1.2.1",
        "requests==2.7.0",
        "wsgiref==0.1.2",
    ],
)
