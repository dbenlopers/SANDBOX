# -*- coding: utf-8 -*-

import datetime
import getpass
import json
import logging
import logging.config
import socket
import time

import yaml

from ge.bpmc import BPM_NAME, BPM_VERSION

GE_DT_FORMAT = "%Y-%m-%dT%H:%M:%S"

GE_LOG_STANDARD_FORMAT = ('%(ts)s - %(logger)s - %(level)s - %(msg)s')

GE_LOG_FULL_FORMAT = (
    '%(ts)s - %(host)s - %(app_name)s#%(app_version)s - ' +
    '%(thread)s@%(fqdn)s - %(logger)s - %(level)s - %(type)s - ' +
    '%(user)s - %(msg)s')


def ge_format_time(dt):
    res = dt.strftime(GE_DT_FORMAT)
    msecs = round(float(dt.microsecond) / float(1000))
    return '%s.%03i%s' % (res, msecs, time.strftime('%z'))


def ge_logger_format_time(record, datefmt=None):
    dt = datetime.datetime.fromtimestamp(record.created)
    return ge_format_time(dt)


class GEFormatter(logging.Formatter):

    def __init__(self, *args, **kwargs):
        self.logger_type = kwargs.pop('logger_type', 'default')
        show_details = kwargs.pop('show_details', 0)
        self.logger_format = (GE_LOG_FULL_FORMAT if show_details
                              else GE_LOG_STANDARD_FORMAT)
        super(GEFormatter, self).__init__(*args, **kwargs)

    def format_time(self, record, datefmt=None):
        return ge_logger_format_time(record, datefmt)

    def ge_format(self, record):
        return {
            'ts': self.format_time(record, self.datefmt),
            'host': socket.gethostname(),
            'app_name': BPM_NAME,
            'app_version': BPM_VERSION,
            'thread': record.threadName,
            'fqdn': '%s:%s:%d' % (
                record.module, record.funcName, record.lineno),
            'logger': record.name,
            'level': record.levelname,
            'type': self.logger_type,
            'user': getpass.getuser(),
            'msg': record.getMessage()
        }

    def format(self, record):
        msg = self.logger_format % (self.ge_format(record))
        return msg


class GEJsonFormatter(GEFormatter):

    mapping = {
        'timestamp': 'ts',
        'appName': 'app_name',
        'appVersion': 'app_version',
        'threadName': 'thread',
        'callerFqdn': 'fqdn',
        'userId': 'user',
        'hostname': 'host',
        'loggerName': 'logger',
        'level': 'level',
        'type': 'type',
        'message': 'msg'
    }

    def format(self, record):
        data = self.ge_format(record)
        return json.dumps({k: data.get(v) for k, v in self.mapping.items()})


def setup_logging(config_file):
    logging.config.dictConfig(yaml.load(open(config_file)))
