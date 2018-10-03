# -*- coding: utf-8 -*-
"""
IBIS `Main` database ORM
This is the application's internal database.
"""
from __future__ import absolute_import

import hashlib
import json

from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from sqlalchemy.orm import mapper, relationship

from ..workflow import ProcessingStatus
from .metadata import IBISMain


class CustomerDictionary(IBISMain):
    __tablename__ = 'customer_dictionary'

    customer_id = Column(Integer,
                         ForeignKey('customer.id'),
                         primary_key=True, nullable=False)
    custom_dictionary_id = Column(Integer,
                                  ForeignKey('custom_dictionary.id'),
                                  primary_key=True, nullable=False)


class CustomerWorkaround(IBISMain):
    __tablename__ = 'customer_workaround'

    workaround_id = Column(Integer,
                           ForeignKey('workaround.id'),
                           primary_key=True, nullable=False)

    customer_id = Column(Integer,
                         ForeignKey('customer.id'),
                         primary_key=True, nullable=False)


class AeFtp(IBISMain):
    __tablename__ = 'ae_ftp'

    application_entity_id = Column(Integer,
                                   ForeignKey('application_entity.id'),
                                   primary_key=True, nullable=False)

    ftp_connection_id = Column(Integer,
                               ForeignKey('ftp_connection.id'),
                               primary_key=True, nullable=False)


class AeIntegration(IBISMain):
    __tablename__ = 'ae_integration'

    application_entity_id = Column(Integer,
                                   ForeignKey('application_entity.id'),
                                   primary_key=True, nullable=False)

    integration_mode_id = Column(Integer,
                                 ForeignKey('integration_mode.id'),
                                 primary_key=True, nullable=False)


class TranslatorConfigDeviceVersionRequirement(IBISMain):
    __tablename__ = 'translator_config_device_version_requirement'

    translator_config_id = Column(
        Integer,
        ForeignKey('translator_config.id', ondelete='CASCADE'),
        primary_key=True, nullable=False)
    deviceversion_requirements_id = Column(
        Integer,
        ForeignKey(
            'device_version_requirement.id'),
        primary_key=True, nullable=False)


class ConnectivityPattern(IBISMain):
    __tablename__ = 'connectivity_pattern'

    connectivity_list_id = Column(
        Integer,
        ForeignKey(
            'connectivity_list.id', ondelete='CASCADE'),
        primary_key=True, nullable=False)

    message_pattern_id = Column(
        Integer,
        ForeignKey('message_pattern.id'),
        primary_key=True, nullable=False)


class ConnectivityFunctionality(IBISMain):
    __tablename__ = 'connectivity_functionality'

    connectivity_list_id = Column(
        Integer,
        ForeignKey(
            'connectivity_list.id', ondelete='CASCADE'),
        primary_key=True, nullable=False)

    dw_functionality_id = Column(
        Integer,
        ForeignKey('dw_functionality.id'),
        primary_key=True, nullable=False
    )


