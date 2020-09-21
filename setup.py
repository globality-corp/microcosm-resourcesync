#!/usr/bin/env python
from setuptools import find_packages, setup

project = "microcosm-resourcesync"
version = "1.0.0"

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
        # 09-21-2020: pin for enforce_white_space issue @pierce
        "isort<5",
    ],
    setup_requires=[
        "nose>=1.3.7",
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
)
