# -*- coding: utf-8 -*-

from ge.bpmc import (HEADER_CMPT_KEY, HEADER_ISSUER_KEY, HEADER_ROLE_KEY,
                     SEC_CMPT_KEY, SEC_ISSUER_KEY, SEC_ROLE_KEY)

IssuerAuthModel = {
    'type': 'apiKey',
    'in': 'header',
    'name': HEADER_ISSUER_KEY
}

RoleAuthModel = {
    'type': 'apiKey',
    'in': 'header',
    'name': HEADER_ROLE_KEY
}

ComponentAuthModel = {
    'type': 'apiKey',
    'in': 'header',
    'name': HEADER_CMPT_KEY
}

ISSUER_KEY_PARAM = {
    'name': SEC_ISSUER_KEY,  # Refers to a security definition key in the API
    'in': 'header',
    'required': True,
    'type': 'string'
}

ROLE_KEY_PARAM = {
    'name': SEC_ROLE_KEY,  # Refers to a security definition key in the API
    'in': 'header',
    'required': True,
    'type': 'string'
}

CMPT_KEY_PARAM = {
    'name': SEC_CMPT_KEY,  # Refers to a security definition key in the API
    'in': 'header',
    'required': True,
    'type': 'string'
}
