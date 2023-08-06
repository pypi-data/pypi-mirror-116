#!/usr/bin/env python3

from setuptools import setup

setup(
    name='filewrap',
    version='1.1.4',
    py_modules=['filewrap'],
    license='MIT',
    description='A Python package for file/archive manipulation & management.',
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CodeConfidant/filewrap-os',
    author='Drew Hainer',
    author_email='codeconfidant@gmail.com',
    platforms=['Windows', 'Linux']
)

# - Update README.md and README.txt
# - Update Version Number
# - Tar Wrap the Package: python setup.py sdist
# - Upload to PYPI: twine upload dist/*
# - Commit Changes
# - Change Release Version in Github Repo