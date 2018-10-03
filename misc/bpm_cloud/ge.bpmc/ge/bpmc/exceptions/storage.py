# -*- coding: utf-8 -*-

from .base import BPMFlaskException


class BPMNoAvailableStorage(BPMFlaskException):

    def __init__(self, target=None, details=[],
                 inner_error=None):
        super(BPMNoAvailableStorage, self).__init__(
            '', 503, target, details, inner_error)


class BPMMissingImage(BPMFlaskException):

    def __init__(self, message, target=None, details=[],
                 inner_error=None):
        super(BPMMissingImage, self).__init__(
            message, 404, target, details, inner_error)
