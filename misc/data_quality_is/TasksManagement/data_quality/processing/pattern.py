# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re

from celery.utils.log import get_task_logger

from data_quality.processing.status_mapping import (rational_mapping,
                                                    status_mapping)
from data_quality.requests.db import (get_ae, get_ae_behind_pacs,
                                      get_dw_version, get_expectedmessagetype,
                                      get_messagepattern_dict)

logger = get_task_logger(__name__)


def _search_match_from_list(to_match, iterable):
    """
    Search the to_match param with list of valid_message_type by constructing regex
    :param to_match: string to match
    :param iterable: list of valid message pattern, iterate over them and construct regex with them
    to match to to_match parameter
    :return: return bool, and if true what has matched
    """
    for message_type in iterable:
        # if 'x' is contained -> regex
        if 'x' in message_type:
            # construct from each elem in iterable, a regex pattern where 'x' 
            # are replace by '\d' for matching all digit
            regex = "{}".format(message_type.replace(
                '(', '\(').replace(')', '\)').replace('x', '\d').replace('± ', ''))
            pattern = re.compile(regex)
            if pattern.match(to_match):
                return True, message_type
        else:
            if message_type.replace('± ', '') == to_match:
                return True, message_type
    return False, None


def _fromdicompattern_get_messagetypes_set(dicompattern):
    """
    From a dicominput row, construct a set that contain in formatted way, all 
    message received, that can be compare
    with expected message type coming from integration mode
    :param dicompattern: dicom pattern in json format
    :return:
    """

    if dicompattern['message_type'] == 'MPPS':
        return "{0} {1}".format(dicompattern['message_type'],
                             dicompattern['study_status'].replace(" ", "-"))
    if dicompattern['message_type'] == 'DICOM-SR':
        return "{0} ({1})".format(dicompattern['message_type'], 
                                    dicompattern['series_number'])
    if dicompattern['message_type'] in ['DICOM-MWL', 'DICOM-RAW']:
        return dicompattern['message_type']


