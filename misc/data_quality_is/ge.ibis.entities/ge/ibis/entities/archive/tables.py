# -*- coding: utf-8 -*-
"""
IBIS `ARchive` database ORM
The purpose of this schema is to be exposed to data consumers.
"""
from __future__ import absolute_import

import hashlib
import json

from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from sqlalchemy.orm import mapper, relationship

from .metadata import IBISArchive
