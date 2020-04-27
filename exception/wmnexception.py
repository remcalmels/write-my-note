#!/usr/bin/env python
# -*- coding: utf-8 -*-

class WmnException(Exception):
    """ Error thrown by app """

    def __init__(self, message, http_code=None):
        self.message = message
        self.http_code = http_code
        super(WmnException, self).__init__(self.__str__())

    def __repr__(self):
        return "WmnException(error={error})".format(error=self.message)

    def __str__(self):
        return self.message