# -*- coding: utf-8 -*-

import logging
import re
from copy import copy

from sqlalchemy import case, delete, func, text, update

from .application import (AeFtp, AeIntegration, ApplicationEntity,
                          ConnectivityFunctionality, ConnectivityList,
                          ConnectivityPattern, CtLogPattern,
                          CtLogPatternStatus, CustomDictionary, Customer,
                          CustomerDictionary, CustomerWorkaround,
                          DeviceVersionRequirement, DicomInput,
                          DicomInputPattern, DicomInputStatus, DicomPattern,
                          Dosimetric, DwFunctionality, FtpConnection,
                          InnovaLogPull, InnovaLogPullStatus, IntegrationMode,
                          IntegrationModeMessageType, MessagePattern,
                          Rationale, SpecificTranslator,
                          SpecificTranslatorElement, Status, Study,
                          SupportedDevice, TranslatorConfig,
                          TranslatorConfigDeviceVersionRequirement,
                          TranslatorConfigStatus, Workaround)
from .datamarts import (CtLogLast15Days, DevicesOverview, DosimetricLast15Days,
                        PatternLast15Days, StudyDataSource)
from .utilities import filter_attributes

_ORM_CLASSES = [
    AeFtp, AeIntegration, ApplicationEntity,
    ConnectivityFunctionality, ConnectivityPattern,
    ConnectivityList, CtLogPattern, CtLogPatternStatus,
    CustomDictionary, Customer, CustomerDictionary,
    CustomerWorkaround, DeviceVersionRequirement,
    DicomInput, DicomInputPattern, DicomInputStatus,
    DicomPattern, Dosimetric, DwFunctionality,
    FtpConnection, InnovaLogPull, InnovaLogPullStatus,
    IntegrationMode, IntegrationModeMessageType,
    MessagePattern, Rationale, SpecificTranslator,
    SpecificTranslatorElement, Status, Study,
    SupportedDevice, TranslatorConfig,
    TranslatorConfigDeviceVersionRequirement,
    TranslatorConfigStatus, Workaround,
    CtLogLast15Days, DevicesOverview, DosimetricLast15Days,
    PatternLast15Days, StudyDataSource
]


