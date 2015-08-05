#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from setuptools import setup


setup(
    name='pyfedex',
    version='1.2',
    url='https://www.fulfil.io/',
    license='BSD',
    author='Fulfil.IO Inc.',
    author_email='support@fulfil.io',
    description='Fedex shipping integration',
    long_description=__doc__,
    package_data={'fedex': ['wsdl/*.wsdl']},
    packages=['fedex'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'suds',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests'
)
