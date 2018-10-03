# -*- coding: utf-8 -*-

import configparser
import datetime
import logging
import logging.config
import os
import re
import traceback
from time import time

import pymysql
import yaml

from ibcp_client import GIBSDataRetriever

LOGGER = logging.getLogger('ibcp.sync')

BLOCK_SIZE = 5000
BLOCKS_COMMIT_THRESHOLD = 10

MEASURES_TABLE_COLUMNS = [
    'date', 'measure_type', 'serial_number', 'hostname', 'measure_name',
    'unit', 'value', 'min_available', 'max_available', 'max_available_unit'
]

INSERT_STATEMENT = 'INSERT INTO measures (%s) VALUES (%s)' % (
    ', '.join(['`%s`' % x for x in MEASURES_TABLE_COLUMNS]),
    ','.join(['%s' for i in range(0, len(MEASURES_TABLE_COLUMNS))])
)

HEADER_WS = 'gibsws'
HEADER_ORIG_DB = 'gibsdb'
HEADER_DEST_DB = 'perfdb'
HEADER_JOB = 'job'

MAPPING = {
    'date': None,
    'measure_type': 'description',
    'hostname': None,
    'max_available': None,
    'max_available_unit': None,
    'measure_name': 'mesureName',
    'serial_number': 'serialNumber',
    'unit': None,
    'value': None
}

RE_FLOAT = re.compile('^\d+?\.\d+?$')
RE_MEASURE = re.compile('^(?P<value>\d+(\.\d+)?)\s?(?P<unit>[\w\%]*)' +
                        '(\((?P<min_available>\d+(\.\d+)?))?' +
                        '(\/(?P<max_available>\d+(\.\d+)?)' +
                        '\s?(?P<max_available_unit>[a-zA-Z]*))?\)?$')

"""
tests = ['80.00/100.00 AZ', '127 AZ', '98.47%Free(917/931GB)', '213',
         '12.80%Used(0.51/3.97GB)', '0.26GB', '0.15GB', '276',
         '8.04%Used(0.24/2.97GB)', '0.20GB', '0.13GB', '213.00', '12.80%',
         '0.26GB', '0.15GB', '276.00', '8.04%', '0.20GB', '0.13GB']
from pprint import pprint
pprint([m.groupdict() for m in [RE_MEASURE.match(x) for x in tests]
       if m is not None])
"""

#######################
#
# DATA MANAGEMENT UTILS
#
#######################


def to_measure(data):
    clean = {dest: data.get(source or dest, None)
             for dest, source in MAPPING.items()}
    clean['serial_number'], clean['hostname'] = clean['hostname'].split('_', 1)
    clean['date'] = datetime.datetime.fromtimestamp(int(clean['date']))
    return clean


def to_measures(perf_obj):
    perf_measures = []
    perf_data = perf_obj.get("performancedata").split('|')[0].strip()
    if not perf_data:
        # Can happen sometimes, string is empty
        return perf_measures
    perf_items = [x.split(':') for x in perf_data.split(', ')]
    perf_results = [{'mesureName': k, 'value': to_standard_value(v)}
                    for k, v in perf_items]
    for result in perf_results:
        value = result['value']
        if RE_FLOAT.match(value):
            result['value'] = float(value)
            perf_measures.append(to_measure({**perf_obj, **result}))
        else:
            match = RE_MEASURE.match(value)
            if match:
                result.update({k: v for k, v in match.groupdict().items()
                               if v is not None})
                perf_measures.append(to_measure({**perf_obj, **result}))
    return perf_measures


def to_standard_value(value):
    return value.replace(",", ".").strip().replace(' ', '')


def format_data(results):
    """
    Business method to extract and format data for 'measures' table.
    """
    measures = []
    counter = 0
    for result in results:
        counter += 1
        try:
            # Skip "DeviceInt*" probes
            if result.get("description").startswith("DeviceInt"):
                continue

            if ('measures' in result and len(result.get("measures")) and
                    result.get("description") not in ['JVM', 'Disk']):
                measures.extend([to_measure({**result, **x})
                                 for x in result.get('measures')
                                 if x is not None])
            elif 'performancedata' in result:
                if result.get("description") not in ['JVM', 'Disk']:
                    continue
                measures.extend(to_measures(result))
        except Exception as e:
            LOGGER.error('Error happened during formating: %s' %
                         traceback.format_exc())
    LOGGER.info('Parsed %i elements, extracted %i measures' % (
        counter, len(measures)))
    return measures


