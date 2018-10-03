# -*- coding: utf-8 -*-
"""
ORM definition of database, each class defined here define a table in database
"""
from __future__ import absolute_import

import hashlib
import json

from sqlalchemy import *
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import \
    declarative_base as real_declarative_base
from sqlalchemy.orm import mapper, relationship, validates
from sqlalchemy.types import TypeDecorator

# JSON type for sqlalchemy

class JSONEncodedDict(TypeDecorator):
    """
    Represents an immutable structure as a json-encoded string.
    Usage::
        JSONEncodedDict()
    """
    impl = MEDIUMBLOB

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = bytes(json.dumps(value), 'utf-8')

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(str(value, 'utf-8'))
        return value


# Let's make this a class decorator
declarative_base = lambda cls: real_declarative_base(cls=cls)


@declarative_base
class Base(object):
    """
    Add some default properties and methods to the SQLAlchemy declarative base.
    """

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def tojson(self):
        return self.columnitems


class MappingBase(object):
    """
    Add some default properties and methods for mapping class.
    """

    def tojson(self):
        return self.__dict__


# ####### DECLARATIVE PART OF DATABASE


class CustomerDictionary(MappingBase):
    def __init__(self, customer_id, CustomDictionary_id):
        self.customer_id = customer_id
        self.customdictionary_id = CustomDictionary_id


assotable_customerdictionary = Table('customer_dictionary', Base.metadata,
                                     Column('customer_id', Integer, ForeignKey('customer.id'),
                                            primary_key=True, nullable=False),
                                     Column('customdictionary_id', Integer, ForeignKey('custom_dictionary.id'),
                                            primary_key=True, nullable=False))

mapper(CustomerDictionary, assotable_customerdictionary)


class CustomerWorkAround(MappingBase):
    def __init__(self, WorkAround_ID, Customer_ID):
        self.workaround_id = WorkAround_ID
        self.customer_id = Customer_ID


assotable_customerworkaround = Table('customer_workaround', Base.metadata,
                                     Column('workaround_id', Integer, ForeignKey('workaround.id'),
                                            primary_key=True, nullable=False),
                                     Column('customer_id', Integer, ForeignKey('customer.id'),
                                            primary_key=True, nullable=False))

mapper(CustomerWorkAround, assotable_customerworkaround)


class AE_FTP(MappingBase):
    def __init__(self, applicationEntity_id, FTPConnection_id):
        self.applicationentity_id = applicationEntity_id
        self.ftpconnection_id = FTPConnection_id


assotable_aeftp = Table('ae_ftp', Base.metadata,
                        Column('applicationentity_id', Integer, ForeignKey('application_entity.id'),
                               primary_key=True, nullable=False),
                        Column('ftpconnection_id', Integer, ForeignKey('ftp_connection.id'),
                               primary_key=True, nullable=False)
                        )

mapper(AE_FTP, assotable_aeftp)


class AE_Integration(MappingBase):
    def __init__(self, ApplicationEntity_ID, IntegrationMode_ID):
        self.applicationentity_id = ApplicationEntity_ID
        self.integrationmode_id = IntegrationMode_ID


assotable_aeintegration = Table('ae_integration', Base.metadata,
                                Column('applicationentity_id', Integer, ForeignKey('application_entity.id'),
                                       primary_key=True, nullable=False),
                                Column('integrationmode_id', Integer, ForeignKey('integration_mode.id'),
                                       primary_key=True, nullable=False)
                                )

mapper(AE_Integration, assotable_aeintegration)


class DicomInputPattern(Base):
    __tablename__ = 'dicom_input_pattern'

    dicominput_id = Column('dicominput_id', Integer, ForeignKey('dicom_input.id'),
                           primary_key=True, nullable=False)
    dicompattern_id = Column('dicompattern_id', Integer, ForeignKey('dicom_pattern.id'),
                             primary_key=True, nullable=False)
    total_number_messages = Column(Integer)

    dicominput = relationship('DicomInput', back_populates="dicom_patterns")
    dicompattern = relationship('DicomPattern', back_populates="dicom_inputs")


