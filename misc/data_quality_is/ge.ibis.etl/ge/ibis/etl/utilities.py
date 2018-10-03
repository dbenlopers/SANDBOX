# coding=utf-8
"""
Utilities for ETL part
"""

import collections
from datetime import datetime

from dateutil.parser import parse
from requests.exceptions import ConnectionError

ERROR_MSG_DATEIFY_INVALID_DATE = (
    'dateify: ' + 'Invalid date without null values allowed')

# Requests error management


def connection_error_handler(func):
    """
    Return a function wrapper to handle requests exceptions
    """
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            return None
    return func_wrapper

# Dict manipulation


def dictionarize(el):
    """
    Returns a dict representation without enumerable types
    """
    _dict = {}
    if isinstance(el, dict):
        for key, value in el.items():
            if isinstance(value, dict):
                _dict[key] = dictionarize(value)
            elif (isinstance(value, (list, tuple)) and value):
                _dict[key] = {str(idx): dictionarize(elt)
                              for idx, elt in enumerate(value)}
            else:
                _dict[key] = value
        return _dict
    elif isinstance(el, list):
        return {str(idx): dictionarize(elt)
                for idx, elt in enumerate(el)}
    else:
        return el


def flatten(d, parent_key='', sep='.'):
    """
    Flattens dict arborescence to a single level.
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_unformatted(nested):
    return flatten(dictionarize(nested))

# Dict rules utilities


def dateify(item, allow_null=False):
    if item is None:
        if not allow_null:
            raise ValueError(ERROR_MSG_DATEIFY_INVALID_DATE)
        else:
            return item
    return item if isinstance(item, datetime) else parse(item)


def substring(item, start=0, end=10):
    if item:
        return item[start:end]


def booleanify(item, false_condition_value=None):
    return not (item == false_condition_value)


def value_or_null(item, condition_value=True, replacement=None):
    if item == condition_value:
        return replacement
    return None


def listify(item, separator=','):
    if not isinstance(item, str):
        ValueError('Item must be a string')
    return item.split(',')

# Aggregation rules


def first_not_null(current_value, item_key, item_value):
    return item_value if not current_value else current_value


def aggregate_dict(current_value, item_key, item_value):
    _dict = current_value or {}
    _dict[item_key.split('.')[-1]] = item_value
    return _dict


def aggregate_version(current_value, item_key, item_value):
    if item_value:
        return '%s' % item_value if not current_value else '%s.%s' % (
            current_value, item_value)

# Other utils


def explode_as_dict(value, separator, keys):
    items = value.split(separator)
    if len(items) != len(keys):
        return
    return {keys[idx]: v for idx, v in enumerate(items)}


def first_available(_dict, keys):
    filtered = [x for x in keys if x in _dict]
    if not filtered:
        return KeyError('No available key')
    return _dict[filtered[0]]

# Business utils


def to_dvr_interval(data):
    lower, upper = dict(), dict()
    lower['rule'] = upper['rule'] = data['_class'].split("$")[-1]
    lower['value'] = data['lowerBound']
    upper['value'] = data['upperBound']
    lower['relation'] = 'GTE' if data["lowerBoundInclusive"] else 'GT'
    upper['relation'] = 'LTE' if data["upperBoundInclusive"] else 'LT'
    return (lower, upper)

DVR_VALUE_KEYS = ['upperBound', 'lowerBound', 'bound', 'version', 'prefix']


def to_dvrs(items):
    dvrs = []
    for dvr in items:
        if dvr['_class'].endswith('$Interval'):
            return to_dvr_interval(dvr)
        dvrs.append({
            'rule': dvr['_class'].split('$')[-1],
            'relation': dvr.get('relation'),
            'value': first_available(dvr, DVR_VALUE_KEYS)
        })
    return dvrs