class BaseEntityManager:

    def __init__(self, logger, session=None):
        self._logger = logger
        self._session = session
        self._reset_auto_increment_ = 'ALTER TABLE {table} AUTO_INCREMENT=1'

    def update_session(self, session):
        self._session = session
        return self

    def _query_add_filters(self, orm_class_, query, filters):
        for attribute, value in filters:
            if isinstance(value, (list, tuple)):
                query = query.filter(getattr(orm_class_, attribute).in_(value))
            else:
                query = query.filter(getattr(orm_class_, attribute) == value)
        return query

    def _statement_add_filters(self, orm_table, query, filters):
        for attribute, value in filters:
            if isinstance(value, (list, tuple)):
                query = query.where(getattr(orm_table.c, attribute).in_(value))
            else:
                query = query.where(getattr(orm_table.c, attribute) == value)
        return query

    def repr_obj(self, orm_class_, obj_values):
        """
        Utility to represent an object instanciated with valid attributes
        from obj_values dict.

        :param orm_class_: SQLAlchemy mapped ORM class
        :param obj_values: Dictionary of item attributes with their values
        used to update the object.
        :return: Orm object as dict
        """
        attrs = obj_values.items()
        filtered_attrs = filter_attributes(orm_class_, attrs)
        obj = orm_class_.from_dict(dict(filtered_attrs))
        return obj.tojson()

    def add_obj(self, orm_class_, obj_values, keep_context=False):
        """
        Utility to add an object in the database.
        Returns the updated object once added.

        :param orm_class_: SQLAlchemy mapped ORM class
        :param obj_values: Dictionary of item attributes with their values
        used to update the object.
        :param keep_context: Wether to keep the SQLAlchemy context or not
        :return: Orm object with or without SQLAlchemy context
        """
        attrs = obj_values.items()
        filtered_attrs = filter_attributes(orm_class_, attrs)
        obj = orm_class_.from_dict(dict(filtered_attrs))
        self._session.add(obj)
        self._session.flush()
        self._session.refresh(obj)
        self._logger.debug('Inserted object %s with id %d' % (
            orm_class_, obj.id))
        return copy(obj) if not keep_context else obj

    def bulk_add_obj(self, orm_class_, obj_values):
        """
        Utility to add an object in the database.
        Returns the updated object once added.

        :param orm_class_: SQLAlchemy mapped ORM class
        :param obj_values: List of dictionaries of item attributes with their
        values used to create the object.
        :param keep_context: Wether to keep the SQLAlchemy context or not
        :return: void
        """
        filtered_mappings = [filter_attributes(orm_class_, x.items())
                             for x in obj_values]
        self._session.bulk_insert_mappings(orm_class_, filtered_mappings)
        self._logger.debug('Inserted %i %s objects' % (
            len(filtered_mappings), orm_class_))
        return

    def all_obj(self, orm_class_, *filters,
                is_eager=False, keep_context=False):
        """
        Utility to get all objects from a certain class in the database.

        :param orm_class_: SQLAlchemy mapped ORM class
        :param filters: multiple tuples with the object attribute use to search
        and the expected value
        :param is_eager: Determines if an eager load is triggered or not
        :param keep_context: Wether to keep the SQLAlchemy context or not
        :return: List of orm objects with or without their context
        """
        query = self._session \
                    .query(orm_class_) \
                    .enable_eagerloads(is_eager)
        query = self._query_add_filters(orm_class_, query, filters)
        return [(copy(x) if not keep_context else x) for x in query.all()]

    def get_obj(self, orm_class_, *filters,
                is_eager=False, keep_context=False):
        """
        Utility to get a single object in the database.
        Returns the object if found or None. In case of multiple objects
        returned, raises a sqlalchemy.orm.exc.MultipleResultsFound error.

        :param orm_class_: SQLAlchemy mapped ORM class
        :param filters: multiple tuples with the object attribute use to search
        and the expected value
        :param is_eager: Determines if an eager load is triggered or not
        :param keep_context: Wether to keep the SQLAlchemy context or not
        :return: Orm object with or without SQLAlchemy context
        """
        query = self._session \
            .query(orm_class_) \
            .enable_eagerloads(is_eager)
        query = self._query_add_filters(orm_class_, query, filters)
        obj = query.one_or_none()
        return copy(obj) if not keep_context else obj

    def hash_obj(self, orm_class_, obj_values):
        """
        Returns the ORM object hash for a dict of values

        :return: hash (str)
        """
        attrs = obj_values.items()
        filtered_attrs = filter_attributes(orm_class_, attrs)
        self._logger.debug('Hash object %s' % (orm_class_))
        return orm_class_.hash_from_dict(filtered_attrs)

    def upd_obj(self, orm_class_, *filters,
                values={}, is_eager=False, keep_context=False):
        """
        Utility to update an object in the database.
        Returns the object if found or None.

        :param orm_class_: SQLAlchemy mapped ORM class
        :param filters: multiple tuples with the object attribute use to search
        and the expected value
        :param values: Dictionary of item attributes with their values
        used to update the object
        :param is_eager: Determines if an eager load is triggered or not
        :param keep_context: Wether to keep the SQLAlchemy context or not
        :return: Orm object with or without SQLAlchemy context
        """
        query = self._session \
            .query(orm_class_) \
            .enable_eagerloads(is_eager)
        query = self._query_add_filters(orm_class_, query, filters)
        obj = query.one_or_none()
        attrs = values.items()
        filtered_attrs = filter_attributes(orm_class_, attrs)
        for attr, value in filtered_attrs.items():
            setattr(obj, attr, value)
        self._session.flush()
        self._session.refresh(obj)
        self._logger.debug('Updated object %s with id %d' %
                           (orm_class_, obj.id))
        return copy(obj) if not keep_context else obj

    def bulk_upd_obj(self, orm_class_, *filters, obj_values={}):
        """
        Utility to update an object in the database.
        Returns the object if found or None.

        :param orm_class_: SQLAlchemy mapped ORM class
        :param filters: multiple tuples with the object attribute use to search
        and the expected value
        :param obj_values: Dictionary of item attributes with their values
        used to update the object
        :return:
        """
        attrs = obj_values.items()
        filtered_attrs = filter_attributes(orm_class_, attrs)
        orm_table = orm_class_._sa_class_manager.mapper.mapped_table
        query = update(orm_table)
        query = self._statement_add_filters(orm_table, query, filters)
        query = query.values(**filtered_attrs)
        self._session.execute(query)
        self._session.flush()
        self._logger.debug('Updated all objects %s using filters %s' %
                           (orm_class_, filters))

    def del_obj(self, orm_class_, *filters):
        """
        Utility to delete an object in the database.

        :param orm_class_: SQLAlchemy mapped ORM class
        :param filters: multiple tuples with the object attribute use to search
        and the expected value
        """
        orm_table = orm_class_._sa_class_manager.mapper.mapped_table
        query = delete(orm_class_)
        query = self._statement_add_filters(orm_table, query, filters)
        self._session.execute(query)
        self._session.flush()

    def truncate_obj(self, orm_class_):
        """
        Utility to truncate the associated table

        :param orm_class_: SQLAlchemy mapped ORM class
        """
        table = orm_class_._sa_class_manager.mapper.mapped_table.name
        # We use delete because truncate cannot be run if table has FKs
        self._session.query(orm_class_).delete()
        stmt = self._reset_auto_increment_.format(**{'table': table})
        self._session.execute(stmt)
        self._logger.debug('TRUNCATED TABLE %s' % (table))


