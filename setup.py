#!/usr/bin/env python
from distutils.core import setup
import setuptools

setup(
    name='test_data_generator',
    version='1.4',
    description='Random Test Data Generator for PLICS system',
    author='dev team',
    packages=setuptools.find_packages(),
    install_requires=['xmlschema', 'faker', 'exrex', 'lxml', 'typer']
)
