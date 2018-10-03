# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import math
import os

from data_quality.processing.status_mapping import (rational_mapping,
                                                    status_mapping)

_filepath = os.path.join(os.path.dirname(__file__), "ConfigTest.json")

with open(_filepath) as json_data:
    cfg_testing = json.load(json_data)
    json_data.close()

_key_dosimetric = 'Dosimetric'
_default_test_param = cfg_testing[_key_dosimetric]['default']


def __relative(a, b, rel_tol):
    return math.isclose(a, b, rel_tol=rel_tol)


def __decimal(a, b, dec_tol):
    return abs(a - b) < dec_tol


def __perform_equality_test(study_lvl, serie_lvl, param):
    """
    Perform an equality test
    :param study_lvl: study value
    :param serie_lvl: serie value
    :param param: parameters as dict
    :return: tuple (equality test , fail_rule)
    """
    _equality_test = True
    _fail_rule = ["OK", "NFF"]

    # iter on rel_tol & dec_tol
    for current_test in ['rel_tol', 'dec_tol']:

        if current_test not in param.keys():
            continue

        if current_test == 'rel_tol':
            _equality_test = __relative(
                study_lvl, serie_lvl, rel_tol=param[current_test]['thres'])
        elif current_test == 'dec_tol':
            _equality_test = __decimal(
                study_lvl, serie_lvl, dec_tol=param[current_test]['thres'])

        # if test has fail, set output to specified output
        if _equality_test is False:
            _fail_rule = param[current_test]['fail_rule']

        # low dose mitigation
        if "low_dose" in param[current_test].keys():
            _lowdose_test = study_lvl < param[current_test]['low_dose']
            if _lowdose_test is True and _equality_test is True:
                _fail_rule = param[current_test]['low_dose_rule']
                return _equality_test, _fail_rule
            if _equality_test is False and _lowdose_test is True and 'low_dose_mitigate_rule' in param[
                    current_test].keys():
                _fail_rule = param[current_test]['low_dose_mitigate_rule']

        if _equality_test is False:
            return _equality_test, _fail_rule

    return _equality_test, _fail_rule


def _dosimetric_equality(study, kpi):
    """
    test the dosimetric equality between study and serie level for given kpi
    :param study: an Study ORM object converted in json
    :param kpi: which dosimetric value to test
    :return:
    """
    study_lvl = study['data'][kpi]
    serie_lvl = study['data'][kpi + '_test']

    # determine difference between study-serie dose information
    _diff = round(study_lvl - serie_lvl, 2)

    # case when study & serie level are not null
    if study_lvl != 0 and serie_lvl != 0:
        # if study value are greater than sum(serie) level
        if study_lvl > serie_lvl:

            # If we don't found specific test for a dose type, take the default one
            try:
                test_param_for_kpi = cfg_testing[_key_dosimetric][kpi]['equality']
            except KeyError:
                test_param_for_kpi = cfg_testing[_key_dosimetric]["default"]['equality']

            _equality_test, fail_rule = __perform_equality_test(
                study_lvl, serie_lvl, test_param_for_kpi)
            
            if _equality_test:
                # if equality test pass
                return {"study_id": study['id'], "type": kpi,
                        "status_id": status_mapping[fail_rule[0]], 
                        "rational_id": rational_mapping[fail_rule[1]],
                        'value': _diff}
            else:
                return {"study_id": study['id'], "type": kpi,
                        "status_id": status_mapping[fail_rule[0]], 
                        "rational_id": rational_mapping[fail_rule[1]],
                        'value': _diff}
        else:
            # if sum(serie) level are greater than study value
            if __decimal(study_lvl, serie_lvl, 0.1):
                return {"study_id": study['id'], "type": kpi,
                        "status_id": status_mapping['OK'], 
                        "rational_id": rational_mapping['NFF'], 
                        'value': _diff}
            elif __relative(study_lvl, serie_lvl, 0.01):
                return {"study_id": study['id'], "type": kpi,
                        "status_id": status_mapping['OK'], 
                        "rational_id": rational_mapping['WARNING'], 
                        'value': _diff}
            else:
                return {"study_id": study['id'], "type": kpi,
                        "status_id": status_mapping['NOK'], 
                        "rational_id": rational_mapping['NONSENSE'], 
                        'value': _diff}

    # case when study & serie level is null for one or both side
    if study_lvl == 0 and serie_lvl != 0:
        return {"study_id": study['id'], "type": kpi,
                "status_id": status_mapping['NOK'], 
                "rational_id": rational_mapping['CRITICAL'], 
                'value': _diff}
    if study_lvl != 0 and serie_lvl == 0:
        return {"study_id": study['id'], "type": kpi,
                "status_id": status_mapping['OK'],
                "rational_id": rational_mapping['ENHANCEMENT'], 
                'value': _diff}
    if study_lvl == 0 and serie_lvl == 0:
        return {"study_id": study['id'], "type": kpi,
                "status_id": status_mapping['OK'], 
                "rational_id": rational_mapping['WARNING'], 
                'value': _diff}


def _dlp_localizer(study, kpi, localizers_name, thres):
    """
    Only for ct study, check if mean dlp by localizers are below theshold
    :param study: an Study ORM object converted in json
    :param kpi: which dosimetric value to test
    :param localizers_name : var name of number of localizers
    :param thres:
    :return:
    """
    study_level = study['data'][kpi]
    serie_level = study['data'][kpi + '_test']
    nb_loc = study['data'][localizers_name]

    try:
        _dlp_by_loc = (study_level - serie_level) / nb_loc
    except ZeroDivisionError:
        _dlp_by_loc = 0

    # case when study & serie level are exactly equal
    if study_level == serie_level:
        return {"study_id": study['id'], "type": 'dlp_localizer',
                "status_id": status_mapping['OK'], 
                "rational_id": rational_mapping['NFF'], 
                "value": nb_loc}

    # case when study & serie level are not different
    if study_level != serie_level:
        if nb_loc == 0:
            return {"study_id": study['id'], "type": 'dlp_localizer',
                    "status_id": status_mapping['OK'], 
                    "rational_id": rational_mapping['WARNING'], 
                    "value": nb_loc}
        else:
            if _dlp_by_loc < thres:
                return {"study_id": study['id'], "type": 'dlp_localizer',
                        "status_id": status_mapping['OK'], 
                        "rational_id": rational_mapping['NFF'], 
                        "value": nb_loc}
            else:
                return {"study_id": study['id'], "type": 'dlp_localizer',
                        "status_id": status_mapping['NOK'], 
                        "rational_id": rational_mapping['WARNING'], 
                        "value": nb_loc}


def dosimetric_test(study):
    """
    Run the dosimetric consistency processing on consolidation data
    :param study: an Study ORM object converted in json
    :return: return a list of dosimetric object results
    """
    _to_store = []

    # Search all dosimetric type in data attribute from study
    try:
        _kpi_in_data = {x.replace('_test', '') for x in study['data'].keys()}
        _kpi_in_data.discard('num_localizers_value')
    except AttributeError:
        return

    for kpi in _kpi_in_data:
        _to_store.append(_dosimetric_equality(study, kpi))

    if study['type'] == 'CT':
        _to_store.append(_dlp_localizer(study, 'total_dlp', "num_localizers_value",
                                        cfg_testing[_key_dosimetric]["CT_localizers_value"]["threshold"]))
    return _to_store
