# -*- coding: utf-8 -*-
"""
All periodic processing are define here
"""
from datetime import datetime, timedelta

import requests
import requests.packages.urllib3.exceptions
from bson.json_util import dumps, loads
from celery.utils.log import get_task_logger
from sqlalchemy import func

from data_quality.celery import app
from data_quality.celeryconfig import cfg_parser
from data_quality.persistence.orm import (ApplicationEntity, CTLogPattern,
                                          Customer, DicomInput, InnovaLogPull,
                                          Study)
from data_quality.persistence.session import create_scoped_session
from data_quality.requests.db import (update_ae_status,
                                      update_ctlogpattern_status,
                                      update_dicominput_status,
                                      update_innovalogpull_status,
                                      update_study_status)
from data_quality.tasks.etl import (_check_webservice_status, _decompress,
                                    import_ae, import_connectivitylist,
                                    import_consolidation, import_ctlog,
                                    import_customer, import_device,
                                    import_dicompatterns, import_innovalog,
                                    import_translatorconfig)
from data_quality.tasks.logic import (batch_ctlog_test, batch_dicominput_test,
                                      batch_dosimetric_test,
                                      batch_innovalog_test,
                                      batch_translator_test)

logger = get_task_logger(__name__)
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.SubjectAltNameWarning)

_BATCH_SIZE_DOSIMETRIC = int(cfg_parser['dosimetric']['_BATCH_SIZE'])
_BATCH_SIZE_INNOVA = int(cfg_parser['innovalog']['_BATCH_SIZE'])
_BATCH_SIZE_CTLOGPATTERN = int(cfg_parser['ctlog']['_BATCH_SIZE'])
_BATCH_SIZE_DICOMINPUT = int(cfg_parser['dicompattern']['_BATCH_SIZE'])
__user_etl_mongo = cfg_parser['etl']['_mongo_user']
__etl_etl_mongo = cfg_parser['etl']['_mongo_pw']
__etl_http_link = cfg_parser['etl']['_http_adress']
_skip_test_site = cfg_parser.getboolean('etl', '_skip_test_site')

DB_SESSION = create_scoped_session()()


def batch(iterable, n=1):
    """
    Function that perform on iterable, return a packet (batch) from this iterable
    :param iterable: iterable object
    :param n: size of packet
    :return: return a packet of size n of iterable object
    """
    size = len(iterable)
    for ndx in range(0, size, n):
        yield iterable[ndx:min(ndx + n, size)]


#####################################################################################
# ETL periodic processing
#####################################################################################


@app.task()
def search_new_dosimetric():
    """
    Check all new study data and create new task for processing them
    :return:
    """
    DB_SESSION.expire_all()
    try:
        # Make a 'lock' on data being process by changing their status with a temp one
        lst = [elem for elem, in DB_SESSION.query(
            Study.id).filter(Study.status == "N")]
        if len(lst) == 0:
            return
        update_study_status(DB_SESSION, lst, 'U')
        DB_SESSION.commit()

        # Process dosimetric test on study by batch of _BATCH_SIZE study
        for x in batch(lst, _BATCH_SIZE_DOSIMETRIC):
            batch_dosimetric_test.apply_async(args=(x,), kwargs={})
    except Exception as e:
        DB_SESSION.rollback()
        logger.error("Fail on searching new dosimetric data: {}".format(e))
    finally:
        DB_SESSION.close()


@app.task()
def search_new_innovalogpull():
    """
    Check all new innovalog pull refresh, and check their status
    :return:
    """
    DB_SESSION.expire_all()
    try:
        # Make a 'lock' on data being process by changing their status with a temp one
        lst = [elem for elem, in DB_SESSION.query(
            InnovaLogPull.id).filter(InnovaLogPull.status == "N")]
        if len(lst) == 0:
            return
        update_innovalogpull_status(DB_SESSION, lst, 'U')
        DB_SESSION.commit()

        # Process innovalog pull test of _BATCH_SIZE innovalog entries
        for x in batch(lst, _BATCH_SIZE_INNOVA):
            batch_innovalog_test.apply_async(args=(x,), kwargs={})
    except Exception as e:
        DB_SESSION.rollback()
        logger.error("Fail on searching new innovalog data: {}".format(e))
    finally:
        DB_SESSION.close()


