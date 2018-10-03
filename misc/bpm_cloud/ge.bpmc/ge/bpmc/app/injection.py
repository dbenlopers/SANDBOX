# -*- coding: utf-8 -*-

import logging

import dependency_injector.containers as containers
import dependency_injector.providers as providers
from flask import Blueprint
from flask_restful_swagger_2 import Api
from sqlalchemy.orm import scoped_session

from ge.bpmc.app import default
from ge.bpmc.persistence import dal, session
from ge.bpmc.services.storage import StorageService
from ge.bpmc.services.workflow import WorkflowService
from ge.bpmc.utilities.base import BPM_ACCEPTED_MIMETYPES
from celery import Celery


class Core(containers.DeclarativeContainer):
    """IoC container of core component providers."""

    config = providers.Configuration('config')
    logger = providers.AbstractSingleton(logging.Logger)
    profiler = providers.AbstractSingleton(logging.Logger)
    science_logger = providers.Singleton(logging.getLogger, 'bpm_science')


class Factories(containers.DeclarativeContainer):
    """IoC container for factories"""

    session_factory = providers.Singleton(session.get_session,
                                          Core.config.database.dsn)

    blueprint_factory = providers.Singleton(Blueprint,
                                            name=Core.config.app.identifier,
                                            import_name=__name__)

    celery_factory = providers.Singleton(Celery,
                                         'bpm-worker')


class Gateways(containers.DeclarativeContainer):
    """IoC container of gateway (API clients to remote services) providers."""

    session = providers.Singleton(scoped_session,
                                  Factories.session_factory)


class Contexts(containers.DeclarativeContainer):
    """IoC container for contexts"""

    em = providers.Singleton(dal.BPMEntityManager,
                             logger=Core.logger,
                             gateways=Gateways)

    api = providers.Singleton(Api,
                              app=Factories.blueprint_factory,
                              add_api_spec_resource=False,
                              consumes=BPM_ACCEPTED_MIMETYPES,
                              produces=BPM_ACCEPTED_MIMETYPES,
                              security_definitions=Core.config.swagger
                              .security_definitions)


class Services(containers.DeclarativeContainer):
    """IoC container of business service providers."""

    storage = providers.Singleton(StorageService,
                                  logger=Core.logger,
                                  em=Contexts.em,
                                  webdav_opts=Core.config.webdav.options,
                                  webdav_client_opts=Core.config.webdav
                                  .client_options)

    workflow = providers.Singleton(WorkflowService,
                                   logger=Core.logger,
                                   science_logger=Core.science_logger,
                                   em=Contexts.em)


class Application(containers.DeclarativeContainer):
    """IoC container of application component providers."""

    api = providers.Callable(default.ApiApplication,
                             title=Core.config.app.title,
                             identifier=Core.config.app.identifier,
                             host=Core.config.app.host,
                             port=Core.config.app.port)

    worker = providers.Callable(default.WorkerApplication,
                                application=Factories.celery_factory)

    beat = providers.Callable(default.BeatApplication,
                              application=Factories.celery_factory)