def crud_function_factory(ftype, orm_class_):
    if ftype == 'repr':
        return lambda self, obj_values: self.repr_obj(
            orm_class_, obj_values)
    elif ftype == 'add':
        return lambda self, obj_values, keep_context=False: self.add_obj(
            orm_class_, obj_values, keep_context)
    elif ftype == 'bulk_add':
        return lambda self, obj_values: self.bulk_add_obj(
            orm_class_, obj_values)
    elif ftype == 'get':
        return lambda self, *filters, is_eager=False, \
            keep_context=False: self.get_obj(
                orm_class_, *filters, is_eager=is_eager,
                keep_context=keep_context)
    elif ftype == 'update':
        return lambda self, *filters, values={}, is_eager=False, \
            keep_context=False: self.upd_obj(
                orm_class_, *filters, values=values, is_eager=is_eager,
                keep_context=keep_context)
    elif ftype == 'bulk_update':
        return lambda self, *filters, obj_values={}: self.bulk_upd_obj(
            orm_class_, *filters, obj_values=obj_values)
    elif ftype == 'delete':
        return lambda self, *filters: \
            self.del_obj(orm_class_, *filters)
    elif ftype == 'all':
        return lambda self, *filters, is_eager=False, keep_context=False: \
            self.all_obj(orm_class_, *filters,
                         is_eager=is_eager, keep_context=keep_context)
    elif ftype == 'hash':
        return lambda self, obj_values: \
            self.hash_obj(orm_class_, obj_values)
    elif ftype == 'truncate':
        return lambda self: self.truncate_obj(orm_class_)


