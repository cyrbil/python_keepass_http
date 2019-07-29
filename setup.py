#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import setuptools
from setuptools.command.build_py import build_py

import keepasshttp

here = os.path.abspath(os.path.dirname(__file__))


def get_content(filename):
    with open(os.path.join(here, filename), encoding="utf-8") as f:
        return f.read()


class PypiPublish(build_py):
    # noinspection PyTypeChecker
    def run(self):
        import sys
        import subprocess

        def python(cmd):
            if isinstance(cmd, str):
                cmd = cmd.split()
            cmd.insert(0, sys.executable)
            subprocess.check_call(cmd)

        python("-m pip install setuptools wheel twine")
        python("setup.py sdist bdist_wheel --universal")
        python("-m twine upload --verbose dist/*")


setuptools.setup(
    name="keepasshttp",
    version=keepasshttp.__VERSION__,
    packages=["keepasshttp"],
    url="https://github.com/cyrbil/python_keepass_http",
    license="License :: OSI Approved :: MIT License",
    author="Cyril DEMINGEON",
    author_email="1126098+cyrbil@users.noreply.github.com",
    description="Python client for KeePassHTTP to interact with KeePass's credentials",
    long_description=get_content("README.md"),
    long_description_content_type="text/markdown",
    install_requires=[
        requirement.split(maxsplit=1)[0] 
        for requirement in get_content("requirements.txt").split('\n')
        if requirement
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest-cov"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Security",
    ],
    cmdclass={"publish": PypiPublish},
)
