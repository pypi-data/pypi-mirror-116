#!/usr/bin/env python3

# Tar Wrap the Package: python setup.py sdist
# Upload to PYPI: twine upload dist/*

from setuptools import setup, find_packages

setup(
    name='connectwrap',
    version='1.1.5',
    packages=find_packages(),
    license='MIT',
    description='A Python package for SQLite database management & object relational mapping.',
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CodeConfidant/connectwrap-sqlite3',
    author='Drew Hainer',
    author_email='codeconfidant@gmail.com',
    platforms=['Windows', 'Linux']
)