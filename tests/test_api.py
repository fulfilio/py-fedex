#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    Fedex API Testing

    Tests the API

    :copyright: (c) 2010 by Sharoon Thomas.
    :copyright: (c) 2010-2015 by Openlabs Technologies & Consulting (P) Ltd.
    :license: GPLv3, see LICENSE for more details
'''
import unittest
import os
import logging

from fedex import AddressValidationService, ProcessShipmentRequest, \
    RateService, load_accountinfo_from_file
from fedex.exceptions import RequestError

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)


class APITestCase(unittest.TestCase):

    def setUp(self):
        """
        Load the account information from configuration file
        """
        directory = os.path.dirname(os.path.abspath(__file__))
        self.accountinfo = load_accountinfo_from_file(
            os.path.join(directory, 'accountinfo.cfg')
        )

    def test_0010_address_validation(self):
        """
        Validate the address
        """
        avs = AddressValidationService(self.accountinfo)
        address_1 = avs.get_element_from_type('AddressToValidate')
        address_1.CompanyName = 'Free Software Foundation'
        address_1.Address.StreetLines = [
            '51 Franklin Street',
            'Suite 500',
        ]
        address_1.Address.City = 'Boston'
        address_1.Address.StateOrProvinceCode = 'MA'
        address_1.Address.PostalCode = 02110
        address_1.Address.CountryCode = 'US'
        address_1.Address.Residential = False
        avs.AddressToValidate.append(address_1)
        if self.accountinfo.ProductId == 'TEST':
            # Fedex does not allow validation of addresses in test mode
            self.assertRaises(RequestError, avs.send_request, '123')
        else:
            print avs.send_request('123')

    def test_0020_process_shipment(self):
        """
        Try sending a shipment
        """
        psr = ProcessShipmentRequest(self.accountinfo)
        psr.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
        psr.RequestedShipment.ServiceType = 'INTERNATIONAL_PRIORITY_FREIGHT'
        psr.RequestedShipment.PackagingType = 'YOUR_PACKAGING'
        # psr.RequestedShipment.PreferredCurrency = 'USD'
        # Shipper
        psr.RequestedShipment.Shipper.AccountNumber = \
            self.accountinfo.AccountNumber
        psr.RequestedShipment.Shipper.Contact.CompanyName = \
            'WAPISENDER-WBUS1100'
        psr.RequestedShipment.Shipper.Contact.PersonName = 'Sender Name'
        psr.RequestedShipment.Shipper.Contact.PhoneNumber = '1234567890'
        psr.RequestedShipment.Shipper.Contact.EMailAddress = \
            'info@openlabs.co.in'
        psr.RequestedShipment.Shipper.Address.StreetLines = [
            'SN2000 Test Meter 8',
            '10 Fedex Parkway'
        ]
        psr.RequestedShipment.Shipper.Address.City = 'Detroit'
        psr.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'MI'
        psr.RequestedShipment.Shipper.Address.PostalCode = '48208'
        psr.RequestedShipment.Shipper.Address.CountryCode = 'US'
        # Recipient
        psr.RequestedShipment.Recipient.Contact.PersonName = 'Recipient_Name'
        psr.RequestedShipment.Recipient.Contact.PhoneNumber = '9018549236'
        psr.RequestedShipment.Recipient.Address.StreetLines = [
            'Recipient Address Line 1',
            'Address line 2'
        ]
        psr.RequestedShipment.Recipient.Address.City = 'Edmonton'
        psr.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'AB'
        psr.RequestedShipment.Recipient.Address.PostalCode = 'T5A1'
        psr.RequestedShipment.Recipient.Address.CountryCode = 'CA'
        # Shipping Charges Payment
        psr.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'
        psr.RequestedShipment.ShippingChargesPayment.Payor.ResponsibleParty = \
            psr.RequestedShipment.Shipper
        # Express Freight Detail
        psr.RequestedShipment.ExpressFreightDetail.PackingListEnclosed = 1
        psr.RequestedShipment.ExpressFreightDetail.ShippersLoadAndCount = 2
        psr.RequestedShipment.ExpressFreightDetail.BookingConfirmationNumber =\
            '123asd789'

        # Customs Clearance Detail
        customs_detail = psr.get_element_from_type('CustomsClearanceDetail')
        customs_detail.DocumentContent = 'DOCUMENTS_ONLY'
        # Customs Value
        customs_detail.CustomsValue.Currency = 'USD'
        customs_detail.CustomsValue.Amount = '5000'
        # Commercial Invoice
        customs_detail.CommercialInvoice.TermsOfSale = 'FOB'

        customs_detail.DutiesPayment.PaymentType = 'SENDER'
        customs_detail.DutiesPayment.Payor.ResponsibleParty = \
            psr.RequestedShipment.Shipper
        psr.RequestedShipment.CustomsClearanceDetail = customs_detail
        # Encoding Items for customs
        commodities = []
        commodity_1 = psr.get_element_from_type('Commodity')
        commodity_1.NumberOfPieces = 1
        commodity_1.Name = 'Shoes'
        commodity_1.Description = 'My Beautiful Adidas Shoes'
        commodity_1.CountryOfManufacture = 'US'
        commodity_1.Weight.Units = 'LB'
        commodity_1.Weight.Value = 10
        commodity_1.Quantity = 1
        commodity_1.QuantityUnits = "pairs"
        commodity_1.UnitPrice.Amount = 100
        commodity_1.UnitPrice.Currency = 'USD'
        commodity_1.CustomsValue.Currency = 'USD'
        commodity_1.CustomsValue.Amount = 100
        commodities.append(commodity_1)
        psr.RequestedShipment.CustomsClearanceDetail.Commodities = commodities
        # Label Specification
        psr.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'
        psr.RequestedShipment.LabelSpecification.ImageType = 'PNG'
        psr.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_4X6'
        # Charges and Payments
        psr.RequestedShipment.RateRequestTypes = ['ACCOUNT']
        # Encoding for items
        items = []
        item_1 = psr.get_element_from_type('RequestedPackageLineItem')
        item_1.SequenceNumber = 1
        item_1.ItemDescription = "My Beautiful Shoes"
        item_1.Weight.Units = 'LB'
        item_1.Weight.Value = 180
        item_1.Dimensions.Length = 12
        item_1.Dimensions.Width = 12
        item_1.Dimensions.Height = 12
        item_1.Dimensions.Units = 'IN'
        items.append(item_1)
        psr.RequestedShipment.RequestedPackageLineItems = items
        psr.RequestedShipment.PackageCount = len(items)

        print psr.send_request('0020')

    def test_0030_rate_service(self):
        """
        Test rate service API
        """
        psr = RateService(self.accountinfo)

        requested_shipment = psr.RequestedShipment
        requested_shipment.DropoffType = 'REGULAR_PICKUP'
        requested_shipment.ServiceType = 'INTERNATIONAL_PRIORITY_FREIGHT'
        requested_shipment.PackagingType = 'YOUR_PACKAGING'
        # Shipper
        shipper = requested_shipment.Shipper
        shipper.AccountNumber = \
            self.accountinfo.AccountNumber
        shipper.Contact.CompanyName = \
            'WAPISENDER-WBUS1100'
        shipper.Contact.PersonName = 'Sender Name'
        shipper.Contact.PhoneNumber = '1234567890'
        shipper.Contact.EMailAddress = \
            'info@openlabs.co.in'
        shipper.Address.StreetLines = [
            'SN2000 Test Meter 8',
            '10 Fedex Parkway'
        ]
        shipper.Address.City = 'Detroit'
        shipper.Address.StateOrProvinceCode = 'MI'
        shipper.Address.PostalCode = '48208'
        shipper.Address.CountryCode = 'US'
        # Recipient
        recipient = requested_shipment.Recipient
        recipient.Contact.PersonName = 'Recipient_Name'
        recipient.Contact.PhoneNumber = '9018549236'
        recipient.Address.StreetLines = [
            'Recipient Address Line 1',
            'Address line 2'
        ]
        recipient.Address.City = 'Edmonton'
        recipient.Address.StateOrProvinceCode = 'AB'
        recipient.Address.PostalCode = 'T5A1'
        recipient.Address.CountryCode = 'CA'
        # Shipping Charges Payment
        shipping_charges = requested_shipment.ShippingChargesPayment
        shipping_charges.PaymentType = 'SENDER'
        shipping_charges.Payor.ResponsibleParty = \
            shipper
        # Express Freight Detail
        fright_detail = requested_shipment.ExpressFreightDetail
        fright_detail.PackingListEnclosed = 1
        fright_detail.ShippersLoadAndCount = 2
        fright_detail.BookingConfirmationNumber =\
            '123asd789'

        # Customs Clearance Detail
        customs_detail = psr.get_element_from_type('CustomsClearanceDetail')
        customs_detail.DocumentContent = 'DOCUMENTS_ONLY'
        # Customs Value
        customs_detail.CustomsValue.Currency = 'USD'
        customs_detail.CustomsValue.Amount = '5000'
        # Commercial Invoice
        customs_detail.CommercialInvoice.TermsOfSale = 'FOB_OR_FCA'

        customs_detail.DutiesPayment.PaymentType = 'SENDER'
        customs_detail.DutiesPayment.Payor.ResponsibleParty = \
            shipper
        requested_shipment.CustomsClearanceDetail = customs_detail
        # Encoding Items for customs
        commodities = []
        commodity_1 = psr.get_element_from_type('Commodity')
        commodity_1.NumberOfPieces = 1
        commodity_1.Name = 'Shoes'
        commodity_1.Description = 'My Beautiful Adidas Shoes'
        commodity_1.CountryOfManufacture = 'US'
        commodity_1.Weight.Units = 'LB'
        commodity_1.Weight.Value = 10
        commodity_1.Quantity = 1
        commodity_1.QuantityUnits = "pairs"
        commodity_1.UnitPrice.Amount = 100
        commodity_1.UnitPrice.Currency = 'USD'
        commodity_1.CustomsValue.Currency = 'USD'
        commodity_1.CustomsValue.Amount = 100
        commodities.append(commodity_1)
        requested_shipment.CustomsClearanceDetail.Commodities = commodities
        # Label Specification
        requested_shipment.LabelSpecification.LabelFormatType = 'COMMON2D'
        requested_shipment.LabelSpecification.ImageType = 'PNG'
        requested_shipment.LabelSpecification.LabelStockType = 'PAPER_4X6'
        # Charges and Payments
        requested_shipment.RateRequestTypes = ['ACCOUNT']
        # Encoding for items
        items = []
        item_1 = psr.get_element_from_type('RequestedPackageLineItem')
        item_1.SequenceNumber = 1
        item_1.GroupPackageCount = 1
        item_1.ItemDescription = "My Beautiful Shoes"
        item_1.Weight.Units = 'LB'
        item_1.Weight.Value = 180
        item_1.Dimensions.Length = 12
        item_1.Dimensions.Width = 12
        item_1.Dimensions.Height = 12
        item_1.Dimensions.Units = 'IN'
        items.append(item_1)
        requested_shipment.RequestedPackageLineItems = items
        requested_shipment.PackageCount = len(items)

        print psr.send_request('0020')


def suite():
    "Fedex API test suite"
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(APITestCase)
    )
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
