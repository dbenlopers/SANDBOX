# coding=utf-8
from data_quality.celery import app
from data_quality.celeryconfig import cfg_parser
from data_quality.persistence.session import create_scoped_session
from data_quality.ETL.lib_etl import insert_customer, upsert_device, insert_ae, insert_connectivitylist, \
    insert_dicominput, construct_consolidation, construct_ctlog, upsert_innovalog, insert_translatorconfig, \
    upsert_consolidation
import gzip
from data_quality.persistence.orm import ConnectivityList, TranslatorConfig, Customer
from bson.json_util import loads, dumps, JSONOptions
from bson.objectid import ObjectId
from dateutil.parser import parse
import json
import os
from data_quality import ETL
import requests
import requests.packages.urllib3.exceptions
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.SubjectAltNameWarning)

__user_etl_mongo = cfg_parser['etl']['_mongo_user']
__etl_etl_mongo = cfg_parser['etl']['_mongo_pw']
__etl_http_link = cfg_parser['etl']['_http_adress']
__ACTIVATED_PURGE = cfg_parser.getboolean('etl', '_activate_purge')

with open(os.path.join(os.path.dirname(ETL.__file__), "mapping.json"), 'r') as mapping_file:
    mapping = json.load(mapping_file)
    mapping_file.close()

DB_scoped_session = create_scoped_session()()


def _check_webservice_status():
    url_target_one = "{0}/".format(__etl_http_link)
    r = requests.get(url_target_one)
    if r.status_code == 200:
        return True
    else:
        return False


def _decompress(compressed):
    return gzip.decompress(compressed).decode('utf-8')


@app.task()
def import_customer(last_pull_date):
    """
    ETL function for import new customer data
    :param last_pull_date: date where retrieve can begin
    :return:
    """
    if not _check_webservice_status():
        logger.error("Web service not available, not ETL integration of Customer")
        return
    url_target = "{0}/find/CustomerRevision".format(__etl_http_link)
    params = dumps({"lastUpdate": {"$gt": parse(last_pull_date)}}, json_options=JSONOptions(datetime_representation=2))

    r = requests.get(url_target, params={"query": params},
                     auth=(__user_etl_mongo, __etl_etl_mongo))

    if r.status_code == 200:
        try:
            for elem in loads(_decompress(r.content)):
                insert_customer(DB_scoped_session, elem, mapping)
            DB_scoped_session.commit()
            logger.info('Successful ETL Customer since {}'.format(last_pull_date))
        except Exception as e:
            logger.error("Error in ETL task (import_customer)({0}): {1}".format(last_pull_date, e))
            DB_scoped_session.rollback()
        finally:
            DB_scoped_session.close()


@app.task()
def import_ae(last_pull_date):
    """
    ETL function for import new application entity data
    :param last_pull_date: date where retrieve can begin
    :return:
    """
    if not _check_webservice_status():
        logger.error("Web service not available, not ETL integration of AE")
        return
    url_target = "{0}/find/ApplicationEntity".format(__etl_http_link)
    params = dumps({"lastAgentUpdate": {"$gt": parse(last_pull_date)}},
                   json_options=JSONOptions(datetime_representation=2))

    r = requests.get(url_target, params={"query": params},
                     auth=(__user_etl_mongo, __etl_etl_mongo))

    if r.status_code == 200:
        try:
            for elem in loads(_decompress(r.content)):
                insert_ae(DB_scoped_session, elem, mapping)
            DB_scoped_session.commit()
            logger.info('Successful ETL AE since {}'.format(last_pull_date))
        except Exception as e:
            logger.error("Error in ETL task (import_ae)({0}): {1}".format(last_pull_date, e))
            DB_scoped_session.rollback()
        finally:
            DB_scoped_session.close()


@app.task()
def import_device():
    """
    ETL function for import new device data
    :return:
    """
    if not _check_webservice_status():
        logger.error("Web service not available, not ETL integration of Device")
        return
    url_target = "{0}/find/Device".format(__etl_http_link)
    params = dumps({})

    r = requests.get(url_target, params={"query": params},
                     auth=(__user_etl_mongo, __etl_etl_mongo))

    if r.status_code == 200:
        try:
            for elem in loads(_decompress(r.content)):
                upsert_device(DB_scoped_session, elem, mapping)
            DB_scoped_session.commit()
            logger.info('Successful ETL Device ')
        except Exception as e:
            logger.error("Error in ETL task (import_device): {}".format(e))
            DB_scoped_session.rollback()
        finally:
            DB_scoped_session.close()


