# coding=utf-8
"""
All functions that retrieve data from database, update status
"""
from celery.utils.log import get_task_logger
from sqlalchemy import update

from data_quality.persistence.orm import (ApplicationEntity, ConnectivityList,
                                          CTLogPattern, Customer, DicomInput,
                                          InnovaLogPull, IntegrationMode,
                                          IntegrationModeMessageTypes,
                                          MessagePattern, Study,
                                          TranslatorConfig)

logger = get_task_logger(__name__)


def update_study_status(sess, list_ids, status):
    """
    Update the status of study row(s)
    :param sess: db session
    :param list_ids: id of study to update
    :param status: status to set
    :return:
    """
    stmt = update(Study).where(Study.id.in_(list_ids)).values(status=status)
    sess.execute(stmt)


def update_ae_status(sess, list_ids, status):
    """
    Update the status of ae row(s)
    :param sess:
    :param list_ids:
    :param status:
    :return:
    """
    stmt = update(ApplicationEntity).where(
        ApplicationEntity.id.in_(list_ids)).values(status=status)
    sess.execute(stmt)


def get_study_by_id(sess, list_ids):
    """
    get study by id
    :param sess: db session
    :param list_ids: list of ids
    :return: list of dict
    """
    lst = [item.tojson() for item in sess.query(
        Study).filter(Study.id.in_(list_ids))]
    return lst


def update_innovalogpull_status(sess, list_ids, status):
    """
    Update status of innovalog pull row(s)
    :param sess: db session
    :param list_ids: id of innovalog pull, single or list
    :param status: status to set
    :return:
    """
    stmt = update(InnovaLogPull).where(
        InnovaLogPull.id.in_(list_ids)).values(status=status)
    sess.execute(stmt)


def get_innovalogpull_by_id(sess, list_ids):
    """
    get innovalog pull by id
    :param sess: db session
    :param list_ids:
    :return:
    """
    lst = [item.tojson() for item in sess.query(
        InnovaLogPull).filter(InnovaLogPull.id.in_(list_ids))]
    return lst


def update_ctlogpattern_status(sess, list_ids, status):
    """
    Update status of ctlog pattern row(s)
    :param sess: db session
    :param list_ids: id of ctlog pattern, single or list
    :param status: status to set
    :return:
    """
    stmt = update(CTLogPattern).where(
        CTLogPattern.id.in_(list_ids)).values(status=status)
    sess.execute(stmt)


def get_ctlogpattern_by_id(sess, list_ids):
    """
    Get ctlogpattern
    :param sess: db session
    :param list_ids:
    :return: list of ctlogpattern
    """
    lst = [item.tojson() for item in sess.query(
        CTLogPattern).filter(CTLogPattern.id.in_(list_ids))]
    return lst


def get_ctlog_integration_mode(sess):
    """
    get integration mode for ctlog, they contain FTP in the name
    :param sess: db session
    :return:
    """
    im_id_for_ctlog = [x for x, in sess.query(IntegrationMode.id).filter(
        IntegrationMode.integration_mode.ilike('FTP%'))]
    messagepattern_by_im_id = {x: get_expectedmessagetype_for_intemode(
        sess, x) for x in im_id_for_ctlog}
    return messagepattern_by_im_id


def get_valid_ctlog_in(sess):
    """
    return valide ftp integration mode specific for ct log
    :param sess:
    :return:
    """
    return [x for x, in sess.query(IntegrationMode.id).filter(
        IntegrationMode.integration_mode.ilike('FTP%'))]


def update_dicominput_status(sess, list_ids, status):
    """
    Update status of dicom input row(s)
    :param sess: db session
    :param list_ids: id of dicom input, single or list
    :param status: status to set
    :return: list with id
    """
    try:
        stmt = update(DicomInput).where(
            DicomInput.id.in_(list_ids)).values(status=status)
        sess.execute(stmt)
        sess.commit()
    except Exception as e:
        sess.rollback()
        logger.error(": {}".format(e))


def get_dicominput_by_id(sess, list_ids):
    """
    Get dicom input by given id
    :param sess: db session
    :param list_ids:
    :return: list of dicominput in json
    """
    lst = [item for item in sess.query(
        DicomInput).filter(DicomInput.id.in_(list_ids))]
    return lst


########################################################################################
# More specific function that requests db, for logic test
########################################################################################


def get_dw_version(sess, serial_number):
    """
    Get DoseWatch version from customer by serial number (last entry)
    :param sess: db session
    :param serial_number: serial number of customer
    :return: dw version
    """
    return get_last_customer_revision(sess, serial_number).dosewatch_version


