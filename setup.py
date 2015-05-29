#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

    :copyright: (c) 2010 by Sharoon Thomas.
    :copyright: (c) 2010-2013 by Openlabs Technologies & Consulting (P) Ltd.
    :license: GPLv3, see LICENSE for more details
'''
from setuptools import setup


setup(
    name='pyfedex',
    version='1.2',
    url='http://openlabs.co.in/projects/python/fedex',
    license='GPL',
    author='Sharoon Thomas, Openlabs Technologies',
    author_email='info@openlabs.co.in',
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
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests'
)
