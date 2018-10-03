# -*- coding: utf-8 -*-

import itertools
import re

from . import utilities

########################
#
# CT log file check
#
########################


def _im_mapping_ids_by_value(im_mapping):
    """
    Groups im ids by values.

    :param im_mapping: dict with integration mode id as key and supported file
    types list as value
    """
    associations = {}
    # Reverse dict to regroup similar im ids
    for k, v in im_mapping.items():
        associations.setdefault(hash(','.join(sorted(v))), []).append(k)
    return associations


def _get_im_id_by_supported_fts(fts, im_mapping):
    """
    Check if there is an exact match between im_mapping values and
    fts. If so, returns the associated im id.

    :param fts: list of supported file types of a ct log pattern (str)
    :param im_mapping: dict with integration mode id as key and supported file
    types list as value
    """
    im_associations = _im_mapping_ids_by_value(im_mapping)
    hash_key = hash(','.join(sorted(fts)))
    return (im_associations.get(hash_key)[0]
            if hash_key in im_associations else None)


def _get_integration_mode_associations(im_mapping):
    """
    Generates a dict returning for each im id the im id with approximately the
    same values.

    :param im_mapping: dict with integration mode id as key and supported file
    types list as value
    :return: dict with integration mode id as key and identical integration
    mode ids as value
    """

    clean_mapping = {k: {x for x in v if "±" not in x}
                     for k, v in im_mapping.items()}
    # Reverse dict to regroup similar im ids
    associations = _im_mapping_ids_by_value(clean_mapping)
    # Generate (im_mode_id, similar_im_modes) pairs
    assoc_by_key = list(itertools.chain.from_iterable(
        [[(im_id, im_assoc) for im_id in im_assoc] for im_assoc
         in associations.values()]))
    return dict(assoc_by_key)


def ct_log_pattern_test(logger, ct_log_pattern, im_mapping, known_im_assoc):
    """
    Process a ctlog pattern entry

    :param logger: logging.Logger instance
    :param ct_log_pattern: a CTLogPattern orm object as dict (x.tojson())
    :param im_mapping: a dict with integration mode id as keys and mode labels
    list as values
    :param known_im_assoc: a list of im ids for a specific ae
    :return: a CTLogPatternStatus orm object as dict
    """
    supported_fts = utilities.get_ctlog_supported_filetypes(ct_log_pattern)
    exact_match_im_id = _get_im_id_by_supported_fts(supported_fts, im_mapping)
    im_assoc_approximations = _get_integration_mode_associations(im_mapping)
    im_assoc = im_assoc_approximations.get(exact_match_im_id)

    result = {'ct_log_pattern_id': ct_log_pattern['id'],
              'infered_integration_mode_id': exact_match_im_id}

    # Files are mssing
    if ((0 in [ct_log_pattern['sum_image'], ct_log_pattern['sum_localizer'],
               ct_log_pattern['sum_screenshot']]) or ct_log_pattern['sum_sr']):
        status_id, rationale_id = utilities.get_status_couple(
            'NOK', 'CRITICAL')
    # Could not match exact integration mode
    elif exact_match_im_id is None:
        status_id, rationale_id = utilities.get_status_couple('NOK', 'ERROR')
    # Could not find associated im to this pattern in db
    elif not known_im_assoc:
        status_id, rationale_id = utilities.get_status_couple(
            'OK', 'ENHANCEMENT')
    # If known_im_id does not fit in im assoc approximations
    elif not set(im_assoc).isdisjoint(known_im_assoc):
        status_id, rationale_id = utilities.get_status_couple('OK', 'NFF')
    else:
        status_id, rationale_id = utilities.get_status_couple('OK', 'LIMITED')

    result.update({'status_id': status_id, 'rationale_id': rationale_id})
    return result

########################
#
# Pattern check
#
########################


RE_SPECIAL_MSG_PATTERN = re.compile('[^\(]*\(x.*')


def _is_mt_available(message_type, available_message_types):
    """
    Check if message_type is contained in available_message_types

    :param message_type: message type to match
    :param iterable: list of valid message patterns
    :return: return bool, and if true what has matched
    """
    for avmt in available_message_types:
        # if special message pattern, using a regex
        # i.e : DICOM-SR (x01)
        if RE_SPECIAL_MSG_PATTERN.match(message_type):
            regex = re.escape(avmt).replace('x', '\d').replace('± ', '')
            return re.match(regex, message_type) and True or False
        else:
            return message_type.replace('± ', '') == message_type
    return False