@app.task()
def import_connectivitylist():
    """
    ETL function for import new connectivity list data
    :return:
    """
    if not _check_webservice_status():
        logger.error("Web service not available, not ETL integration of Connectivity list")
        return
    url_target = "{0}/find/IntegrationRevision".format(__etl_http_link)
    params = dumps({"supported": "YES", "deleted": False})

    r = requests.get(url_target, params={"query": params},
                     auth=(__user_etl_mongo, __etl_etl_mongo))

    r_device = requests.get("{}/find/Device".format(__etl_http_link),
                            params={"query": dumps({})},
                            auth=(__user_etl_mongo, __etl_etl_mongo))

    __DEVICE = {data['_id']: data for data in loads(_decompress(r_device.content))}

    if r.status_code == 200 and r_device.status_code == 200:
        try:
            # empty table related to connectivity list
            # DB_scoped_session.query(Connectivity_Pattern).delete()
            # DB_scoped_session.query(Connectivity_Functionality).delete()
            DB_scoped_session.query(ConnectivityList).delete()
            DB_scoped_session.execute("ALTER TABLE connectivity_list AUTO_INCREMENT=1")
            for elem in loads(_decompress(r.content)):
                _device = __DEVICE[ObjectId(elem['device'].id)]
                if 'sdmKey' in _device.keys():
                    insert_connectivitylist(DB_scoped_session, elem, mapping, _device)
            DB_scoped_session.commit()
            # ## Call stored procedure which update table that make correspondance with sdmKey, dwV, Imid and MT
            DB_scoped_session.execute("CALL update_im_mt()")
            logger.info('Successful ETL Connectivity list')
        except Exception as e:
            logger.error("Error in ETL task (import_connectivitylist): {}".format(e))
            DB_scoped_session.rollback()
        finally:
            DB_scoped_session.close()
    else:
        logger.error('Query Error at data retrieving from dwib web service')


@app.task()
def import_translatorconfig():
    """
    ETL function for translator config
    :return:
    """
    if not _check_webservice_status():
        logger.error("Web service not available, not ETL integration of Translator config")
        return
    url_target = "{0}/find/TranslatorConfiguration".format(__etl_http_link)
    params = dumps({})

    r = requests.get(url_target, params={"query": params},
                     auth=(__user_etl_mongo, __etl_etl_mongo))

    r_device = requests.get("{}/find/Device".format(__etl_http_link),
                            params={"query": dumps({})},
                            auth=(__user_etl_mongo, __etl_etl_mongo))

    __DEVICE = {data['_id']: data for data in loads(_decompress(r_device.content))}

    if r.status_code == 200 and r_device.status_code == 200:
        try:
            # empty translator config table
            DB_scoped_session.query(TranslatorConfig).delete()
            DB_scoped_session.execute("ALTER TABLE translator_config AUTO_INCREMENT=1")

            for elem in loads(_decompress(r.content)):
                _device = __DEVICE[ObjectId(elem['device'].id)]
                if 'sdmKey' in _device.keys():
                    insert_translatorconfig(DB_scoped_session, elem, mapping, _device)
            DB_scoped_session.commit()
            logger.info('Successful ETL Translator config ')
        except Exception as e:
            logger.error("Error in ETL task (import_translatorconfig): {}".format(e))
            DB_scoped_session.rollback()
        finally:
            DB_scoped_session.close()