def generate_crud_methods(entity_class_):
    for orm_class_ in _ORM_CLASSES:
        item = re.sub(r'([A-Z])',
                      lambda x: '_' + x.group(1).lower(),
                      orm_class_.__name__.replace('ORM', ''))

        setattr(entity_class_, 'repr%s' % item,
                crud_function_factory('repr', orm_class_))
        setattr(entity_class_, 'add%s' % item,
                crud_function_factory('add', orm_class_))
        setattr(entity_class_, 'bulk_add%s' % item,
                crud_function_factory('bulk_add', orm_class_))
        setattr(entity_class_, 'hash%s' % item,
                crud_function_factory('hash', orm_class_))
        setattr(entity_class_, 'all%s' % item,
                crud_function_factory('all', orm_class_))
        setattr(entity_class_, 'get%s' % item,
                crud_function_factory('get', orm_class_))
        setattr(entity_class_, 'upd%s' % item,
                crud_function_factory('update', orm_class_))
        setattr(entity_class_, 'bulk_upd%s' % item,
                crud_function_factory(
                    'bulk_update', orm_class_))
        setattr(entity_class_, 'del%s' % item,
                crud_function_factory('delete', orm_class_))
        setattr(entity_class_, 'truncate%s' % item,
                crud_function_factory('truncate', orm_class_))


GeneratedEntityManager = type(
    'GeneratedEntityManager', BaseEntityManager.__bases__,
    dict(BaseEntityManager.__dict__))
generate_crud_methods(GeneratedEntityManager)


class IBISEntityManager(GeneratedEntityManager):

    def get_customer_by_attrs(
            self, serial_number, revision_number):
        return (self._session.query(Customer)
                .filter(Customer.serial_number == serial_number)
                .filter(Customer.revision_number == revision_number)
                .one_or_none())

    def get_custom_dictionary_by_attrs(self, local_id, code, description):
        return (self._session.query(CustomDictionary)
                .filter(CustomDictionary.local_id == local_id)
                .filter(CustomDictionary.code == code)
                .filter(CustomDictionary.description == description)
                .one_or_none())

    def get_im_by_attrs(self, integration_mode, modality):
        return (self._session.query(IntegrationMode)
                .filter(IntegrationMode.integration_mode == integration_mode)
                .filter(IntegrationMode.modality == modality).one_or_none())

    def get_innovalogpull_by_attrs(self, serial_number, aet):
        return (self._session.query(InnovaLogPull)
                .filter(InnovaLogPull.serial_number == serial_number)
                .filter(InnovaLogPull.aet == aet).one_or_none())

    def get_last_application_entity_by_attrs(self, local_ae_id, serial_number):
        return (self._session.query(ApplicationEntity)
                .filter(ApplicationEntity.local_ae_id == local_ae_id)
                .filter(ApplicationEntity.serial_number == serial_number)
                .filter(ApplicationEntity.is_last.is_(True)).one_or_none())

    def get_last_customer_by_serial(self, serial_number):
        return (self._session.query(Customer)
                .filter(Customer.serial_number == serial_number)
                .filter(Customer.is_last.is_(True)).one_or_none())

    def get_previous_customer_revision_by_serial(
            self, serial_number, revision_number):
        return (self._session.query(Customer)
                .filter(Customer.serial_number == serial_number)
                .filter(Customer.revision_number == (revision_number - 1))
                .one_or_none())

    def get_study_by_attrs(self, serial_number, encrypted_siuid):
        return (self._session.query(Study)
                .filter(Study.serial_number == serial_number)
                .filter(Study.encrypted_siuid == encrypted_siuid)
                .one_or_none())

    def get_dvr_by_values(self, rule, value, relation):
        return self._session.query(DeviceVersionRequirement).filter(
            DeviceVersionRequirement.rule == rule,
            DeviceVersionRequirement.value == value,
            DeviceVersionRequirement.relation == relation).one_or_none()

    def upd_customer_monitor_flag(self, serial_number, value):
        return (self._session.query(Customer)
                .filter(Customer.serial_number == serial_number)
                .filter(Customer.is_last.is_(True))
                .update({'is_monitored': value}))

    def del_study_related_dosimetric(self, study_id):
        return (self._session.query(Dosimetric)
                .filter(Dosimetric.study_id == study_id)
                .delete())
