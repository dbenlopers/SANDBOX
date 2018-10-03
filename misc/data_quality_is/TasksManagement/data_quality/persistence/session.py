# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, exc, pool
from sqlalchemy.orm import sessionmaker, scoped_session
from data_quality.celeryconfig import cfg_parser


class LookLively(object):
    """Ensures that MySQL connections checked out of the pool are alive."""
    def checkout(self, dbapi_con, con_record, con_proxy):
        try:
            if hasattr(dbapi_con, 'ping'):
                try:
                    dbapi_con.ping(False)
                except TypeError:
                    dbapi_con.ping()
        except dbapi_con.OperationalError as ex:
            if ex.args[0] in (2006, 2013, 2014, 2045, 2055):
                raise exc.DisconnectionError()
            else:
                raise


def create_session():
    """
    return a session
    :return: return a session factory
    """
    # construct the database url with config parameters
    __database_url = '{}?charset=utf8'.format(cfg_parser['database']['url'])

    # an Engine, which the Session will use for connection
    # resources
    db_engine = create_engine(__database_url,
                              poolclass=pool.QueuePool,
                              listeners=[LookLively()],
                              pool_recycle=cfg_parser.getint('sqlalchemy', 'pool_recycle'),
                              pool_size=cfg_parser.getint('sqlalchemy', 'pool_size'),
                              echo=cfg_parser.getboolean('sqlalchemy', 'echo'),
                              convert_unicode=True)

    # Create a session factory
    session_factory = sessionmaker(bind=db_engine,
                                   autocommit=cfg_parser.getboolean('sqlalchemy', 'autocommit'),
                                   autoflush=cfg_parser.getboolean('sqlalchemy', 'autoflush'))

    return session_factory


def create_scoped_session():
    """
    Create a scoped session
    :return: return a scoped session
    """
    return scoped_session(create_session())


DB_SESSION = create_session()()
SCOPED_DB_SESSION = create_scoped_session()()
