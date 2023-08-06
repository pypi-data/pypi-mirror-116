from setuptools import setup, find_packages
from tdfs import __version__

NAME = "tdfs"

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("docs/pypi.md", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=__version__,
    description="Feature Store client using Teradata Dataframes",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6.0',
    author="Teradata",
    author_email="teradata.corporation@teradatacorporation.com",
    url="",
    install_requires=required,
    packages=find_packages(exclude=('tests',)),
    include_package_data=True
)
