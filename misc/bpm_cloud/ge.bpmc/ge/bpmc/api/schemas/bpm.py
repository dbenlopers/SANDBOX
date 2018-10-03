# -*- coding: utf-8 -*-

from copy import copy

from flask_restful_swagger_2 import Schema

from ge.bpmc.api.schemas.default import (AngleModel, ArrayModel, BigIntModel,
                                         BinaryModel, BooleanModel, ByteModel,
                                         DateModel, DatetimeModel, DoubleModel,
                                         DoublePointModel, FloatModel,
                                         ImageBytesModel, IntModel, JsonModel,
                                         LineModel, NumberModel, PasswordModel,
                                         PointModel, SimpleImageModel,
                                         SmallIntModel, StatusModel,
                                         StringModel, TinyIntModel)
from ge.bpmc.api.schemas.orm import (IssuerModelWithoutPrimary,
                                     ModalityTypeModelWithoutPrimary)
from ge.bpmc.persistence.orm import (ImageStatusEnum, LateralityEnum,
                                     PresentationIntentTypeEnum,
                                     ProcedureStatusEnum)

# Parts


class SizeOfReturnModel(Schema):
    type = 'object'
    properties = {
        'rows': IntModel,
        'columns': IntModel
    }
    required = ['rows', 'columns']


class ImagerPixelSpacingModel(Schema):
    type = 'object'
    properties = {
        'horizontal': FloatModel,
        'vertical': FloatModel
    }
    required = ['horizontal', 'vertical']


class OverlayModel(Schema):
    type = 'object'
    properties = {
        'centricity': PointModel,
        'bottom_overlapping': IntModel,
        'opposite_overlapping': IntModel,
        'top_overlapping': IntModel,
        'pectoral_muscle_angle': AngleModel,
        'pectoral_muscle_visible_up_to_nipple_line': PointModel,
        'pectoral_muscle_width': LineModel,
        'inframmary_fold_visible': PointModel,
        'axillary_tail_visible': PointModel,
        'transition_to_intermammary_cleft_visible': PointModel,
        'nipple_visible_in_profile': PointModel,
        'nipple_angle': DoublePointModel,
        'absence_of_breast_sagging': PointModel,
        'compression': PointModel
    }
    required = []


class CriteriaModel(Schema):
    type = 'object'
    properties = {
        'centricity': FloatModel,
        'symmetry': FloatModel,
        'bottom_overlapping': FloatModel,
        'opposite_overlapping': FloatModel,
        'top_overlapping': FloatModel,
        'length_of_posterior_nipple_line': FloatModel,
        'pectoral_muscle_angle': SmallIntModel,
        'pectoral_muscle_visible_up_to_nipple_line': FloatModel,
        'pectoral_muscle_width': FloatModel,
        'inframmary_fold_visible':
        {
            'inframmary_fold_visible_vertical_distance': FloatModel,
            'inframmary_fold_visible_horizontal_distance': FloatModel
        },
        'inframmary_fold_without_skin_folds':
        {
            'inframmary_fold_without_skin_folds_angle': SmallIntModel,
            'inframmary_fold_without_skin_folds_radius': FloatModel
        },
        'axillary_tail_visible':
        {
            'axillary_tail_visible_distance': FloatModel,
            'axillary_tail_visible_area': SmallIntModel
        },
        'transition_to_intermammary_cleft_visible':
        {
            'transition_to_intermammary_cleft_visible_distance': FloatModel,
            'transition_to_intermammary_cleft_visible_area': SmallIntModel
        },
        'nipple_visible_in_profile': BooleanModel,
        'nipple_angle': SmallIntModel,
        'absence_of_breast_sagging': FloatModel,
        'compression': SmallIntModel
    }
    required = []


class ProcessingImageModel(Schema):
    type = 'object'
    properties = {
        'metrics_uid': BigIntModel,
        'image': ImageBytesModel
    }


ImageTypeModel = copy(ArrayModel)
ImageTypeModel.update({'items': StringModel})


