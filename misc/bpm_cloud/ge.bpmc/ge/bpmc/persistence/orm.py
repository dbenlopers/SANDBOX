# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import enum

from sqlalchemy import *
from sqlalchemy.orm import mapper, relationship

metadata = MetaData()

BPMC_COLL = 'utf8_bin'


class DictBase(object):

    __ignored_keys = ['_sa_instance_state']

    def to_dict(self):
        return dict([(k, v) for k, v in self.__dict__.items()
                     if k not in self.__ignored_keys])

# -------- Enums --------


class LateralityEnum(enum.Enum):
    Right = 'R'
    Left = 'L'
    Both = 'B'
    Unpaired = 'U'


class ExamStatusEnum(enum.Enum):
    Waiting = 'W'
    Processed = 'P'
    Done = 'D'
    Error = 'E'


class ProcedureStatusEnum(enum.Enum):
    Waiting = 'W'
    Closed = 'C'
    Processed = 'P'
    Done = 'D'
    Error = 'E'


class ImageStatusEnum(enum.Enum):
    Waiting = 'W'
    Processed = 'P'
    Invalid = 'I'
    Error = 'E'


class PresentationIntentTypeEnum(enum.Enum):
    PROCESSING = 'FOR PROCESSING'
    PRESENTATION = 'FOR PRESENTATION'

# -------- ORM Objects --------


class RepositoryORM(DictBase):
    def __init__(self, uid, name, host, use_ssl=False, available=True):
        self.uid = uid
        self.name = name
        self.host = host
        self.use_ssl = use_ssl
        self.available = available


class IssuerORM(DictBase):
    def __init__(self, uid, identifier, key):
        self.uid = uid
        self.identifier = identifier
        self.key = key


class ExamORM(DictBase):
    def __init__(self, uid, issuer_uid):
        self.uid = uid
        self.issuer_uid = issuer_uid


class ExamStatusORM(DictBase):
    def __init__(self, uid, exam_uid, sent=0,
                 status=ExamStatusEnum.Waiting.value):
        self.uid = uid
        self.exam_uid = exam_uid
        self.sent = sent
        self.status = status


class ProcedureORM(DictBase):
    def __init__(self, uid, exam_uid):
        self.uid = uid
        self.exam_uid = exam_uid


class ProcedureStatusORM(DictBase):
    def __init__(self, uid, procedure_uid, ready=0, sent=0,
                 status=ProcedureStatusEnum.Waiting.value):
        self.uid = uid
        self.procedure_uid = procedure_uid
        self.ready = ready
        self.sent = sent
        self.status = status


class SopClassORM(DictBase):
    def __init__(self, uid, sop_class_identifier):
        self.uid = uid
        self.sop_class_identifier = sop_class_identifier


class ImageORM(DictBase):
    def __init__(
            self, uid, procedure_uid, repository_uid, modality_type_uid,
            sop_class_uid, metadata_uid, inserted_on):
        self.uid = uid
        self.procedure_uid = procedure_uid
        self.repository_uid = repository_uid
        self.modality_type_uid = modality_type_uid
        self.sop_class_uid = sop_class_uid
        self.metadata_uid = metadata_uid
        self.inserted_on = inserted_on


class ModalityTypeORM(DictBase):
    def __init__(self, uid, model_name, software_version, manufacturer_name):
        self.uid = uid
        self.model_name = model_name
        self.software_version = software_version
        self.manufacturer_name = manufacturer_name


class ImageMatchORM(DictBase):
    def __init__(self, uid, origin, destination):
        self.uid = uid
        self.origin = origin
        self.destination = destination


class ImageMetadataORM(DictBase):
    def __init__(self, uid, breast_implant_present, image_laterality,
                 acquisition_time, processing_data, view_position,
                 compression_force=None, size_of_return_rows=None,
                 size_of_return_columns=None, extra=None):
        self.uid = uid
        self.breast_implant_present = breast_implant_present
        self.image_laterality = image_laterality
        self.acquisition_time = acquisition_time
        self.processing_data = processing_data
        self.view_position = view_position
        self.compression_force = compression_force
        self.size_of_return_rows = size_of_return_rows
        self.size_of_return_columns = size_of_return_columns
        self.extra = extra


class ImageStatusORM(DictBase):
    def __init__(self, uid, image_uid, ready, status):
        self.uid = uid
        self.image_uid = image_uid
        self.ready = ready
        self.status = status


