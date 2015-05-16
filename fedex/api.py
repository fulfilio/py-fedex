#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    fedex.api

    Different APIs for Fedex

    :copyright: (c) 2010 by Sharoon Thomas.
    :copyright: (c) 2010-2013 by Openlabs Technologies & Consulting (P) Ltd.
    :license: GPLv3, see LICENSE for more details
'''
import os
from datetime import datetime
import logging

from suds import WebFault
from suds.client import Client
from .exceptions import RequestError, NotImplementedYet

VERSION = '0.2dev'
BETA = int(VERSION[0]) < 1


logging.basicConfig(level=logging.INFO)


class APIBase(object):
    """Base API
    All FedEx services will inherit this and implement features
    """
    __slots__ = (
        'WebAuthenticationDetail',
        'ClientDetail',
        'TransactionDetail',
        'Version',
        'RequestTimestamp',

        'account_info',
        'version_info',
        'service_name',
        'wsdl_client',
        'response',
    )

    def __init__(self, transaction_id=None):
        """
        Initialises the API service base class

        :param account_info: Instance of `fedex.structures.AccountInformation`
                             with all required auth info
        :param transaction_id: Transaction ID could be set in initialisation
                        or later using the `set_transaction_details` method
        """
        self._set_account_elements()
        self._set_version()
        if transaction_id is not None:
            self.set_transaction_details(transaction_id)

    def get(self, attribute):
        """
        Gets the specified attribute from this class
        """
        return getattr(self, attribute)

    def _set_account_elements(self):
        """
        Initialises
            WebAuthenticationDetail
                |- WebAuthenticationCredential
                    |-Key
                    |-Password
            ClientDetail
        """
        assert self.account_info is not None
        # WebAuthenticationDetail
        self.WebAuthenticationDetail = self.get_element_from_type(
            "WebAuthenticationDetail"
        )
        temp_credential = self.get_element_from_type(
            "WebAuthenticationCredential"
        )
        temp_credential.Key = self.account_info.Key
        temp_credential.Password = self.account_info.Password
        self.WebAuthenticationDetail.UserCredential = temp_credential
        # ClientDetail
        self.ClientDetail = self.get_element_from_type('ClientDetail')
        self.ClientDetail.AccountNumber = self.account_info.AccountNumber
        self.ClientDetail.MeterNumber = self.account_info.MeterNumber
        if hasattr(self.ClientDetail, 'IntegratorId'):
            self.ClientDetail.IntegratorId = self.account_info.IntegratorId

    def _set_version(self):
        """
        Sets the version element
        """
        assert self.version_info is not None
        self.Version = self.get_element_from_type('VersionId')
        self.Version.ServiceId = self.version_info.ServiceId
        self.Version.Major = self.version_info.Major
        self.Version.Intermediate = self.version_info.Intermediate
        self.Version.Minor = self.version_info.Minor

    def get_element_from_type(self, type_name):
        """
        Generates the object if it exists and returns from
        factory.
        """
        assert self.wsdl_client is not None
        return self.wsdl_client.factory.create(type_name)

    def set_wsdl_client(self, uri):
        """
        Sets wsdl_client with the wsdl in `uri`
        """
        wsdl_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'wsdl'
        )
        if '://' not in uri:
            uri = 'file://%s' % os.path.join(wsdl_folder, uri)
        self.wsdl_client = Client(uri)

    def _set_timestamp(self):
        """
        Adds the request timestamp
        """
        # The date format must be YYYY-MM-DDTHH:MM:SS- xx:xx.
        # The time must be in the format: HH:MM:SS using a 24-hour clock.
        # The date and time are separated by the letter T
        # (e.g., 2009-06-26T17:00:00).
        # The UTC offset indicates the number of hours/minutes
        # (e.g. xx:xx) from UTC (e.g. 2009-06-26T17:00:00-04:00
        # is defined as June 26, 2009 5:00 p.m. Eastern Time).
        self.RequestTimestamp = datetime.utcnow().replace(
            microsecond=0).isoformat()

    def set_transaction_details(self, transaction_id):
        """
        Sets the transaction details with given data
        """
        self.TransactionDetail = self.get_element_from_type(
            "TransactionDetail"
        )
        self.TransactionDetail.CustomerTransactionId = transaction_id

    def _send_request(self, elements):
        """
        Sends the Request using suds.
        This function should be called by the inherited send_request
        functions

        :param service_name: Name of the service to use
        :param elements: Dictionary of the elements to send
        """
        assert self.service_name is not None
        self._set_timestamp()
        data = dict(zip(elements, map(self.get, elements)))
        try:
            service = getattr(self.wsdl_client.service, self.service_name)
            self.response = service(**data)
        except WebFault, fault:
            raise RequestError(fault)
        try:
            self.test_response_for_errors()
        except Warning, warning:
            logging.warning(warning)
        return self.response

    def test_response_for_errors(self):
        """
        Tests the response for errors
        """
        if self.response.HighestSeverity == 'SUCCESS':
            return True
        message = ''
        for notification in self.response.Notifications:
            notification_message = '[%s] %s (Source:%s)' % (
                notification.Code,
                notification.Message,
                notification.Source,
            )
            if notification.Severity == 'ERROR':
                message += '\n' + notification_message
        if self.response.HighestSeverity == 'WARNING':
            raise Warning(notification_message)
        if self.response.HighestSeverity == 'ERROR':
            raise RequestError(message)

    def send_request(self):
        """
        Method the subclasses should inherit to send the request
        """
        raise NotImplementedYet("Send Request")


class PackageMovementInformationService(APIBase):
    pass


class TrackingandVisibilityServices(APIBase):
    pass


class CourierDispatchServices(APIBase):
    pass


class LocatorService(APIBase):
    pass


class ShipService(APIBase):
    pass
