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

setup(
    name="graphene-gis",
    version="0.0.2",
    description="GIS support for graphene-django",
    keywords="api graphql graphene geos gis",
    packages=find_packages(exclude=["tests"]),
    author="Rishabh Mehta",
    author_email="eternal.blizzard23@gmail.com",
    install_requires=[
        "graphene==2.1.8",
        "graphene-django==2.5.0",
        "graphql-core==2.2.1",
        "psycopg2==2.8.3"
    ],

    setup_requires=["pytest-runner"],
    tests_require=tests_require,

    extras_require={
        "test": tests_require,
        "dev": dev_requires,
    },

    include_package_data=True,
    zip_safe=False,
    platforms="any",
)
