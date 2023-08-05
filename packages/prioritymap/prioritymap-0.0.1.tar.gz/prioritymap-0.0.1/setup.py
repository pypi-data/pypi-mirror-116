from setuptools import setup

import prioritymap  # noqa: F401

with open("README.md") as reader:
    readme = reader.read()

setup(
    name="prioritymap",
    version="0.0.1",
    author="Ryan Tjoa",
    license="Apache 2.0",
    description="Priority Map -- efficient heap x map",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "prioritymap"},
)
