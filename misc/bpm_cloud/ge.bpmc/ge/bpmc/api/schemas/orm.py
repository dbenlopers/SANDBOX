# -*- coding: utf-8 -*-

from ge.bpmc.api.schemas.base import SQLAlchemySchemaBase
from ge.bpmc.persistence.orm import (ExamStatusTable, ExamTable,
                                     ImageMetadataTable,
                                     ImageMetricsDisplayTable,
                                     ImageMetricsTable, ImageStatusTable,
                                     ImageTable, IssuerTable,
                                     ModalityTypeTable, ProcedureStatusTable,
                                     ProcedureTable, RepositoryTable,
                                     SopClassTable)
from ge.bpmc.utilities.swagger import get_table_swagger_schema

ISSUER_DEFAULTS = get_table_swagger_schema(IssuerTable)
REPOSITORY_DEFAULTS = get_table_swagger_schema(RepositoryTable)
EXAM_DEFAULTS = get_table_swagger_schema(ExamTable)
EXAM_STATUS_DEFAULTS = get_table_swagger_schema(ExamStatusTable)
PROCEDURE_DEFAULTS = get_table_swagger_schema(ProcedureTable)
PROCEDURE_STATUS_DEFAULTS = get_table_swagger_schema(ProcedureStatusTable)
SOP_CLASS_DEFAULTS = get_table_swagger_schema(SopClassTable)
IMAGE_DEFAULTS = get_table_swagger_schema(ImageTable)
IMAGE_METADATA_DEFAULTS = get_table_swagger_schema(ImageMetadataTable)
IMAGE_STATUS_DEFAULTS = get_table_swagger_schema(ImageStatusTable)
IMAGE_METRICS_DEFAULTS = get_table_swagger_schema(ImageMetricsTable)
IMAGE_METRICS_DISPLAY_DEFAULTS = \
    get_table_swagger_schema(ImageMetricsDisplayTable)
MODALITY_TYPE_DEFAULTS = get_table_swagger_schema(ModalityTypeTable)


# ISSUER


class IssuerModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = ISSUER_DEFAULTS

IssuerModelWithoutPrimary = type(
    'IssuerModelWithoutPrimary', IssuerModel.__bases__,
    dict(IssuerModel.__dict__))
(IssuerModelWithoutPrimary.properties,
 IssuerModelWithoutPrimary.required) = \
    IssuerModel.requirements_without_primary()

# REPOSITORY


class RepositoryModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = REPOSITORY_DEFAULTS

RepositoryModelWithoutPrimary = type(
    'RepositoryModelWithoutPrimary', RepositoryModel.__bases__,
    dict(RepositoryModel.__dict__))
(RepositoryModelWithoutPrimary.properties,
 RepositoryModelWithoutPrimary.required) = \
    RepositoryModel.requirements_without_primary()

# EXAM


class ExamModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = EXAM_DEFAULTS

ExamModelWithoutPrimary = type(
    'ExamModelWithoutPrimary', ExamModel.__bases__,
    dict(ExamModel.__dict__))
(ExamModelWithoutPrimary.properties,
 ExamModelWithoutPrimary.required) = \
    ExamModel.requirements_without_primary()


class ExamStatusModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = EXAM_STATUS_DEFAULTS

ExamStatusModelWithoutPrimary = type(
    'ExamStatusModelWithoutPrimary', ExamStatusModel.__bases__,
    dict(ExamStatusModel.__dict__))
(ExamStatusModelWithoutPrimary.properties,
 ExamStatusModelWithoutPrimary.required) = \
    ExamStatusModel.requirements_without_primary()

# PROCEDURE


class ProcedureModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = PROCEDURE_DEFAULTS

ProcedureModelWithoutPrimary = type(
    'ProcedureModelWithoutPrimary', ProcedureModel.__bases__,
    dict(ProcedureModel.__dict__))
(ProcedureModelWithoutPrimary.properties,
 ProcedureModelWithoutPrimary.required) = \
    ProcedureModel.requirements_without_primary()


class ProcedureStatusModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = PROCEDURE_STATUS_DEFAULTS

ProcedureStatusModelWithoutPrimary = type(
    'ProcedureStatusModelWithoutPrimary', ProcedureStatusModel.__bases__,
    dict(ProcedureStatusModel.__dict__))
(ProcedureStatusModelWithoutPrimary.properties,
 ProcedureStatusModelWithoutPrimary.required) = \
    ProcedureStatusModel.requirements_without_primary()

# SOP CLASS


class SopClassModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = SOP_CLASS_DEFAULTS

SopClassModelWithoutPrimary = type(
    'SupportedSopClassModelWithoutPrimary', SopClassModel.__bases__,
    dict(SopClassModel.__dict__))
(SopClassModelWithoutPrimary.properties,
 SopClassModelWithoutPrimary.required) = \
    SopClassModel.requirements_without_primary()

# IMAGE


class ImageModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = IMAGE_DEFAULTS

ImageModelWithoutPrimary = type(
    'ImageModelWithoutPrimary', ImageModel.__bases__,
    dict(ImageModel.__dict__))
(ImageModelWithoutPrimary.properties,
 ImageModelWithoutPrimary.required) = \
    ImageModel.requirements_without_primary()


class ImageMetadataModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = IMAGE_METADATA_DEFAULTS


ImageMetadataModelWithoutPrimary = type(
    'ImageMetadataModelWithoutPrimary', ImageMetadataModel.__bases__,
    dict(ImageMetadataModel.__dict__))
(ImageMetadataModelWithoutPrimary.properties,
 ImageMetadataModelWithoutPrimary.required) = \
    ImageMetadataModel.requirements_without_primary()


class ImageStatusModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = IMAGE_STATUS_DEFAULTS

ImageStatusModelWithoutPrimary = type(
    'ImageStatusModelWithoutPrimary', ImageStatusModel.__bases__,
    dict(ImageStatusModel.__dict__))
(ImageStatusModelWithoutPrimary.properties,
 ImageStatusModelWithoutPrimary.required) = \
    ImageStatusModel.requirements_without_primary()


class ImageMetricsModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = IMAGE_METRICS_DEFAULTS

ImageMetricsModelWithoutPrimary = type(
    'ImageMetricsModelWithoutPrimary', ImageMetricsModel.__bases__,
    dict(ImageMetricsModel.__dict__))
(ImageMetricsModelWithoutPrimary.properties,
 ImageMetricsModelWithoutPrimary.required) = \
    ImageMetricsModel.requirements_without_primary()


class ImageMetricsDisplayModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = IMAGE_METRICS_DISPLAY_DEFAULTS

ImageMetricsDisplayModelWithoutPrimary = type(
    'ImageMetricsDisplayModelWithoutPrimary',
    ImageMetricsDisplayModel.__bases__,
    dict(ImageMetricsDisplayModel.__dict__))
(ImageMetricsDisplayModelWithoutPrimary.properties,
 ImageMetricsDisplayModelWithoutPrimary.required) = \
    ImageMetricsDisplayModel.requirements_without_primary()


class ModalityTypeModel(SQLAlchemySchemaBase):
    type = 'object'
    properties, required, _primary = MODALITY_TYPE_DEFAULTS

ModalityTypeModelWithoutPrimary = type(
    'ModalityTypeModelWithoutPrimary', ModalityTypeModel.__bases__,
    dict(ModalityTypeModel.__dict__))
(ModalityTypeModelWithoutPrimary.properties,
 ModalityTypeModelWithoutPrimary.required) = \
    ModalityTypeModel.requirements_without_primary()
