# -*- coding: utf-8 -*-

import inspect
import re
from copy import copy

from sqlalchemy import case, delete, func, text, update
from sqlalchemy.orm.attributes import InstrumentedAttribute

from ge.bpmc.persistence.orm import (ExamORM, ExamStatusEnum, ExamStatusORM,
                                     ExamStatusTable, ExamTable, ImageMatchORM,
                                     ImageMetadataORM, ImageMetricsDisplayORM,
                                     ImageMetricsDisplayTable, ImageMetricsORM,
                                     ImageMetricsTable, ImageORM,
                                     ImageStatusEnum, ImageStatusORM,
                                     ImageStatusTable, ImageTable, IssuerORM,
                                     IssuerTable, LateralityEnum,
                                     ModalityTypeORM, ModalityTypeTable,
                                     PresentationIntentTypeEnum, ProcedureORM,
                                     ProcedureStatusEnum, ProcedureStatusORM,
                                     ProcedureStatusTable, ProcedureTable,
                                     RepositoryORM, RepositoryTable,
                                     SopClassORM, SopClassTable)
from ge.bpmc.utilities.sqlalchemy import sqlalchemy_get_unique_item_or_none

_ORM_CLASSES = [
    ExamORM, ExamStatusORM, ImageMatchORM, ImageMetadataORM,
    ImageMetricsDisplayORM, ImageMetricsORM, ImageORM, ImageStatusORM,
    IssuerORM, ModalityTypeORM, ProcedureORM, ProcedureStatusORM,
    RepositoryORM, SopClassORM
]

_ENUM_CLASSES = [
    LateralityEnum,
    ImageStatusEnum,
    PresentationIntentTypeEnum,
    ProcedureStatusEnum,
    ExamStatusEnum
]


def orm_attributes(class_):
    return [x[0] for x in
            filter(lambda x: isinstance(x[1], InstrumentedAttribute),
                   inspect.getmembers(class_))]


class BaseEntityManager:

    _session_ = None

    def __init__(self, logger, gateways):
        self._gateways_ = gateways
        self._logger_ = logger

    def init_session(self):
        self._session_ = self._gateways_.session()

    def close_session(self):
        if self._session_:
            self._session_.close()

    def add_obj(self, orm_class_, obj_values):
        """
        Utility to add an object in the database.
        Returns the updated object once added.

        Keyword arguments:
        orm_class_ -- SQLAlchemy mapped ORM class
        obj_values -- Dictionary of item attributes with their values.
        Used to updated the object
        """
        attrs = obj_values.items()
        filtered_attrs = dict(
            filter(lambda x: x[0] in orm_attributes(orm_class_),
                   attrs))
        filtered_attrs.update({'uid': None})
        obj = orm_class_(**dict(filtered_attrs))
        self._session_.add(obj)
        self._session_.flush()
        self._session_.refresh(obj)
        return copy(obj)

    def all_obj(self, orm_class_, is_eager=False):
        """
        Utility to get all objects from a certain class in the database.

        Keyword arguments:
        orm_class_ -- SQLAlchemy mapped ORM class
        is_eager -- Determines if an eager load is triggered or not
        """
        items = self._session_ \
                    .query(orm_class_) \
                    .enable_eagerloads(is_eager) \
                    .all()
        return [copy(x) for x in items]

    @sqlalchemy_get_unique_item_or_none
    def get_obj(self, orm_class_, obj_attribute, attribute_value,
                is_eager=False):
        """
        Utility to get a single object in the database.
        Returns the object if found or None thanks to the
        sqlalchemy_get_unique_item_or_none decorator. In case
        of multiple objects return, raises a
        sqlalchemy.orm.exc.MultipleResultsFound error.

        Keyword arguments:
        orm_class_ -- SQLAlchemy mapped ORM class
        obj_attribute -- The class attribute used to filter
        attribute_value -- The obj_attribute expected value
        is_eager -- Determines if an eager load is triggered or not
        """
        obj = self._session_ \
            .query(orm_class_) \
            .enable_eagerloads(is_eager) \
            .filter(getattr(orm_class_, obj_attribute) == attribute_value) \
            .one()
        return copy(obj)

    @sqlalchemy_get_unique_item_or_none
    def upd_obj(self, orm_class_, obj_attribute, attribute_value,
                obj_values, is_eager=False):
        """
        Utility to update an object in the database.
        Returns the object if found or None thanks to the
        sqlalchemy_get_unique_item_or_none decorator.

        Keyword arguments:
        orm_class_ -- SQLAlchemy mapped ORM class
        obj_attribute -- The class attribute used to filter
        attribute_value -- The obj_attribute expected value
        obj_values -- Dictionary of item attributes with their values.
        Used to updated the object
        """
        obj = self._session_ \
                  .query(orm_class_) \
                  .filter(
                      getattr(orm_class_, obj_attribute) == attribute_value) \
                  .enable_eagerloads(is_eager) \
                  .one()
        attrs = obj_values.items()
        filtered_attrs = dict(
            filter(lambda x: x[0] in orm_attributes(orm_class_),
                   attrs))
        for attr, value in filtered_attrs.items():
            setattr(obj, attr, value)
        self._session_.flush()
        self._session_.refresh(obj)
        return copy(obj)

    def del_obj(self, orm_class_, obj_attribute, attribute_value):
        """
        Utility to delete an object in the database.

        Keyword arguments:
        orm_class_ -- SQLAlchemy mapped ORM class
        obj_attribute -- The table attribute used to filter
        attribute_value -- The obj_attribute expected value
        """
        table_column = getattr(
            orm_class_._sa_class_manager.mapper.mapped_table.c, obj_attribute)
        stmt = delete(orm_class_).where(table_column == attribute_value)
        self._session_.execute(stmt)


