# -*- coding: utf-8 -*-

from copy import copy

from flask_restful_swagger_2 import Schema

# Base

StringModel = {'type': 'string'}
DateModel = {'type': 'string', 'format': 'date'}
DatetimeModel = {'type': 'string', 'format': 'date-time'}
PasswordModel = {'type': 'string', 'format': 'password'}
ByteModel = {'type': 'string', 'format': 'byte'}
BinaryModel = {'type': 'string', 'format': 'binary'}

TinyIntModel = {'type': 'integer', 'format': 'int8'}
SmallIntModel = {'type': 'integer', 'format': 'int16'}
IntModel = {'type': 'integer', 'format': 'int32'}
BigIntModel = {'type': 'integer', 'format': 'int64'}
NumberModel = {'type': 'number'}
FloatModel = {'type': 'number', 'format': 'float'}
DoubleModel = {'type': 'number', 'format': 'double'}

JsonModel = {'type': 'object',
             'description': 'JSON'}

ArrayModel = {'type': 'array'}

BooleanModel = {'type': 'boolean'}

# Status


class StatusModel(Schema):
    type = 'object'
    properties = {
        'message': StringModel
    }

# Available items


available_items = copy(ArrayModel)
available_items.update({'items': BigIntModel})


class AvailableItemsModel(Schema):
    type = 'object'
    properties = {
        'items': available_items
    }

# Geometry


class PointModel(Schema):
    type = 'object'
    properties = {
        'x': IntModel,
        'y': IntModel
    }


class DoublePointModel(Schema):
    type = 'object'
    properties = {
        'start': PointModel,
        'end': PointModel
    }


class LineModel(Schema):
    type = 'object'
    properties = {
        'start': PointModel,
        'end': PointModel
    }


class AngleModel(Schema):
    type = 'object'
    properties = {
        'start': LineModel,
        'end': LineModel
    }

# Imaging


ImageLineModel = copy(ArrayModel)
ImageLineModel.update({'items': IntModel})


ImageBytesModel = copy(ArrayModel)
ImageBytesModel.update({
    'items': ImageLineModel,
    'example': [[137, 80, 78, 71],
                [10, 0, 0, 0]]
})


class SimpleImageModel(Schema):
    type = 'object'
    properties = {
        'bytes': ImageBytesModel
    }
