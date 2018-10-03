# -*- coding: utf-8 -*-

from enum import Enum


class ProcessingStatus(Enum):
    NEW = 'N'
    COMPUTED = 'C'
    FAIL = 'F'
    BEING_PROCESSED = 'U'
