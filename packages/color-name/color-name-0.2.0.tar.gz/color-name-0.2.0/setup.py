
import pathlib
from setuptools import setup
from colorname import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="color-name",
    version=__version__,
    description="Tells you what name a color has",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tvanderplas/color-name",
    author="Tim Vanderplas",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["colorname"],
    include_package_data=True,
    install_requires=["pillow"],
)
