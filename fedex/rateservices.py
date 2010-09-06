#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    fedex.rateservices

    Rate Service APIs for Fedex

    :copyright: (c) 2010 by Sharoon Thomas.
    :license: GPL3, see LICENSE for more details
'''

from api import APIBase


class RateServices(APIBase):
    __slots__ = (
        ReturnTransitAndCommit,
        CarrierCodes,
        VariableOptions,
        RequestedShipment
    )
    

