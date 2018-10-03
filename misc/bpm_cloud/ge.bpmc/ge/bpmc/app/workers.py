# -*- coding: utf-8 -*-

import configparser
import logging
import os

from dependency_injector import providers
from ge.bpmc.app.injection import (Application, Contexts, Core, Factories,
                                   Services)
from ge.bpmc.tasks import matching, periodic, processing
from ge.bpmc.tasks.routes import ROUTES
from ge.bpmc.utilities.celery import celery_config
from ge.bpmc.utilities.conf import check_configuration_keys
from ge.bpmc.utilities.injector import set_configuration
from ge.bpmc.utilities.logging import setup_logging
from ge.bpmc.utilities.profiling import setup_task_profiling


class BPMWorker:

    app_name = 'bpmworker'
    configparser = configparser.ConfigParser()
    expected_keys = {'broker': ['dsn'],
                     'database': ['dsn'],
                     'logging': ['configuration'],
                     'storage': ['proto', 'uri'],
                     'application': ['cpnttoken']}
    loglevel = logging.WARN

    def __init__(self, configfile):
        if not os.path.exists(configfile):
            raise IOError('No such configuration file: %s' % configfile)
        self.configparser.read(configfile)
        check_configuration_keys(self.expected_keys, self.configparser)

        logging_config = self.configparser.get('logging', 'configuration')
        if not os.path.exists(logging_config):
            raise IOError('No such configuration file: %s' % logging_config)
        setup_logging(logging_config)

        database_dsn = self.configparser.get('database', 'dsn')
        broker_dsn = self.configparser.get('broker', 'dsn')
        storage_uri = '%(proto)s://%(uri)s' % ({
            'proto': self.configparser.get('storage', 'proto'),
            'uri': self.configparser.get('storage', 'uri')
        })

        component_token = self.configparser.get('application', 'cpnttoken')
        data = {'broker': {'dsn': broker_dsn},
                'database': {'dsn': database_dsn},
                'app': {'storage_uri': storage_uri},
                'tokens': {'component': component_token}}
        set_configuration(data)
        celery_app = Factories.celery_factory()
        celery_app.config_from_object(celery_config())
        celery_app.conf.task_routes = ROUTES

        Core.logger.override(providers.Singleton(
            logging.getLogger, 'bpm'))
        Core.profiler.override(providers.Singleton(
            logging.getLogger, 'bpm_profiling'))

        self.loglevel = (
            logging.getLevelName(logging.getLogger().getEffectiveLevel()) or
            logging.WARN)

        profiling = (self.configparser.getboolean('application', 'profiling')
                     if (
            self.configparser.has_section('application') and
            self.configparser.has_option('application', 'profiling'))
            else False)

        if profiling:
            Core.logger().info('Running with profiling active')
            setup_task_profiling()


class ProcessingWorker(BPMWorker):

    def __init__(self, configfile):
        super(ProcessingWorker, self).__init__(configfile)
        worker = Application.worker(
            name='worker.processing', queues=['processing'],
            level=self.loglevel)
        worker.run()


class PeriodicWorker(BPMWorker):

    def __init__(self, configfile):
        app = Factories.celery_factory()
        super(PeriodicWorker, self).__init__(configfile)
        worker = Application.worker(
            name='worker.periodic', queues=['periodic'],
            level=self.loglevel)
        worker.run()


class MatchingWorker(BPMWorker):

    def __init__(self, configfile):
        app = Factories.celery_factory()
        super(MatchingWorker, self).__init__(configfile)
        worker = Application.worker(
            name='worker.matching', queues=['matching'],
            level=self.loglevel)
        worker.run()
