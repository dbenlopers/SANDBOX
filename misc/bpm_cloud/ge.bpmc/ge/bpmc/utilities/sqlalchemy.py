# -*- coding: utf-8 -*-

import traceback
from time import time

from sqlalchemy.orm.exc import NoResultFound


def sqlalchemy_get_unique_item_or_none(func):
    """
    Return a function wrapper to handle SQLAlchemy NoResultFound error.

    Keyword arguments:
    func -- An function which might raise a NoResultFound
    i.e a query using .one()
    """
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoResultFound as e:
            return None
    return func_wrapper


def transaction(logger_factory, em_factory):
    def func_decorator(func):
        def func_wrapper(*args, **kwargs):
            logger = logger_factory()
            em = em_factory()
            error = None
            em.init_session()
            try:
                result = func(*args, **kwargs)
                em._session_.commit()
            except Exception as e:
                msg = '\n'.join(
                    ['An error occured during call to func %s, rolling back.' %
                      func, 'Message was: %s' % str(e)])
                error = e
                logger.warning(msg)
                em._session_.rollback()
            finally:
                em.close_session()
                if error is not None:
                    raise error
            return result
        return func_wrapper
    return func_decorator
