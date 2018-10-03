# -*- coding:utf-8 -*-

import binascii
import os

token = binascii.hexlify(os.urandom(50)).decode('utf-8')