class ProcessingMinimalData(Schema):
    type = 'object'
    properties = {
        'imager_pixel_spacing': ImagerPixelSpacingModel,
        'rows': SmallIntModel,
        'columns': SmallIntModel,
        'photometric_interpretation': StringModel,
        'presentation_intent_type': {
            'type': 'string',
            'enum': [x.value for x in
                     PresentationIntentTypeEnum.__members__.values()]
        },
        'bits_allocated': IntModel,
        'image_type': ImageTypeModel,
        'body_part_examined': StringModel,
        'collimator_shape': StringModel,
        'collimator_left_vertical_edge': IntModel,
        'collimator_right_vertical_edge': IntModel,
        'collimator_lower_horizontal_edge': IntModel,
        'collimator_upper_horizontal_edge': IntModel
    }

    required = ['imager_pixel_spacing', 'rows', 'columns',
                'presentation_intent_type', 'bits_allocated', 'image_type']


class ModalityImageModel(Schema):
    type = 'object'
    properties = {
        'image': ImageBytesModel,
        'exam_uid': BigIntModel,
        'procedure_uid': BigIntModel,
        'modality': ModalityTypeModelWithoutPrimary,
        'sop_class': StringModel,
        'breast_implant_present': {
            'type': 'string',
            'enum': ['yes', 'no']
        },
        'image_laterality': {
            'type': 'string',
            'enum': [x.value for x in LateralityEnum.__members__.values()]
        },
        'acquisition_time': DatetimeModel,
        'view_position': StringModel,
        'processing_data': ProcessingMinimalData,
        'compression_force': SmallIntModel,
        'size_of_return': SizeOfReturnModel,
        'extra': JsonModel
    }
    required = ['image', 'image_laterality', 'view_position',
                'processing_data', 'columns', 'sop_class', 'acquisition_time']


class SystemIDModel(Schema):
    type = 'object'
    properties = {
        'identifier': IssuerModelWithoutPrimary.properties.get('identifier')
    }
    required = ['identifier']


class ComputationModel(Schema):
    type = 'object'
    properties = {
        'exam_uid': BigIntModel,
        'procedure_uid': BigIntModel,
        'image_uid': BigIntModel
    }


class ImageResultModel(Schema):
    type = 'object'
    properties = {
        'image_uid': BigIntModel,
        'status': {
            'type': 'string',
            'enum': [x.value for x in ImageStatusEnum.__members__.values()]
        },
        'image': ImageBytesModel,
        'overlay': OverlayModel,
        'criteria': CriteriaModel,
        'extra': JsonModel
    }


ProcedureResultsModel = copy(ArrayModel)
ProcedureResultsModel.update({'items': ImageResultModel})


class ProcedureKpisModel(Schema):
    type = 'object'
    properties = {
        'symmetry': IntModel,
        'length_of_posterior_nipple_line': IntModel
    }


class ProcedureImageOverlayModel(Schema):
    type = 'object'
    properties = {
        'symmetry': PointModel,
        'length_of_posterior_nipple_line': LineModel
    }


class ProcedureOverlayModel(Schema):
    type = 'object'
    properties = {
        'image_uid': IntModel,
        'overlay': ProcedureImageOverlayModel
    }


ProcedureOverlaysModel = copy(ArrayModel)
ProcedureOverlaysModel.update({'items': ProcedureOverlayModel})

PairModel = copy(ArrayModel)
PairModel.update({'items': IntModel})


class ProcedureMatchModel(Schema):
    type = 'object'
    properties = {
        'pair': PairModel,
        'kpis': ProcedureKpisModel,
        'overlays': ProcedureOverlaysModel
    }


ProcedureMatchesModel = copy(ArrayModel)
ProcedureMatchesModel.update({'items': ProcedureMatchModel})


class ProcedureResultModel(Schema):
    type = 'object'
    properties = {
        'procedure_uid': BigIntModel,
        'status': {
            'type': 'string',
            'enum': [x.value for x in ProcedureStatusEnum.__members__.values()]
        },
        'matched': ProcedureMatchesModel,
        'images': ProcedureResultsModel
    }


ExamResultsModel = copy(ArrayModel)
ExamResultsModel.update({'items': ProcedureResultModel})


class ExamResultModel(Schema):
    type = 'object'
    properties = {
        'exam_uid': BigIntModel,
        'procedures': ExamResultsModel
    }
