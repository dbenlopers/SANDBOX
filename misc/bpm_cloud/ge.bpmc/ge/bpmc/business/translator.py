# -*- coding: utf-8 -*-

import hashlib
from copy import deepcopy

import numpy as np

from ge.bpmc.api.schemas.bpm import CriteriaModel, OverlayModel
from ge.bpmc.api.schemas.default import (AngleModel, BigIntModel, BooleanModel,
                                         DoubleModel, DoublePointModel,
                                         FloatModel, IntModel, LineModel,
                                         NumberModel, PointModel,
                                         SmallIntModel, StringModel,
                                         TinyIntModel)

LATERALITY_MATCHING_KEY = 'laterality_match_uid'
VIEW_POSITION_MATCHING_KEY = 'view_position_match_uid'
DUMMY_PIXEL_RESULT = [
    [255, 255, 255, 255],
    [255, 255, 255, 255],
    [255, 255, 255, 255],
    [255, 255, 255, 255]
]

###############################
#
#       TO BUSINESS
#
###############################

CRITERIA_MAPPING = {
    'attribute_length_of_posterior_nipple_line': {
        'key': 'length_of_posterior_nipple_line'},
    'attribute_symmetry': {
        'key': 'symmetry'},
    'kpi_centricity': {
        'key': 'centricity'},
    'kpi_absence_of_breast_sagging': {
        'key': 'absence_of_breast_sagging'},
    'kpi_compression': {
        'key': 'compression'},
    'kpi_imf_horizontal_position_in_mm': {
        'key': 'inframmary_fold_visible_vertical_distance',
        'parent': 'inframmary_fold_visible'},
    'kpi_imf_vertical_position_in_mm': {
        'key': 'inframmary_fold_visible_horizontal_distance',
        'parent': 'inframmary_fold_visible'},
    'kpi_inframmary_fold_without_skin_folds_angle': {
        'key': 'inframmary_fold_without_skin_folds_angle',
        'parent': 'inframmary_fold_without_skin_folds'},
    'kpi_inframmary_fold_without_skin_folds_radius': {
        'key': 'inframmary_fold_without_skin_folds_radius',
        'parent': 'inframmary_fold_without_skin_folds'},
    'kpi_nipple_visible_in_profile': {
        'key': 'nipple_visible_in_profile'},
    'kpi_nipple_angle': {
        'key': 'nipple_angle'},
    'kpi_no_bottom_overlapping': {
        'key': 'bottom_overlapping'},
    'kpi_no_opposite_overlapping': {
        'key': 'opposite_overlapping'},
    'kpi_no_top_overlapping': {
        'key': 'top_overlapping'},
    'pectoral_muscle_angle': {
        'key': 'pectoral_muscle_angle'},
    'pectoral_muscle_visible_up_to_nipple_line': {
        'key': 'pectoral_muscle_visible_up_to_nipple_line'},
    'pectoral_muscle_width': {
        'key': 'pectoral_muscle_width'},
    'kpi_axillary_tail_area': {
        'key': 'axillary_tail_visible_area',
        'parent': 'axillary_tail_visible'},
    'kpi_axillary_taildistance': {
        'key': 'axillary_tail_visible_distance',
        'parent': 'axillary_tail_visible'},
    'kpi_transition_to_intermammary_cleft_area': {
        'key': 'transition_to_intermammary_cleft_visible_area',
        'parent': 'transition_to_intermammary_cleft_visible'},
    'kpi_transition_to_intermammary_cleft_distance': {
        'key': 'transition_to_intermammary_cleft_visible_distance',
        'parent': 'transition_to_intermammary_cleft_visible'},
}


OVERLAY_MAPPING = {
    'axillary_tail_point': {
        'key': 'axillary_tail_visible'},
    'imf_point': {
        'key': 'inframmary_fold_visible'},
    'intersection_point_pm_pnl': {
        'key': 'pectoral_muscle_visible_up_to_nipple_line'},
    'nipple_detected_point': {
        'key': 'nipple_angle',
        'aggregate': True,
        'position': 0},
    'nipple_ideal_point': {
        'key': 'nipple_angle',
        'aggregate': True,
        'position': 1},
    'no_bottom_overlapping': {
        'key': 'bottom_overlapping'},
    'no_opposite_overlapping': {
        'key': 'opposite_overlapping'},
    'no_top_overlapping': {
        'key': 'top_overlapping'},
    'pectoral_muscle_start_point': {
        'key': 'pectoral_muscle_width',
        'aggregate': True,
        'position': 0},
    'pectoral_muscle_end_point': {
        'key': 'pectoral_muscle_width',
        'aggregate': True,
        'position': 1},
    'transition_to_intermammary_cleft_point': {
        'key': 'transition_to_intermammary_cleft_visible'}
}


def generate_default_dict(dict_, branch):
    for k, v in branch.items():
        if isinstance(v, dict) and 'type' not in v:
            dict_[k] = generate_default_dict({}, v)
        else:
            dict_[k] = None
    return dict_


