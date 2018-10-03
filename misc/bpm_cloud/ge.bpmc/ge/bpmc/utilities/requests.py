# -*- coding: utf-8 -*-

from requests.exceptions import ConnectionError

from ge.bpmc.utilities.base import ResponseData
from ge.bpmc.utilities.flask import flask_format_error


def flask_manage_python_requests_connectivity(func):
    """
    Return a function wrapper to handle requests exceptions

    Keyword arguments:
    func -- .api._base.BPMDBResource class function
    """
    def func_wrapper(*args, **kwargs):
        resource = args[0] if len(args) > 0 else object()
        logger = getattr(resource, '_logger_')
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            logger.exception(e)
            formatted_msg = flask_format_error(
                'Internal application error', 500)
            return ResponseData(formatted_msg, 500)
    return func_wrapper


def bpm_flask_connectivity_mixin(func):
    """
    Return a function wrapper for default connectivity
    management

    Keyword arguments:
    func -- Resource class function
    """
    @flask_manage_python_requests_connectivity
    def func_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return func_wrapper
