# -*- coding: utf-8 -*-

import configparser
import logging
import os
import sqlalchemy
import sys
import time

delay = 5
default_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probes.cfg')
log = logging.getLogger('db-wait')

log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

def extract_config():
    config = configparser.ConfigParser()
    config.read(default_config_file)
    return config

def try_connection(config):
    conn = None
    db_uri = config.get('probe','db_uri')
    print('db_uri %s'%db_uri)
    engine = None
    
    try:
        engine = sqlalchemy.create_engine(db_uri)
    except Exception as e:
        while True:
            log.warn('Invalid configuration: %s'%(e))
            time.sleep(delay)

    while conn is None:
        try:
            conn = engine.connect()
            return conn
        except sqlalchemy.exc.OperationalError as e:
            log.info('DB is unreachable')
            time.sleep(delay)

if __name__ == '__main__':
    config = extract_config()
    conn = try_connection(config)
    log.info('Connectivity with database established')