@app.task()
def search_new_ctlogpattern():
    """
    Check all new innovalog pull refresh, and check their status
    :return:
    """
    DB_SESSION.expire_all()
    try:
        # Make a 'lock' on data being process by changing their status with a temp one
        lst = [elem for elem, in DB_SESSION.query(
            CTLogPattern.id).filter(CTLogPattern.status == "N")]
        if len(lst) == 0:
            return
        update_ctlogpattern_status(DB_SESSION, lst, 'U')
        DB_SESSION.commit()

        # Process ct log pattern by batch
        for x in batch(lst, _BATCH_SIZE_CTLOGPATTERN):
            batch_ctlog_test.apply_async(args=(x,), kwargs={})
    except Exception as e:
        DB_SESSION.rollback()
        logger.error("Fail on searching new ctlog data: {}".format(e))
    finally:
        DB_SESSION.close()


@app.task()
def search_new_dicominput():
    """
    Check all new innovalog pull refresh, and check their status
    :return:
    """
    DB_SESSION.expire_all()
    try:
        # Make a 'lock' on data being process by changing their status with a temp one
        lst = [elem for elem, in DB_SESSION.query(
            DicomInput.id).filter(DicomInput.status == "N")]
        if len(lst) == 0:
            return
        update_dicominput_status(DB_SESSION, lst, 'U')
        DB_SESSION.commit()

        # Process dicominput by batch
        for x in batch(lst, _BATCH_SIZE_DICOMINPUT):
            batch_dicominput_test.apply_async(args=(x,), kwargs={})
    except Exception as e:
        DB_SESSION.rollback()
        logger.error("Fail on searching new dicom input data: {}".format(e))
    finally:
        DB_SESSION.close()


@app.task()
def search_new_ae():
    """
    Check for new ae, for testing translator config
    :return:
    """
    DB_SESSION.expire_all()
    try:
        # Make a 'lock' on data being process by changing their status with a temp one
        lst = [elem for elem, in DB_SESSION.query(
            ApplicationEntity.id).filter(ApplicationEntity.status == "N")]
        if len(lst) == 0:
            return
        update_ae_status(DB_SESSION, lst, 'U')
        DB_SESSION.commit()

        # Process ae by batch
        for x in batch(lst, 10):
            batch_translator_test.apply_async(args=(x,), kwargs={})
    except Exception as e:
        DB_SESSION.rollback()
        logger.error("Fail on searching ae: {}".format(e))
    finally:
        DB_SESSION.close()


@app.task()
def etl_update_device(expires_in_hrs=11):
    """

    :param expires_in_hrs:
    :return:
    """
    import_device.apply_async(args=(),
                              kwargs={},
                              expires=datetime.now() + timedelta(hours=expires_in_hrs))


@app.task()
def etl_update_customer(expires_in_hrs=11):
    """

    :param expires_in_hrs:
    :return:
    """
    _fallback_date = "2011-01-01T00:00:00"
    DB_SESSION.expire_all()

    try:
        _last_pull_date = DB_SESSION.query(
            func.max(Customer.last_update)).scalar()
        _date_to_pull = _last_pull_date.isoformat(
        ) if _last_pull_date is not None else _fallback_date
        import_customer.apply_async(args=(_date_to_pull,),
                                    kwargs={},
                                    expires=datetime.now() + timedelta(hours=expires_in_hrs))
    except Exception as e:
        DB_SESSION.rollback()
        logger.error("Fail on launching etl customer update: {}".format(e))
    finally:
        DB_SESSION.close()


