# -*- coding: utf-8 -*-

from __future__ import absolute_import
from data_quality.processing.status_mapping import rational_mapping, status_mapping


def innovalog_test(data):
    """
    Run innova log test on singe entry
    :param data: json object created from an innova orm object
    :return:
    """
    assert isinstance(data, dict), 'data must be in json format'

    _timedelta = (data['measure_date'] - data['datetime_last_pull']).days

    if data['nb_fail'] is None:
        data['nb_fail'] = 0

    if data['nb_fail'] > 5 and _timedelta > 7:
        return {"innovalog_id": data['id'],
                "status_id": status_mapping['NOK'], "rational_id": rational_mapping['CRITICAL']}
    if data['nb_fail'] < 5 and _timedelta > 7:
        return {"innovalog_id": data['id'],
                "status_id": status_mapping['OK'], "rational_id": rational_mapping['WARNING']}
    if data['nb_fail'] > 5 and _timedelta < 7:
        return {"innovalog_id": data['id'],
                "status_id": status_mapping['NOK'], "rational_id": rational_mapping['ERROR']}
    if data['nb_fail'] < 5 and _timedelta < 7:
        return {"innovalog_id": data['id'],
                "status_id": status_mapping['OK'], "rational_id": rational_mapping['NFF']}