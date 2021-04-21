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

required = [
    'apache-libcloud>=3.2.0',
    'colour>=0.1.5',
    'conllu>=4.2.2',
    'dj-database-url>=0.5.0',
    'django-cors-headers>=3.5.0',
    'django-filter>=2.4.0',
    'django-rest-polymorphic>=0.1.9',
    'djangorestframework-csv>=2.1.0',
    'djangorestframework-xml>=2.0.0',
    'drf-yasg>=1.20.0',
    'environs>=9.2.0',
    'furl>=2.1.0',
    'pyexcel>=0.6.6',
    'pyexcel-xlsx>=0.6.0',
    'python-jose>=3.2.0',
    'seqeval>=1.2.2',
    'social-auth-app-django>=4.0.0',
    'whitenoise>=5.2.0',
    'auto-labeling-pipeline>=0.1.12',
    'celery>=5.0.5',
    'dj-rest-auth>=2.1.4',
    'django-celery-results>=2.0.1',
    'django-drf-filepond>=0.3.0',
    'sqlalchemy>=1.4.7',
    'gunicorn>=20.1.0',
]

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
            'doccano = backend.cli:main'
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