@app.task()
def etl_update_ae(expires_in_hrs=11):
    """

    :param expires_in_hrs:
    :return:
    """
    _fallback_date = "2011-01-01T00:00:00"
    DB_SESSION.expire_all()

    try:
        _last_pull_date = DB_SESSION.query(
            func.max(ApplicationEntity.last_updated)).scalar()
        _date_to_pull = _last_pull_date.isoformat(
        ) if _last_pull_date is not None else _fallback_date
        import_ae.apply_async(args=(_date_to_pull,),
                              kwargs={},
                              expires=datetime.now() + timedelta(hours=expires_in_hrs))
    except Exception as e:
        DB_SESSION.rollback()
        logger.error("Fail on launching etl ae update: {}".format(e))
    finally:
        DB_SESSION.close()


@app.task()
def etl_import_probes_data_dicompattern(expires_in_hrs=11):
    """

    :param expires_in_hrs:
    :return:
    """
    if not _check_webservice_status():
        logger.error(
            "Web service not available, cannot start ETL probes processing dispatch ")
        return

    _fallback_date = "2017-01-01T00:00:00"
    DB_SESSION.expire_all()

    try:
        url_target = "{}/aggregate/IBAutomation".format(__etl_http_link)
        x = dumps([{"$match": {"data.dwibInformationType": {"$in": ["EltRegularPatterns"]}}},
                   {"$group": {"_id": "$data.serialNumber",
                               "receptionDate": {"$max": "$receptionDate"}}}])
        r = requests.get(url_target, params={"query": x},
                         auth=(__user_etl_mongo, __etl_etl_mongo))

        if r.status_code == 200:
            # retrieve from db last insert (by measure date)
            req = DB_SESSION.query(DicomInput.serial_number, func.max(DicomInput.reception_date)).group_by(
                DicomInput.serial_number).all()
            dicominput_db_time = {x: y for x, y in req}
            # retrieve from dwib last inserted ctlog element by serial number
            probe_last_time = {data['_id']: data['receptionDate']
                               for data in loads(_decompress(r.content))}

            for sn, time in probe_last_time.items():
                # skip test site
                if _skip_test_site and sn.startswith('T'):
                    continue
                if sn not in dicominput_db_time.keys():
                    import_dicompatterns.apply_async(args=(sn, _fallback_date,),
                                                     kwargs={},
                                                     expires=datetime.now() + timedelta(hours=expires_in_hrs))
                elif time.replace(tzinfo=None) > dicominput_db_time[sn]:
                    _datetime_retrieve = dicominput_db_time[sn]
                    # we add microseconds after this date, if old data for a sn is still with µs to 000
                    if _datetime_retrieve <= datetime(2018, 1, 10):
                        _datetime_retrieve += timedelta(seconds=1)
                    import_dicompatterns.apply_async(args=(sn, _datetime_retrieve.isoformat(),),
                                                     kwargs={},
                                                     expires=datetime.now() + timedelta(hours=expires_in_hrs))
    except Exception as e:
        logger.error(
            "Fail on launching etl dicom pattern data update: {}".format(e))
        DB_SESSION.rollback()
    finally:
        DB_SESSION.close()


@app.task()
def etl_import_probes_data_innovalog(expires_in_hrs=11):
    """

    :param expires_in_hrs:
    :return:
    """
    if not _check_webservice_status():
        logger.error(
            "Web service not available, cannot start ETL probes processing dispatch ")
        return

    _fallback_date = "2017-01-01T00:00:00"
    DB_SESSION.expire_all()

    try:
        url_target = "{}/aggregate/IBAutomation".format(__etl_http_link)
        x = dumps([{"$match": {"data.dwibInformationType": {"$in": ["EltInnovaLog"]}}},
                   {"$group": {"_id": "$data.serialNumber",
                               "receptionDate": {"$max": "$receptionDate"}}}])
        r = requests.get(url_target, params={"query": x},
                         auth=(__user_etl_mongo, __etl_etl_mongo))

        if r.status_code == 200:
            # retrieve from db last insert (by measure date)
            req = DB_SESSION.query(InnovaLogPull.serial_number, func.max(InnovaLogPull.reception_date)).group_by(
                InnovaLogPull.serial_number).all()
            innovalog_db_time = {x: y for x, y in req}
            # retrieve from dwib last inserted ctlog element by serial number
            probe_last_time = {data['_id']: data['receptionDate']
                               for data in loads(_decompress(r.content))}

            for sn, time in probe_last_time.items():
                # skip test site
                if _skip_test_site and sn.startswith('T'):
                    continue
                if sn not in innovalog_db_time.keys():
                    # this sn were not previously in db
                    import_innovalog.apply_async(args=(sn, _fallback_date,),
                                                 kwargs={},
                                                 expires=datetime.now() + timedelta(hours=expires_in_hrs))
                elif time.replace(tzinfo=None) > innovalog_db_time[sn]:
                    _datetime_retrieve = innovalog_db_time[sn]
                    # we add microseconds after this date, if old data for a sn is still with µs to 000
                    if _datetime_retrieve <= datetime(2018, 1, 10):
                        _datetime_retrieve += timedelta(seconds=1)
                    import_innovalog.apply_async(args=(sn, _datetime_retrieve.isoformat(),),
                                                 kwargs={},
                                                 expires=datetime.now() + timedelta(hours=expires_in_hrs))

    except Exception as e:
        logger.error(
            "Fail on launching etl innovalog data update: {}".format(e))
        DB_SESSION.rollback()
    finally:
        DB_SESSION.close()