CRITERIA_DEFAULT_DICT = generate_default_dict({}, CriteriaModel.properties)
OVERLAY_DEFAULT_DICT = generate_default_dict({}, OverlayModel.properties)


def to_point_model(scpt):
    """
    Science ImagePoint to PointModel transformation utility
    """
    if scpt is None:
        return scpt
    return PointModel(
        x=int(round(scpt.x)),
        y=int(round(scpt.y)))


def to_expected_output_type(value, output_type):
    if not value:
        return None
    if output_type in (TinyIntModel, SmallIntModel, IntModel, BigIntModel):
        return int(value) if not np.isnan(value) else None
    if output_type in (NumberModel, FloatModel, DoubleModel):
        return float(value) if not np.isnan(value) else None
    if output_type is BooleanModel:
        return bool(value)
    if output_type is PointModel:
        return to_point_model(value)
    if output_type in (DoublePointModel, LineModel):
        start, end = value.get(0), value.get(1)
        return {
            'start': to_point_model(start),
            'end': to_point_model(end)}
    if output_type is AngleModel:
        start = value.get('start', {})
        end = value.get('end', {})
        line1_start, line1_end = start.get('start'), start.get('end')
        line2_start, line2_end = end.get('start'), end.get('end')
        return {
            'start': {
                'start': to_point_model(line1_start),
                'end': to_point_model(line1_end)
            },
            'end': {
                'start': to_point_model(line2_start),
                'end': to_point_model(line2_end)
            }}


def to_application_model(processed, mapping, default_dict, model):
    """
    Morphs processing algorythm result dict to expected application dict

    :processed: dict from business algorythm
    :mapping: the mapping to use to select and extract data
    :default_dict: the pre-filled dict with expected keys
    :model: the Flask swagger Schema to use to identify data types
    """
    # Filtering & filling result dict
    filtered = {k: processed[k]
                for k in processed if k in mapping}
    results = deepcopy(default_dict)
    for k in filtered:
        destination = mapping.get(k)
        parent = destination.get('parent', None)
        key = destination['key']
        is_agg = destination.get('aggregate', False)
        agg_position = destination.get('position', 0)
        if is_agg:
            value = results[parent][key] if parent else results[key]
            value = value if value else {}
            value[agg_position] = filtered[k]
        else:
            value = filtered[k]
        if parent:
            results[parent][key] = value
        else:
            results[key] = value
    # Sanitizing
    for key, conf in {x['key']: x for x in mapping.values()}.items():
        parent = conf.get('parent', None)
        output_type = (model.properties
                       .get(parent, model.properties)
                       .get(key))
        if parent:
            results[parent][key] = to_expected_output_type(
                results[parent][key], output_type)
        else:
            results[key] = to_expected_output_type(
                results[key], output_type)
    return results


def to_application_criteria(dict_):
    return to_application_model(dict_, CRITERIA_MAPPING,
                                CRITERIA_DEFAULT_DICT, CriteriaModel)


def to_application_overlay(dict_):
    return to_application_model(dict_, OVERLAY_MAPPING,
                                OVERLAY_DEFAULT_DICT, OverlayModel)


def to_processing_data(image):
    """
    Transforms an Image into a business usable tuple for processing

    :image: a "science" Image object
    """
    return (
        to_application_criteria(image.kpi),
        to_application_overlay(image.display),
        DUMMY_PIXEL_RESULT  # image.pixel_array_original
    )


def get_match_key(match):
    return hashlib.md5(str(sorted(match['pair'])).encode('utf-8')).hexdigest()


def to_matching_data(procedure):
    """
    Transforms a Procedure matcher result into a list of dicts for each unique
    match

    :procedure: a "science" Procedure matcher object
    """
    mixed = (procedure.image_list_for_processing +
             procedure.image_list_for_presentation)
    results = []
    for obj in mixed:
        elt = obj.to_dict()
        uid = elt['image_uid']
        laterality_match = elt.get(LATERALITY_MATCHING_KEY)
        vp_match = elt.get(VIEW_POSITION_MATCHING_KEY)
        if laterality_match:
            results.append({
                'pair': [uid, laterality_match],
                'criteria': {
                    'length_of_posterior_nipple_line':
                    elt.get('kpi_length_of_posterior_line')}
            })
        if vp_match:
            results.append({
                'pair': [uid, vp_match],
                'criteria': {'symmetry': elt.get('kpi_symmetry')}
            })
    return {get_match_key(x): x for x in results}.values()

###############################
#
#       TO SCIENCE & BEYOND
#
###############################


