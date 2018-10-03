# -*- coding: utf-8 -*-

from __future__ import absolute_import
from data_quality.requests.db import get_last_customer_revision, \
    get_translatorconfig
import re


def __format_input_translator(str_to_process):
    """
    to 'SR_999_CT_GENERIC (5) / SR_997_CT_GENERIC (4)' to ['SR_999_CT_GENERIC', 'SR_997_CT_GENERIC']
    remove translator id (into parenthesis) and make split by /
    :param str_to_process: string to process
    """
    return re.sub(r'\([^)]*\)', '', str_to_process).replace(' ', '').split('/')


def _compare_translator(ae_config, tc_config):
    """
    Compare two dict that contain information about translator
    """
    status_list = []

    # iter on all data type as key and translator set to this data type for the incoming ae
    for current_ae_datatype, current_ae_dt_translator in ae_config.items():
        # check only data type not set at None
        if current_ae_datatype is not None:
            # if data type from ae is not found in translator config
            if current_ae_datatype not in tc_config.keys():
                status_list.append(5)

            # iter on translator for a data type, trans are type of translator (image or not)
            # & trans_value are value of translator use
            for translator_code, translator_value in current_ae_dt_translator.items():

                if current_ae_datatype not in tc_config.keys():
                    status_list.append(5)
                    continue

                # if a translator is set to None on ae side, -> default to be used
                if translator_value is None:
                    if tc_config[current_ae_datatype][translator_code]['code'] is not None:
                        if tc_config[current_ae_datatype][translator_code]['default']:
                            pass
                        else:
                            _not_default_translator = __format_input_translator(
                                tc_config[current_ae_datatype][translator_code]['code'])
                            if translator_value not in _not_default_translator:
                                status_list.append(5)
                            else:
                                pass
                else:
                    # check if specified translator finished with _SPE
                    if re.search('_SPE', translator_value):
                        __specific_trans = translator_value[: re.search('_SPE', translator_value).start()]
                        __lst_posi = __format_input_translator(tc_config[current_ae_datatype][translator_code]['code'])

                        if __specific_trans in __lst_posi:
                            pass
                        else:
                            status_list.append(5)

                    # check in case of a specified translator
                    elif tc_config[current_ae_datatype][translator_code]['code'] != translator_value:
                        status_list.append(5)
                #                     else:
                #                         status_list.append(1)
                if tc_config[current_ae_datatype][translator_code]['default']:
                    pass
    status_list.append(1)
    return status_list


def _ae_tc_as_dict(input_ae):
    ae_config = {}
    for key, value in lst_elt.items():
        if input_ae[key] not in ae_config.keys():
            ae_config[input_ae[key]] = {}
        for translator in value:
            ae_config[input_ae[key]][translator.split('secondary_')[-1].split('tertiary_')[-1]] = input_ae[translator]
    return ae_config


def _tc_as_dict(input_translator):
    translator_config = {}
    for key, value in lst_elt.items():
        if input_translator[key] not in translator_config.keys():
            translator_config[input_translator[key]] = {}
        for translator_code in value:
            translator_config[input_translator[key]][translator_code.split('secondary_')[-1].split('tertiary_')[-1]] = {
                'code': input_translator[translator_code + "_code"],
                'default': input_translator[translator_code + "_default"]}
    return translator_config


def _get_datatypes(input_dict):
    """
    Get the data type for given data, in our case, data type are the key, we return a set for avoiding double same type
    """
    return set(filter(None.__ne__, set(input_dict.keys())))


def _compare_version(x, y):
    """
    Test if x is greater taht y, if x or y is equal to *, then return True
    """
    if x == '*' or y == '*':
        return True
    return x > y


lst_elt = {'data_type': ['translator', 'image_translator'],
           'secondary_data_type': ['secondary_translator', 'secondary_image_translator'],
           'tertiary_data_type': ['tertiary_translator', 'tertiary_image_translator']}


def ae_translator_test(sess, ae):
    """
    Test a single ae
    :param sess: pass a db session
    :param ae: pass an ApplicationEntity orm object
    """
    if ae.device_type in ['RIS', 'PACS']:
        return 10

    ae_dict = ae.tojson()
    im = ae.integration_mode

    customer = get_last_customer_revision(sess, ae_dict['serial_number'])

    if not im:
        return 9

    # search of translator for this sdm and integration mode
    transconf = get_translatorconfig(sess, ae.sdm_key, im[0].integration_mode)

    # search with the optional ocr injection report for ftp mainly
    if transconf.count() == 0 and not im[0].integration_mode.count(" \u00B1 OCR Injection Report"):
        # check if integration is a FTP like connection
        if im[0].integration_mode[:3] == 'FTP' and not im[0].integration_mode == 'FTP':
            im_to_test = im[0].integration_mode[:-1] + " \u00B1 OCR Injection Report" + im[0].integration_mode[-1:]
        else:
            im_to_test = im[0].integration_mode + " \u00B1 OCR Injection Report"

        transconf = get_translatorconfig(sess, ae.sdm_key, im_to_test)

    # if we found some tc
    if transconf.count() != 0:
        ae_tc_cfg = _ae_tc_as_dict(ae_dict)
        # iter over all tc found
        _check_status_translator = []
        for elem in transconf:
            # compare criteria of lower dw version against ref of customer
            if not _compare_version(customer.dosewatch_version, elem.dosewatch_lower_version_bound):
                return 10

            tc_cfg = _tc_as_dict(elem.tojson())
            res = _compare_translator(ae_tc_cfg, tc_cfg)
            _check_status_translator.append(max(res))
        check_status_id = min(_check_status_translator, default=10)
    else:
        # we didn't found anything
        check_status_id = 10
    return check_status_id