class ImageMetricsORM(DictBase):
    def __init__(self, uid, image_uid, criteria, overlay):
        self.uid = uid
        self.image_uid = image_uid
        self.criteria = criteria
        self.overlay = overlay


class ImageMetricsDisplayORM(DictBase):
    def __init__(self, uid, image_metrics_uid, repository_uid):
        self.uid = uid
        self.image_metrics_uid = image_metrics_uid
        self.repository_uid = repository_uid

# -------- ORM Tables --------


RepositoryTable = Table('repository', metadata,
                        Column('uid', Integer, primary_key=True,
                               autoincrement=True),
                        Column('name', String(30, collation=BPMC_COLL),
                               nullable=False),
                        Column('host', String(50, collation=BPMC_COLL),
                               nullable=False),
                        Column('use_ssl', Boolean, default=False,
                               nullable=False),
                        Column('available', Boolean, default=True,
                               nullable=False, index=True),
                        UniqueConstraint('name'),
                        UniqueConstraint('host')
                        )

IssuerTable = Table('issuer', metadata,
                    Column('uid', BigInteger, primary_key=True,
                           autoincrement=True),
                    Column('identifier', String(50, collation=BPMC_COLL),
                           nullable=False),
                    Column('key', String(255, collation=BPMC_COLL),
                           nullable=False, index=True),
                    UniqueConstraint('identifier'),
                    UniqueConstraint('key')
                    )

ExamTable = Table('exam', metadata,
                  Column('uid', BigInteger, primary_key=True,
                         autoincrement=True),
                  Column('issuer_uid', BigInteger,
                         ForeignKey('issuer.uid'),
                         nullable=False),
                  )

ExamStatusTable = Table('exam_status', metadata,
                        Column('uid', BigInteger, primary_key=True,
                               autoincrement=True),
                        Column('exam_uid', BigInteger,
                               ForeignKey('exam.uid'),
                               nullable=False),
                        Column('sent', Boolean, default=False,
                               nullable=False, index=True),
                        Column('status', String(1, collation=BPMC_COLL),
                               default=ExamStatusEnum.Waiting.value,
                               nullable=False, index=True),
                        UniqueConstraint('exam_uid')
                        )

ProcedureTable = Table('procedure', metadata,
                       Column('uid', BigInteger, primary_key=True,
                              autoincrement=True),
                       Column('exam_uid', BigInteger,
                              ForeignKey('exam.uid'),
                              nullable=False)
                       )

ProcedureStatusTable = Table('procedure_status', metadata,
                             Column('uid', BigInteger, primary_key=True,
                                    autoincrement=True),
                             Column('procedure_uid', BigInteger,
                                    ForeignKey('procedure.uid'),
                                    nullable=False),
                             Column('ready', Boolean, default=False,
                                    nullable=False, index=True),
                             Column('sent', Boolean, default=False,
                                    nullable=False, index=True),
                             Column('status', String(1, collation=BPMC_COLL),
                                    default=ProcedureStatusEnum.Waiting.value,
                                    nullable=False, index=True),
                             UniqueConstraint('procedure_uid')
                             )

SopClassTable = Table('sop_class', metadata,
                      Column('uid', Integer,
                             primary_key=True, autoincrement=True),
                      Column('sop_class_identifier',
                             String(40, collation=BPMC_COLL),
                             nullable=False),
                      UniqueConstraint('sop_class_identifier')
                      )

ImageTable = Table('image', metadata,
                   Column('uid', BigInteger, primary_key=True,
                          autoincrement=True),
                   Column('procedure_uid', BigInteger,
                          ForeignKey('procedure.uid'),
                          nullable=False),
                   Column('repository_uid', Integer,
                          ForeignKey('repository.uid'),
                          nullable=False),
                   Column('modality_type_uid', SmallInteger,
                          ForeignKey('modality_type.uid'),
                          nullable=False),
                   Column('sop_class_uid', Integer,
                          ForeignKey('sop_class.uid'),
                          nullable=False),
                   Column('metadata_uid', BigInteger,
                          ForeignKey('image_metadata.uid'),
                          nullable=False),
                   Column('inserted_on', DateTime,
                          default=func.now(), nullable=False, index=True)
                   )

