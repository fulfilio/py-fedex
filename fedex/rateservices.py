#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    fedex.rateservices

    Rate Service APIs for Fedex

    :copyright: (c) 2010 by Sharoon Thomas.
    :copyright: (c) 2010-2013 by Openlabs Technologies & Consulting (P) Ltd.
    :license: GPLv3, see LICENSE for more details
'''

from api import APIBase


class RateServices(APIBase):
    __slots__ = (
        ReturnTransitAndCommit,
        CarrierCodes,
        VariableOptions,
        RequestedShipment
    )
