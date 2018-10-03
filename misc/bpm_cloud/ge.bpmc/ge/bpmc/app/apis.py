# -*- coding: utf-8 -*-

import configparser
import logging
import os

from dependency_injector import providers

from ge.bpmc import SEC_CMPT_KEY, SEC_ISSUER_KEY, SEC_ROLE_KEY
from ge.bpmc.api.bundles import (generate_available_api, generate_crud_api,
                                 generate_public_api, generate_storage_api)
from ge.bpmc.api.schemas.security import (ComponentAuthModel, IssuerAuthModel,
                                          RoleAuthModel)
from ge.bpmc.app.injection import (Application, Contexts, Core, Factories,
                                   Gateways, Services)
from ge.bpmc.persistence.orm import metadata
from ge.bpmc.tasks import matching, processing
from ge.bpmc.tasks.routes import ROUTES
from ge.bpmc.utilities.celery import celery_config
from ge.bpmc.utilities.conf import check_configuration_keys
from ge.bpmc.utilities.injector import set_configuration
from ge.bpmc.utilities.logging import setup_logging
from ge.bpmc.utilities.profiling import setup_resource_profiling

WEBDAV_CONFIGURATION_OPTS_WHITELIST = set([
    'proxy_hostname', 'proxy_login', 'proxy_password',
    'ssl_auth_cert_path', 'ssl_auth_key_path', 'auth_login', 'auth_password'
])
WEBDAV_CONFIGURATION_CLIENT_OPTS_WHITELIST = set(['verify'])
WEBDAV_CONFIGURATION_KEYS_IGNORE = []
WEBDAV_CONFIGURATION_KEYS_PREFIX_BLACKLIST = ['ssl_auth_', 'auth_']


def translate_webdav_key(
        current_key,
        blacklist=WEBDAV_CONFIGURATION_KEYS_PREFIX_BLACKLIST):
    for prefix in blacklist:
        if current_key.startswith(prefix):
            return current_key.replace(prefix, '')
    return current_key


def get_webdav_configuration_entry(key, config, section):
    return (translate_webdav_key(key), config.get(section, key))


def get_webdav_configuration(keys, config):
    return dict(
        map(lambda x: get_webdav_configuration_entry(x, config, 'webdav_opts'),
            keys))