@app.task()
def etl_import_probes_data_consolidation(expires_in_hrs=11):
    """

    :param expires_in_hrs:
    :return:
    """
    if not _check_webservice_status():
        logger.error(
            "Web service not available, cannot start ETL probes processing dispatch ")
        return

    _fallback_date = "2017-01-01T00:00:00"
    DB_SESSION.expire_all()

    try:
        url_target = "{}/aggregate/IBAutomation".format(__etl_http_link)
        x = dumps([{"$match": {"data.dwibInformationType": {"$in": ["EltXAConsolidation",
                                                                    "EltMGConsolidation",
                                                                    "EltCTConsolidation",
                                                                    "EltRFConsolidation"]}}},
                   {"$group": {"_id": "$data.serialNumber",
                               "receptionDate": {"$max": "$receptionDate"}}}])
        r = requests.get(url_target, params={"query": x},
                         auth=(__user_etl_mongo, __etl_etl_mongo))

        if r.status_code == 200:
            # retrieve from db last insert (by measure date)
            req = DB_SESSION.query(Study.serial_number, func.max(Study.reception_date)).group_by(
                Study.serial_number).all()
            study_db_time = {x: y for x, y in req}
            # retrieve from dwib last inserted ctlog element by serial number
            probe_last_time = {data['_id']: data['receptionDate']
                               for data in loads(_decompress(r.content))}

            for sn, time in probe_last_time.items():
                # skip test site
                if _skip_test_site and sn.startswith('T'):
                    continue
                if sn not in study_db_time.keys():
                    # this sn were not previously in db
                    import_consolidation.apply_async(args=(sn, _fallback_date,),
                                                     kwargs={},
                                                     expires=datetime.now() + timedelta(hours=expires_in_hrs))
                elif time.replace(tzinfo=None) > study_db_time[sn]:
                    _datetime_retrieve = study_db_time[sn]
                    # we add microseconds after this date, if old data for a sn is still with µs to 000
                    if _datetime_retrieve <= datetime(2018, 1, 10):
                        _datetime_retrieve += timedelta(seconds=1)
                    import_consolidation.apply_async(args=(sn, _datetime_retrieve.isoformat(),),
                                                     kwargs={},
                                                     expires=datetime.now() + timedelta(hours=expires_in_hrs))
    except Exception as e:
        logger.error(
            "Fail on launching etl consolidation data update: {}".format(e))
        DB_SESSION.rollback()
    finally:
        DB_SESSION.close()