def _process_dicominput(sess, dicominput, ae):
    """
    Process a dicom input with im specified in ae, check if dicom pattern are 
    valid by checking in connectivity list
    :param dicominput: dicom input to process
    :param ae: ae for this dicom input
    :return:
    """
    # list for saving data from results test
    dicominput_status = []
    # list of dicom pattern in json format
    received_dicompatterns = [x.dicompattern.tojson()
                              for x in dicominput.dicom_patterns]

    # if not dicom were received, return empty list
    if len(received_dicompatterns) == 0:
        return dicominput_status

    received_messagepatterns = set()
    # get current version of dw
    dw_v = get_dw_version(sess, ae.serial_number)

    # list of integration mode id if available
    integrationmode_ids = [im.id for im in ae.integration_mode]

    # get the hashmap where key is message pattern and value the id
    hashmap_messagepattern_id = get_messagepattern_dict(sess)

    expected_messagetypes = get_expectedmessagetype(sess=sess,
                                                    sdm_key=ae.sdm_key,
                                                    im_id=integrationmode_ids)

    # iterate over all dicom pattern receive for this dicom input
    for current_dicompattern in received_dicompatterns:
        
        # Filter DICOM-MWL file
        if current_dicompattern['message_type'] == 'DICOM-MWL':
            continue

        # If we received a MPPS DISCONTINUED, we consider it as a COMPLETED
        if current_dicompattern['study_status'] == 'DISCONTINUED':
            current_dicompattern['study_status'] == "COMPLETED"

        _current_message_status = current_dicompattern['message_status']

        # sometime, this will fail with older probe data
        try:
            current_messagetype = _fromdicompattern_get_messagetypes_set(
                current_dicompattern)
        except:
            return dicominput_status

        # Considering E-status as a major outage
        if _current_message_status == 'E':
            dicominput_status.append({"dicominput_id": dicominput.id,
                                      "dicompattern_id": current_dicompattern['id'],
                                      "messagepattern_id": None,
                                      "status_id": status_mapping['NOK'],
                                      "rational_id": rational_mapping['CRITICAL']})
            continue

        # No integration mode available
        if len(integrationmode_ids) == 0:
            dicominput_status.append({"dicominput_id": dicominput.id,
                                      "dicompattern_id": current_dicompattern['id'],
                                      "messagepattern_id": None,
                                      "status_id": status_mapping['NA'],
                                      "rational_id": rational_mapping['NOIM']})
            continue

        # No expected message retrieve for this AE/IM/DWV
        if len(expected_messagetypes) == 0:
            dicominput_status.append({"dicominput_id": dicominput.id,
                                      "dicompattern_id": current_dicompattern['id'],
                                      "messagepattern_id": None,
                                      "status_id": status_mapping['NA'],
                                      "rational_id": rational_mapping['CL_UNKNOWN']})
            continue

        # search if message pattern are in expected message type
        testbool, mpfound = _search_match_from_list(
            current_messagetype, expected_messagetypes)

        if testbool:
            # the dicom pattern are found from connectivity list possibilities
            dicominput_status.append({"dicominput_id": dicominput.id,
                                      "dicompattern_id": current_dicompattern['id'],
                                      "messagepattern_id": hashmap_messagepattern_id[mpfound],
                                      "status_id": status_mapping['OK'],
                                      "rational_id": rational_mapping['NFF']})
            received_messagepatterns.add(mpfound)
        else:
            dicominput_status.append({"dicominput_id": dicominput.id,
                                      "dicompattern_id": current_dicompattern['id'],
                                      "messagepattern_id": None,
                                      "status_id": status_mapping['NOK'],
                                      "rational_id": rational_mapping['EXTRA']})
            received_messagepatterns.add(mpfound)

    if len(integrationmode_ids) != 0 and len(expected_messagetypes) != 0:
        # research not received
        not_received = expected_messagetypes - received_messagepatterns
        for single_not_received in not_received:
            # skip this because not found in dicom pattern
            if single_not_received == 'Proprietary Logs':
                continue
                # skip them because they are optional
            if single_not_received.startswith('±'):
                continue
            dicominput_status.append({"dicominput_id": dicominput.id,
                                      "dicompattern_id": None,
                                      "messagepattern_id": hashmap_messagepattern_id[single_not_received],
                                      "status_id": status_mapping['NOK'],
                                      "rational_id": rational_mapping['MISSING']})
    return dicominput_status


def _generate_data_for_unknow_ae(dicominput, status='NA', rational='AE_UNKNOWN'):
    """
    Return a dict for dicom_input where the AE is unknown
    :param dicominput:
    :param status: which status to set
    :param rational: which rational statement to set
    :return:
    """
    return [{"dicominput_id": dicominput.id,
             "dicompattern_id": dicom_pattern['id'],
             "messagepattern_id": None,
             "status_id": status_mapping[status],
             "rational_id": rational_mapping[rational]} for dicom_pattern in
            [x.dicompattern.tojson() for x in dicominput.dicom_patterns]]


def dicominput_test(sess, dicominput):
    """
    Run the dicom input test on dicom input passed in parameter
    :param sess: db session
    :param dicominput: dicom input orm object
    :return: test result in json format
    """
    # Search for ae data linked to dicom input
    ae = get_ae(sess, dicominput.serial_number, aet=dicominput.aet)

    # If no ae is linked to dicom input, we generated AE_UNKNOWN output, else test are performed
    if ae is not None:
        # If ae is a PACS/RIS, search for ae with SN & station_name (if station_name are available)
        # if we enter is case ae == PACS/RIS and station_name == None, nothing is produced
        if ae.device_type in ['RIS', 'PACS']:
            if dicominput.station_name is not None:
                ae = get_ae_behind_pacs(sess, dicominput.serial_number,
                                        station_name=dicominput.station_name)
            else:
                return _generate_data_for_unknow_ae(dicominput)
        if ae is None:  # In case of searching ae with station_name result by None
            return _generate_data_for_unknow_ae(dicominput)
        try:
            return _process_dicominput(sess, dicominput, ae)
        except Exception as e:
            logger.error("Error catched in dicominput_test  : {}".format(e))
    else:
        return _generate_data_for_unknow_ae(dicominput)
