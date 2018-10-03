# -*- coding: utf-8 -*-

import re

BPM_NAME = 'BPMCloud'
BPM_VERSION = '1.0.0'

# API

HEADER_ISSUER_KEY = 'X-Issuer-Key'
HEADER_ROLE_KEY = 'X-BPM-Role-Key'
HEADER_CMPT_KEY = 'X-BPM-Component-Key'

SEC_ISSUER_KEY = 'issuer_key'
SEC_ROLE_KEY = 'role_key'
SEC_CMPT_KEY = 'cmpt_key'

API_ENTRYPOINT = '/api'
# API_JSON_ENTRYPOINT: add .json or .html to get the actual content
API_JSON_ENTRYPOINT = API_ENTRYPOINT + '/swagger'
API_UI = API_ENTRYPOINT + '/ui'

STORE_ENTRYPOINT = '/store'
STORE_IMAGE_ENTRYPOINT = STORE_ENTRYPOINT + '/image'
STORE_METRICS_IMAGE_ENTRYPOINT = STORE_ENTRYPOINT + '/metrics_image'

# STORAGE

STORAGE_DEFAULT_FORMAT = 'pickle'
STORAGE_METRICS_SUFFIX = '_metrics'

# APPLICATION LOGIC

SOP_CLASS_FORMAT = re.compile(r'^[\d\.]*$')

# RETRY POLICY

MAX_BUSINESS_TASK_RETRIES = 3
