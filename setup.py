#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os

from setuptools import find_packages, setup

NAME = 'doccano'
DESCRIPTION = 'doccano, text annotation tool for machine learning practitioners'
URL = 'https://github.com/doccano/doccano'
EMAIL = 'hiroki.nakayama.py@gmail.com'
AUTHOR = 'Hironsan'
LICENSE = 'MIT'

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Todo: make a cleaned requirements.txt
required = [line.rstrip() for line in io.open(os.path.join(here, 'app/requirements.txt'))
            if not line.startswith(('psycopg2', 'django-heroku', 'django-mssql-backend'))]

setup(
    name=NAME,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('*.tests',)),
    entry_points={
        'console_scripts': [
            'doccano = app.doccano.doccano:main'
        ]
    },
    install_requires=required,
    extras_require={
        'postgresql': ['psycopg2-binary>=2.8.6'],
        'mssql': ['django-mssql-backend>=2.8.1'],
    },
    include_package_data=True,
    license=LICENSE,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
