# -*- coding: utf-8 -*-

BPM_ACCEPTED_MIMETYPES = [
    'application/json',
    'application/xml'
]

#   Utilities class


class InnerError(object):

    def __init__(self, code, inner_error=None):
        self.code = code
        self.inner_error = inner_error


class ResponseData(object):

    def __init__(self, message, code):
        self.message = message
        self.code = code
