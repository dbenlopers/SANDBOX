# -*- coding: utf-8 -*-

from . import utilities

########################
#
# Innova log file check
#
########################


def innovalog_test(logger, data):
    """
    Checks if InnovaLogPull fails are within acceptance range.

    :param logger: logging.Logger instance
    :param data: an InnovaLogPull orm object as json
    :return: result dict with innovalog_id, status_id and rationale_id
    """

    fails = data['nb_fail'] or 0
    delta = (data['measure_date'] - data['datetime_last_pull']).days
    result = {'innova_log_id': data['id']}

    if delta > 7:
        status_id, rationale_id = (
            utilities.get_status_couple('NOK', 'CRITICAL') if fails > 5 else
            utilities.get_status_couple('OK', 'WARNING'))
    else:
        status_id, rationale_id = (
            utilities.get_status_couple('NOK', 'ERROR') if fails > 5 else
            utilities.get_status_couple('OK', 'NFF'))
    result.update({'status_id': status_id, 'rationale_id': rationale_id})
    return result
