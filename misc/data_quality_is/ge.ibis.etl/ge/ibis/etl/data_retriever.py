# -*- coding: utf-8 -*-

import gzip
import json
import logging
from enum import Enum

import requests
from bson.json_util import JSONOptions, dumps, loads
from bson.objectid import ObjectId
from dateutil.parser import parse as parse_date
from requests.exceptions import ConnectionError

from .utilities import connection_error_handler


class Entities(Enum):
    CustomerRevision = 'CustomerRevision'
    ApplicationEntity = 'ApplicationEntity'
    Device = 'Device'
    IntegrationRevision = 'IntegrationRevision'
    TranslatorConfiguration = 'TranslatorConfiguration'
    IBAutomation = 'IBAutomation'


class GIBSDataRetriever():

    URL_ACTION_FORMAT = '{root}/{action}/{entity}'

    def __init__(self, logger, ws_root_url, db_user,
                 db_password, allow_purge=False,
                 ):
        self._logger_ = logger
        self.ws_root_url = ws_root_url
        self.db_user = db_user
        self.db_password = db_password
        self.allow_purge = allow_purge

    # Utils

    def decompress(self, _data):
        return gzip.decompress(_data).decode('utf-8')

    @connection_error_handler
    def check_ws_availability(self):
        ct = requests.get(self.ws_root_url)
        return ct.status_code == 200

    def get_ws_url(self, action, entity):
        return self.URL_ACTION_FORMAT.format(**{
            'root': self.ws_root_url,
            'action': action,
            'entity': entity
        })

    def get_formatted_params(self, params):
        return dumps(
            params, json_options=JSONOptions(datetime_representation=2))

    def get_ib_automation_params(
            self, serial_number, information_type, last_pull_date):
        return [{"$unwind": "$data.resultRows"},
                {"$match": {"data.serialNumber": serial_number,
                            "data.dwibInformationType": information_type,
                            "receptionDate": {
                                "$gt": parse_date(last_pull_date)}}
                 }]

    @connection_error_handler
    def query_ws(self, method, action, entity, params={}):
        """
        Returns a request response if successful or None.
        """
        formatted_params = self.get_formatted_params(params)
        func = getattr(requests, method)
        url = self.get_ws_url(action, entity)
        req = func(url, params={'query': formatted_params},
                   auth=(self.db_user, self.db_password))
        if req.status_code != 200:
            raise ValueError('Error while querying %s: %s - %s' %
                             (req.url, req.status_code, req.reason))
        return req.content

    def iterate(self, method, action, entity, params={}):
        self._logger_.warn('Querying %s/%s' % (action, entity))
        ct = self.query_ws(method, action, entity, params)
        for item in loads(self.decompress(ct)):
            yield item

    # Data imports

    def import_customers(self, last_pull_date):
        params = {"lastUpdate": {"$gt": parse_date(last_pull_date)}}
        return self.iterate(
            'get', 'find', Entities.CustomerRevision.value, params)

    def import_aes(self, last_pull_date):
        params = {"lastAgentUpdate": {"$gt": parse_date(last_pull_date)}}
        return self.iterate(
            'get', 'find', Entities.ApplicationEntity.value, params)

    def import_devices(self):
        return self.iterate(
            'get', 'find', Entities.Device.value)

    def import_integration_revisions(self):
        params = {"supported": "YES", "deleted": False}
        return self.iterate(
            'get', 'find', Entities.IntegrationRevision.value, params)

    def import_dicom_patterns(self, serial_number, last_pull_date):
        params = self.get_ib_automation_params(
            serial_number, 'EltRegularPatterns', last_pull_date)
        return self.iterate(
            'get', 'aggregate', Entities.IBAutomation.value, params)

    def import_studies(self, serial_number, last_pull_date):
        types = {"$in": ["EltXAConsolidation",
                         "EltMGConsolidation",
                         "EltCTConsolidation",
                         "EltRFConsolidation"]}
        params = self.get_ib_automation_params(
            serial_number, types, last_pull_date)
        return self.iterate(
            'get', 'aggregate', Entities.IBAutomation.value, params)

    def import_ct_logs(self,  serial_number, last_pull_date):
        params = self.get_ib_automation_params(
            serial_number, 'EltCTLog', last_pull_date)
        return self.iterate(
            'get', 'aggregate', Entities.IBAutomation.value, params)

    def import_innova_logs(self,  serial_number, last_pull_date):
        params = self.get_ib_automation_params(
            serial_number, 'EltInnovaLog', last_pull_date)
        return self.iterate(
            'get', 'aggregate', Entities.IBAutomation.value, params)

    def import_translator_configuration(self):
        return self.iterate(
            'get', 'find', Entities.TranslatorConfiguration.value)
