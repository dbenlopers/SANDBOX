# -*- coding: utf-8 -*-

import logging
import time
from configparser import ConfigParser

from sqlalchemy import *
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker


default_config_file = "/opt/sources/configuration/config.cfg"
log = logging.getLogger('db-probe')
delay = 5


def extractConfig():
    config = ConfigParser()
    config.read(default_config_file)
    return config


def get_session(formatted_url, pool_size=5, max_overflow=5):
    eng = create_engine(formatted_url,
                        max_overflow=1,
                        pool_size=1,
                        pool_recycle=3600, encoding='utf-8')
    return sessionmaker(bind=eng)


def getConnection(config):
    conn = None
    dsn = config.get('database', 'dsn')
    session = get_session(dsn)()
    log.info('Checking if db is available with dsn: %s' % dsn)
    while conn is None:
        try:
            conn = session.connection()
        except exc.OperationalError as e:
            log.warning('Waiting for database...')
            time.sleep(delay)
    conn.close()


if __name__ == '__main__':
    config = extractConfig()
    conn = getConnection(config)
    log.info('Db ready')
