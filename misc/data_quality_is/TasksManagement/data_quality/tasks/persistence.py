# -*- coding: utf-8 -*-
"""
All function/processing define as sync processing that have interaction with database
"""
from data_quality.celery import app
from data_quality.persistence.orm import Study, InnovaLogPull, CTLogPattern, DicomInput, InnovalogpullStatus, \
    Dosimetric, CtlogpatternStatus, DicominputStatus, ApplicationEntity, TranslatorconfigStatus
from data_quality.persistence.session import create_scoped_session
from sqlalchemy import update
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

scoped_db_session = create_scoped_session()()


def store_objects(list_objects):
    """
    Store a list of ORM objects
    :param list_objects: list objects
    :return:
    """
    assert isinstance(list_objects, list)
    try:
        scoped_db_session.bulk_save_objects(list_objects)
        scoped_db_session.commit()
    except Exception as e:
        scoped_db_session.rollback()
        logger.error("Fail object insert : {}".format(e))
    finally:
        scoped_db_session.close()


@app.task()
def batch_store_dosimetrics_update_study_status(list_ids, status, dosi_lst):
    """
    Store dosimetric results (in batch) and update status of study to new status
    :param list_ids: id of study to update
    :param status: new status
    :param dosi_lst: list of dosimetric results to store
    :return:
    """
    try:
        scoped_db_session.execute(update(Study).where(Study.id.in_(list_ids)).values(status=status))
        scoped_db_session.bulk_insert_mappings(Dosimetric, dosi_lst)
        scoped_db_session.commit()
    except Exception as e:
        scoped_db_session.rollback()
        scoped_db_session.execute(update(Study).where(Study.id.in_(list_ids)).values(status="F"))
        scoped_db_session.commit()
        logger.error("Fail dosimetric insert : {}".format(e))
    finally:
        scoped_db_session.close()


@app.task()
def batch_store_innovalog_state_update_innova_status(list_ids, status, state_lst):
    """
    Store innovalog pull state (in batch) and update status of innova to new status
    :param list_ids: id of innova to update
    :param status: new status
    :param state_lst: list of innova state to update
    :return:
    """
    _existing = [elem for elem, in scoped_db_session.query(InnovalogpullStatus.innovalog_id)]
    _to_insert = []
    _to_update = []

    for elem in state_lst:
        if elem['innovalog_id'] in _existing:
            _to_update.append(elem)
        else:
            _to_insert.append(elem)

    try:
        scoped_db_session.execute(update(InnovaLogPull).where(InnovaLogPull.id.in_(list_ids)).values(status=status))
        scoped_db_session.bulk_insert_mappings(InnovalogpullStatus, _to_insert)
        scoped_db_session.bulk_update_mappings(InnovalogpullStatus, _to_update)
        scoped_db_session.commit()
    except Exception as e:
        scoped_db_session.rollback()
        scoped_db_session.execute(update(InnovaLogPull).where(InnovaLogPull.id.in_(list_ids)).values(status="F"))
        scoped_db_session.commit()
        logger.error("Fail innovalog upsert : {}".format(e))
    finally:
        scoped_db_session.close()


@app.task()
def batch_store_ctlogpattern_status_update_ctlogpattern_status(list_ids, status, state_lst):
    """
    Store ctlogpattern_status and update ctlopattern status by batch
    :param list_ids: list of ids
    :param status: status to set
    :param state_lst: data to store
    :return:
    """
    try:
        scoped_db_session.execute(update(CTLogPattern).where(CTLogPattern.id.in_(list_ids)).values(status=status))
        scoped_db_session.bulk_insert_mappings(CtlogpatternStatus, state_lst)
        scoped_db_session.commit()
    except Exception as e:
        scoped_db_session.rollback()
        scoped_db_session.execute(update(CTLogPattern).where(CTLogPattern.id.in_(list_ids)).values(status="F"))
        scoped_db_session.commit()
        logger.error("Fail ctlogpattern insert : {}".format(e))
    finally:
        scoped_db_session.close()


@app.task()
def batch_store_dicominput_status_update_dicominput_status(list_ids, status, state_lst):
    """
    Store a list of dicominput_status in json frmt, and update status of dicom input
    :param list_ids: list of dicom input id, to update status
    :param status: status to set
    :param state_lst: dicominput_status in json frmt to store
    :return:
    """
    try:
        scoped_db_session.execute(update(DicomInput).where(DicomInput.id.in_(list_ids)).values(status=status))
        scoped_db_session.bulk_insert_mappings(DicominputStatus, state_lst)
        scoped_db_session.commit()
    except Exception as e:
        scoped_db_session.rollback()
        scoped_db_session.execute(update(DicomInput).where(DicomInput.id.in_(list_ids)).values(status="F"))
        scoped_db_session.commit()
        logger.error("Fail dicom input insert : {}".format(e))
    finally:
        scoped_db_session.close()


@app.task()
def batch_store_translatorconf_status_update_ae_status(list_ids, status, state_lst):
    """
    Store a list of translatorconfig_status in json frmt, and update status of ae
    :param list_ids: list of ae id, to update status
    :param status: status to set to ae
    :param state_lst: dicominput_status in json frmt to store
    :return:
    """
    try:
        scoped_db_session.execute(
            update(ApplicationEntity).where(ApplicationEntity.id.in_(list_ids)).values(status=status))
        scoped_db_session.bulk_insert_mappings(TranslatorconfigStatus, state_lst)
        scoped_db_session.commit()
    except Exception as e:
        scoped_db_session.rollback()
        scoped_db_session.execute(
            update(ApplicationEntity).where(ApplicationEntity.id.in_(list_ids)).values(status="F"))
        scoped_db_session.commit()
        logger.error("Fail translatorconfig status insert : {}".format(e))
    finally:
        scoped_db_session.close()
