# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful_swagger_2 import Api

from ge.bpmc import STORE_IMAGE_ENTRYPOINT, STORE_METRICS_IMAGE_ENTRYPOINT
from ge.bpmc.api.resources.available import (AvailableImagesResource,
                                             AvailableProceduresResource)
from ge.bpmc.api.resources.bpm import (ComputationResource, ExamResultResource,
                                       ImageResultResource,
                                       ProcedureResultResource,
                                       RepositoryRegistrationResource,
                                       RepositoryUpdateResource,
                                       SystemResource)
from ge.bpmc.api.resources.orm import (IssuerByKeyResource, IssuerResource,
                                       IssuersResource)
from ge.bpmc.api.resources.storage import (ImageQueryResource,
                                           ImageStorageResource,
                                           MetricsImageQueryResource,
                                           MetricsImageStorageResource)
from ge.bpmc.api.schemas.security import IssuerAuthModel

# Resources registries

# ORM


def register_requester(api):
    api.add_resource(IssuersResource,
                     '/issuer',
                     endpoint='issuers')
    # , methods=['GET',])

    api.add_resource(IssuerResource,
                     '/issuer/<int:uid>',
                     endpoint='issuer')

    api.add_resource(IssuerByKeyResource,
                     '/issuer/<string:key>',
                     endpoint='issuer_by_key')

# COMPUTATION


def register_repository(api):
    api.add_resource(
        RepositoryRegistrationResource,
        '/repository')
    api.add_resource(
        RepositoryUpdateResource,
        '/repository/<int:uid>',
        endpoint="repository.update")


def register_system(api):
    api.add_resource(
        SystemResource,
        '/system')


def register_computation(api):
    api.add_resource(
        ComputationResource,
        '/computation')


def register_kpis(api):
    api.add_resource(
        ExamResultResource,
        '/kpis/exam/<int:uid>')
    api.add_resource(
        ProcedureResultResource,
        '/kpis/procedure/<int:uid>')
    api.add_resource(
        ImageResultResource,
        '/kpis/image/<int:uid>')

# IMAGE STORAGE


def register_image_storage(api):
    api.add_resource(ImageQueryResource,
                     '/'.join([STORE_IMAGE_ENTRYPOINT, '<int:uid>']),
                     endpoint='image_query')
    api.add_resource(MetricsImageQueryResource,
                     '/'.join([STORE_METRICS_IMAGE_ENTRYPOINT, '<int:uid>']),
                     endpoint='metrics_image_query')
    api.add_resource(ImageStorageResource,
                     STORE_IMAGE_ENTRYPOINT,
                     endpoint='image_store')
    api.add_resource(MetricsImageStorageResource,
                     STORE_METRICS_IMAGE_ENTRYPOINT,
                     endpoint='metricsimage_store')

# AVAILABLE ITEMS


def register_available_items(api):
    api.add_resource(
        AvailableImagesResource,
        '/available/images')

    api.add_resource(
        AvailableProceduresResource,
        '/available/procedures')

# APIs


def generate_crud_api(api):
    """Registers on a flask restful API Crud components"""
    register_requester(api)


def generate_public_api(api):
    """Registers on a flask restful API Public components"""
    register_computation(api)
    register_kpis(api)
    register_system(api)
    register_repository(api)


def generate_storage_api(api):
    """Registers on a flask restful API Storage components"""
    register_image_storage(api)


def generate_available_api(api):
    """Registers on a flask restful API Available components"""
    register_available_items(api)