def _get_dicom_pattern_message_type(dicom_pattern):
    """
    Return expected message pattern for a given dicom_pattern
    with expected message type coming from integration mode
    :param dicom_pattern: Dicom Pattern orm object as json
    :return: expected message type as str
    """

    if dicom_pattern['message_type'] == 'MPPS':
        return "{0} {1}".format(
            dicom_pattern['message_type'],
            dicom_pattern['study_status'].replace(' ', '-'))
    if dicom_pattern['message_type'] == 'DICOM-SR':
        return "{0} ({1})".format(dicom_pattern['message_type'],
                                  dicom_pattern['series_number'])
    if dicom_pattern['message_type'] in ['DICOM-MWL', 'DICOM-RAW']:
        return dicom_pattern['message_type']


def _aggregate_message_types_by_dw_version(im_mapping):
    """
    Aggregate message types by dw_version for all im ids.

    :param im_mapping: See known_ae 'message_types' key in dicom_input_test
    :return: dict of aggregated mts for each dw version
    """
    aggregation = {}
    for _, subset in im_mapping.items():
        for dw_version, mts in subset.items():
            aggregation.setdefault(dw_version, []).extend([x[0] for x in mts])

    return {dw_v: set(mts) for dw_v, mts in aggregation.items()}


def _get_message_types_hashmap(logger, im_mapping):
    """
    Aggregate message types by dw_version for all im ids.

    :param im_mapping: See known_ae 'message_types' key in dicom_input_test
    i.e: {'8': {'1.2.2': [['DICOM-SR (502)', 17], ['DICOM-SR (1)', 15]]}}
    :return: dict of mt as key and mt id as value
    """
    hashmap = {}
    for ae_id, version_subsets in im_mapping.items():
        for version, subset in version_subsets.items():
            hashmap.update({mt: mt_id for mt, mt_id in subset})
    return hashmap


def _output_for_known_ae(logger, known_ae, dicom_input):
    """
    Generate test result for dicom_input_test. Use this when application entity
    is known.

    :param logger: logging.Logger instance
    :param known_ae: same dicom_input used in known_ae
    :param dicom_input: same dicom_input used in dicom_input_test
    :return: expected return of dicom_input_test
    """

    dicom_input_statuses = []
    dicom_patterns = dicom_input['dicom_patterns']

    if not dicom_patterns:
        return dicom_input_statuses

    message_types_per_im_ids = known_ae['message_types']
    message_types_per_dw_version = _aggregate_message_types_by_dw_version(
        message_types_per_im_ids)
    message_types_hashmap = _get_message_types_hashmap(
        logger, message_types_per_im_ids)
    expected_message_types = (message_types_per_dw_version[
        max(message_types_per_dw_version)] if message_types_per_dw_version
        else set())
    received_message_patterns = set()
    dw_version = known_ae['dw_version']

    for dicom_pattern in dicom_patterns:
        # Ignore DICOM-MWL file
        if dicom_pattern['message_type'] == 'DICOM-MWL':
            continue

        # MPPS DISCONTINUED status is considered as COMPLETED
        if dicom_pattern['study_status'] == 'DISCONTINUED':
            dicom_pattern['study_status'] == "COMPLETED"

        message_status = dicom_pattern['message_status']
        message_type = _get_dicom_pattern_message_type(dicom_pattern)

        if not message_type:
            return dicom_input_statuses

        # E-status considered as a major outage
        if message_status == 'E':
            status_id, rationale_id = utilities.get_status_couple(
                'NOK', 'CRITICAL')
            dicom_input_statuses.append({
                'dicom_input_id': dicom_input['id'],
                'dicom_pattern_id': dicom_pattern['id'],
                'message_pattern_id': None,
                'status_id': status_id, 'rationale_id': rationale_id})
            continue

        # No integration mode available
        elif not message_types_per_im_ids:
            status_id, rationale_id = utilities.get_status_couple(
                'NA', 'NOIM')
            dicom_input_statuses.append({
                'dicom_input_id': dicom_input['id'],
                'dicom_pattern_id': dicom_pattern['id'],
                'message_pattern_id': None,
                'status_id': status_id, 'rationale_id': rationale_id})
            continue
        # No expected messages for this AE/IMs/max DWV
        elif not expected_message_types:
            status_id, rationale_id = utilities.get_status_couple(
                'NA', 'CL_UNKNOWN')
            dicom_input_statuses.append({
                'dicom_input_id': dicom_input['id'],
                'dicom_pattern_id': dicom_pattern['id'],
                'message_pattern_id': None,
                'status_id': status_id, 'rationale_id': rationale_id})
            continue

        # If message_type is in expected mts and hashmap has a message pattern
        # id associated to this message_type
        if (_is_mt_available(message_type, expected_message_types) and
                message_types_hashmap.get(message_type)):
            status_id, rationale_id = utilities.get_status_couple('OK', 'NFF')
            dicom_input_statuses.append({
                'dicom_input_id': dicom_input['id'],
                'dicom_pattern_id': dicom_pattern['id'],
                'message_pattern_id': message_types_hashmap[message_type],
                'status_id': status_id, 'rationale_id': rationale_id})
            received_message_patterns.add(message_type)
        else:
            status_id, rationale_id = utilities.get_status_couple(
                'NOK', 'EXTRA')
            dicom_input_statuses.append({
                'dicom_input_id': dicom_input['id'],
                'dicom_pattern_id': dicom_pattern['id'],
                'message_pattern_id': None,
                'status_id': status_id, 'rationale_id': rationale_id})
            received_message_patterns.add(message_type)

    if message_types_per_im_ids and expected_message_types:
        # Determines if some mts were not received using set substraction
        not_received = expected_message_types - received_message_patterns
        for mt in not_received:
            # Skip this because it does not exist in Dicom Patterns
            # or odly formatted mts
            if (mt == 'Proprietary Logs') or (mt.startswith('±')):
                continue

            status_id, rationale_id = utilities.get_status_couple(
                'NOK', 'MISSING')
            dicom_input_statuses.append({
                'dicom_input_id': dicom_input['id'],
                'dicom_pattern_id': dicom_pattern['id'],
                'message_pattern_id': message_types_hashmap.get(message_type),
                'status_id': status_id, 'rationale_id': rationale_id})

    return dicom_input_statuses


