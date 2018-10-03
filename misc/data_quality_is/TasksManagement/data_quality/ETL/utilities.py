# coding=utf-8
"""
Utilities for ETL part
"""
from data_quality.persistence.orm import Customer, CustomeDictionary, IntegrationMode, FTPconnection, DicomPattern, \
    InnovaLogPull
from datetime import datetime
from dateutil.parser import parse


def insert_object(sess, to_insert):
    """
    Insert new object into session
    :param sess: db session
    :param to_insert: object to insert
    :return:
    """
    sess.add(to_insert)
    sess.flush()


def update_object(sess, to_update, param, exclude=None):
    """
    Update object passed, update it into database with param
    :param sess: db session
    :param to_update: orm object to update
    :param param: dict that contain new value of att
    :param exclude: which att to exclude, typically we have 'id' and 'ID' (PK in database)
    :return:
    """
    if exclude is None:
        exclude = []

    for key, value in param.items():
        if key not in exclude:
            setattr(to_update, key, value)
    sess.flush()


def flattenDict(d, result=None, index=None, Key=None):
    """
    Flatten a input dict
    param d:  input dict to flatten
    """
    if result is None:
        result = {}
    if isinstance(d, (list, tuple)):
        for indexB, element in enumerate(d):
            if Key is not None:
                newkey = Key
            flattenDict(element, result, index=indexB, Key=newkey)
    elif isinstance(d, dict):
        for key in d:
            value = d[key]
            if Key is not None and index is not None:
                newkey = ".".join([Key, (str(key) + '.' + str(index))])
            elif Key is not None:
                newkey = ".".join([Key, (str(key))])
            else:
                newkey = str(key)
            flattenDict(value, result, index=None, Key=newkey)
    else:
        result[Key] = d
    return result


def flattenDict_alt(d, result=None, index=None, Key=None):
    """
    Flatten a input dict
    param d:  input dict to flatten
    """
    if result is None:
        result = {}
    if isinstance(d, (list, tuple)):
        if not any(isinstance(el, dict) for el in d):
            result[Key] = '.'.join(map(str, d))
            return result
        for indexB, element in enumerate(d):
            if Key is not None:
                newkey = Key
            flattenDict_alt(element, result, index=indexB, Key=newkey)
    elif isinstance(d, dict):
        for key in d:
            value = d[key]
            if Key is not None and index is not None:
                newkey = ".".join([Key, (str(key) + '.' + str(index))])
            elif Key is not None:
                newkey = ".".join([Key, (str(key))])
            else:
                newkey = str(key)
            flattenDict_alt(value, result, index=None, Key=newkey)
    else:
        result[Key] = d
    return result


def _date(data):
    if isinstance(data, datetime):
        return data
    elif isinstance(data, str):
        return parse(data)


def _substring(data, mapping):
    return data[mapping['substring'][0]:mapping['substring'][1]]


def fill_object(obj, data, mapping):
    """
    :param obj: object to fill
    :param data: flatten data dict
    :param mapping: mapping dict
    :return: filled object
    """
    for key, value in data.items():
        if key in mapping:
            if "date" in mapping[key]:
                setattr(obj, mapping[key]['target'], _date(value))
            elif "iftrue" in mapping[key]:
                if value is not False:
                    setattr(obj, mapping[key]['target'], mapping[key]['iftrue'])
            elif "agg" in mapping[key]:
                if getattr(obj, mapping[key]['target']) is None:
                    setattr(obj, mapping[key]['target'], {})
                getattr(obj, mapping[key]['target'])[key.split('.')[-1]] = value
            elif "substring" in mapping[key]:
                setattr(obj, mapping[key]['target'], _substring(value, mapping[key]))
            elif "ifexists" in mapping[key]:
                setattr(obj, mapping[key]['target'], mapping[key]['ifexists'])
            else:
                if isinstance(value, bool):
                    setattr(obj, mapping[key]['target'], value)
                elif isinstance(value, str):
                    setattr(obj, mapping[key]['target'], value)
                elif isinstance(value, int):
                    setattr(obj, mapping[key]['target'], value)
                else:
                    setattr(obj, mapping[key]['target'], str(value).encode('utf-8'))
                    # setattr(obj, mapping[key]['target'], str(value).encode('utf-8'))

    return obj


def _parse_interval(data):
    lower = {}
    upper = {}
    lower['rule'] = data['_class'].split("$")[-1]
    upper['rule'] = data['_class'].split("$")[-1]
    lower['value'] = data['lowerBound']
    upper['value'] = data['upperBound']

    if data["lowerBoundInclusive"]:
        lower['relation'] = "GTE"
    else:
        lower['relation'] = "GT"

    if data["upperBoundInclusive"]:
        upper['relation'] = "LTE"
    else:
        upper['relation'] = "LT"

    return [lower, upper]


def parse_deviceversionrequirement(input):
    """

    :param input:
    :return:
    """
    for elem in input:
        if elem['_class'].split("$")[-1] == 'Interval':
            return _parse_interval(elem)
        Data = {}
        for key, value in elem.items():
            if key == "_class":
                Data["rule"] = value.split("$")[-1]
            if key == "relation":
                Data["relation"] = value
            if key in ["prefix", "version", "bound", "lowerBound", "upperBound"]:
                Data["value"] = value
        return [Data]

############################################################################################


def _check_customer(sess, customer):
    q = sess.query(Customer).filter(Customer.serial_number == customer.serial_number,
                                    Customer.revision_number == customer.revision_number)
    return q


def _check_customdictionary(sess, customdict):
    q = sess.query(CustomeDictionary).filter(CustomeDictionary.local_id == customdict.local_id,
                                             CustomeDictionary.code == customdict.code,
                                             CustomeDictionary.description == customdict.description)
    return q


def _check_im(sess, im):
    q = sess.query(IntegrationMode).filter(IntegrationMode.integration_mode == im.integration_mode,
                                           IntegrationMode.modality == im.modality)
    return q


def _check_ftpco(sess, ftpco):
    q = sess.query(FTPconnection).filter(FTPconnection.hash == ftpco.hash)
    return q


def _check_pattern(sess, pattern):
    q = sess.query(DicomPattern).filter(DicomPattern.hash == pattern.hash)
    return q


def _check_innovalog(sess, innovalog):
    q = sess.query(InnovaLogPull).filter(InnovaLogPull.serial_number == innovalog.serial_number,
                                         InnovaLogPull.aet == innovalog.aet)
    return q