class TranslatorConfigDeviceVersionRequirement(MappingBase):
    def __init__(self, TranslatorConfig_ID, deviceVersionRequirement_ID):
        self.translatorconfig_id = TranslatorConfig_ID
        self.deviceversionrequirements_id = deviceVersionRequirement_ID


assotable_translatorconfigdeviceversionrequirement = Table('translator_config_device_version_requirement',
                                                           Base.metadata,
                                                           Column('translatorconfig_id', Integer,
                                                                  ForeignKey('translator_config.id'),
                                                                  primary_key=True, nullable=False
                                                                  ),
                                                           Column('deviceversionrequirements_id', Integer,
                                                                  ForeignKey('device_version_requirement.id'),
                                                                  primary_key=True, nullable=False)
                                                           )

mapper(TranslatorConfigDeviceVersionRequirement, assotable_translatorconfigdeviceversionrequirement)


class Connectivity_Pattern(MappingBase):
    def __init__(self, connectivity_list_id, message_pattern_id):
        self.connectivity_list_id = connectivity_list_id
        self.message_pattern_id = message_pattern_id


assotable_connectivitypattern = Table('connectivity_pattern', Base.metadata,
                                      Column('connectivity_list_id', Integer, ForeignKey('connectivity_list.id'),
                                             primary_key=True, nullable=False),
                                      Column('message_pattern_id', Integer, ForeignKey('message_pattern.id'),
                                             primary_key=True, nullable=False))

mapper(Connectivity_Pattern, assotable_connectivitypattern)


class Connectivity_Functionality(MappingBase):
    def __init__(self, connectivity_list_id, dwfunctionality_id):
        self.connectivity_list_id = connectivity_list_id
        self.dwfunctionality_id = dwfunctionality_id


assotable_connectivityfunct = Table('connectivity_functionality', Base.metadata,
                                    Column('connectivity_list_id', Integer, ForeignKey('connectivity_list.id'),
                                           primary_key=True, nullable=False),
                                    Column('dwfunctionality_id', Integer, ForeignKey('dwfunctionality.id'),
                                           primary_key=True, nullable=False))

mapper(Connectivity_Functionality, assotable_connectivityfunct)


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, nullable=False)
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

    custome_dictionarys = relationship('CustomeDictionary',
                                       secondary=assotable_customerdictionary,
                                       back_populates='customers')
    workarounds = relationship('WorkAround',
                               secondary=assotable_customerworkaround,
                               back_populates='customers')


class CustomeDictionary(Base):
    __tablename__ = 'custom_dictionary'

    id = Column(Integer, primary_key=True, nullable=False)
    local_id = Column(Integer)
    code = Column(String(100))
    description = Column(String(255))

    customers = relationship('Customer',
                             secondary=assotable_customerdictionary,
                             back_populates='custome_dictionarys')


class WorkAround(Base):
    __tablename__ = 'workaround'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255))

    customers = relationship('Customer',
                             secondary=assotable_customerworkaround,
                             back_populates='workarounds')


class FTPconnection(Base):
    __tablename__ = 'ftp_connection'

    id = Column(Integer, primary_key=True, nullable=False)
    enabled = Column(Boolean, default=False)
    active_mode_enabled = Column(Boolean, default=False)
    ftp_secured = Column(Boolean, default=False)
    ip_adress = Column(String(45))
    pass_phrase = Column(String(100))
    port = Column(Integer)
    private_key = Column(String(100))
    data = Column(JSONEncodedDict)
    hash = Column(String(50))

    @validates('private_key')
    def validate_code(self, key, value):
        max_len = getattr(self.__class__, key).prop.columns[0].type.length
        if value and len(value) > max_len:
            return value[:max_len]
        return value

    application_entity = relationship('ApplicationEntity',
                                      secondary=assotable_aeftp,
                                      back_populates='ftp_connection')

    def _hash(self):
        text = bytes(str(self.enabled).encode('utf-8') +
                     str(self.active_mode_enabled).encode('utf-8') +
                     str(self.ftp_secured).encode('utf-8') +
                     str(self.ip_adress).encode('utf-8') +
                     str(self.pass_phrase).encode('utf-8') +
                     str(self.port).encode('utf-8') +
                     str(self.private_key).encode('utf-8') +
                     str(sorted(self.data.items())).encode('utf-8'))
        return hashlib.md5(text).hexdigest()


