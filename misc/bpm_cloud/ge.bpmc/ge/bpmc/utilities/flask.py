# -*- coding: utf-8 -*-

import json
import traceback

from dict2xml import dict2xml
from flask import Response, abort, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.scoping import scoped_session

from ge.bpmc import HEADER_CMPT_KEY, HEADER_ISSUER_KEY, HEADER_ROLE_KEY
from ge.bpmc.app.injection import Contexts, Core
from ge.bpmc.exceptions.auth import BPMAuthFailedException
from ge.bpmc.exceptions.base import BPMFlaskException
from ge.bpmc.exceptions.storage import BPMNoAvailableStorage
from ge.bpmc.persistence.orm import *
from ge.bpmc.utilities.auth import (validate_component_token,
                                    validate_role_token)
from ge.bpmc.utilities.base import (BPM_ACCEPTED_MIMETYPES, InnerError,
                                    ResponseData)
from ge.bpmc.utilities.sqlalchemy import (sqlalchemy_get_unique_item_or_none,
                                          transaction)
from ge.bpmc.utilities.swagger import validate_payload

XML_HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

#   Message formatters


def flask_format_message(msg, code):
    """
    Format message in a common dictionnary structure for all flask responses.

    Keyword arguments:
    msg -- A string containing the expected message
    code -- HTTP Code returned by flask
    """
    return {'code': code, 'message': msg}


def flask_format_error(msg, code, target=None, details=[], inner_error=None):
    """
    Format error in a common dictionnary structure for all flask responses.
    Design base on MS guidelines for error message formating:
    https://github.com/Microsoft/api-guidelines/blob/master/Guidelines.md#710-response-formats.

    Keyword arguments:
    msg -- A string containing the expected message
    code -- HTTP Code returned by flask
    target -- A string containing info on targeted feature. Optional.
    details -- A list containing strings providing
    additionnal details, useful for validation
    inner_error -- An InnerError allowing embed errors management
    """
    msg = flask_format_message(msg, code)
    infos = {
        'target': target,
        'details': details
    }
    if inner_error:
        inner_infos = {
            'code': inner_error.code
        }
        parent = inner_infos
        current_error = inner_error
        while(current_error.inner_error is not None):
            parent['innererror'] = {
                'code': current_error.inner_error.code
            }
            parent = parent['innererror']
            current_error = current_error.inner_error
        infos['innererror'] = inner_infos

    msg.update(infos)
    error = {
        'error': msg
    }
    return error


def flask_unsupported_media_type_message(code=415):
    """
    Format unsupported media error message.

    Keyword arguments:
    code -- HTTP Code returned by flask
    """
    return flask_format_error(
        'Supported media types are %s' % ', '.join(BPM_ACCEPTED_MIMETYPES),
        code)


def flask_format_response_for_mimetype(mimetype, content):
    """
    Formats python dictionnary based on a requested mimetype.
    Note that his method only supports BPM_ACCEPTED_MIMETYPES
    and that it doesn't filter unsupported one. If the mimetype
    is not handled by this function, returns the untouched content.

    Keyword arguments:
    mimetype -- The requested mimetype
    content -- Python dictionnary containing the expected content
    """
    if mimetype == 'application/json':
        return json.dumps(content)
    elif mimetype == 'application/xml':
        return '\n'.join([XML_HEAD, dict2xml(content)])
    else:
        return content


# CRUD OBJECT FORMATING


def flask_object_to_dict(item):
    """
    Formats objects into a desired dictionnary structure.

    Keyword arguments:
    item -- Actual object. Can either inherit from DictBase tagging it as an
    SQLAlchemy object or primitive python object
    """
    return item.to_dict() if isinstance(item, DictBase) else item


def flask_method_return_to_dict(func):
    """
    Return a formated dict for resource method objects formating.
    Allows to use of common structure for HTTP Code 200 responses.
    In case a ResponseData bubbles here, the function return will be
    untouched.

    Keyword arguments:
    func -- .api._base.BPMDBResource class function
    """
    def func_wrapper(*args, **kwargs):
        raw = func(*args, **kwargs)
        # Acting as a proxy if raw is a ResponseData
        if isinstance(raw, ResponseData):
            return raw
        # Actual object formating
        is_list = isinstance(raw, list)
        return [
            {'item': flask_object_to_dict(x)}
            for x in raw] if is_list \
            else flask_object_to_dict(raw)
    return func_wrapper

# "AUTHENTICATION" MANAGEMENT


def bpm_flask_public_access(func):
    """
    Return a function wrapper for BPM public access.
    This assumes the payload contains the role header.

    Keyword arguments:
    func -- .api.base.BPMDBResource class function
    """
    def func_wrapper(*args, **kwargs):
        token = request.headers.get(HEADER_ROLE_KEY, '')
        if not validate_role_token(token):
            raise BPMAuthFailedException('Role token provided is invalid', 401)
        return func(*args, **kwargs)
    return func_wrapper


def bpm_flask_component_access(func):
    """
    Return a function wrapper for BPM component access.
    This assumes the payload contains the component header.
    It ensures that only a BPM component can access to this service.

    Keyword arguments:
    func -- .api.base.BPMDBResource class function
    """
    def func_wrapper(*args, **kwargs):
        token = request.headers.get(HEADER_CMPT_KEY, '')
        if not validate_component_token(token):
            raise BPMAuthFailedException('Component token provided is invalid',
                                         401)
        return func(*args, **kwargs)
    return func_wrapper


