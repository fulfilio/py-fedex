#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    fedex.ship_services

    Process and submit various shipping requests to FedEx,
    such as express and ground U.S. and international shipments
    as well as Return shipments.

    :copyright: (c) 2010 by Sharoon Thomas.
    :copyright: (c) 2010-2015 by Openlabs Technologies & Consulting (P) Ltd.
    :license: GPLv3, see LICENSE for more details
'''
import string
from datetime import datetime

from .api import APIBase
from .structures import VersionInformation


class ProcessShipmentRequest(APIBase):
    """
    Process a shipment
    """
    __slots__ = (
        'RequestedShipment',
        )

    version_info = VersionInformation('ship', 15, 0, 0)
    service_name = 'processShipment'

    def __init__(self, account_info):
        """
        :param account_info: Instance of `structures.AccountInformation`
                             with all the details of accounts
        """
        self.account_info = account_info
        self.set_wsdl_client('ShipService_v15.wsdl')
        self.RequestedShipment = self.get_element_from_type(
            'RequestedShipment'
        )
        super(ProcessShipmentRequest, self).__init__()

    def send_request(self, transaction_id=None):
        """
        Inherit and implement send_request
        :param transaction_id: ID of the transaction
        """
        if transaction_id is not None:
            self.set_transaction_details(transaction_id)

        # The date format must be YYYY-MM-DDTHH:MM:SS- xx:xx.
        # The time must be in the format: HH:MM:SS using a 24-hour clock.
        # The date and time are separated by the letter T
        # (e.g., 2009-06-26T17:00:00).
        # The UTC offset indicates the number of hours/minutes
        # (e.g. xx:xx) from UTC (e.g. 2009-06-26T17:00:00-04:00
        # is defined as June 26, 2009 5:00 p.m. Eastern Time).
        self.RequestedShipment.ShipTimestamp = datetime.utcnow().replace(
            microsecond=0).isoformat()

        fields = self.__slots__ + super(
            ProcessShipmentRequest,
            self).__slots__
        fields = [x for x in fields if x[0] in string.uppercase]
        return self._send_request(fields)