def crud_function_factory(ftype, orm_class_):
    if ftype is 'create':
        return lambda self, obj_values: self.add_obj(
            orm_class_, obj_values)
    elif ftype is 'get':
        return lambda self, attr, attr_value, is_eager=False: self.get_obj(
            orm_class_, attr, attr_value, is_eager)
    elif ftype is 'update':
        return lambda self, attr, attr_value, obj_values, is_eager=False: \
            self.upd_obj(orm_class_, attr, attr_value, obj_values, is_eager)
    elif ftype is 'delete':
        return lambda self, attr, attr_value: \
            self.del_obj(orm_class_, attr, attr_value)
    elif ftype is 'all':
        return lambda self, is_eager=False: \
            self.all_obj(orm_class_, is_eager)


def in_enum_function_factory(enum_class_):
    return lambda self, value: value in \
        [x.value for x in enum_class_.__members__.values()]


def generate_crud_methods(entity_class_):
    for orm_class_ in _ORM_CLASSES:
        item = re.sub(r'([A-Z])',
                      lambda x: '_' + x.group(1).lower(),
                      orm_class_.__name__.replace('ORM', ''))
        setattr(entity_class_, 'add%s' % item,
                crud_function_factory('create', orm_class_))
        setattr(entity_class_, 'all%s' % item,
                crud_function_factory('all', orm_class_))
        setattr(entity_class_, 'get%s' % item,
                crud_function_factory('get', orm_class_))
        setattr(entity_class_, 'upd%s' % item,
                crud_function_factory('update', orm_class_))
        setattr(entity_class_, 'del%s' % item,
                crud_function_factory('delete', orm_class_))


def generate_in_enum_methods(entity_class_):
    for enum_class_ in _ENUM_CLASSES:
        item = re.sub(r'([A-Z])',
                      lambda x: '_' + x.group(1).lower(),
                      enum_class_.__name__.replace('Enum', ''))

        setattr(entity_class_, 'in%s' % item,
                in_enum_function_factory(enum_class_))


ORMEntityManager = type(
    'ORMEntityManager', BaseEntityManager.__bases__,
    dict(BaseEntityManager.__dict__))
generate_crud_methods(ORMEntityManager)
generate_in_enum_methods(ORMEntityManager)


