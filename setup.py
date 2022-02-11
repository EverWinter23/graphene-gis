from setuptools import find_packages, setup

tests_require = [
    "pytest>=5.1.2",
    "pytest-cov==2.7.1",
    "pytest-django>=3.5.1"
]

dev_requires = [
    "black==19.3b0",
    "flake8==3.7.8",
] + tests_require

with open("README.md", "r") as desc:
    long_description = desc.read()

setup(
    name="graphene-gis",
    version="0.0.7",
    description="GIS support for graphene-django",
    long_description_content_type='text/markdown',
    url="https://github.com/EverWinter23/graphene-gis",
    long_description=long_description,
    keywords="api graphql graphene geos gis",
    packages=find_packages(exclude=["tests"]),
    author="Rishabh Mehta",
    author_email="eternal.blizzard23@gmail.com",
    install_requires=[
        "graphene>=2.1,<3",
        "graphene-django>=2.5,<3",
        "graphql-core>=2.1,<3",
    ],

    setup_requires=["pytest-runner"],
    tests_require=tests_require,

    extras_require={
        "test": tests_require,
        "dev": dev_requires,
    },

    classifiers=(
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),

    include_package_data=True,
    zip_safe=False,
    platforms="any",
)
