#!/usr/bin/env python3.10
from __future__ import annotations

import glob
import os
import pathlib

from mypyc.build import mypycify  # type: ignore
from setuptools import find_packages, setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()
VERSION = "0.0.1"


# Adopted from https://github.com/python/mypy/blob/master/setup.py
def find_package_data(base: str, globs: list[str]) -> list[str]:
    """Find all interesting data files, for setup(package_data=)
    Arguments:
      root:  The directory to search in.
      globs: A list of glob patterns to accept files.
    """

    rv_dirs = [root for root, _, _ in os.walk(base)]
    rv = []
    for rv_dir in rv_dirs:
        files = []
        for pat in globs:
            files += glob.glob(os.path.join(rv_dir, pat))
        if not files:
            continue
        rv.extend(files)
    return rv


setup(
    name="codecomrade",
    version=VERSION,
    description="Git helpers with CODEOWNERS awareness.",
    author="Jamison Lahman",
    author_email="jamison@lahman.dev",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jmelahman/codecomrade",
    py_modules=[],
    ext_modules=mypycify(find_package_data("codecomrade", ["*.py"])),
    package_dir={"codecomrade": "codecomrade"},
    packages=find_packages(),
    scripts=["bin/codecomrade"],
    keywords=["github", "codeowners"],
    download_url=f"https://github.com/jmelahman/codecomrade/archive/refs/tags/v{VERSION}.tar.gz",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: System :: Software Distribution",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=["click", "codeowners"],
)
