#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'mechanize',
    'webhelpers',
    'bs4',
    'jinja2',
    'premailer',
    'cloudinary',
    'requests',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='norman',
    version='0.1.0',
    description="Quickly create html emails",
    long_description=readme + '\n\n' + history,
    author="Steven Brien",
    author_email='sbrien@hlkagency.com',
    url='https://github.com/spbrien/norman',
    packages=find_packages(),
    package_dir={'norman':
                 'norman'},
    entry_points={
        'console_scripts': [
            'norman=norman.cli:main'
        ]
    },
    include_package_data=True,
    package_data={
        '': ['*.*', '.*', '**/*.*', '**/.*'],
    },
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='norman',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