class BaseApi:

    title = 'BPM Default'
    identifier = 'bpm-default'
    configparser = configparser.ConfigParser()
    security_defs = {
        SEC_ISSUER_KEY: IssuerAuthModel,
        SEC_ROLE_KEY: RoleAuthModel
    }
    expected_keys = {'database': ['dsn'],
                     'logging': ['configuration'],
                     'application': ['roletoken', 'cpnttoken']}

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
        host = self.configparser.get('application', 'host') if (
            self.configparser.has_section('application') and
            self.configparser.has_option('application', 'host')) \
            else '0.0.0.0'
        port = int(self.configparser.get('application', 'port')) if (
            self.configparser.has_section('application') and
            self.configparser.has_option('application', 'port')) \
            else 8080
        storage_uri = '%(proto)s://%(uri)s' % ({
            'proto': self.configparser.get('storage', 'proto') if (
                self.configparser.has_section('storage') and
                self.configparser.has_option('storage', 'proto')) else 'http',
            'uri': self.configparser.get('storage', 'uri') if (
                self.configparser.has_section('storage') and
                self.configparser.has_option('storage', 'uri')) else (
                    'localhost:9080')
        })
        role_token = self.configparser.get('application', 'roletoken')
        component_token = self.configparser.get('application', 'cpnttoken')

        data = {
            'database': {'dsn': database_dsn},
            'app': {'identifier': self.identifier,
                    'title': self.title,
                    'host': host,
                    'port': port,
                    'storage_uri': storage_uri},
            'tokens': {'role': role_token,
                       'component': component_token},
            'webdav': {'options': {}, 'client_options': {}},
            'swagger': {'security_definitions': self.security_defs},
        }
        set_configuration(data)
        self.build_webdav_opts()

        Core.logger.override(providers.Singleton(
            logging.getLogger, 'bpm'))
        Core.profiler.override(providers.Singleton(
            logging.getLogger, 'bpm_profiling'))

        profiling = (self.configparser.getboolean('application', 'profiling')
                     if (
            self.configparser.has_section('application') and
            self.configparser.has_option('application', 'profiling'))
            else False)

        ignite = (self.configparser.getboolean('application', 'ignite') if (
            self.configparser.has_section('application') and
            self.configparser.has_option('application', 'ignite'))
            else False)

        if profiling:
            Core.logger().info('Running with profiling active')
            setup_resource_profiling()

        if ignite:
            Core.logger().info('Igniting application')
            metadata.create_all(Gateways.session().bind)

    def build_webdav_opts(self):

        if self.configparser.has_section('webdav_opts'):
            configuration_keys = set(self.configparser['webdav_opts'].keys())\
                .intersection(WEBDAV_CONFIGURATION_OPTS_WHITELIST)
            filtered_configuration_keys = \
                [x for x in configuration_keys
                 if x not in WEBDAV_CONFIGURATION_KEYS_IGNORE]
            set_configuration({
                'webdav': {
                    'options': get_webdav_configuration(
                        filtered_configuration_keys, self.configparser)}
            })

        if self.configparser.has_section('webdav_client_opts'):
            keys = set(self.configparser['webdav_client_opts'].keys())\
                .intersection(WEBDAV_CONFIGURATION_CLIENT_OPTS_WHITELIST)
            client_opts = {}
            for key in keys:
                client_opts.update({
                    key: self.configparser.get('webdav_client_opts', key)
                })
            set_configuration({
                'webdav': {
                    'client_options': client_opts}
            })


class BrokerApi(BaseApi):

    def __init__(self, configfile):
        self.expected_keys.update({'broker': ['dsn']})
        super(BrokerApi, self).__init__(configfile)
        broker_dsn = self.configparser.get('broker', 'dsn')
        data = {'broker': {'dsn': broker_dsn},
                'app': {'celery_app_name': 'bpm'}}
        set_configuration(data)
        celery_app = Factories.celery_factory()
        celery_app.config_from_object(celery_config())
        celery_app.conf.task_routes = ROUTES


class PublicApi(BaseApi):
    """
        BPM Public API
    """

    title = 'BPM Public'
    identifier = 'bpm-public'

    def __init__(self, configfile):
        self.expected_keys.update({'storage': ['proto', 'uri']})
        super(PublicApi, self).__init__(configfile)
        api = Contexts.api()
        generate_public_api(api)
        app = Application.api(api=api)
        app.run()


class StorageApi(BrokerApi):
    """
        BPM Storage Application
    """

    title = 'BPM Storage'
    identifier = 'bpm-storage'

    def __init__(self, configfile):
        self.security_defs.update({
            SEC_CMPT_KEY: ComponentAuthModel
        })
        super(StorageApi, self).__init__(configfile)
        api = Contexts.api()
        generate_storage_api(api)
        app = Application.api(api=api)
        app.run()


class CRUDApi(BaseApi):
    """
        BPM CRUD Application
    """

    title = 'BPM CRUD'
    identifier = 'bpm-crud'

    def __init__(self, configfile):
        super(CRUDApi, self).__init__(configfile)
        api = Contexts.api()
        generate_crud_api(api)
        app = Application.api(api=api)
        app.run()


class AvailableApi(BrokerApi):
    """
        BPM Available Application
    """

    title = 'BPM Available'
    identifier = 'bpm-available'

    def __init__(self, configfile):
        super(AvailableApi, self).__init__(configfile)
        api = Contexts.api()
        generate_available_api(api)
        app = Application.api(api=api)
        app.run()
