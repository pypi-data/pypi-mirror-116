from setuptools import setup
import os
import re

def _requirements_from_file(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()

def get_version(package):
    path = os.path.join(package,"__init__.py")
    with open(path, "r", encoding="utf-8") as f:
        init_py = f.read()
    return re.search(
        r"__version__ = ['\"]([^'\"]+)['\"]",
        init_py
    ).group(1)

setup(
    install_requires = _requirements_from_file("requirements.txt"),
    version = get_version("printm"),
)
