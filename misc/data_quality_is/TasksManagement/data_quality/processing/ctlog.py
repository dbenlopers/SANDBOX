# -*- coding: utf-8 -*-

from __future__ import absolute_import
from data_quality.requests.db import get_in_mode_for_ae
from data_quality.processing.status_mapping import rational_mapping, status_mapping


mapping_ctlogp = {"sum_exam_proto": "EXAM_PROTO",
                  "sum_image": "IMAGE",
                  "sum_localizer": "LOCALIZER",
                  "sum_rdsr": "RDSR",
                  "sum_scan_request": "SCAN_REQUEST",
                  "sum_screenshot": "SCREENSHOT",
                  "sum_screenshot_contrast": "± DICOM-SR (996)"}


def _compute_equivalent_integration_mode(messagepattern_by_im_id):
    """
    From the dict (key, im id: value, set of message patter) & compute/search integration mode that are equivalent
    :param messagepattern_by_im_id:
    :return:
    """
    messagepattern_by_im_id_clear = messagepattern_by_im_id
    # remove optional content
    for key, value in messagepattern_by_im_id_clear.items():
        messagepattern_by_im_id_clear[key] = {x for x in value if not "±" in x}

    im_equ = {key: [] for key in messagepattern_by_im_id_clear.keys()}

    # Construct a dict where you get equivalent integration mode
    for im in messagepattern_by_im_id_clear.keys():
        for key, value in messagepattern_by_im_id_clear.items():
            if messagepattern_by_im_id_clear[im] == value:
                im_equ[im].append(key)
    return im_equ


# Messagepattern_by_im_id = get_ctlog_integration_mode(db_session)
# im_equ = _compute_equivalent_integration_mode(Messagepattern_by_im_id)


def __ctlog_pattern_construct_im(input):
    """
    From ctlog json, construct an integration mode
    :param input:
    :return:
    """
    _contained = []
    for k, v in mapping_ctlogp.items():
        if input[k] != 0:
            _contained.append(v)
    return _contained


def __ctlog_pattern_infering_connection_mode(lst_mp, im_mapping):
    """
    For ctlog pattern, with input data, try to infere the connection mode
    :param lst_mp: list of message pattern received to test against im_mapping
    :param im_mapping:
    :return:
    """
    for k, v in im_mapping.items():
        if set(v) == set(lst_mp):
            return k


def ctlogpattern_test(db_session, ctlogpattern, im_mapping):
    """
    Process a ctlog pattern entrie
    :param db_session: db session
    :param im_mapping: dict that contain key as integration mode id and value all message pattern for this im
    :param ctlogpattern: dict repr of ctlogpattern
    :return: return a dict that repr ctlogpatternstatus
    """

    im_eq = _compute_equivalent_integration_mode(im_mapping)

    __infered_im_id = __ctlog_pattern_infering_connection_mode(__ctlog_pattern_construct_im(ctlogpattern), im_mapping)
    if ctlogpattern['sum_image'] == 0 or ctlogpattern['sum_localizer'] == 0 or ctlogpattern['sum_screenshot'] == 0 \
            or ctlogpattern['sum_sr'] != 0:
        return {"ctlogpattern_id": ctlogpattern['id'],
                "status_id": status_mapping['NOK'], "rational_id": rational_mapping['CRITICAL'],
                "infered_integrationmode_id": __infered_im_id}

    if __infered_im_id is None:
        return {"ctlogpattern_id": ctlogpattern['id'],
                "status_id": status_mapping['NOK'], "rational_id": rational_mapping['ERROR'],
                "infered_integrationmode_id": __infered_im_id}

    # get integration mode specified in the connectivity list for this ae
    __know_im_id = get_in_mode_for_ae(sess=db_session,
                                      serial_number=ctlogpattern['serial_number'],
                                      aet=ctlogpattern['aet'])

    # If we get some infered im but im is not define
    if __know_im_id is None:
        return {"ctlogpattern_id": ctlogpattern['id'],
                "status_id": status_mapping['OK'], "rational_id": rational_mapping['ENHANCEMENT'],
                "infered_integrationmode_id": __infered_im_id}

    if not set(im_eq[__infered_im_id]).isdisjoint(__know_im_id):
        return {"ctlogpattern_id": ctlogpattern['id'],
                "status_id": status_mapping['OK'], "rational_id": rational_mapping['NFF'],
                "infered_integrationmode_id": __infered_im_id}
    else:
        return {"ctlogpattern_id": ctlogpattern['id'],
                "status_id": status_mapping['OK'], "rational_id": rational_mapping['LIMITED'],
                "infered_integrationmode_id": __infered_im_id}