def to_row_data(row_dict):
    return [row_dict.get(x) for x in MEASURES_TABLE_COLUMNS]

#######################
#
# PROCESSING
#
#######################

# Loading config


config_parser = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'ibcp_sync.cfg')
logging_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'logging.yml')
logging.config.dictConfig(yaml.load(open(logging_file)))

if not os.path.exists(config_file):
    raise IOError('No such configuration file: %s' % config_file)
config_parser.read(config_file)

ws_url = '%(proto)s://%(uri)s' % ({
    'proto': config_parser.get(HEADER_WS, 'proto'),
    'uri': config_parser.get(HEADER_WS, 'uri')})
orig_db_user = config_parser.get(HEADER_ORIG_DB, 'user')
orig_db_pwd = config_parser.get(HEADER_ORIG_DB, 'pwd')

dsn_data = {
    'user': config_parser.get(HEADER_DEST_DB, 'user'),
    'password': config_parser.get(HEADER_DEST_DB, 'pwd'),
    'host': config_parser.get(HEADER_DEST_DB, 'host'),
    'port': int(config_parser.get(HEADER_DEST_DB, 'port')),
    'database': config_parser.get(HEADER_DEST_DB, 'schema')
}

period = int(config_parser.get(HEADER_JOB, 'synced_period'))

# Components instanciation

data_retriever = GIBSDataRetriever(ws_url, orig_db_user, orig_db_pwd)
connection = pymysql.connect(**dsn_data, charset='utf8')

# Start date selection

MODE_SYSTEM = 'system'
MODE_FORCED = 'forced'
MODE_LAST = 'last_occurence'
JOB_MODES = [MODE_SYSTEM, MODE_FORCED, MODE_LAST]

if config_parser.has_option('job', 'sync_mode'):
    job_mode = config_parser.get('job', 'sync_mode')
    if job_mode not in JOB_MODES:
        raise ValueError('Job sync mode can only be an instance of %s' % (
            ','.join(JOB_MODES)))
else:
    job_mode = MODE_LAST

if job_mode == MODE_FORCED:
    if not config_parser.has_option('job', 'start'):
        raise ValueError('Forced mode needs to have a start date')
    start_date = config_parser.get('job', 'start')
    LOGGER.info('Start date has been forced')
elif job_mode == MODE_SYSTEM:
    if (not config_parser.has_option('job', 'delay') or
            not config_parser.has_option('job', 'delay_unit')):
        raise ValueError('System mode needs to have a delay specified')
    delay = config_parser.getint('job', 'delay')
    delay_unit = config_parser.get('job', 'delay_unit')
    start_date = (datetime.datetime.now() - datetime.timedelta(**{
        delay_unit: delay}))
    LOGGER.info('Start date has been forced using system with delay %s %s' % (
        delay, delay_unit))
else:
    # MODE_LAST management
    cursor = connection.cursor()
    rows = cursor.execute('SELECT max(date) FROM measures')
    start_date = cursor.fetchone()[0] if rows == 1 else datetime.datetime.now()
    cursor.close()
    LOGGER.info('Start date queried from database')

# Data extraction & transformation

results = data_retriever.import_results(start_date, period=period)
LOGGER.info('Retrieving data starting from %s with period %s' % (
    start_date, period
))
etl_start = time()
formatted = format_data(results)
etl_transform = time()
LOGGER.info('Extraction and transformation done in %0.2f' % (
    etl_transform - etl_start))

# Insertion

cursor = connection.cursor()
loop_counter = 0

while len(formatted) > 0:
    block = formatted[0:BLOCK_SIZE]
    formatted = formatted[BLOCK_SIZE:-1]
    row_data = list(map(to_row_data, block))
    cursor.executemany(INSERT_STATEMENT, row_data)
    loop_counter += 1
    if loop_counter == BLOCKS_COMMIT_THRESHOLD:
        loop_counter = 0
        cursor.close()
        connection.commit()
        cursor = connection.cursor()

cursor.close()
connection.commit()
connection.close()

etl_load = time()
LOGGER.info('Load done in %0.2f' % (
    etl_load - etl_transform))
