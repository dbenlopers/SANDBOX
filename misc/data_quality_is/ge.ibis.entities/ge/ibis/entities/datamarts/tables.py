# -*- coding: utf-8 -*-
"""
IBIS `Data` database ORM
The purpose of this schema is to be exposed to data consumers.
"""
from __future__ import absolute_import

import hashlib
import json

from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from sqlalchemy.orm import mapper, relationship

from .metadata import IBISData


class StudyDataSource(IBISData):
    __tablename__ = 'agg_study_data_source'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    serial_number = Column(String(50))
    customer_name = Column(String(255))
    pole = Column(String(50))
    country = Column(String(50))
    sdm_key = Column(Integer, index=True)
    integration_mode = Column(String(100))
    encrypted_siuid = Column(String(255))
    local_study_id = Column(Integer)
    modality = Column(String(10))
    study_date = Column(DateTime)
    dicom_first_received = Column(DateTime)
    dicom_last_received = Column(DateTime)
    ctlog_first_insert = Column(DateTime)
    aet = Column(String(100))
    nb_dicom_aet_producer = Column(Integer)
    dicom_aet_producer = Column(String(150))
    dosimetric_success_rate = Column(Float)
    dicompattern_success_rate = Column(Float)
    ctlog_status = Column(String(4))
    ctlog_obs = Column(String(15))
    inferred_integration_mode = Column(String(100))


class PatternLast15Days(IBISData):
    __tablename__ = 'pattern_last_15days'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    serial_number = Column(String(50))
    encrypted_siuid = Column(String(255))
    customer_name = Column(String(255))
    aet = Column(String(100))
    sdm_key = Column(Integer)
    modality = Column(String(10))
    integration_mode = Column(String(100))
    study_date = Column(DateTime)
    datetime_first_received = Column(DateTime)
    prod_command = Column(String(20))
    prod_sop_class = Column(String(100))
    prod_message_type = Column(String(25))
    prod_series_number = Column(String(20))
    prod_study_status = Column(String(20))
    prod_message_status = Column(String(1))
    message_type = Column(String(50))
    status = Column(String(4))
    rational = Column(String(15))


class DosimetricLast15Days(IBISData):
    __tablename__ = 'dosimetric_last_15days'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    serial_number = Column(String(50))
    pole = Column(String(10))
    customer_name = Column(String(255))
    aet = Column(String(100))
    sdm_key = Column(Integer)
    modality = Column(String(30))
    integration_mode = Column(String(100))
    study_date = Column(DateTime)
    study_id = Column(Integer)
    dosimetric_type = Column(String(25))
    dosimetric_diff = Column(Numeric(16))
    status = Column(String(4))
    rational = Column(String(15))


class CtLogLast15Days(IBISData):
    __tablename__ = 'ctlog_last_15days'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    serial_number = Column(String(50))
    aet = Column(String(100))
    local_study_id = Column(Integer)
    datetime_first_insert = Column(DateTime)
    status = Column(String(4))
    rational = Column(String(15))
    inferred_integration_mode = Column(String(100))


class DevicesOverview(IBISData):
    __tablename__ = 'devices_overview'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    serial_number = Column(String(50), index=True)
    customer_name = Column(String(255))
    aet = Column(String(100))
    common_name = Column(String(100))
    local_ae_id = Column(Integer)
    contrast = Column(Numeric(8, 0))
    ftp_connection_type = Column(String(50))
    deleted = Column(Numeric(8, 0))
    device = Column(String(100))
    modality = Column(String(10))
    sdm_key = Column(Integer)
    manufacturer = Column(String(100))
    software_version = Column(String(255))
    aet_system_id = Column(String(50))
    station_name = Column(String(100))
    mpps_series_duplicate_removal = Column(Numeric(8, 0))
    modality_worklist_enabled = Column(Numeric(8, 0))
    data_type = Column(String(50))
    translator = Column(String(70))
    image_translator = Column(String(70))
    secondary_data_type = Column(String(50))
    secondary_translator = Column(String(70))
    secondary_image_translator = Column(String(70))
    tertiary_data_type = Column(String(50))
    tertiary_translator = Column(String(70))
    tertiary_image_translator = Column(String(70))
    ae_last_update = Column(DateTime)
    integration_mode = Column(String(100))
    ftp_enabled = Column(Integer)
    ftp_secured = Column(Numeric(8, 0))
    project_type = Column(String(40))
    project_manager = Column(String(50))
    application_specialist = Column(String(50))
    country = Column(String(40))
    pole = Column(String(10))
    dosewatch_version = Column(String(50))
    dictionary_version = Column(String(40))
    state = Column(String(50))
    town = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
    product_type = Column(String(20))
    customer_system_id = Column(String(150))
    customer_installation_date = Column(DateTime)
    customer_last_update = Column(DateTime)
    is_active = Column(Numeric(8, 0))
    worklist_enabled = Column(Numeric(8, 0))
    decommissioning = Column(Numeric(8, 0))
    iguana_channels = Column(Numeric(8, 0))
    has_active_monitoring = Column(Integer)
    Numeric
    agg_aet = Column(String(250))
    number_of_examinations = Column(Integer)
    last_study_date = Column(DateTime)
    last_received_dicom = Column(DateTime)
    last_received_ctlog = Column(DateTime)
    avg_dosimetric_success_rate = Column(Numeric(20, 3))
    avg_dicom_success_rate = Column(Numeric(20, 3))
    ctlog_success_rate = Column(Numeric(54))
    dosi_test = Column(String(15))
    dicom_test = Column(String(15))
    dosi_test_verbose = Column(String(26))
    dicom_test_verbose = Column(String(28))
    aet_plus_exams = Column(String(274))


sds_table = (StudyDataSource._sa_class_manager.mapper
             .mapped_table)
pl15_table = (PatternLast15Days._sa_class_manager.mapper
              .mapped_table)
dl15_table = (DosimetricLast15Days._sa_class_manager.mapper
              .mapped_table)
ct15_table = (CtLogLast15Days._sa_class_manager.mapper
              .mapped_table)

Index('idx_aggstudy_ds_sdmkey', sds_table.c.serial_number,
      sds_table.c.aet,
      sds_table.c.dicom_aet_producer)

Index('idx_pattern', pl15_table.c.serial_number,
      pl15_table.c.aet)
Index('idx_dosimetric', dl15_table.c.serial_number,
      dl15_table.c.aet)
Index('idx_ctlog', ct15_table.c.serial_number,
      ct15_table.c.aet)
