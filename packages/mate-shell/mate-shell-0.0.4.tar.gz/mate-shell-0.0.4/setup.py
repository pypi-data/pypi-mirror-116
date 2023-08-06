# pylint: disable=undefined-variable
from os import path
from setuptools import setup, find_packages

__version__ = "0.0.4"
__author__ = "r00t3r"


def read_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


requirements = read_requirements()

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="mate-shell",
    license="GPL",
    version=__version__,
    author=__author__,
    url="https://github.com/twisted-fun/mate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source Code": "https://github.com/twisted-fun/mate",
        "Documentation": "https://github.com/twisted-fun/mate/README.md",
    },
    packages=find_packages(exclude=(["tests", "docs"])),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["mate = mate.__main__:main"]},
)