class SupportedDevice(Base):
    __tablename__ = 'supported_device'

    id = Column(Integer, primary_key=True, nullable=False)
    is_deleted = Column(Boolean, default=False)
    manufacturer = Column(String(100))
    name = Column(String(100))
    type = Column(String(100))
    characteristics = Column(String(255))
    alternate_name = Column(String(255))
    last_update = Column(DateTime)


class ApplicationEntity(Base):
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
    status = Column(String(1), default='N')

    def _hash(self):
        text = bytes(str(self.aet).encode('utf-8') + str(self.common_name).encode('utf-8') +
                     str(self.contrast).encode('utf-8') + str(self.ftp_connection_type).encode('utf-8') +
                     str(self.data_type).encode('utf-8') + str(self.deleted).encode('utf-8') +
                     str(self.device).encode('utf-8') + str(self.device_type).encode('utf-8') +
                     str(self.image_translator).encode('utf-8') + str(self.ip).encode('utf-8') +
                     str(self.licensed).encode('utf-8') + str(self.message_type).encode('utf-8') +
                     str(self.modality_worklist_enabled).encode('utf-8') +
                     str(self.mpps_series_duplicate_removal).encode('utf-8') + str(self.port).encode('utf-8') +
                     str(self.ris_ae_name).encode('utf-8') + str(self.screenshot_translator).encode('utf-8') +
                     str(self.secondary_data_type).encode('utf-8') +
                     str(self.secondary_image_translator).encode('utf-8') +
                     str(self.secondary_translator).encode('utf-8') + str(self.software_version).encode('utf-8') +
                     str(self.tertiary_translator).encode('utf-8') + str(self.tertiary_data_type).encode('utf-8') +
                     str(self.tertiary_image_translator).encode('utf-8') + str(self.translator).encode('utf-8'))
        return hashlib.md5(text).hexdigest()

    ftp_connection = relationship('FTPconnection',
                                  secondary=assotable_aeftp,
                                  back_populates='application_entity')
    integration_mode = relationship('IntegrationMode',
                                    secondary=assotable_aeintegration,
                                    back_populates='application_entity')


class IntegrationMode(Base):
    __tablename__ = 'integration_mode'

    id = Column(Integer, primary_key=True, nullable=False)
    integration_mode = Column(String(100))
    modality = Column(String(20))

    application_entity = relationship('ApplicationEntity',
                                      secondary=assotable_aeintegration,
                                      back_populates='integration_mode')


class TranslatorConfig(Base):
    __tablename__ = 'translator_config'

    id = Column(Integer, primary_key=True, nullable=False)
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
    integration_mode = Column(String(50))
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

    device_version_requirement = relationship('DeviceVersionRequirement',
                                              secondary=assotable_translatorconfigdeviceversionrequirement,
                                              back_populates='translator_config')


class DeviceVersionRequirement(Base):
    __tablename__ = 'device_version_requirement'

    id = Column(Integer, primary_key=True, nullable=False)
    value = Column(String(255))
    rule = Column(String(20))
    relation = Column(String(20), default=None)

    translator_config = relationship('TranslatorConfig',
                                     secondary=assotable_translatorconfigdeviceversionrequirement,
                                     back_populates='device_version_requirement')


class Study(Base):
    __tablename__ = 'study'

    id = Column(Integer, primary_key=True, nullable=False)
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
    data = Column(JSONEncodedDict)
    image_translator_code = Column(String(70))
    status = Column(String(1), default='N')
    reception_date = Column(DateTime)

    def _data_hash(self):
        return hashlib.md5(bytes(str(json.dumps(self.data, sort_keys=True)).encode('utf-8'))).hexdigest()


