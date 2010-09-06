#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    fedex.structures

    Data Structures for common purposes

    :copyright: (c) 2010 by Sharoon Thomas.
    :license: GPL3, see LICENSE for more details
'''
__all__ = (
            'AccountInformation',
            'VersionInformation',
            'load_accountinfo_from_file',
            )

import ConfigParser
from collections import namedtuple

AccountInformation = namedtuple(
    'AccountInformation',
    (
        'Key',
        'Password',
        'AccountNumber',
        'MeterNumber',
        'IntegratorId',
        'ProductId',
        'ProductVersion'
        )
    )

VersionInformation = namedtuple(
    'VersionInformation',
    (
        'ServiceId',
        'Major',
        'Intermediate',
        'Minor',
        )
    )

def load_accountinfo_from_file(file):
    """
    Loads the config using config parser from file
    :param file: Absolute path of file
    """
    config = ConfigParser.RawConfigParser()
    config.readfp(open(file))
    data = dict(zip(AccountInformation._fields,
                    [config.get('fedex', field.lower()) \
                        for field in AccountInformation._fields]))
    return AccountInformation(**data)

