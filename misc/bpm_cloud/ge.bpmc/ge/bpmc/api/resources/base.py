# -*- coding: utf-8 -*-

from contextlib import contextmanager

from flask_restful import Resource
from flask_restful_swagger_2 import Schema
from sqlalchemy.orm import scoped_session

from ge.bpmc.app.injection import Contexts, Core, Factories, Gateways, Services


class BPMDBResource(Resource):

    @property
    def _logger_(self):
        return Core.logger()

    @contextmanager
    def em_context(self):
        yield Contexts.em()

    @contextmanager
    def wf_context(self):
        yield Services.workflow()


class BPMMessageProducer:

    @contextmanager
    def broker_context(self):
        yield Factories.celery_factory()


class StorageBaseResource(BPMDBResource, BPMMessageProducer):

    @contextmanager
    def storage_context(self):
        yield Services.storage(wf=Services.workflow())
