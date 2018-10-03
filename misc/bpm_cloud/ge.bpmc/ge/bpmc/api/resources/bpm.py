# -*- coding: utf-8 -*-

import json
import uuid

import requests
from flask import abort, current_app, request, url_for
from flask_restful_swagger_2 import swagger

from ge.bpmc import (HEADER_ISSUER_KEY, SEC_CMPT_KEY, SEC_ISSUER_KEY,
                     SEC_ROLE_KEY)
from ge.bpmc.api.resources.base import BPMDBResource
from ge.bpmc.api.schemas.bpm import (ComputationModel, CriteriaModel,
                                     ExamResultModel, ImageResultModel,
                                     ModalityImageModel, OverlayModel,
                                     ProcedureResultModel, SystemIDModel)
from ge.bpmc.api.schemas.default import BigIntModel, StringModel
from ge.bpmc.api.schemas.orm import (IssuerModel, RepositoryModel,
                                     RepositoryModelWithoutPrimary)
from ge.bpmc.api.schemas.security import (CMPT_KEY_PARAM, ISSUER_KEY_PARAM,
                                          ROLE_KEY_PARAM)
from ge.bpmc.services.storageclient import StorageClient
from ge.bpmc.utilities.base import ResponseData
from ge.bpmc.utilities.flask import (bpm_flask_authentication_mixin,
                                     bpm_flask_component_access,
                                     bpm_flask_mixin, bpm_flask_public_access,
                                     bpm_flask_sqlalchemy_mixin)
from ge.bpmc.utilities.requests import bpm_flask_connectivity_mixin
from ge.bpmc.utilities.swagger import get_validation_schema


