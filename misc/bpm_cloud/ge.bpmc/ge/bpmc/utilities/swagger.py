# -*- coding: utf-8 -*-
import inspect

from flask_restful_swagger_2 import Schema
from sqlalchemy.types import ARRAY, Enum

from ge.bpmc.api.schemas.default import (AngleModel, ArrayModel, BigIntModel,
                                         BinaryModel, BooleanModel, ByteModel,
                                         DateModel, DatetimeModel, DoubleModel,
                                         DoublePointModel, FloatModel,
                                         ImageBytesModel, IntModel, JsonModel,
                                         LineModel, NumberModel, PasswordModel,
                                         PointModel, SimpleImageModel,
                                         SmallIntModel, StatusModel,
                                         StringModel, TinyIntModel)

TYPES_DOC = {
    'BigInteger': BigIntModel,
    'Integer': IntModel,
    'SmallInteger': SmallIntModel,
    'Text': StringModel,
    'Date': StringModel,
    'DateTime': StringModel,
    'Time': StringModel,
    'Float': DoubleModel,
    'Numeric': NumberModel,
    'JSON': JsonModel,
    'ARRAY': ArrayModel,
    'Boolean': BooleanModel
}


def get_swagger_enum_type(enum_values):
    """
    Return a swagger type based on enumeration values.

    Keyword arguments:
    enum_values -- A list of primitive objects
    """
    if len(enum_values) > 0:
        obj_type = type(enum_values[0])
        if obj_type is str:
            return 'string'
        if obj_type is float:
            return 'numeric'
        if obj_type is int:
            return 'integer'
    return 'string'


def get_table_swagger_schema(table, required=[], blacklist=[]):
    """
    Return a swagger schema information
    based on a SQLAlchemy table definition (Table)

    Keyword arguments:
    table -- A sqlalchemy.sql.schema.Table instance
    required -- A list of required attributes. Optional
    blacklist -- A list of attributes that will be ignored. Optional.
    """
    _required = []
    properties = {}
    primary = None
    for name, col in [x for x in table.columns.items() if x not in blacklist]:
        if col.primary_key:
            primary = name
        if not col.nullable:
            _required.append(name)
        if isinstance(col.type, Enum):
            enum_type = get_swagger_enum_type(col.type.enums)
            properties[name] = {'type': enum_type, 'enum': col.type.enums}
        elif isinstance(col.type, ARRAY):
            array_type = TYPES_DOC.get(col.type.item_type, 'string')
            properties[name] = {'type': 'array', 'items': {'type': array_type}}
        else:
            col_type = repr(col.type).split('(')[0]
            properties[name] = TYPES_DOC.get(
                col_type, {'type': col_type.lower()})

    required = set(_required).union(set(required))
    return properties, list(required), primary


def get_validation_schema(class_):
    _properties = {}
    _model = class_.__name__.split('.')[-1]
    for k, v in class_.properties.items():
        if inspect.isclass(v) and issubclass(v, Schema):
            _properties[k] = get_validation_schema(v)
        else:
            _properties[k] = v
    return {'_properties': _properties,
            '_model': _model, '_requirements': getattr(class_, 'required', [])}


validation_msg = 'The attribute "{0}" must be {1}, but was "{2}" ({3})'


def validate_payload(definition, payload, _errors=[]):
    _properties = definition['_properties']
    _requirements = definition['_requirements']
    for k, v in _properties.items():
        if (k in _requirements) and (k not in payload.keys()):
            _errors.append('Missing attribute %s' % k)
            continue
        if '_properties' in v:
            validate_payload(_properties[k], payload[k], _errors)
        else:
            _type = v['type']
            value = payload.get(k)
            type_error_msg = None
            if _type == 'integer' and not isinstance(value, int):
                type_error_msg = 'an int'
            if _type == 'number' and not isinstance(value, int) \
                    and not isinstance(value, float):
                type_error_msg = 'an int or float'
            if _type == 'string' and not isinstance(value, str):
                type_error_msg = 'a string'
            if _type == 'boolean' and not isinstance(value, bool):
                type_error_msg = 'a boolean'
            if type_error_msg and (
                    (k not in _requirements) and (value is not None)):
                _errors.append(validation_msg.format(
                               k, type_error_msg, type(value), value))
    return _errors