@app.task()
def import_dicompatterns(serial_number, last_pull_date):
    """
    ETL function for import new dicompattern data
    :param serial_number: serial number to retrieve
    :param last_pull_date: date where retrieve can begin
    :return:
    """
    if not _check_webservice_status():
        logger.error("Web service not available, not ETL integration of dicom patterns for {}".format(serial_number))
        return
    launch_purge = False
    url_target = "{0}/aggregate/IBAutomation".format(__etl_http_link)
    params = dumps([{"$unwind": "$data.resultRows"},
                    {"$match": {"data.serialNumber": serial_number,
                                "data.dwibInformationType": "EltRegularPatterns",
                                "receptionDate": {"$gt": parse(last_pull_date)}}
                     }], json_options=JSONOptions(datetime_representation=2))

    r = requests.get(url_target, params={"query": params},
                     auth=(__user_etl_mongo, __etl_etl_mongo))

    if r.status_code == 200:
        try:
            for elem in loads(_decompress(r.content)):
                insert_dicominput(DB_scoped_session, elem, mapping)

            if DB_scoped_session.query(Customer).filter(Customer.serial_number == serial_number,
                                                        Customer.is_last == True).count() != 0:
                DB_scoped_session.query(Customer).filter(Customer.serial_number == serial_number,
                                                         Customer.is_last == True).update({"is_monitored": 1})
            DB_scoped_session.commit()
            launch_purge = True
            logger.info('Successful ETL dicom pattern for {0} since {1}'.format(serial_number, last_pull_date))
        except Exception as e:
            logger.error("Error in ETL task (import_dicompatterns)({0}-{1}): {2}".format(serial_number,
                                                                                         last_pull_date, e))
            DB_scoped_session.rollback()
        finally:
            DB_scoped_session.close()

    if launch_purge and __ACTIVATED_PURGE:
        url_target = "{0}/delete/IBAutomation".format(__etl_http_link)
        params = dumps({"data.serialNumber": serial_number,
                        "data.dwibInformationType": "EltRegularPatterns",
                        "receptionDate": {"$lt": parse(last_pull_date)}},
                       json_options=JSONOptions(datetime_representation=2))

        r = requests.delete(url_target, params={"query": params},
                            auth=(__user_etl_mongo, __etl_etl_mongo))

        logger.warning("ETL dicominput purge task ->status_code {0} : {1}".format(r.status_code, r.content))


@app.task()
def import_ctlog(serial_number, last_pull_date):
    """
    ETL function for import new ctlog data
    :param serial_number: serial number to retrieve
    :param last_pull_date: date where retrieve can begin
    :return:
    """
    if not _check_webservice_status():
        logger.error("Web service not available, not ETL integration of ctlog for {}".format(serial_number))
        return
    launch_purge = False
    url_target = "{0}/aggregate/IBAutomation".format(__etl_http_link)
    params = dumps([{"$unwind": "$data.resultRows"},
                    {"$match": {"data.serialNumber": serial_number,
                                "data.dwibInformationType": "EltCTLog",
                                "receptionDate": {"$gt": parse(last_pull_date)}}
                     }], json_options=JSONOptions(datetime_representation=2))

    r = requests.get(url_target, params={"query": params},
                     auth=(__user_etl_mongo, __etl_etl_mongo))

    if r.status_code == 200:
        try:
            _list_to_insert = []
            for elem in loads(_decompress(r.content)):
                _list_to_insert.append(construct_ctlog(elem, mapping))

            DB_scoped_session.bulk_save_objects(_list_to_insert)
            if DB_scoped_session.query(Customer).filter(Customer.serial_number == serial_number,
                                                        Customer.is_last == True).count() != 0:
                DB_scoped_session.query(Customer).filter(Customer.serial_number == serial_number,
                                                         Customer.is_last == True).update({"is_monitored": 1})
            DB_scoped_session.commit()
            launch_purge = True
            logger.info('Successful ETL ctlog for {0} since {1}'.format(serial_number, last_pull_date))
        except Exception as e:
            logger.error("Error in ETL task (import_ctlog)({0}-{1}): {2}".format(serial_number,
                                                                                 last_pull_date, e))
            DB_scoped_session.rollback()
        finally:
            DB_scoped_session.close()

    if launch_purge and __ACTIVATED_PURGE:
        url_target = "{0}/delete/IBAutomation".format(__etl_http_link)
        params = dumps({"data.serialNumber": serial_number,
                        "data.dwibInformationType": "EltCTLog",
                        "receptionDate": {"$lt": parse(last_pull_date)}},
                       json_options=JSONOptions(datetime_representation=2))

        r = requests.delete(url_target, params={"query": params},
                            auth=(__user_etl_mongo, __etl_etl_mongo))

        logger.warning("ETL ctlog purge task ->status_code {0} : {1}".format(r.status_code, r.content))