@app.task()
def etl_import_probes_data_ctlog(expires_in_hrs=11):
    """

    :param expires_in_hrs:
    :return:
    """
    if not _check_webservice_status():
        logger.error(
            "Web service not available, cannot start ETL probes processing dispatch ")
        return

    _fallback_date = "2017-01-01T00:00:00"
    DB_SESSION.expire_all()

    try:
        url_target = "{}/aggregate/IBAutomation".format(__etl_http_link)
        x = dumps([{"$match": {"data.dwibInformationType": {"$in": ["EltCTLog"]}}},
                   {"$group": {"_id": "$data.serialNumber",
                               "receptionDate": {"$max": "$receptionDate"}}}])
        r = requests.get(url_target, params={"query": x},
                         auth=(__user_etl_mongo, __etl_etl_mongo))

        if r.status_code == 200:
            # retrieve from db last insert (by measure date)
            req = DB_SESSION.query(CTLogPattern.serial_number, func.max(CTLogPattern.reception_date)).group_by(
                CTLogPattern.serial_number).all()
            ctlog_db_time = {x: y for x, y in req}
            # retrieve from dwib last inserted ctlog element by serial number
            probe_last_time = {data['_id']: data['receptionDate']
                               for data in loads(_decompress(r.content))}

            for sn, time in probe_last_time.items():
                # skip test site
                if _skip_test_site and sn.startswith('T'):
                    continue
                if sn not in ctlog_db_time.keys():
                    # this sn were not previously in db
                    import_ctlog.apply_async(args=(sn, _fallback_date,),
                                             kwargs={},
                                             expires=datetime.now() + timedelta(hours=expires_in_hrs))
                elif time.replace(tzinfo=None) > ctlog_db_time[sn]:
                    _datetime_retrieve = ctlog_db_time[sn]
                    # we add microseconds after this date, if old data for a sn is still with µs to 000
                    if _datetime_retrieve <= datetime(2018, 1, 10):
                        _datetime_retrieve += timedelta(seconds=1)
                    import_ctlog.apply_async(args=(sn, _datetime_retrieve.isoformat(),),
                                             kwargs={},
                                             expires=datetime.now() + timedelta(hours=expires_in_hrs))
    except Exception as e:
        logger.error("Fail on launching etl ctlog data update: {}".format(e))
        DB_SESSION.rollback()
    finally:
        DB_SESSION.close()


#####################################################################################
# ETL periodic processing wrapper
#####################################################################################

@app.task()
def etl_update_probes_data(expires_in_hrs=11):
    """
    Function that launch check of of new probes data from remote monitored site
    :return:
    """
    if not _check_webservice_status():
        logger.error(
            "Web service not available, cannot start ETL probes processing dispatch")
        return

    etl_import_probes_data_consolidation(expires_in_hrs)
    etl_import_probes_data_ctlog(expires_in_hrs)
    etl_import_probes_data_dicompattern(expires_in_hrs)
    etl_import_probes_data_innovalog(expires_in_hrs)


@app.task()
def reconstruct_connectivity_list():
    """
    Function that recreate the connecitivty list
    :return:
    """
    import_connectivitylist.apply_async(args=(), kwargs={})


@app.task()
def reconstruct_translatorconfig():
    """
    Launch the reconstruction of all translator config
    :return:
    """
    import_translatorconfig.apply_async(args=(), kwargs={})


@app.task()
def etl_update_business_data(expires_in_hrs=11):
    """
    Function that launch check of new business data from dwib
    it launch multiple celery task per type of data
    :return:
    """
    if not _check_webservice_status():
        logger.error(
            "Web service not available, cannot start ETL business processing dispatch")
        return

    etl_update_device(expires_in_hrs)
    etl_update_customer(expires_in_hrs)
    etl_update_ae(expires_in_hrs)


@app.task()
def search_all_new_input():
    """
    Function that launch search of new data inserted
    it launch multiple celery task per type of data
    :return:
    """
    search_new_ctlogpattern()
    search_new_dicominput()
    search_new_dosimetric()
    search_new_innovalogpull()


@app.task()
def refresh_materialized_view():
    """
    Refresh materialized view by calling procedure
    :return:
    """
    logger.info("Refreshing materialized view")
    try:
        DB_SESSION.execute("CALL update_all_stored_view()")
        logger.info("Successful refresh of materialized view")
    except Exception as e:
        logger.error("Error in refreshing materialized view : {}".format(e))
        DB_SESSION.rollback()
    finally:
        DB_SESSION.close()