class BPMEntityManager(ORMEntityManager):

    def get_available_repository(self, blacklist=None):
        """
        Returns a Repository with an available status.

        Keyword arguments:
        blacklist -- A list of Repository uids to ignore
        """
        default = self._session_ \
            .query(RepositoryORM) \
            .enable_eagerloads(False) \
            .filter(getattr(RepositoryORM, 'available').is_(True))
        if blacklist:
            default = default.filter(RepositoryORM.uid.notin_(blacklist))
        return default.limit(1).first()

    def get_image_repository(self, image_uid):
        """
        Returns the repository uid based on the image uid

        Keyword arguments:
        image_uid -- Int, an Image uid
        """
        image = self.get_image('uid', image_uid)
        return self.get_repository('uid', image.repository_uid) \
            if image else None

    def get_metrics_image_repository(self, image_uid):
        """
        Returns the repository uid based on the image uid

        Keyword arguments:
        image_uid -- Int, a metrics image uid
        """
        image = self.get_image_metrics_display('uid', image_uid)
        return self.get_repository('uid', image.repository_uid) \
            if image else None

    @sqlalchemy_get_unique_item_or_none
    def get_modality_type_by_unicity(self, model, version, manufacturer):
        """
        Get a Modality type by its unicity parameters.

        Keyword arguments:
        model -- String, model name
        version -- String, software version
        manufacturer -- String, manufacturer name
        """
        return self._session_ \
            .query(ModalityTypeORM) \
            .enable_eagerloads(False) \
            .filter(ModalityTypeORM.model_name == model) \
            .filter(ModalityTypeORM.software_version == version) \
            .filter(ModalityTypeORM.manufacturer_name == manufacturer).one()

    def get_or_create_modality_type(self, model, version, manufacturer):
        """
        Get or creates a Modality type.

        Keyword arguments:
        model -- String, model name
        version -- String, software version
        manufacturer -- String, manufacturer name
        """
        return self.get_modality_type_by_unicity(model, version, manufacturer)\
            or self.add_modality_type(
                {'model_name': model,
                 'software_version': version,
                 'manufacturer_name': manufacturer})

    def get_or_create_sop_class(self, sop_class_identifier):
        """
        Get or creates a SopClass.

        Keyword arguments:
        sop_class_identifier -- String, sop_class_identifier
        """
        return self.get_sop_class('sop_class_identifier',
                                  sop_class_identifier) or \
            self.add_sop_class({'sop_class_identifier': sop_class_identifier})

    def get_or_create_exam(self, exam_uid, issuer_uid):
        """
        Get or creates an Exam.

        Keyword arguments:
        exam_uid -- Int, an Exam uid
        issuer_uid -- Int, an Issuer uid
        """
        return (self.get_exam('uid', exam_uid) or
                self.add_exam({'issuer_uid': issuer_uid}))

    def get_or_create_exam_status(self, exam_uid, status):
        """
        Get or create exam status.

        Keyword arguments:
        exam_uid -- Int, an Exam uid
        status -- Str, an exam status
        """
        return (self.get_exam_status('exam_uid', exam_uid) or
                self.add_exam_status({'exam_uid': exam_uid,
                                      'status': status}))

    def get_or_create_procedure(self, procedure_uid, exam_uid):
        """
        Get or creates a Procedure.

        Keyword arguments:
        procedure_uid -- Int, a Procedure uid
        exam_uid -- Int, an Exam uid
        """
        return (self.get_procedure('uid', procedure_uid) or
                self.add_procedure({'exam_uid': exam_uid}))

    def get_or_create_procedure_status(self, procedure_uid, status):
        """
        Get or create procedure status.

        Keyword arguments:
        procedure_uid -- Int, a Procedure uid
        status -- Str, a procedure status
        """
        return (self.get_procedure_status('procedure_uid', procedure_uid) or
                self.add_procedure_status({'procedure_uid': procedure_uid,
                                           'status': status}))

    def get_image_matches(self, origin_uid):
        """
        Gets matched images uids for a specific origin.

        Keyword arguments:
        origin_uid -- Int, an ImageMatchORM origin
        """
        return [x[0] for x in (
            self._session_
            .query(ImageMatchORM.destination)
            .filter(ImageMatchORM.origin == origin_uid)).all()]