@app.task()
def import_innovalog(serial_number, last_pull_date):
    """
    ETL function for import new innovalog data
    :param serial_number: serial number to retrieve
    :param last_pull_date: date where retrieve can begin
    :return:
    """
    if not _check_webservice_status():
        logger.error("Web service not available, not ETL integration of innova log for {}".format(serial_number))
        return
    launch_purge = False
    url_target = "{0}/aggregate/IBAutomation".format(__etl_http_link)
    params = dumps([{"$unwind": "$data.resultRows"},
                    {"$match": {"data.serialNumber": serial_number,
                                "data.dwibInformationType": "EltInnovaLog",
                                "receptionDate": {"$gt": parse(last_pull_date)}}
                     }], json_options=JSONOptions(datetime_representation=2))

    r = requests.get(url_target, params={"query": params},
                     auth=(__user_etl_mongo, __etl_etl_mongo))

    if r.status_code == 200:
        try:
            for elem in loads(_decompress(r.content)):
                upsert_innovalog(DB_scoped_session, elem, mapping)

            if DB_scoped_session.query(Customer).filter(Customer.serial_number == serial_number,
                                                        Customer.is_last == True).count() != 0:
                DB_scoped_session.query(Customer).filter(Customer.serial_number == serial_number,
                                                         Customer.is_last == True).update({"is_monitored": 1})
            DB_scoped_session.commit()
            launch_purge = True
            logger.info('Successful ETL innovalog for {0} since {1}'.format(serial_number, last_pull_date))
        except Exception as e:
            logger.error("Error in ETL task (import_innovalog)({0}-{1}): {2}".format(serial_number,
                                                                                     last_pull_date, e))
            DB_scoped_session.rollback()
        finally:
            DB_scoped_session.close()

    if launch_purge and __ACTIVATED_PURGE:
        url_target = "{0}/delete/IBAutomation".format(__etl_http_link)
        params = dumps({"data.serialNumber": serial_number,
                        "data.dwibInformationType": "EltInnovaLog",
                        "receptionDate": {"$lt": parse(last_pull_date)}},
                       json_options=JSONOptions(datetime_representation=2))

        r = requests.delete(url_target, params={"query": params},
                            auth=(__user_etl_mongo, __etl_etl_mongo))

        logger.warning("ETL innovalog purge task ->status_code {0} : {1}".format(r.status_code, r.content))


@app.task()
def import_consolidation(serial_number, last_pull_date):
    """
    ETL function for import new consolidation data
    :param serial_number: serial number to retrieve
    :param last_pull_date: date where retrieve can begin
    :return:
    """
    if not _check_webservice_status():
        logger.error("Web service not available, not ETL integration of consolidation for {}".format(serial_number))
        return
    launch_purge = False
    url_target = "{0}/aggregate/IBAutomation".format(__etl_http_link)
    params = dumps([{"$unwind": "$data.resultRows"},
                    {"$match": {"data.serialNumber": serial_number,
                                "data.dwibInformationType": {"$in": ["EltXAConsolidation",
                                                                     "EltMGConsolidation",
                                                                     "EltCTConsolidation",
                                                                     "EltRFConsolidation"]},
                                "receptionDate": {"$gt": parse(last_pull_date)}}
                     }], json_options=JSONOptions(datetime_representation=2))

    r = requests.get(url_target, params={"query": params},
                     auth=(__user_etl_mongo, __etl_etl_mongo))

    if r.status_code == 200:
        try:
            _list_to_insert = []
            for elem in loads(_decompress(r.content)):
                # upsert_consolidation(DB_scoped_session, elem, mapping)
                _list_to_insert.append(construct_consolidation(elem, mapping))

            DB_scoped_session.bulk_save_objects(_list_to_insert)
            if DB_scoped_session.query(Customer).filter(Customer.serial_number == serial_number,
                                                        Customer.is_last == True).count() != 0:
                DB_scoped_session.query(Customer).filter(Customer.serial_number == serial_number,
                                                         Customer.is_last == True).update({"is_monitored": 1})
            DB_scoped_session.commit()
            launch_purge = True
            logger.info('Successful ETL consolidation for {0} since {1}'.format(serial_number, last_pull_date))
        except Exception as e:
            logger.error("Error in ETL task (import_consolidation)({0}-{1}): {2}".format(serial_number,
                                                                                         last_pull_date, e))
            DB_scoped_session.rollback()
        finally:
            DB_scoped_session.close()

    if launch_purge and __ACTIVATED_PURGE:
        url_target = "{0}/delete/IBAutomation".format(__etl_http_link)
        params = dumps({"data.serialNumber": serial_number,
                        "data.dwibInformationType": {"$in": ["EltXAConsolidation", "EltMGConsolidation",
                                                             "EltCTConsolidation", "EltRFConsolidation"]},
                        "receptionDate": {"$lt": parse(last_pull_date)}},
                       json_options=JSONOptions(datetime_representation=2))

        r = requests.delete(url_target, params={"query": params},
                            auth=(__user_etl_mongo, __etl_etl_mongo))

        logger.warning("ETL consolidation purge task ->status_code {0} : {1}".format(r.status_code, r.content))