class RepositoryRegistrationResource(BPMDBResource):

    @swagger.doc({
        'tags': ['repository'],
        'description': 'Register a repository',
        'security': {
            SEC_CMPT_KEY: []
        },
        'parameters': [
            CMPT_KEY_PARAM,
            {
                'name': 'body',
                'description': 'Expected payload',
                'in': 'body',
                'type': 'object',
                'schema': RepositoryModelWithoutPrimary,
                'required': True,
            }
        ],
        'responses': {
            '200': {
                'description': 'Repository registered',
                'schema': RepositoryModel,
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
    @bpm_flask_mixin(get_validation_schema(RepositoryModelWithoutPrimary))
    @bpm_flask_sqlalchemy_mixin
    @bpm_flask_component_access
    def post(self):
        with self.em_context() as em:
            name = request.form.get('name')
            host = request.form.get('host')
            use_ssl = request.form.get('use_ssl')
            repo = em.get_repository('name', name)
            if repo:
                updater = RepositoryUpdateResource()
                data = json.loads(updater.patch(repo.uid).data.decode('utf-8'))
                return RepositoryModel(**data)
            return em.add_repository({
                'name': name, 'host': host, 'use_ssl': use_ssl})


class RepositoryUpdateResource(BPMDBResource):

    @swagger.doc({
        'tags': ['repository'],
        'description': 'Register a repository',
        'security': {
            SEC_CMPT_KEY: []
        },
        'parameters': [
            CMPT_KEY_PARAM,
            {
                'name': 'body',
                'description': 'Expected payload',
                'in': 'body',
                'type': 'object',
                'schema': RepositoryModelWithoutPrimary,
                'required': True,
            }
        ],
        'responses': {
            '200': {
                'description': 'Repository registered',
                'schema': RepositoryModel,
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
    @bpm_flask_mixin(get_validation_schema(RepositoryModelWithoutPrimary))
    @bpm_flask_sqlalchemy_mixin
    @bpm_flask_component_access
    def patch(self, uid):
        with self.em_context() as em:
            name = request.form.get('name')
            host = request.form.get('host')
            use_ssl = request.form.get('use_ssl')
            return em.upd_repository('uid', uid, {
                'name': name, 'host': host, 'use_ssl': use_ssl})


class SystemResource(BPMDBResource):

    @swagger.doc({
        'tags': ['system'],
        'description': 'Register a system',
        'security': {
            SEC_ROLE_KEY: []
        },
        'parameters': [
            ROLE_KEY_PARAM,
            {
                'name': 'body',
                'description': 'Expected payload',
                'in': 'body',
                'type': 'object',
                'schema': SystemIDModel,
                'required': True,
            }
        ],
        'responses': {
            '200': {
                'description': 'System registered',
                'schema': IssuerModel,
            },
            '400': {
                'description': 'Bad request, see details'
            },
            '401': {
                'description': 'Authentication failed'
            },
            '409': {
                'description': 'Already exists'
            },
            '503': {
                'description': 'Service is busy'
            }
        }
    })
    @bpm_flask_mixin(get_validation_schema(SystemIDModel))
    @bpm_flask_sqlalchemy_mixin
    @bpm_flask_public_access
    def post(self):
        with self.em_context() as em:
            key = uuid.uuid4()
            while em.get_issuer('key', str(key)) is not None:
                key = uuid.uuid4()
            data = {
                'identifier': request.form.get('identifier'),
                'key': str(key)
            }
            return em.add_issuer(data)


class ComputationResource(BPMDBResource):

    @swagger.doc({
        'tags': ['computation'],
        'description': 'Submit a computation request',
        'security': {
            SEC_ISSUER_KEY: [],
            SEC_ROLE_KEY: [],
        },
        'parameters': [
            ISSUER_KEY_PARAM,
            ROLE_KEY_PARAM,
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
                'description': 'Computation request success',
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
    @bpm_flask_connectivity_mixin
    @bpm_flask_sqlalchemy_mixin
    @bpm_flask_authentication_mixin
    @bpm_flask_public_access
    def post(self):
        expected_ct = request.headers.get(
            'Content-Type', 'application/json').lower()
        headers = {
            'Content-Type': expected_ct,
            HEADER_ISSUER_KEY: request.headers.get(HEADER_ISSUER_KEY),
        }
        req = StorageClient.post_computation_request(
            headers, request.data.decode('utf-8'))
        return ResponseData(req.json(), req.status_code)


class ExamResultResource(BPMDBResource):

    @swagger.doc({
        'tags': ['result'],
        'description': 'Query exam result',
        'security': {
            SEC_ISSUER_KEY: [],
            SEC_ROLE_KEY: [],
        },
        'parameters': [
            ISSUER_KEY_PARAM,
            ROLE_KEY_PARAM,
            {
                'name': 'uid',
                'description': 'Exam uid',
                'in': 'path',
                'type': BigIntModel.get('type'),
                'format': BigIntModel.get('format'),
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'Exam result',
                'schema': ExamResultModel,
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
    @bpm_flask_authentication_mixin
    @bpm_flask_public_access
    def get(self, uid):
        issuer_key = request.headers.get(HEADER_ISSUER_KEY)
        with self.wf_context() as wf:
            item = wf.get_exam_result(issuer_key, uid)
            if not item:
                abort(404)
        expected_ct = request.headers.get(
            'Content-Type', 'application/json').lower()
        headers = {
            'Content-Type': expected_ct,
            HEADER_ISSUER_KEY: issuer_key,
        }
        procedures = []
        for proc in item.procedures:
            image_results = []
            for img in proc.images:
                req = StorageClient.get_metrics_image(
                    headers, img.tmp_image_metrics_display_uid)
                bytes_ = req.json().get('bytes') if req.status_code == 200 \
                    else []
                overlay = {k: v for k, v in img.overlay.items()
                           if v is not None} if img.overlay else {}
                criteria = {k: v for k, v in img.criteria.items()
                            if v is not None} if img.criteria else {}
                image_results.append(ImageResultModel(
                    image_uid=img.uid, status=img.status,
                    image=bytes_, overlay=OverlayModel(**overlay),
                    criteria=CriteriaModel(**criteria),
                    extra=img.extra))
            procedures.append(
                ProcedureResultModel(
                    procedure_uid=proc.uid, status=proc.status,
                    matched=proc.matching_data,
                    images=image_results))
        return ExamResultModel(exam_uid=uid, procedures=procedures)


class ProcedureResultResource(BPMDBResource):

    @swagger.doc({
        'tags': ['result'],
        'description': 'Query procedure result',
        'security': {
            SEC_ISSUER_KEY: [],
            SEC_ROLE_KEY: [],
        },
        'parameters': [
            ISSUER_KEY_PARAM,
            ROLE_KEY_PARAM,
            {
                'name': 'uid',
                'description': 'Procedure uid',
                'in': 'path',
                'type': BigIntModel.get('type'),
                'format': BigIntModel.get('format'),
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'Computation result',
                'schema': ProcedureResultModel,
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
    @bpm_flask_authentication_mixin
    @bpm_flask_public_access
    def get(self, uid):
        issuer_key = request.headers.get(HEADER_ISSUER_KEY)
        with self.wf_context() as wf:
            item = wf.get_procedure_result(issuer_key, uid)
            if not item:
                abort(404)

        image_results = []
        expected_ct = request.headers.get(
            'Content-Type', 'application/json').lower()
        headers = {
            'Content-Type': expected_ct,
            HEADER_ISSUER_KEY: issuer_key,
        }

        for img_result in item.images:
            req = StorageClient.get_metrics_image(
                headers, img_result.tmp_image_metrics_display_uid)
            image_bytes = req.json().get('bytes') if req.status_code == 200 \
                else []
            overlay = {k: v for k, v in img_result.overlay.items()
                       if v is not None} if img_result.overlay else {}
            criteria = {k: v for k, v in img_result.criteria.items()
                        if v is not None} if img_result.criteria else {}
            image_results.append(ImageResultModel(
                image_uid=img_result.uid, status=img_result.status,
                image=image_bytes, overlay=OverlayModel(**overlay),
                criteria=CriteriaModel(**criteria),
                extra=img_result.extra))
        return ProcedureResultModel(
            procedure_uid=item.uid, status=item.status,
            matched=item.matching_data, images=image_results)


class ImageResultResource(BPMDBResource):

    @swagger.doc({
        'tags': ['result'],
        'description': 'Query image result',
        'security': {
            SEC_ISSUER_KEY: [],
            SEC_ROLE_KEY: [],
        },
        'parameters': [
            ISSUER_KEY_PARAM,
            ROLE_KEY_PARAM,
            {
                'name': 'uid',
                'description': 'Image uuid',
                'in': 'path',
                'type': BigIntModel.get('type'),
                'format': BigIntModel.get('format'),
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'Computation request success',
                'schema': ImageResultModel,
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
    @bpm_flask_authentication_mixin
    @bpm_flask_public_access
    def get(self, uid):
        issuer_key = request.headers.get(HEADER_ISSUER_KEY)
        with self.wf_context() as wf:
            item = wf.get_image_result(issuer_key, uid)
            if not item:
                abort(404)
        expected_ct = request.headers.get(
            'Content-Type', 'application/json').lower()
        headers = {
            'Content-Type': expected_ct,
            HEADER_ISSUER_KEY: issuer_key,
        }
        req = StorageClient.get_metrics_image(
            headers, item.tmp_image_metrics_display_uid)
        image_bytes = req.json().get('bytes') if req.status_code == 200 \
            else []
        overlay = {k: v for k, v in item.overlay.items()
                   if v is not None} if item.overlay else {}
        criteria = {k: v for k, v in item.criteria.items()
                    if v is not None} if item.criteria else {}
        return ImageResultModel(
            image_uid=item.uid, status=item.status,
            image=image_bytes, overlay=OverlayModel(**overlay),
            criteria=CriteriaModel(**criteria),
            extra=item.extra)