class Customer(IBISMain):
    __tablename__ = 'customer'
    __table_args__ = (
        UniqueConstraint('serial_number', 'revision_number', name='uq_cust'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    is_active = Column(Boolean, default=False)
    last_update = Column(DateTime)
    revision_number = Column(Integer)
    serial_number = Column(String(50), nullable=False)
    dosewatch_version = Column(String(50))
    serphylink_version = Column(String(50))
    customer_name = Column(String(255))
    project_type = Column(String(40))
    is_identified_agreement = Column(Boolean, default=False)
    is_important = Column(Boolean, default=False)
    project_manager = Column(String(50))
    application_specialist = Column(String(50))
    dictionary_version = Column(String(40))
    country = Column(String(40))
    pole = Column(String(10))
    worklist_enabled = Column(Boolean, default=False)
    decommissioning = Column(Boolean, default=False)
    iguana_channels = Column(Boolean, default=False)
    installation_date = Column(DateTime)
    state = Column(String(50))
    system_id = Column(String(150))
    town = Column(String(50))
    # location = Column(Geometry('POINT'))
    latitude = Column(Float)
    longitude = Column(Float)
    deal_type = Column(String(50))
    product_type = Column(String(20))
    is_last = Column(Boolean)
    is_monitored = Column(Boolean, default=False)

    custom_dictionaries = relationship(
        'CustomDictionary',
        secondary=CustomerDictionary.__tablename__,
        back_populates='customers')
    workarounds = relationship(
        'Workaround',
        secondary=CustomerWorkaround.__tablename__,
        back_populates='customers')


class CustomDictionary(IBISMain):
    __tablename__ = 'custom_dictionary'
    __table_args__ = (
        UniqueConstraint('local_id', 'code', 'description',
                         name='uq_cstm_dict'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    local_id = Column(Integer)
    code = Column(String(100))
    description = Column(String(255))

    customers = relationship('Customer',
                             secondary=CustomerDictionary.__tablename__,
                             back_populates='custom_dictionaries')


class Workaround(IBISMain):
    __tablename__ = 'workaround'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255))

    customers = relationship('Customer',
                             secondary=CustomerWorkaround.__tablename__,
                             back_populates='workarounds')


class FtpConnection(IBISMain):
    __tablename__ = 'ftp_connection'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    enabled = Column(Boolean, default=False)
    active_mode_enabled = Column(Boolean, default=False)
    ftp_secured = Column(Boolean, default=False)
    ip_address = Column(String(45))
    pass_phrase = Column(String(100))
    port = Column(SmallInteger)
    private_key = Column(String(100))
    data = Column(JSON)
    hash = Column(String(50), index=True)

    application_entity = relationship('ApplicationEntity',
                                      secondary=AeFtp.__tablename__,
                                      back_populates='ftp_connection')

    ignored_attributes = ['id', 'hash']


class SupportedDevice(IBISMain):
    __tablename__ = 'supported_device'

    id = Column(Integer, primary_key=True, nullable=False)
    is_deleted = Column(Boolean, default=False)
    manufacturer = Column(String(100))
    name = Column(String(100))
    type = Column(String(100))
    characteristics = Column(String(255))
    alternate_name = Column(String(255))
    last_update = Column(DateTime)

    ignored_attributes = ['id', 'last_update']


class ApplicationEntity(IBISMain):
    __tablename__ = 'application_entity'

    id = Column(Integer, primary_key=True)
    local_ae_id = Column(Integer)
    aet = Column(String(100))
    common_name = Column(String(100))
    contrast = Column(Boolean, default=False)
    ftp_connection_type = Column(String(50))
    data_type = Column(String(50))
    deleted = Column(Boolean, default=False)
    device = Column(String(100))
    device_type = Column(String(10))
    has_integration_request = Column(Boolean, default=False)
    ignored_sr_numbers = Column(String(255))
    image_translator = Column(String(70))
    ip = Column(String(45))
    last_updated = Column(DateTime)
    licensed = Column(Boolean, default=False)
    manufacturer = Column(String(100))
    message_type = Column(String(50))
    modality_worklist_enabled = Column(Boolean, default=False)
    mpps_series_duplicate_removal = Column(Boolean, default=False)
    port = Column(Integer)
    ris_ae_name = Column(String(50))
    screenshot_translator = Column(String(70))
    sdm_key = Column(Integer, nullable=False)
    secondary_data_type = Column(String(50))
    secondary_image_translator = Column(String(70))
    secondary_translator = Column(String(70))
    serial_number = Column(String(50), nullable=False)
    software_version = Column(String(255))
    station_name = Column(String(100))
    system_id = Column(String(50))
    tertiary_data_type = Column(String(50))
    tertiary_image_translator = Column(String(70))
    tertiary_translator = Column(String(70))
    translator = Column(String(70))
    update_type = Column(String(50))
    is_last = Column(Boolean)
    status = Column(String(1), default=ProcessingStatus.NEW.value)

    ignored_attributes = ['id', 'local_ae_id', 'has_integration_request',
                          'ignored_sr_numbers', 'last_updated', 'manufacturer',
                          'serial_number', 'station_name', 'system_id',
                          'update_type', 'is_last', 'status']

    ftp_connection = relationship('FtpConnection',
                                  secondary=AeFtp.__tablename__,
                                  back_populates='application_entity')
    integration_mode = relationship('IntegrationMode',
                                    secondary=AeIntegration.__tablename__,
                                    back_populates='application_entity')


class IntegrationMode(IBISMain):
    __tablename__ = 'integration_mode'
    __table_args__ = (
        UniqueConstraint('integration_mode', 'modality', name='uq_im'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    integration_mode = Column(String(100))
    modality = Column(String(20))

    ignored_attributes = ['id']

    application_entity = relationship('ApplicationEntity',
                                      secondary=AeIntegration.__tablename__,
                                      back_populates='integration_mode')


class TranslatorConfig(IBISMain):
    __tablename__ = 'translator_config'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    allow_mpps_series_duplicate_removal = Column(Boolean, default=False)
    contrast = Column(Boolean, default=False)
    data_type = Column(String(20))
    translator_id = Column(BigInteger)
    translator_default = Column(Boolean, default=False)
    translator_code = Column(String(70))
    deleted = Column(Boolean, default=False)
    device_name = Column(String(255))
    device_version = Column(String(50))
    dosewatch_lower_version_bound = Column(String(10))
    dosewatch_upper_version_bound = Column(String(10))
    integration_mode = Column(String(70))
    manufacturer = Column(String(100))
    modality = Column(String(20))
    image_translator_id = Column(BigInteger)
    image_translator_default = Column(Boolean, default=False)
    image_translator_code = Column(String(70))
    sdm_key = Column(Integer, ForeignKey('supported_device.id'))
    secondary_data_type = Column(String(30))
    secondary_translator_id = Column(BigInteger)
    secondary_translator_default = Column(Boolean, default=False)
    secondary_translator_code = Column(String(70))
    tertiary_data_type = Column(String(20))
    tertiary_translator_id = Column(BigInteger)
    tertiary_translator_default = Column(Boolean, default=False)
    tertiary_translator_code = Column(String(70))
    secondary_image_translator_id = Column(BigInteger)
    secondary_image_translator_default = Column(Boolean, default=False)
    secondary_image_translator_code = Column(String(70))
    tertiary_image_translator_id = Column(BigInteger)
    tertiary_image_translator_default = Column(Boolean, default=False)
    tertiary_image_translator_code = Column(String(70))
    update_date = Column(DateTime)

    ignored_attributes = ['id', 'update_date']

    device_version_requirement = relationship(
        'DeviceVersionRequirement',
        secondary=TranslatorConfigDeviceVersionRequirement.__tablename__,
        back_populates='translator_config')


class DeviceVersionRequirement(IBISMain):
    __tablename__ = 'device_version_requirement'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    value = Column(String(255))
    rule = Column(String(20))
    relation = Column(String(20), default=None)

    ignored_attributes = ['id']

    translator_config = relationship(
        'TranslatorConfig',
        secondary=TranslatorConfigDeviceVersionRequirement.__tablename__,
        back_populates='device_version_requirement')


class Study(IBISMain):
    __tablename__ = 'study'
    __table_args__ = (
        UniqueConstraint('serial_number', 'encrypted_siuid', name='uq_study'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    type = Column(String(30))
    measure_date = Column(DateTime)
    serial_number = Column(String(50))
    aet = Column(String(100))
    encrypted_siuid = Column(String(255))
    local_study_id = Column(Integer)
    software_version = Column(String(255))
    start_date = Column(DateTime)
    sdm_key = Column(Integer, ForeignKey('supported_device.id'))
    translator_code = Column(String(70))
    data = Column(JSON)
    image_translator_code = Column(String(70))
    status = Column(String(1), default=ProcessingStatus.NEW.value)
    reception_date = Column(DATETIME(fsp=3))

    ignored_attributes = ['id', 'reception_date']


class DicomPattern(IBISMain):
    __tablename__ = 'dicom_pattern'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    software_version = Column(String(255))
    message_command = Column(String(20))
    sop_class = Column(String(100))
    message_type = Column(String(25))
    series_number = Column(String(20))
    study_status = Column(String(20))
    message_status = Column(String(1))
    hash = Column(String(50), index=True)

    dicom_inputs = relationship('DicomInputPattern',
                                back_populates='dicom_pattern')

    ignored_attributes = ['id', 'hash']


class DicomInput(IBISMain):
    __tablename__ = 'dicom_input'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    measure_date = Column(DateTime)
    serial_number = Column(String(50))
    aet = Column(String(100))
    encrypted_siuid = Column(String(255))
    datetime_first_received = Column(DateTime)
    datetime_last_received = Column(DateTime)
    status = Column(String(1), default=ProcessingStatus.NEW.value)
    reception_date = Column(DATETIME(fsp=3))
    dicom_patterns = relationship('DicomInputPattern',
                                  back_populates='dicom_input')

    ignored_attributes = ['id', 'reception_date']


class DicomInputPattern(IBISMain):
    __tablename__ = 'dicom_input_pattern'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    dicom_input_id = Column('dicom_input_id', Integer,
                            ForeignKey('dicom_input.id', ondelete='CASCADE'),
                            primary_key=True, nullable=False)
    dicom_pattern_id = Column('dicom_pattern_id', Integer,
                              ForeignKey('dicom_pattern.id'),
                              primary_key=True, nullable=False)
    total_number_messages = Column(Integer)

    dicom_input = relationship('DicomInput', back_populates="dicom_patterns")
    dicom_pattern = relationship('DicomPattern', back_populates="dicom_inputs")

    ignored_attributes = ['id']


class InnovaLogPull(IBISMain):
    __tablename__ = 'innova_log_pull'
    __table_args__ = (
        UniqueConstraint('serial_number', 'aet', name='uq_innovalogpull'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    measure_date = Column(DateTime)
    serial_number = Column(String(50))
    aet = Column(String(100))
    local_ae_id = Column(Integer)
    nb_fail = Column(SmallInteger)
    datetime_first_fail = Column(DateTime)
    datetime_last_fail = Column(DateTime)
    datetime_last_pull = Column(DateTime)
    status = Column(
        String(1), default=ProcessingStatus.NEW.value, nullable=False)
    reception_date = Column(DATETIME(fsp=3))

    ignored_attributes = ['id', 'reception_date']


class CtLogPattern(IBISMain):
    __tablename__ = 'ct_log_pattern'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    measure_date = Column(DateTime)
    serial_number = Column(String(50))
    local_ae_id = Column(Integer)
    aet = Column(String(100))
    parent_message_key = Column(Integer)
    exam_number = Column(Integer)
    local_study_id = Column(Integer)
    datetime_first_insert = Column(DateTime)
    number_of_files = Column(SmallInteger)
    message_status = Column(SmallInteger)
    number_of_message_type = Column(SmallInteger)
    sum_exam_proto = Column(SmallInteger)
    sum_protocol_xml = Column(SmallInteger)
    sum_scan_request = Column(SmallInteger)
    sum_localizer = Column(SmallInteger)
    sum_image = Column(SmallInteger)
    sum_rdsr = Column(SmallInteger)
    sum_screenshot = Column(SmallInteger)
    sum_sr = Column(SmallInteger)
    sum_unknow = Column(SmallInteger)
    sum_screenshot_contrast = Column(SmallInteger)
    sum_prodiag_exam = Column(SmallInteger)
    sum_prodiag = Column(SmallInteger)
    sum_auto_ma = Column(SmallInteger)
    sum_wrong_file = Column(SmallInteger)
    status = Column(String(1), default=ProcessingStatus.NEW.value)
    reception_date = Column(DATETIME(fsp=3))

    ignored_attributes = ['id', 'reception_date']


class Status(IBISMain):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    status = Column(String(4), nullable=False)

    ignored_attributes = ['id']


class Rationale(IBISMain):
    __tablename__ = 'rationale'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    rationale = Column(String(15), nullable=False)

    ignored_attributes = ['id']


class ConnectivityList(IBISMain):
    __tablename__ = 'connectivity_list'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    supported_device_id = Column(Integer, ForeignKey('supported_device.id'))
    dosewatch_version = Column(String(50))
    integration_mode_id = Column(Integer, ForeignKey('integration_mode.id'))
    device_version = Column(String(255))
    revision_number = Column(Integer)
    priority = Column(Integer)
    difficulty = Column(String(20))
    last_update = Column(DateTime)

    ignored_attributes = ['id', 'last_update']

    messages_pattern = relationship(
        'MessagePattern',
        secondary=ConnectivityPattern.__tablename__,
        back_populates="connectivity_lists")

    functionalities = relationship(
        'DwFunctionality',
        secondary=ConnectivityFunctionality.__tablename__,
        back_populates="connectivity_lists")


class MessagePattern(IBISMain):
    __tablename__ = 'message_pattern'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    message_type = Column(String(50), unique=True)

    ignored_attributes = ['id']

    connectivity_lists = relationship(
        'ConnectivityList',
        secondary=ConnectivityPattern.__tablename__,
        back_populates="messages_pattern")


class DwFunctionality(IBISMain):
    __tablename__ = 'dw_functionality'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    functionality = Column(String(100), unique=True)

    ignored_attributes = ['id']

    connectivity_lists = relationship(
        'ConnectivityList',
        secondary=ConnectivityFunctionality.__tablename__,
        back_populates="functionalities")


class Dosimetric(IBISMain):
    __tablename__ = 'dosimetric'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    study_id = Column(Integer, ForeignKey('study.id', ondelete='CASCADE'))
    type = Column(String(25), nullable=False)
    status_id = Column(Integer, ForeignKey('status.id'))
    rationale_id = Column(Integer, ForeignKey('rationale.id'))
    value = Column(Numeric)

    ignored_attributes = ['id']


class InnovaLogPullStatus(IBISMain):
    __tablename__ = "innova_log_pull_status"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    innova_log_id = Column(Integer, ForeignKey(
        'innova_log_pull.id', ondelete='CASCADE'), nullable=False)
    status_id = Column(Integer, ForeignKey('status.id'))
    rationale_id = Column(Integer, ForeignKey('rationale.id'))


class CtLogPatternStatus(IBISMain):
    __tablename__ = "ct_log_pattern_status"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ct_log_pattern_id = Column(
        Integer, ForeignKey('ct_log_pattern.id', ondelete='CASCADE'))
    status_id = Column(Integer, ForeignKey('status.id'))
    rationale_id = Column(Integer, ForeignKey('rationale.id'))
    infered_integration_mode_id = Column(Integer)

    ignored_attributes = ['id']


class DicomInputStatus(IBISMain):
    __tablename__ = "dicom_input_status"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    dicom_input_id = Column(Integer,
                            ForeignKey('dicom_input.id', ondelete='CASCADE'))
    message_pattern_id = Column(Integer)
    dicom_pattern_id = Column(Integer)
    status_id = Column(Integer, ForeignKey('status.id'))
    rationale_id = Column(Integer, ForeignKey('rationale.id'))

    ignored_attributes = ['id']


class TranslatorConfigStatus(IBISMain):
    __tablename__ = "translator_config_status"
    __table_args__ = (
        UniqueConstraint('ae_id', name='uq_tcs_ae_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ae_id = Column(Integer, ForeignKey(
        'application_entity.id', ondelete='CASCADE'), nullable=False)
    rationale_id = Column(Integer, ForeignKey('rationale.id'))


class IntegrationModeMessageType(IBISMain):
    __tablename__ = "integration_mode_message_type"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    sdm_key = Column(Integer, primary_key=True)
    dw_v = Column(String(50), primary_key=True)
    im_id = Column(Integer, primary_key=True)
    im = Column(String(100), primary_key=True)
    message_type = Column(String(50), primary_key=True)
    modality = Column(String(20), primary_key=True)


class SpecificTranslator(IBISMain):
    __tablename__ = "specific_translator"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    specific_translator_id = Column(Integer)
    code = Column(String(255))
    description = Column(String(255))
    datatype = Column(String(10))
    is_image_translator = Column(String(1))
    modality = Column(String(10))
    parent_translator_key = Column(Integer)
    series_number = Column(String(100))
    constructor = Column(String(100))
    model = Column(String(100))
    software_release = Column(String(255))
    calculator_name = Column(String(255))
    version = Column(String(255))
    is_study_updator = Column(String(1), default=ProcessingStatus.NEW.value)
    computing_in_progress = Column(Boolean, default=False)
    deleting_study = Column(Boolean, default=False)


class SpecificTranslatorElement(IBISMain):
    __tablename__ = "specific_translator_element"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    specific_translator_element_id = Column(Integer, nullable=False)
    translator_key = Column(Integer)
    dictionary_element_key = Column(Integer)
    element_name = Column(String(255))
    formula = Column(String(255))
    formula_separator = Column(String(1), default=',')
    cumulated_value = Column(Numeric(8, 0), default=0)
    reference_element = Column(String(255))
    control_element = Column(Integer)
    reference_element_level = Column(Integer)
    is_ref_relative_path = Column(String(1))
    override_vr = Column(String(1))


customer_table = Customer._sa_class_manager.mapper.mapped_table
dosimetric_table = Dosimetric._sa_class_manager.mapper.mapped_table
cl_table = ConnectivityList._sa_class_manager.mapper.mapped_table
study_table = Study._sa_class_manager.mapper.mapped_table
translator_table = TranslatorConfig._sa_class_manager.mapper.mapped_table
app_table = ApplicationEntity._sa_class_manager.mapper.mapped_table
supdev_table = SupportedDevice._sa_class_manager.mapper.mapped_table
intmod_table = IntegrationMode._sa_class_manager.mapper.mapped_table
cusdic_table = CustomDictionary._sa_class_manager.mapper.mapped_table
intmmt_table = (IntegrationModeMessageType._sa_class_manager.mapper
                .mapped_table)


Index('idx_customer', customer_table.c.last_update,
      customer_table.c.revision_number,
      customer_table.c.serial_number,
      customer_table.c.customer_name,
      customer_table.c.is_last)
Index('idx_sn_islast', customer_table.c.serial_number,
      customer_table.c.is_last)

Index('idx_connectivity_list', cl_table.c.supported_device_id,
      cl_table.c.dosewatch_version,
      cl_table.c.device_version,
      cl_table.c.integration_mode_id)

Index('idx_dosimetric', dosimetric_table.c.study_id,
      dosimetric_table.c.type)

Index('idx_study', study_table.c.type,
      study_table.c.sdm_key,
      study_table.c.serial_number)
Index('idx_start', study_table.c.start_date)
Index('idx_sn_aet', study_table.c.aet,
      study_table.c.serial_number)
Index('idx_sn', study_table.c.serial_number)
Index('idx_siuid', study_table.c.encrypted_siuid)
Index('idx_sn_start_date', study_table.c.serial_number,
      study_table.c.start_date)

Index('idx_translator', translator_table.c.sdm_key,
      translator_table.c.data_type,
      translator_table.c.translator_code,
      translator_table.c.device_version,
      translator_table.c.integration_mode,
      translator_table.c.image_translator_code,
      translator_table.c.secondary_data_type,
      translator_table.c.secondary_translator_code)

Index('idx_ae_sr', app_table.c.serial_number,
      app_table.c.local_ae_id,
      app_table.c.is_last)
Index('idx_sn_islast', app_table.c.serial_number,
      app_table.c.is_last)
Index('idx_sn_aet_islast', app_table.c.serial_number,
      app_table.c.aet,
      app_table.c.is_last)

Index('idx_supported_device', supdev_table.c.manufacturer,
      supdev_table.c.name,
      supdev_table.c.type,
      supdev_table.c.id)

Index('idx_im', intmod_table.c.integration_mode,
      intmod_table.c.modality)

Index('idx_custom_dict', cusdic_table.c.local_id,
      cusdic_table.c.code,
      cusdic_table.c.description)

Index('idx_integration_mode_message_types', intmmt_table.c.sdm_key,
      intmmt_table.c.dw_v,
      intmmt_table.c.im_id,
      intmmt_table.c.im,
      intmmt_table.c.message_type,
      intmmt_table.c.modality)