class DicomPattern(Base):
    __tablename__ = 'dicom_pattern'

    id = Column(Integer, primary_key=True, nullable=False)
    software_version = Column(String(255))
    message_command = Column(String(20))
    sop_class = Column(String(100))
    message_type = Column(String(25))
    series_number = Column(String(20))
    study_status = Column(String(20))
    message_status = Column(String(1))
    hash = Column(String(50))

    dicom_inputs = relationship('DicomInputPattern',
                                back_populates='dicompattern')

    def _hash(self):
        text = bytes(str(self.software_version).encode('utf-8') +
                     str(self.message_command).encode('utf-8') +
                     str(self.sop_class).encode('utf-8') +
                     str(self.message_type).encode('utf-8') +
                     str(self.series_number).encode('utf-8') +
                     str(self.study_status).encode('utf-8') +
                     str(self.message_status).encode('utf-8'))
        return hashlib.md5(text).hexdigest()


class DicomInput(Base):
    __tablename__ = 'dicom_input'

    id = Column(Integer, primary_key=True, nullable=False)
    measure_date = Column(DateTime)
    serial_number = Column(String(50))
    aet = Column(String(100))
    station_name = Column(String(255))
    manufacturers_model_name = Column(String(512))
    encrypted_siuid = Column(String(255))
    datetime_first_received = Column(DateTime)
    datetime_last_received = Column(DateTime)
    status = Column(String(1), default='N')
    reception_date = Column(DateTime)
    dicom_patterns = relationship('DicomInputPattern',
                                  back_populates='dicominput')


class InnovaLogPull(Base):
    __tablename__ = 'innova_log_pull'

    id = Column(Integer, primary_key=True, nullable=False)
    measure_date = Column(DateTime)
    serial_number = Column(String(50))
    aet = Column(String(100))
    local_ae_id = Column(Integer)
    nb_fail = Column(SMALLINT(unsigned=True))
    datetime_first_fail = Column(DateTime)
    datetime_last_fail = Column(DateTime)
    datetime_last_pull = Column(DateTime)
    status = Column(String(1), default='N', nullable=False)
    reception_date = Column(DateTime)


class CTLogPattern(Base):
    __tablename__ = 'ct_log_pattern'

    id = Column(Integer, primary_key=True, nullable=False)
    measure_date = Column(DateTime)
    serial_number = Column(String(50))
    local_ae_id = Column(Integer)
    aet = Column(String(100))
    parent_message_key = Column(Integer)
    exam_number = Column(Integer)
    local_study_id = Column(Integer)
    patient_key = Column(Integer)
    datetime_first_insert = Column(DateTime)
    number_of_files = Column(SMALLINT(unsigned=True))
    message_status = Column(SMALLINT(unsigned=True))
    number_of_message_type = Column(SMALLINT(unsigned=True))
    sum_exam_proto = Column(SMALLINT(unsigned=True))
    sum_protocol_xml = Column(SMALLINT(unsigned=True))
    sum_scan_request = Column(SMALLINT(unsigned=True))
    sum_localizer = Column(SMALLINT(unsigned=True))
    sum_image = Column(SMALLINT(unsigned=True))
    sum_rdsr = Column(SMALLINT(unsigned=True))
    sum_screenshot = Column(SMALLINT(unsigned=True))
    sum_sr = Column(SMALLINT(unsigned=True))
    sum_unknow = Column(SMALLINT(unsigned=True))
    sum_screenshot_contrast = Column(SMALLINT(unsigned=True))
    sum_prodiag_exam = Column(SMALLINT(unsigned=True))
    sum_prodiag = Column(SMALLINT(unsigned=True))
    sum_auto_ma = Column(SMALLINT(unsigned=True))
    sum_wrong_file = Column(SMALLINT(unsigned=True))
    status = Column(String(1), default='N')
    reception_date = Column(DateTime)


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(4), nullable=False)


class Rational(Base):
    __tablename__ = 'rational'

    id = Column(Integer, primary_key=True, nullable=False)
    rational = Column(String(15), nullable=False)


