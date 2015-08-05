# -*- coding: UTF-8 -*-
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
    data = dict(
        zip(
            AccountInformation._fields,
            [config.get('fedex', field.lower())
                for field in AccountInformation._fields]
        )
    )
    return AccountInformation(**data)
