#!/usr/bin/env python
from setuptools import find_packages, setup


project = "microcosm-resourcesync"
version = "2.0.0"

setup(
    name=project,
    version=version,
    description="Synchronize resources between endpoints",
    author="Globality Engineering",
    author_email="engineering@globality.com",
    url="https://github.com/globality-corp/microcosm-resourcesync",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    keywords="microcosm",
    install_requires=[
        "click>=6.7",
        "PyYAML>=3.12",
        "requests>=2.18.4",
    ],
    setup_requires=[
    ],
    dependency_links=[
    ],
    entry_points={
        "console_scripts": [
            "resource-sync = microcosm_resourcesync.main:main",
        ],
    },
    tests_require=[
        "coverage>=4.3.4",
        "PyHamcrest>=1.9.0",
    ],
    extras_require={
        "test": [
            "coverage>=3.7.1",
            "PyHamcrest>=1.8.5",
            "pytest-cov>=3.0.0",
            "pytest>=6.2.5",
            "pytest-cov>=5.0.0",
        ],
        "lint": [
            "flake8",
            "flake8-print",
            "flake8-isort",
        ],
        "typehinting": [
            "mypy",
            "types-PyYAML",
            "types-requests",
        ],
    },
)