class ConnectivityList(Base):
    __tablename__ = 'connectivity_list'

    id = Column(Integer, primary_key=True, nullable=False)
    supported_device_id = Column(Integer, ForeignKey('supported_device.id'))
    dosewatch_version = Column(String(50))
    integration_mode_id = Column(Integer, ForeignKey('integration_mode.id'))
    device_version = Column(String(255))
    revision_number = Column(Integer)
    priority = Column(Integer)
    difficulty = Column(String(20))
    last_update = Column(DateTime)

    messages_pattern = relationship('MessagePattern',
                                    secondary=assotable_connectivitypattern,
                                    back_populates="connectivity_lists")

    functionalities = relationship('DWFunctionality',
                                   secondary=assotable_connectivityfunct,
                                   back_populates="connectivity_lists")


class MessagePattern(Base):
    __tablename__ = 'message_pattern'

    id = Column(Integer, primary_key=True, nullable=False)
    message_type = Column(String(50), unique=True)

    connectivity_lists = relationship('ConnectivityList',
                                      secondary=assotable_connectivitypattern,
                                      back_populates="messages_pattern")


class DWFunctionality(Base):
    __tablename__ = 'dwfunctionality'

    id = Column(Integer, primary_key=True, nullable=False)
    functionality = Column(String(100), unique=True)

    connectivity_lists = relationship('ConnectivityList',
                                      secondary=assotable_connectivityfunct,
                                      back_populates="functionalities")


class Dosimetric(Base):
    __tablename__ = 'dosimetric'

    id = Column(Integer, primary_key=True, nullable=False)
    study_id = Column(Integer, ForeignKey('study.id'))
    type = Column(String(25), nullable=False)
    status_id = Column(Integer, ForeignKey('status.id'))
    rational_id = Column(Integer, ForeignKey('rational.id'))
    value = Column(DOUBLE)


class InnovalogpullStatus(Base):
    __tablename__ = "innovalogpull_status"

    innovalog_id = Column(Integer, ForeignKey('innova_log_pull.id'), primary_key=True)
    status_id = Column(Integer, ForeignKey('status.id'))
    rational_id = Column(Integer, ForeignKey('rational.id'))


class CtlogpatternStatus(Base):
    __tablename__ = "ctlogpattern_status"

    id = Column(Integer, primary_key=True, nullable=False)
    ctlogpattern_id = Column(Integer, ForeignKey('ct_log_pattern.id'))
    status_id = Column(Integer, ForeignKey('status.id'))
    rational_id = Column(Integer, ForeignKey('rational.id'))
    infered_integrationmode_id = Column(Integer)


class DicominputStatus(Base):
    __tablename__ = "dicominput_status"

    id = Column(Integer, primary_key=True, nullable=False)
    dicominput_id = Column(Integer, ForeignKey('dicom_input.id'))
    messagepattern_id = Column(Integer)
    dicompattern_id = Column(Integer)
    status_id = Column(Integer, ForeignKey('status.id'))
    rational_id = Column(Integer, ForeignKey('rational.id'))


class TranslatorconfigStatus(Base):
    __tablename__ = "translatorconfig_status"

    ae_id = Column(Integer, ForeignKey('application_entity.id'),primary_key=True)
    rational_id = Column(Integer, ForeignKey('rational.id'))


class IntegrationModeMessageTypes(Base):
    __tablename__ = "integrationmode_messagetypes"

    sdm_key = Column(Integer, primary_key=True)
    dw_v = Column(String, primary_key=True)
    im_id = Column(Integer, primary_key=True)
    im = Column(String, primary_key=True)
    message_type = Column(String, primary_key=True)
    modality = Column(String, primary_key=True)


class SpecificTranslator(Base):
    __tablename__ = "specific_translator"

    id = Column(Integer, primary_key=True)
    serial_number = Column(String(50))
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
    is_study_updator = Column(String(1), default='N')
    computing_in_progress = Column(Boolean, default=False)
    deleting_study = Column(Boolean, default=False)


class SpecificTranslatorElement(Base):
    __tablename__ = "specific_translator_element"

    id = Column(Integer, primary_key=True)
    serial_number = Column(String(50))
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
