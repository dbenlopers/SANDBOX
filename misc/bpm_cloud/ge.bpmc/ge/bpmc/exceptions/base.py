# -*- coding: utf-8 -*-


class BPMException(Exception):
    pass


class BPMFlaskException(BPMException):

    def __init__(self, message, code=400, target=None, details=[],
                 inner_error=None):
        self.message = message
        self.code = code
        self.target = target
        self.details = details
        self.inner_error = inner_error