def _output_for_unknown_ae(dicom_input, status='NA', rationale='AE_UNKNOWN'):
    """
    Generate test result for dicom_input_test. Use this when application entity
    is unknown.

    :param dicom_input: same dicom_input used in dicom_input_test
    :param status: wanted output for status (see __init__.py for
    available statuses)
    :param rationale: wanted output for rationale (see __init__.py for
    available rationales)
    :return: expected return of dicom_input_test
    """

    status_id, rationale_id = utilities.get_status_couple(status, rationale)
    return [{'dicom_input_id': dicom_input['id'], 'dicom_pattern_id': x['id'],
             'message_pattern_id': None, 'status_id': status_id,
             'rationale_id': rationale_id}
            for x in dicom_input['dicom_patterns']]


def dicom_input_test(logger, known_ae, dicom_input):
    """
    Run the dicom input test on dicom input passed in parameter

    :param logger: logging.Logger instance
    :param known_ae: AE associated to dicom_input using aet, orm object as
    json with an added message_types key (associated list of message type tuple
    (mt, message pattern id) for each integration mode id and supported DW
    versions of an AE) and dw_version key containing the latest DoseWatch
    version available for this ae serial number
    :param dicom_input: Dicom Input orm object as json with an added
    dicom_patterns key (associated dicom patterns as json)
    :return: list of Dicom Input Status as dictionaries
    """

    if not known_ae:
        return _output_for_unknown_ae(dicom_input)
    else:
        # If ae is a PACS/RIS Modality
        if known_ae['device_type'] in ['RIS', 'PACS']:
            if not dicom_input['station_name']:
                return _output_for_unknown_ae(dicom_input)
            known_ae = xxx
        return (_output_for_known_ae(logger, known_ae, dicom_input)
                if known_ae else _output_for_unknown_ae(dicom_input))

########################
#
# Translator config check
#
########################


_, RATIONALE_CL_UK_ID = utilities.get_status_couple('OK', 'CL_UNKNOWN')
_, RATIONALE_NOIM_ID = utilities.get_status_couple('OK', 'NOIM')
_, RATIONALE_ERROR_ID = utilities.get_status_couple('OK', 'ERROR')
_, RATIONALE_NFF_ID = utilities.get_status_couple('OK', 'NFF')

FTP_LIKE_INT_MODE_RE = re.compile('FTP\s?\(([^\)]*)\)')
MAPPING_TRANSLATOR = {
    'data_type': ['translator', 'image_translator'],
    'secondary_data_type': [
        'secondary_translator', 'secondary_image_translator'],
    'tertiary_data_type': ['tertiary_translator', 'tertiary_image_translator']}


def _is_version_higher_than(x, y):
    """
    Check if x is higher than y. If one of them is '*', returns True.
    Keep in mind that it compares strings and not actual numbers.

    :param x: str, i.e: 2.3.1
    :param y: str, i.e: 2.3.1
    :return: bool
    """
    return ('*' in [x, y] or x > y) if y else True


def _sanitize_key(key):
    """
    Sanitizer for keys starting with secondary or tertiary

    :param key: str
    :return: str
    """
    return key.replace('secondary_', '').replace('tertiary_', '')


