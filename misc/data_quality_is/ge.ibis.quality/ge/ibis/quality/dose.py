# -*- coding: utf-8 -*-

from . import utilities

CATEGORY = 'Dosimetric'


def _below_dose_mitigation(expected_study_dose, cumulative_series_dose):
    """
    Mitigate test result when study dose is below cumulative dose.
    Sometimes, rounding values makes them inferior to cumulative dose while
    being fairly close.

    :param expected_study_dose: dose for study
    :param cumulative_series_dose: Σ of series dose
    :return: tuple(bool, int, int) being test result, status_id
    and rationale_id
    """
    passed = True
    # Acceptance margin for decimal dose
    if utilities.decimal(expected_study_dose, cumulative_series_dose, 0.1):
        status_id, rationale_id = utilities.get_status_couple('OK', 'NFF')
    # Acceptance margin for relative dose
    elif utilities.relative(expected_study_dose, cumulative_series_dose, 0.01):
        status_id, rationale_id = utilities.get_status_couple('OK', 'WARNING')
    # Acceptance margins exceeded
    else:
        passed = False
        status_id, rationale_id = utilities.get_status_couple(
            'NOK', 'NONSENSE')
    return (passed, status_id, rationale_id)


def _dose_test(config, method, expected_study_dose, cumulative_series_dose):
    """
    Run actual dose test using comparison method.

    :param config: test configuration coming from rules (see rules.json)
    :param method: func a b t -> bool with a, b, t being study dose,
    cumulative serie dose and tolerance
    :param expected_study_dose: dose for study
    :param cumulative_series_dose: Σ of series dose
    :return: tuple(bool, int, int) being test result, status_id
    and rationale_id
    """
    if not config:
        raise ValueError('Unknown configuration queried')
    threshold = config['thres']
    passed = method(expected_study_dose, cumulative_series_dose,
                    threshold)
    status_id, rationale_id = utilities.get_status_couple(
        *config['fail_rule'])

    if 'low_dose' in config:
        low_dose_passed = expected_study_dose < config['low_dose']
        if passed and low_dose_passed:
            status_id, rationale_id = utilities.get_status_couple(
                *config['low_dose_rule'])
        elif (not passed and low_dose_passed and
              'low_dose_mitigate_rule' in config):
            status_id, rationale_id = utilities.get_status_couple(
                *config['low_dose_mitigate_rule'])
    return passed, status_id, rationale_id


def _dose_quality(expected_study_dose, cumulative_series_dose,
                  variant='default'):
    """
    Check if difference between cumulative serie dose et expected study dose
    is within acceptance range.

    :param expected_study_dose: dose for study
    :param cumulative_series_dose: Σ of series dose
    :param variant: rule variant to use
    :return: tuple(bool, int, int) being test result,
    status_id and rationale_id
    """
    if expected_study_dose < cumulative_series_dose:
        return _below_dose_mitigation(
            expected_study_dose, cumulative_series_dose)

    rule = utilities.get_rule(CATEGORY, variant=variant).get('equality')
    passed = True
    if 'rel_tol' in rule:
        config = rule.get('rel_tol')
        passed, status_id, rationale_id = _dose_test(
            config, utilities.relative, expected_study_dose,
            cumulative_series_dose)

    if passed and 'dec_tol' in rule:
        config = rule.get('dec_tol')
        passed, status_id, rationale_id = _dose_test(
            config, utilities.decimal, expected_study_dose,
            cumulative_series_dose)

    return (passed, status_id, rationale_id)


def _dosimetric_quality(study, kpi):
    """
    Run dose_quality test for a given kpi

    :param study: a Study ORM object as json
    :param kpi: kpi used to run the test
    :return: dict with study_id, type (kpi), passed, status_id, rationale_id
    and value (dose difference between study and series dose)
    """
    data = study['data']
    expected_study_dose = data[kpi] or 0
    cumulative_series_dose = data['%s_test' % kpi] or 0

    result = {'study_id': study['id'], 'type': kpi, 'passed': True}
    diff = round(expected_study_dose - cumulative_series_dose, 2)

    if expected_study_dose and cumulative_series_dose:
        passed, status_id, rationale_id = _dose_quality(
            expected_study_dose, cumulative_series_dose, variant=kpi)
    elif not expected_study_dose and cumulative_series_dose:
        status_id, rationale_id, passed = (utilities.get_status_couple(
            'NOK', 'CRITICAL') + (False,))
    elif expected_study_dose and not cumulative_series_dose:
        status_id, rationale_id, passed = (utilities.get_status_couple(
            'OK', 'ENHANCEMENT') + (True,))
    elif not expected_study_dose and not cumulative_series_dose:
        status_id, rationale_id, passed = (
            utilities.get_status_couple('OK', 'WARNING') + (True,))
    result.update({'status_id': status_id, 'rationale_id': rationale_id,
                   'value': diff, 'passed': passed})
    return result


def _localizers_dlp_quality(study, kpi, threshold,
                            localizers_key='num_localizers_value'):
    """
    Check if mean dlp per localizer is within acceptance range. Only
    available for CT.

    :param study: a Study ORM object as json
    :param kpi: kpi used to run the test
    :param threshold: threshold used for acceptance
    :param localizer_key: key in 'data' dict pointing to the number of
    localizers
    :return: dict with study_id, type (kpi), passed, status_id, rationale_id
    and value (nb of localizers)
    """
    data = study['data']
    expected_study_dose = data[kpi] or 0
    cumulative_series_dose = data['%s_test' % kpi] or 0

    nb_localizers = data[localizers_key]
    dlp_per_loc = (((expected_study_dose - cumulative_series_dose) /
                    nb_localizers) if
                   nb_localizers else 0)
    result = {'study_id': study['id'], 'type': 'dlp_localizer',
              'value': nb_localizers}

    passed = True

    if expected_study_dose == cumulative_series_dose:
        status_id, rationale_id = utilities.get_status_couple('OK', 'NFF')
    else:
        if nb_localizers == 0:
            status_id, rationale_id = utilities.get_status_couple(
                'OK', 'WARNING')
        else:
            if dlp_per_loc < threshold:
                status_id, rationale_id = utilities.get_status_couple(
                    'OK', 'NFF')
            else:
                status_id, rationale_id, passed = (utilities.get_status_couple(
                    'NOK', 'WARNING') + (False,))
    result.update({'status_id': status_id,
                   'rationale_id': rationale_id, 'passed': passed})
    return result

###########################
#
# Meta tests
#
###########################


LOCALIZERS_CONFIG = utilities.get_rule(CATEGORY, variant='CT_localizers_value')
LOCALIZERS_THRESHOLD = LOCALIZERS_CONFIG.get('threshold')


def dosimetric_test(logger, study):
    """
    Run the dosimetric consistency processing on consolidated data.

    :param logger: logging.Logger instance
    :param study: a Study ORM object as json
    :return: list of dosimetric object results
    """
    results = []
    data = study.get('data', {})
    # Creates a set
    kpis = {x.replace('_test', '') for x in data.keys()}
    kpis.discard('num_localizers_value')
    results.extend(list(map(lambda x: _dosimetric_quality(study, x), kpis)))
    if study['type'] == 'CT':
        results.append(_localizers_dlp_quality(
            study, 'total_dlp', LOCALIZERS_THRESHOLD))

    return results
