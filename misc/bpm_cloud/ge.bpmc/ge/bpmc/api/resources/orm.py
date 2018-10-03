# -*- coding: utf-8 -*-

from flask import abort, jsonify, request
from flask_restful import Resource
from flask_restful_swagger_2 import Schema, swagger
from sqlalchemy import delete

from ge.bpmc.api.resources.base import BPMDBResource
from ge.bpmc.api.schemas.default import BigIntModel, StatusModel, StringModel
from ge.bpmc.api.schemas.orm import IssuerModel, IssuerModelWithoutPrimary
from ge.bpmc.utilities.flask import (bpm_flask_authentication_mixin,
                                     bpm_flask_mixin,
                                     bpm_flask_sqlalchemy_mixin,
                                     flask_validate_payload)
from ge.bpmc.utilities.swagger import get_validation_schema

# #######################
# Resources
# #######################

# ISSUER


class IssuersResource(BPMDBResource):

    @swagger.doc({
        'tags': ['issuer'],
        'description': 'Returns a list of issuers',
        'parameters': [],
        'responses': {
            '200': {
                'description': 'Issuers',
                'schema': {
                    'type': 'array',
                    'items': IssuerModel
                }
            }
        }
    })
    @bpm_flask_mixin()
    @bpm_flask_sqlalchemy_mixin
    def get(self):
        with self.em_context() as em:
            return em.all_issuer()

    @swagger.doc({
        'tags': ['issuer'],
        'description': 'Creates an issuer',
        'parameters': [
            {
                'name': 'body',
                'description': 'Issuer payload',
                'in': 'body',
                'type': 'object',
                'schema': IssuerModelWithoutPrimary,
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'Issuer',
                'schema': IssuerModel,
            },
            '400': {
                'description': 'Bad request, see details'
            },
            '409': {
                'description': 'Already exists'
            },
        }
    })
    @bpm_flask_mixin(get_validation_schema(IssuerModelWithoutPrimary))
    @bpm_flask_sqlalchemy_mixin
    def post(self):
        data = request.form
        with self.em_context() as em:
            return em.add_issuer(IssuerModelWithoutPrimary(**data))


class IssuerResource(BPMDBResource):

    @swagger.doc({
        'tags': ['issuer'],
        'description': 'Returns an issuer',
        'parameters': [
            {
                'name': 'uid',
                'description': 'Issuer uid',
                'in': 'path',
                'type': BigIntModel.get('type'),
                'format': BigIntModel.get('format'),
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'Requester',
                'schema': IssuerModel
            }
        }
    })
    @bpm_flask_mixin()
    @bpm_flask_sqlalchemy_mixin
    def get(self, uid):
        with self.em_context() as em:
            issuer = em.get_issuer('uid', uid)
            if issuer is None:
                abort(404)
            return issuer

    @swagger.doc({
        'tags': ['issuer'],
        'description': 'Returns an issuer',
        'parameters': [
            {
                'name': 'uid',
                'description': 'Issuer id',
                'in': 'path',
                'type': BigIntModel.get('type'),
                'format': BigIntModel.get('format'),
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'Issuer deleted'
            },
            '404': {
                'description': 'Item does not exist'
            }
        }
    })
    @bpm_flask_mixin()
    @bpm_flask_sqlalchemy_mixin
    def delete(self, uid):
        with self.em_context() as em:
            em.del_issuer('uid', uid)
            return StatusModel(message='success')

    @swagger.doc({
        'tags': ['issuer'],
        'description': 'Updates an issuer',
        'parameters': [
            {
                'name': 'uid',
                'description': 'Issuer uid',
                'in': 'path',
                'type': BigIntModel.get('type'),
                'format': BigIntModel.get('format'),
                'required': True
            },
            {
                'name': 'body',
                'description': 'Issuer payload',
                'in': 'body',
                'type': 'object',
                'schema': IssuerModelWithoutPrimary,
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'Updated issuer',
                'schema': IssuerModel
            },
            '400': {
                'description': 'Bad request, see details'
            },
            '404': {
                'description': 'Item does not exist'
            },
            '409': {
                'description': 'Already exists'
            },
        }
    })
    @bpm_flask_mixin(get_validation_schema(IssuerModelWithoutPrimary))
    @bpm_flask_sqlalchemy_mixin
    def patch(self, uid):
        with self.em_context() as em:
            data = IssuerModelWithoutPrimary(**request.form)
            return em.upd_issuer('uid', uid, data)


class IssuerByKeyResource(BPMDBResource):

    @swagger.doc({
        'tags': ['issuer'],
        'description': 'Returns an issuer by key',
        'parameters': [
            {
                'name': 'key',
                'description': 'Issuer key',
                'in': 'path',
                'type': StringModel.get('type'),
                'required': True,
            }
        ],
        'responses': {
            '200': {
                'description': 'Issuer',
                'schema': IssuerModel,
            },
            '404': {
                'description': 'Item does not exist'
            }
        }
    })
    @bpm_flask_mixin()
    @bpm_flask_sqlalchemy_mixin
    def get(self, key):
        with self.em_context() as em:
            issuer = em.get_issuer('key', key)
            if issuer is None:
                abort(404)
            return issuer
