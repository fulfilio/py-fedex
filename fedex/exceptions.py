#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    fedex.exceptions

    Exceptions used in Fedex

    :copyright: (c) 2010 by Sharoon Thomas.
    :license: GPL3, see LICENSE for more details
'''


class FedexException(Exception):
    """
    Base class for all exceptions
    Integrating applications should catch this
    exception to display meaningful error messages
    """
    pass


class ElementNotFilled(FedexException):
    """
    Raised when a required element is not filled
    in the data
    """
    def __init__(self, element):
        message = "%s is not set yet"
        super(ElementNotFilled, self).__init__(message)


class RequestError(FedexException):
    """
    Raised when error occurs when the request is sent
    """
    pass


class NotImplementedYet(FedexException):
    """
    Raised when a method is not implemented
    """
    pass
