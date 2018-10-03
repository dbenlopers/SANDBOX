# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy import exc
from sqlalchemy import pool
from sqlalchemy.orm import mapper, sessionmaker


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


def get_session(formatted_url, pool_size=5, max_overflow=5):
    """
    Returns a session_factory.

    :param formatted_url: the connexion string used to create the engine
    :return: return a session_factory
    """
    eng = create_engine(formatted_url,
                        max_overflow=max_overflow,
                        poolclass=pool.QueuePool,
                        pool_size=pool_size,
                        pool_recycle=3600, encoding='utf-8',
                        listeners=[LookLively()])
    return sessionmaker(bind=eng)
