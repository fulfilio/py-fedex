# -*- coding: UTF-8 -*-
'''
    fedex.address_validation_service

    Use the Address Validation Service to validate or
    complete recipient addresses.

    :copyright: (c) 2010 by Sharoon Thomas.
    :license: GPL, see LICENSE for more details
'''
import string

from .api import APIBase, BETA
from .structures import VersionInformation

class AddressValidationService(APIBase):
    """
    The `AddressValidationService` allows you to validate
    recipient address information before you ship a package.
    Correct addresses on the shipping label will eliminate delivery 
    delays and additional service fees.

    Use the Address Validation request to perform the following:
      * Confirm the validity and completeness of U.S.,
        Puerto Rico and Canadian addresses.
      * Complete incomplete recipient addresses.
      * Correct invalid recipient addresses.
      * Determine whether an address is business or residential 
        to increase the accuracy of courtesy rate quotes. 
        Applies to U.S. addresses only.
    """
    __slots__=(
        'AddressToValidate',
        'AddressValidationOptions'
    )

    version_info = VersionInformation('aval', 2, 0, 0)
    service_name = 'addressValidation'

    def __init__(self, account_info):
        """
        :param account_info: Instance of `structures.AccountInformation`
                             with all the details of accounts
        """
        self.account_info = account_info
        self.AddressToValidate = []
        self.set_wsdl_client('AddressValidationService_v2.wsdl')
        self.AddressValidationOptions = self.get_element_from_type(
                                            'AddressValidationOptions'
                                            )
        super(AddressValidationService, self).__init__()

    def send_request(self, transaction_id=None):
        """
        Inherit and implement send_request

        :param transaction_id: ID of the transaction
        """
        if transaction_id is not None:
            self.set_transaction_details(transaction_id)
        fields = self.__slots__ + super(
                                    AddressValidationService,
                                    self).__slots__
        fields = [x for x in fields if x[0] in string.uppercase]
        return self._send_request(fields)