def _get_ae_translator_config(ae):
    """
    Get translator configuration for an AE using MAPPING_TRANSLATOR dict
    format

    :param ae: an AE object as described in ae_translator_test
    :return: based on MAPPING_TRANSLATOR, {
        'data_type': {'translator': 'value', 'image_translator': 'value'},
        'secondary_data_type': {
            'translator': 'value', 'image_translator': 'value'},
        'tertiary_data_type': {
            'translator': 'value', 'image_translator': 'value'}
    }
    """
    return {k: {_sanitize_key(x): ae.get(x) for x in translators}
            for k, translators in MAPPING_TRANSLATOR.items()}


def _get_translator_config(translator_config):
    """
    Get translator configuration for a TranslatorConfig object using
    MAPPING_TRANSLATOR dict format

    :param translator_config: an ORM translator config object as json
    :return: based on MAPPING_TRANSLATOR, {
        'data_type': {'translator': {'code': 'value', 'default': 'value'},
                      'image_translator': {'code': 'value', 'default': 'value'}
        },
        'secondary_data_type': {
            'translator': {'code': 'value', 'default': 'value'},
            'image_translator': {'code': 'value', 'default': 'value'}
        },
        'tertiary_data_type': {
            'translator': {'code': 'value', 'default': 'value'},
            'image_translator': {'code': 'value', 'default': 'value'}
        }
    }
    """
    return {k: {_sanitize_key(x): {
        'code': translator_config.get('%s_code' % x),
        'default': translator_config.get('%s_default' % x)
    } for x in translators}
        for k, translators in MAPPING_TRANSLATOR.items()}


def _tokenize_translator_code(ts_code):
    """
    Splits the translator code into subitems, using '/' as separator.
    The 'version' of the translator is removed, i.e:
    'SR_999_CT_GENERIC (5) / SR_997_CT_GENERIC (4)' becomes
    ['SR_999_CT_GENERIC', 'SR_997_CT_GENERIC'].

    :param ts_code: str, the content of a translator_code-like column for a
    TranslatorConfig object
    :return: list of strings
    """
    return [x.strip() for x in re.sub('\(\w*\)', '', ts_code).split('/')]


def _cmp_ae_config_to_translator(ae_tl_config, tl_config):
    """
    Compares the AE translator config to a translator config

    :param ae_tl_config: Output of _get_ae_translator_config
    :param tl_config:  Output of _get_translator_config
    :return: rationale id (see __init__.py)
    """
    for datatype, config in ae_tl_config.items():
        for translator_type, value in config.items():
            raw_code = tl_config[datatype][translator_type]['code']
            code = raw_code if isinstance(raw_code, str) else str(code)
            default = tl_config[datatype][translator_type]['default']
            if not value:
                if code and not default:
                    if value not in _tokenize_translator_code(code):
                        return RATIONALE_ERROR_ID
            else:
                # Checks if this is a specific translator
                # Specific translators have the same name of their parent
                # with _SPE added at the end
                value = value.strip()  # just in case
                if value.endswith('_SPE'):
                    specific_tl = re.sub('_SPE$', '', value)
                    if specific_tl not in _tokenize_translator_code(code):
                        return RATIONALE_ERROR_ID
                # Check consistency between expected and configured value
                elif code != value:
                    return RATIONALE_ERROR_ID
    return RATIONALE_NFF_ID


def ae_translator_test(logger, ae):
    """
    Checks config for an application entity

    :param logger: logging.Logger instance
    :param ae: an ApplicationEntity orm object as json with an added key
    integration_mode as an IM ORM object linked to the AE and dw_version key
    containing the latest DoseWatch version available for this ae serial number
    and key translator_config containing the list of TranslatorConfig orm
    objects as json for the first AE's IM's integration_mode
    :return:
    """
    if ae['device_type'] in ['RIS', 'PACS']:
        return {'ae_id': ae['id'], 'rationale_id': RATIONALE_CL_UK_ID}

    integration_mode = ae.pop('integration_mode')
    dw_version = ae.pop('dw_version')
    translator_configurations = ae.pop('translator_configurations')

    if not integration_mode:
        return {'ae_id': ae['id'], 'rationale_id': RATIONALE_NOIM_ID}

    tc_statuses = []
    if translator_configurations:
        ae_translator_config = _get_ae_translator_config(ae)
        for tc in translator_configurations:
            if not _is_version_higher_than(
                    dw_version, tc['dosewatch_lower_version_bound']):
                return {'ae_id': ae['id'], 'rationale_id': RATIONALE_CL_UK_ID}
            translator_config = _get_translator_config(tc)
            tc_statuses.append(_cmp_ae_config_to_translator(
                ae_translator_config, translator_config))
        # Return lowest status returned by comparator, meaning that if at least
        # one translator was properly configured the test will result in an
        # NFF status
        return {'ae_id': ae['id'], 'rationale_id': min(tc_statuses)}
    else:
        return {'ae_id': ae['id'], 'rationale_id': RATIONALE_CL_UK_ID}