def get_ae(sess, serial_number, ae_id=None, aet=None):
    """
    Return last updated ae entrie for specified serial_number and aet or ae_id
    :param sess: db session
    :param serial_number: serial_number of customer
    :param ae_id: if given, get ae by local ae id
    :param aet: if given, get ae by aet
    :return: return ae orm object
    """
    query = sess.query(ApplicationEntity).filter(ApplicationEntity.serial_number == serial_number,
                                                 ApplicationEntity.is_last == True)
    if ae_id is not None:
        query = query.filter(ApplicationEntity.local_ae_id == ae_id)

    if aet is not None:
        query = query.filter(ApplicationEntity.aet == aet)

    return query.scalar()


def get_ae_behind_pacs(sess, serial_number, station_name):
    """
    Return last updated ae entrie for specified serial_number and station_name
    :param sess: db session
    :param serial_number: serial_number of customer
    :param station_name: station_name to search
    :return: return ae orm object
    """
    query = sess.query(ApplicationEntity).filter(ApplicationEntity.serial_number == serial_number,
                                                 ApplicationEntity.station_name == station_name,
                                                 ApplicationEntity.is_last == True)
    return query.scalar()


def get_aes(sess, ids):
    """
    Retrieve a list of ae by id
    :param sess:
    :param ids:
    :return:
    """
    return sess.query(ApplicationEntity).filter(ApplicationEntity.id.in_(ids))


def get_in_mode_for_ae(sess, serial_number, ae_id=None, aet=None, ae=None):
    """
    Get all integration mode for device, search information from connectivity list
    you can query with local_ae_id or aet
    :param sess: db session
    :param serial_number: serial_number of client
    :param ae_id: id of customer ae
    :param aet: aet of device
    :param ae: ae orm object
    :return: list of integration mode id from connectivity list, or None if empty
    """
    if ae_id is None and aet is None and ae is None:
        return None

    dw_v = get_dw_version(sess, serial_number)

    ae = get_ae(sess=sess, serial_number=serial_number,
                ae_id=ae_id, aet=aet) if ae is None else ae
    if ae is None:
        return None

    _device_soft_vers = ae.software_version if ae.software_version is not None else '*'

    clim = sess.query(ConnectivityList).filter(ConnectivityList.supported_device_id == ae.sdm_key,
                                               ConnectivityList.dosewatch_version.ilike(
                                                   dw_v[:3] + '%'),
                                               ConnectivityList.device_version.ilike(
                                                   '%' + _device_soft_vers + '%'))
    # if with version we found no possible integration mode, then try with fallback mode (*)
    if clim.count() == 0:
        clim = sess.query(ConnectivityList).filter(ConnectivityList.supported_device_id == ae.sdm_key,
                                                   ConnectivityList.dosewatch_version.ilike(
                                                       dw_v[:3] + '%'),
                                                   ConnectivityList.device_version.ilike('%*%'))

    lst_im_cl = [cl.integration_mode_id for cl in clim]
    return lst_im_cl


def get_expectedmessagetype_for_intemode(sess, im_id):
    """
    Get all expected message from one integration mode
    :param sess: db session
    :param im_id: id of integration mode
    :return: list of str
    """
    expected_message_type = sess.query(IntegrationModeMessageTypes.message_type).filter(
        IntegrationModeMessageTypes.im_id == im_id).distinct()
    return {elem for elem, in expected_message_type}


def get_expectedmessagetype(sess, sdm_key, im_id):
    """
    Get all expected message type possibilities into a set (avoid double)
    If for one sdm and list of integration mode, we have multiple possibilities
    of dw version, we choose the higher
    :param sess: db session
    :param sdm_key: sdm key of device
    :param im_id: list of integration mode id if available
    :return:
    """
    query = sess.query(IntegrationModeMessageTypes).filter(IntegrationModeMessageTypes.sdm_key == sdm_key,
                                                           IntegrationModeMessageTypes.im_id.in_(im_id))

    dict_x = {}
    for elem in query:
        dict_x.setdefault(elem.dw_v, []).append(elem.message_type)
    
    return set(dict_x[max(dict_x)]) if len(dict_x) != 0 else set()


def get_messagepattern_dict(sess):
    """
    Get as hashmap message pattern as key and message pattern id as value
    :param sess: db session
    :return:
    """
    return {elem.message_type: elem.id for elem in sess.query(MessagePattern)}


def get_last_customer_revision(sess, serial_number):
    """
    Retrieve last customer
    :param sess:
    :param serial_number:
    :return:
    """
    return sess.query(Customer).filter(Customer.serial_number == serial_number,
                                       Customer.is_last == 1).scalar()


def get_translatorconfig(sess, sdm_key, integration_mode):
    """
    Retrieve translator config if found
    :param sess:
    :param sdm_key:
    :param integration_mode:
    :return:
    """
    return sess.query(TranslatorConfig).filter(TranslatorConfig.sdm_key == sdm_key,
                                               TranslatorConfig.integration_mode == integration_mode)
