#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

packages = ['robozilla',
            'robozilla.filters',
            'robozilla.providers',
            'robozilla.reporters'
            ]

with open('README.rst') as readme_file:
    readme = readme_file.read()

entry_points = {'console_scripts': ['robozilla=robozilla.scan:main']}

requirements = [
    'Click>=6.0',
    'python_bugzilla==1.2.2',
    'six'
]
test_requirements = []


setup(
    name='robozilla',
    version='0.1.3',
    packages=packages,
    url='https://github.com/ldjebran/robozilla',
    license='GNU General Public License v3 (GPLv3)',
    author='Djebran Lezzoum',
    author_email='ldjebran@gmail.com',
    description='Robottelo Bugzilla Parser',
    long_description=readme,
    include_package_data=True,
    install_requires=requirements,
    entry_points=entry_points,
    zip_safe=False,
    keywords='robozilla',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