SC_IMAGE_MAPPING = {
    'PixelArray': {
        'origins': [{'key': 'image'}]},
    'ManufacturerModelName': {
        'origins': [{'key': 'model_name',
                     'parent': 'modality'}]},
    'SoftwareVersions': {
        'origins': [{'key': 'software_version',
                     'parent': 'modality'}]},
    'Manufacturer': {
        'origins': [{'key': 'manufacturer_name',
                     'parent': 'modality'}]},
    'SOPClassUID': {
        'origins': [{'key': 'sop_class'}]},
    'BreastImplantPresent': {
        'origins': [{'key': 'breast_implant_present'}]},
    'ImageLaterality': {
        'origins': [{'key': 'image_laterality'}]},
    'AcquisitionDatetime': {
        'origins': [{'key': 'acquisition_time'}]},
    'ViewPosition': {
        'origins': [{'key': 'view_position'}]},
    'ImagerPixelSpacing': {
        'aggregate': True,
        'aggregation_mode': 'join_by_slash',
        'origins': [{'key': 'horizontal',
                     'position': 0,
                     'parent': 'imager_pixel_spacing',
                     'entry': 'processing_data'},
                    {'key': 'vertical',
                     'position': 1,
                     'parent': 'imager_pixel_spacing',
                     'entry': 'processing_data'}]},
    'Rows': {
        'origins': [{'key': 'rows',
                     'parent': 'processing_data'}]},
    'Columns': {
        'origins': [{'key': 'columns',
                     'parent': 'processing_data'}]},
    'PhotometricInterpretation': {
        'origins': [{'key': 'photometric_interpretation',
                     'parent': 'processing_data'}]},
    'PresentationIntentType': {
        'origins': [{'key': 'presentation_intent_type',
                     'parent': 'processing_data'}]},
    'BitsAllocated': {
        'origins': [{'key': 'bits_allocated',
                     'parent': 'processing_data'}]},
    'ImageType': {
        'aggregate': True,
        'aggregation_mode': 'single_item_join_by_slash',
        'origins': [{'key': 'image_type',
                     'parent': 'processing_data',
                     'position': 0, }]},
    'CompressionForce': {
        'origins': [{'key': 'compression_force'}]},

    'BodyPartExamined': {
        'origins': [{'key': 'body_part_examined',
                     'parent': 'processing_data'}]},
    'CollimatorShape': {
        'origins': [{'key': 'collimator_shape',
                     'parent': 'processing_data'}]},
    'CollimatorLeftVerticalEdge': {
        'origins': [{'key': 'collimator_left_vertical_edge',
                     'parent': 'processing_data'}]},
    'CollimatorLowerHorizontalEdge': {
        'origins': [{'key': 'collimator_lower_horizontal_edge',
                     'parent': 'processing_data'}]},
    'CollimatorRightVerticalEdge': {
        'origins': [{'key': 'collimator_right_vertical_edge',
                     'parent': 'processing_data'}]},
    'CollimatorUpperHorizontalEdge': {
        'origins': [{'key': 'collimator_upper_horizontal_edge',
                     'parent': 'processing_data'}]}
}

# See ge.bpmc.services.workflow.WorkflowService.get_procedure_matching_data
SC_IMAGE_MATCHER_MAPPING = {
    'acquisition_date': {
        'origins': [{'key': 'acquisition_time'}]
    },
    'image_uid': {
        'origins': [{'key': 'uid'}]
    },
    'presentation_intent_type': {
        'origins': [{'key': 'presentation_intent_type',
                     'parent': 'processing_data'}]
    },
    'image_laterality': {
        'origins': [{'key': 'image_laterality'}]
    },
    'view_position': {
        'origins': [{'key': 'view_position'}]
    },
    'attribute_symmetry': {
        'origins': [{'key': 'symmetry', 'parent': 'criteria'}]
    },
    'attribute_length_of_posterior_nipple_line': {
        'origins': [{'key': 'length_of_posterior_nipple_line',
                     'parent': 'criteria'}]
    }
}


def crawl_dict(dict_, keys):
    if keys and dict_:
        return crawl_dict(dict_.get(keys.pop(0), None), keys)
    else:
        return dict_


def to_science_model(payload, mapping=SC_IMAGE_MAPPING):
    """
    Morphs computation request payload to a "science"-based model

    :payload: Payload of a computation request.
    See ge.bpmc.api.schemas.bpm.ModalityImageModel
    """
    results = {}
    for k in mapping:
        conf = mapping[k]
        origins = conf['origins']
        aggregate = conf.get('aggregate', False)
        aggregation_mode = conf.get('aggregation_mode', False)
        for item in origins:
            key = item['key']
            parent = item.get('parent', None)
            entry = item.get('entry', None)
            position = item.get('position', 0)
            value = crawl_dict(payload, [x for x in [entry, parent, key]
                                         if x is not None])
            if aggregate:
                results.setdefault(k, {})[position] = value
            else:
                # This overrides previous configuration if multiples items
                # exist in origins list and aggregation params are not properly
                # set
                results[k] = value
        if aggregate and results[k]:
            if aggregation_mode == 'single_item_join_by_slash':
                # single_item is expected to be of iterable type
                single_item = [x for x in results[k].values()][0]
                results[k] = '/'.join([str(x) for x in single_item])
            if aggregation_mode == 'join_by_slash':
                results[k] = '/'.join(
                    [str(results[k][x]) for x in sorted(results[k].keys())])
    return results


def to_science_image(payload):
    return to_science_model(payload)


def to_science_image_match(match):
    return to_science_model(match, mapping=SC_IMAGE_MATCHER_MAPPING)


def to_science_image_matches(matches):
    return [to_science_image_match(x) for x in matches]
