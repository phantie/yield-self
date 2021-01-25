"""Build with
   > py setup.py sdist"""

from setuptools import setup, find_packages
from os.path import join, dirname
from yself import __version__

setup(
    author = 'phantie',
    name = 'yself',
    version = __version__,
    packages = find_packages(),
    long_description = open(join(dirname(__file__), 'README.md')).read(),
)