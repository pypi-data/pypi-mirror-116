from setuptools import setup

import treecontainers  # noqa: F401

with open("README.md") as reader:
    readme = reader.read()

setup(
    name="treecontainers",
    version="0.0.1",
    author="Ryan Tjoa",
    license="Apache 2.0",
    description="Tree Containers -- PriorityMap, PrioritySet, TreeMap",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["treecontainers"],
)
