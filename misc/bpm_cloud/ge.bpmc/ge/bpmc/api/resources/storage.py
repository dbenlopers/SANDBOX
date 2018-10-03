# -*- coding: utf-8 -*-

import json
from contextlib import contextmanager

import requests
from flask import abort, request
from flask_restful_swagger_2 import swagger

from ge.bpmc import HEADER_ISSUER_KEY, SEC_CMPT_KEY, SEC_ISSUER_KEY
from ge.bpmc.api.resources.base import StorageBaseResource
from ge.bpmc.api.schemas.bpm import (ComputationModel, ModalityImageModel,
                                     ProcessingImageModel)
from ge.bpmc.api.schemas.default import SimpleImageModel, StatusModel
from ge.bpmc.api.schemas.orm import ImageMetricsModel, ImageModel
from ge.bpmc.api.schemas.security import (CMPT_KEY_PARAM, ISSUER_KEY_PARAM,
                                          ROLE_KEY_PARAM)
from ge.bpmc.utilities.flask import (bpm_flask_authentication_mixin,
                                     bpm_flask_component_access,
                                     bpm_flask_mixin,
                                     bpm_flask_sqlalchemy_mixin)
from ge.bpmc.utilities.network import check_broker_state
from ge.bpmc.utilities.swagger import get_validation_schema


def produce_processing_task(broker, image, metadata):
    check_broker_state(broker)
    task_fqdn = 'ge.bpmc.tasks.processing.process_image'
    broker.send_task(task_fqdn, (image, metadata))


class ImageQueryResource(StorageBaseResource):

    @swagger.doc({
        'tags': ['image'],
        'security': {
            SEC_CMPT_KEY: [],
        },
        'parameters': [
            CMPT_KEY_PARAM,
            {
                'name': 'uid',
                'description': 'Image id',
                'in': 'path',
                'type': ImageModel.properties.get('uid').get('type'),
                'format':
                    ImageModel.properties.get('uid').get('format'),
                'required': True,
            }
        ],
        'responses': {
            '200': {
                'description': 'Image storage request success',
                'schema': SimpleImageModel,
            },
            '400': {
                'description': 'Bad request, see details'
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
    @bpm_flask_component_access
    def get(self, uid):
        with self.storage_context() as storage_manager:
            image_bytes = storage_manager.query_image(uid)
            if not image_bytes:
                abort(404)
            return SimpleImageModel(bytes=image_bytes)


class MetricsImageQueryResource(StorageBaseResource):

    @swagger.doc({
        'tags': ['image'],
        'description': 'Gets a metrics image based on its UID',
        'security': {
            SEC_CMPT_KEY: [],
        },
        'parameters': [
            CMPT_KEY_PARAM,
            {
                'name': 'uid',
                'description': 'Image id',
                'in': 'path',
                'type': ImageMetricsModel.properties.get('uid').get('type'),
                'format':
                    ImageMetricsModel.properties.get('uid').get('format'),
                'required': True,
            }
        ],
        'responses': {
            '200': {
                'description': 'Image storage request success',
                'schema': SimpleImageModel,
            },
            '400': {
                'description': 'Bad request, see details'
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
    @bpm_flask_component_access
    def get(self, uid):
        with self.storage_context() as storage_manager:
            image_bytes = storage_manager.query_metrics_image(uid)
            if not image_bytes:
                abort(404)
            return SimpleImageModel(bytes=image_bytes)


class ImageStorageResource(StorageBaseResource):

    @swagger.doc({
        'tags': ['computation'],
        'description': 'Submit a image storage request',
        'security': {
            SEC_ISSUER_KEY: [],
            SEC_CMPT_KEY: [],
        },
        'parameters': [
            ISSUER_KEY_PARAM,
            CMPT_KEY_PARAM,
            {
                'name': 'body',
                'description': 'Expected payload',
                'in': 'body',
                'type': 'object',
                'schema': ModalityImageModel,
                'required': True,
            }
        ],
        'responses': {
            '200': {
                'description': 'Image storage request success',
                'schema': ComputationModel,
            },
            '400': {
                'description': 'Bad request, see details'
            },
            '401': {
                'description': 'Authentication failed'
            },
            '503': {
                'description': 'Service is busy'
            }
        }
    })
    @bpm_flask_mixin(get_validation_schema(ModalityImageModel))
    @bpm_flask_sqlalchemy_mixin
    @bpm_flask_component_access
    def post(self):
        with self.storage_context() as storage_manager:
            issuer = request.headers.get(HEADER_ISSUER_KEY)
            computation = storage_manager.store_image(issuer, request.form)
        with self.broker_context() as broker:
            image_metadata = request.form
            # Drop pixel data for broker
            del image_metadata['image']
            produce_processing_task(broker, computation.get('image'),
                                    image_metadata)
        return ComputationModel(exam_uid=computation.get('exam'),
                                procedure_uid=computation.get('procedure'),
                                image_uid=computation.get('image'))


class MetricsImageStorageResource(StorageBaseResource):

    @swagger.doc({
        'tags': ['computation'],
        'description': 'Submit a metrics image storage request',
        'security': {
            SEC_CMPT_KEY: [],
        },
        'parameters': [
            CMPT_KEY_PARAM,
            {
                'name': 'body',
                'description': 'Expected payload',
                'in': 'body',
                'type': 'object',
                'schema': ProcessingImageModel,
                'required': True,
            }
        ],
        'responses': {
            '200': {
                'description': 'Metrics image storage request success',
                'schema': StatusModel,
            },
            '400': {
                'description': 'Bad request, see details'
            },
            '401': {
                'description': 'Authentication failed'
            },
            '503': {
                'description': 'Service is busy'
            }
        }
    })
    @bpm_flask_mixin(get_validation_schema(ProcessingImageModel))
    @bpm_flask_sqlalchemy_mixin
    @bpm_flask_component_access
    def post(self):
        with self.storage_context() as storage_manager:
            computation = storage_manager.store_metrics_image(
                request.form.get('metrics_uid'),
                request.form.get('image'))
        return StatusModel(message='success')
