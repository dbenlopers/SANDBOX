# -*- coding: utf-8 -*-
"""
Implementation of all logic/processing processing
"""
from __future__ import absolute_import
from data_quality.celery import app
from data_quality.tasks.persistence import batch_store_dicominput_status_update_dicominput_status, \
    batch_store_innovalog_state_update_innova_status, batch_store_ctlogpattern_status_update_ctlogpattern_status, \
    batch_store_dosimetrics_update_study_status, batch_store_translatorconf_status_update_ae_status
from data_quality.requests.db import get_study_by_id, get_innovalogpull_by_id, get_dicominput_by_id, \
    get_ctlogpattern_by_id, update_study_status, update_ctlogpattern_status, update_dicominput_status, \
    update_innovalogpull_status, get_ctlog_integration_mode, get_aes, update_ae_status
from data_quality.persistence.session import create_scoped_session
from data_quality.processing import ae_translator_test, dosimetric_test, dicominput_test, ctlogpattern_test, \
    innovalog_test

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

db_session = create_scoped_session()()


@app.task()
def batch_dosimetric_test(list_ids):
    """
    Process by batch dosimetric test on study (list) and change their id (list)
    store result and update status by async processing batch
    :param list_ids:
    :return:
    """
    _dosi_to_store = []
    try:
        for data in get_study_by_id(db_session, list_ids):
            res = dosimetric_test(data)
            if res is not None:
                _dosi_to_store.extend(res)

        batch_store_dosimetrics_update_study_status.apply_async(args=(list_ids, 'C', _dosi_to_store,),
                                                                kwargs={})
    except Exception as e:
        db_session.rollback()
        logger.error("Error catched in batch_dosimetric_test  : {}".format(e))
        update_study_status(db_session, list_ids, 'F')
        db_session.commit()
    finally:
        db_session.close()


########################################################################################################################


@app.task()
def batch_innovalog_test(list_ids):
    """
    Process by batch of innovalog data, run/save test and chabnge status
    :param list_ids:
    :return:
    """
    _state_to_update = []
    try:
        for data in get_innovalogpull_by_id(db_session, list_ids):
            res = innovalog_test(data)
            if res is not None:
                _state_to_update.append(res)

        batch_store_innovalog_state_update_innova_status.apply_async(args=(list_ids, 'C', _state_to_update,),
                                                                     kwargs={})
    except Exception as e:
        db_session.rollback()
        logger.error("Error catched in batch_innova_log  : {}".format(e))
        update_innovalogpull_status(db_session, list_ids, 'F')
        db_session.commit()
    finally:
        db_session.close()


########################################################################################################################


@app.task()
def batch_ctlog_test(list_ids):
    """
    Run the dosimetric consistency processing on consolidation data
    :return:
    """
    _ctlogpatstatus = []
    messagepattern_by_im_id = get_ctlog_integration_mode(db_session)

    try:
        for data in get_ctlogpattern_by_id(db_session, list_ids):
            res = ctlogpattern_test(db_session, data, messagepattern_by_im_id)
            if res is not None:
                _ctlogpatstatus.append(res)

        batch_store_ctlogpattern_status_update_ctlogpattern_status.apply_async(args=(list_ids, 'C', _ctlogpatstatus,),
                                                                               kwargs={})
    except Exception as e:
        db_session.rollback()
        logger.error("Error catched in batch_ctlog_test : {}".format(e))
        update_ctlogpattern_status(db_session, list_ids, 'F')
        db_session.commit()
    finally:
        db_session.close()


########################################################################################################################


@app.task()
def batch_dicominput_test(list_ids):
    """
    Run dicom pattern test on a list of dicom input id
    execute test for each dicom input and store them into dicominput_status table
    store all results at once and update status (async processing)
    :param list_ids: list of dicom input id
    :return:
    """
    _dicominputstatus = []

    try:
        for data in get_dicominput_by_id(db_session, list_ids):
            res = dicominput_test(db_session, data)
            if res is not None:
                _dicominputstatus.extend(res)
        if len(_dicominputstatus) != 0:
            batch_store_dicominput_status_update_dicominput_status.apply_async(args=(list_ids, 'C', _dicominputstatus,),
                                                                               kwargs={})
        else:
            update_dicominput_status(sess=db_session, list_ids=list_ids, status='C')
    except Exception as e:
        db_session.rollback()
        logger.error("Error catched in batch_dicominput_test : {}".format(e))
        update_dicominput_status(db_session, list_ids, 'F')
        db_session.commit()
    finally:
        db_session.close()


########################################################################################################################


@app.task()
def batch_translator_test(list_ids):
    """
    Run the dosimetric consistency processing on consolidation data
    :param list_ids: List of ae.id to test
    :return:
    """
    try:
        res_output = []

        ae_query = get_aes(db_session, list_ids)

        for ae in ae_query:
            check_status = ae_translator_test(db_session, ae)
            if check_status is None:
                check_status = 2
            res_output.append({"ae_id": ae.id, "rational_id": check_status})

        if len(res_output) != 0:
            batch_store_translatorconf_status_update_ae_status.apply_async(args=(list_ids, 'C', res_output,),
                                                                           kwargs={})
        else:
            update_ae_status(sess=db_session, list_ids=list_ids, status='C')
    except Exception as e:
        db_session.rollback()
        logger.error(e)
        update_ae_status(db_session, list_ids, 'F')
        db_session.commit()
    finally:
        db_session.close()
