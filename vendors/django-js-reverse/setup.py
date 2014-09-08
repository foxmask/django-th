#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import find_packages
from distutils.core import setup


try:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
except IOError:
    README = ''


version_tuple = __import__('django_js_reverse').VERSION
version = '.'.join([str(v) for v in version_tuple])
setup(
    name='django-js-reverse',
    version=version,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    license='MIT',
    description='Javascript url handling for Django that doesn\'t hurt.',
    long_description=README,
    author='Bernhard Janetzki',
    author_email='boerni@gmail.com',
    url='https://github.com/version2/django-js-reverse',
    download_url='http://pypi.python.org/pypi/django-js-reverse/',
    packages=find_packages(),
    package_data={
        'django_js_reverse': [
            'templates/django_js_reverse/*',
        ]
    },
    install_requires=[
        'Django >= 1.4',
    ]
)