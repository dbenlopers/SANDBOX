# -*- coding: utf-8 -*-

from flask import request
from flask_restful_swagger_2 import swagger

from ge.bpmc import HEADER_ISSUER_KEY, SEC_ISSUER_KEY, SEC_ROLE_KEY
from ge.bpmc.api.resources.base import BPMDBResource
from ge.bpmc.api.schemas.default import AvailableItemsModel
from ge.bpmc.api.schemas.security import (CMPT_KEY_PARAM, ISSUER_KEY_PARAM,
                                          ROLE_KEY_PARAM)
from ge.bpmc.utilities.flask import (bpm_flask_authentication_mixin,
                                     bpm_flask_mixin,
                                     bpm_flask_public_access,
                                     bpm_flask_sqlalchemy_mixin)


class AvailableProceduresResource(BPMDBResource):

    @swagger.doc({
        'tags': ['available'],
        'description': 'Query available procedures',
        'security': {
            SEC_ISSUER_KEY: [],
            SEC_ROLE_KEY: [],
        },
        'parameters': [
            ISSUER_KEY_PARAM,
            ROLE_KEY_PARAM,
        ],
        'responses': {
            '200': {
                'description': 'Available procedures',
                'schema': AvailableItemsModel,
            },
            '401': {
                'description': 'Authentication failed'
            },
            '503': {
                'description': 'Service is busy'
            }
        }
    })
    @bpm_flask_mixin()
    @bpm_flask_sqlalchemy_mixin
    @bpm_flask_authentication_mixin
    @bpm_flask_public_access
    def get(self):
        issuer = request.headers.get(HEADER_ISSUER_KEY)
        with self.wf_context() as wf:
            procs = wf.consume_issuer_available_procedures(issuer)
            return AvailableItemsModel(items=[x.uid for x in procs])


class AvailableImagesResource(BPMDBResource):

    @swagger.doc({
        'tags': ['available'],
        'description': 'Query available images',
        'security': {
            SEC_ISSUER_KEY: [],
            SEC_ROLE_KEY: [],
        },
        'parameters': [
            ISSUER_KEY_PARAM,
            ROLE_KEY_PARAM,
        ],
        'responses': {
            '200': {
                'description': 'Available images',
                'schema': AvailableItemsModel,
            },
            '401': {
                'description': 'Authentication failed'
            },
            '503': {
                'description': 'Service is busy'
            }
        }
    })
    @bpm_flask_mixin()
    @bpm_flask_sqlalchemy_mixin
    @bpm_flask_authentication_mixin
    @bpm_flask_public_access
    def get(self):
        issuer = request.headers.get(HEADER_ISSUER_KEY)
        with self.wf_context() as wf:
            images = wf.consume_issuer_available_images(issuer)
            return AvailableItemsModel(items=[x.uid for x in images])