ModalityTypeTable = Table('modality_type', metadata,
                          Column('uid', SmallInteger, primary_key=True,
                                 autoincrement=True),
                          Column('model_name', String(50, collation=BPMC_COLL),
                                 nullable=False),
                          Column('software_version',
                                 String(80, collation=BPMC_COLL),
                                 nullable=False),
                          Column('manufacturer_name',
                                 String(50, collation=BPMC_COLL),
                                 nullable=False),
                          UniqueConstraint(
                              'model_name', 'software_version',
                              'manufacturer_name', name='uq_modality')
                          )


ImageMatchTable = Table('image_match', metadata,
                        Column('uid', BigInteger, primary_key=True,
                               autoincrement=True),
                        Column('origin', BigInteger,
                               ForeignKey('image.uid'),
                               nullable=False),
                        Column('destination', BigInteger,
                               ForeignKey('image.uid'),
                               nullable=False),
                        UniqueConstraint(
                            'origin', 'destination', name='uq_match')
                        )

ImageMetadataTable = Table('image_metadata', metadata,
                           Column('uid', BigInteger, primary_key=True,
                                  autoincrement=True),
                           Column('breast_implant_present', Boolean,
                                  nullable=False, default=False),
                           Column('image_laterality',
                                  String(1, collation=BPMC_COLL),
                                  nullable=False),
                           Column('acquisition_time',
                                  DateTime(6), nullable=False),
                           Column('processing_data', JSON),
                           Column('view_position',
                                  String(10, collation=BPMC_COLL),
                                  nullable=False),
                           Column('compression_force', Integer, nullable=True),
                           Column('size_of_return_rows',
                                  Integer, nullable=True),
                           Column('size_of_return_columns',
                                  Integer, nullable=True),
                           Column('extra', JSON, nullable=True)
                           )

ImageStatusTable = Table('image_status', metadata,
                         Column('uid', BigInteger, primary_key=True,
                                autoincrement=True),
                         Column('image_uid', BigInteger,
                                ForeignKey('image.uid'), nullable=False),
                         Column('ready', Boolean,
                                default=False, nullable=False, index=True),
                         Column('status', String(1, collation=BPMC_COLL),
                                default=ImageStatusEnum.Waiting.value,
                                nullable=False, index=True),
                         UniqueConstraint('image_uid')
                         )

ImageMetricsTable = Table('image_metrics', metadata,
                          Column('uid', BigInteger, primary_key=True,
                                 autoincrement=True),
                          Column('image_uid', BigInteger,
                                 ForeignKey('image.uid'), nullable=False),
                          Column('criteria', JSON, nullable=False),
                          Column('overlay', JSON, nullable=False),
                          UniqueConstraint('image_uid')
                          )

ImageMetricsDisplayTable = Table('image_metrics_display', metadata,
                                 Column('uid', BigInteger, primary_key=True,
                                        autoincrement=True),
                                 Column('image_metrics_uid', BigInteger,
                                        ForeignKey('image_metrics.uid'),
                                        nullable=False),
                                 Column('repository_uid', Integer,
                                        ForeignKey('repository.uid'),
                                        nullable=False),
                                 UniqueConstraint('image_metrics_uid')
                                 )

# -------- ORM Mappings --------

mapper(RepositoryORM, RepositoryTable)
mapper(IssuerORM, IssuerTable)
mapper(ExamORM, ExamTable, properties={
    'procedures': relationship(ProcedureORM, backref='exam', lazy='raise'),
    'status': relationship(ExamStatusORM, lazy='raise'),
    'issuer': relationship(IssuerORM, lazy='raise')
})
mapper(ExamStatusORM, ExamStatusTable)
mapper(ProcedureORM, ProcedureTable, properties={
    'images': relationship(ImageORM, backref='procedure', lazy='raise'),
    'status': relationship(ProcedureStatusORM, lazy='raise'),
})
mapper(ProcedureStatusORM, ProcedureStatusTable)
mapper(SopClassORM, SopClassTable)
mapper(ImageORM, ImageTable, properties={
    'metadata': relationship(ImageMetadataORM, lazy='raise')
})
mapper(ImageMatchORM, ImageMatchTable)
mapper(ImageMetadataORM, ImageMetadataTable)
mapper(ImageStatusORM, ImageStatusTable)
mapper(ImageMetricsORM, ImageMetricsTable)
mapper(ImageMetricsDisplayORM, ImageMetricsDisplayTable)
mapper(ModalityTypeORM, ModalityTypeTable)