def flask_check_issuer_existence(func):
    """
    Return a function wrapper for Issuer authentication.
    This assumes the payload contains the issuer header
    and that the Resource has an entity manager context

    Keyword arguments:
    func -- .api.base.BPMDBResource class function
    """
    def func_wrapper(*args, **kwargs):
        resource = args[0] if len(args) > 0 else object()
        logger = getattr(resource, '_logger_')
        with resource.em_context() as em:
            if not isinstance(em._session_, scoped_session):
                logger.warning(
                    'Session not available while looking for issuer')
                raise BPMAuthFailedException('Unable to validate issuer', 401)
            key = request.headers.get(HEADER_ISSUER_KEY, '')
            try:
                if not em.get_issuer('key', key):
                    raise BPMAuthFailedException(
                        'Invalid requester key', 400,
                        'Authentication',
                        ['Provided key is not known by the application'])
            except SQLAlchemyError as e:
                logger.exception(e)
                raise BPMAuthFailedException('Unable to validate issuer', 401)
            return func(*args, **kwargs)
    return func_wrapper


# FLASK REQUEST MANAGEMENT


def flask_validate_payload(definition=None, request_attribute='data'):
    """
    Return a function wrapper for request validation.
    Validates request payload using based on generated definition from Schema
    class. See .utilies.swagger.get_validation_schema utility.

    Keyword arguments:
    definition -- Schema definition
    request_attribute -- The request attribute used to extract payload content.
    Must be readable by json.loads method.
    """
    def func_decorator(func):
        def func_wrapper(*args, **kwargs):
            if not definition:
                return func(*args, **kwargs)
            content = getattr(request, request_attribute, None)
            if content:
                if type(content) is bytes:
                    content = content.decode('utf-8')
                params = json.loads(content) \
                    if type(content) in [str] else content
                request.form = params
                errors = validate_payload(definition, params, [])
                if errors:
                    raise BPMFlaskException(
                        'Payload format does not match requirements',
                        400,
                        'Validation',
                        errors)
            else:
                raise BPMFlaskException('Empty payload', 400, 'Validation')
            return func(*args, **kwargs)
        return func_wrapper
    return func_decorator

# FLASK RESPONSE MANAGEMENT


def flask_manage_object_does_not_exist(func):
    """
    Return a function wrapper to handle SQLAlchemy No result errors

    Keyword arguments:
    func -- A method using SQLAlchemy query
    """
    @sqlalchemy_get_unique_item_or_none
    def func_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    def actual_wrapper(*args, **kwargs):
        return func_wrapper(*args, **kwargs) or abort(404)
    return actual_wrapper


def flask_manage_duplication(func):
    """
    Return a function wrapper to handle SQLAlchemy duplication errors

    Keyword arguments:
    func -- A method using SQLAlchemy query
    """
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            if e.orig.args[0] in (1062,):
                formatted_msg = flask_format_error(
                    'Item already exists', 409, '', [], None)
                return ResponseData(formatted_msg, 409)
            else:
                raise e
    return func_wrapper


def flask_handle_bpm_application_errors(func):
    """
    Return a function wrapper to handle BPM Flask application errors

    Keyword arguments:
    func -- .api._base.BPMDBResource class function
    """
    def func_wrapper(*args, **kwargs):
        resource = args[0] if len(args) > 0 else object()
        logger = getattr(resource, '_logger_')
        try:
            return func(*args, **kwargs)
        except BPMNoAvailableStorage as e:
            logger.warning('No storage client available')
            formatted_msg = flask_format_error(
                'An issue occured while handling your content',
                e.code, '', [], None)
            return ResponseData(formatted_msg, e.code)
        except BPMFlaskException as e:
            formatted_msg = flask_format_error(e.message, e.code, e.target,
                                               e.details, e.inner_error)
            return ResponseData(formatted_msg, e.code)
    return func_wrapper


def flask_manage_expected_contenttype(func):
    """
    Return a function wrapper to handle expected mimetype return.
    (see BPM_ACCEPTED_MIMETYPES). If nothing is passed in the
    'Content-Type' header, assumes application/json.

    Keyword arguments:
    func -- .api._base.BPMDBResource class function
    """
    def func_wrapper(*args, **kwargs):
        raw = func(*args, **kwargs)
        mimetype = request.headers.get(
            'Content-Type', 'application/json').lower()
        if mimetype not in BPM_ACCEPTED_MIMETYPES:
            mimetype = 'application/json'
            code = 415
            content = flask_unsupported_media_type_message(code)
        else:
            is_response = isinstance(raw, ResponseData)
            content = flask_format_response_for_mimetype(
                mimetype,
                raw.message if is_response else raw)
            code = raw.code if is_response else 200
        resp = Response(response=content, status=code, mimetype=mimetype)
        resp.headers['Accept'] = mimetype
        return resp
    return func_wrapper

# Mixins


def bpm_flask_mixin(validation_class_=None):
    """
    Return a function wrapper for default Flask management

    Keyword arguments:
    validation_class_ -- Flask swagger Schema class
    """
    def func_decorator(func):
        @flask_manage_expected_contenttype
        @flask_handle_bpm_application_errors
        @flask_method_return_to_dict
        @flask_validate_payload(validation_class_)
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return func_wrapper
    return func_decorator


def bpm_flask_sqlalchemy_mixin(func):
    """
    Return a function wrapper for default SQLAlchemy management

    Keyword arguments:
    func -- Resource class function
    """
    @flask_manage_duplication
    @flask_manage_object_does_not_exist
    @transaction(Core.logger, Contexts.em)
    def func_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return func_wrapper


def bpm_flask_authentication_mixin(func):
    """
    Return a function wrapper for default authentication management

    Keyword arguments:
    func -- Resource class function
    """
    @flask_check_issuer_existence
    def func_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return func_wrapper
