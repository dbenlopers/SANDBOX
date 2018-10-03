# -*- coding: utf-8 -*-

from ge.bpmc.persistence.orm import DictBase


def get_view_model_value(v):
    if isinstance(v, (list, tuple, set)) and len(v) != 0 \
            and isinstance(v[0], DictBase):
        return [x.to_dict() for x in v]
    elif isinstance(v, DictBase):
        return v.to_dict()
    return v


class ViewModelDictBase(object):

    __ignored_keys_prefixes = ['tmp_']

    def to_dict(self):
        return dict(
            [(k, get_view_model_value(v)) for k, v in self.__dict__.items()
             if (True not in map(k.startswith, self.__ignored_keys_prefixes))])


class ImageResultVM(ViewModelDictBase, DictBase):

    def __init__(self, uid, status, matched_with, overlay, criteria,
                 tmp_image_metrics_display_uid, extra, image=None):
        self.uid = uid
        self.status = status
        self.matched_with = matched_with
        self.overlay = overlay
        self.criteria = criteria
        self.tmp_image_metrics_display_uid = tmp_image_metrics_display_uid
        self.extra = extra
        self.image = None


class ImageMatchingDataVM(ViewModelDictBase, DictBase):

    def __init__(self, uid, image_laterality, view_position, acquisition_time,
                 criteria, processing_data):
        self.uid = uid
        self.image_laterality = image_laterality
        self.view_position = view_position
        self.acquisition_time = acquisition_time
        self.criteria = criteria
        self.processing_data = processing_data


class ProcedureImageResultsVM(ViewModelDictBase, DictBase):

    def __init__(self, uid, status, matching_data, images=[]):
        self.uid = uid
        self.status = status
        self.matching_data = matching_data
        self.images = images


class ExamProceduresImageResultsVM(ViewModelDictBase, DictBase):

    def __init__(self, uid, procedures=[]):
        self.uid = uid
        self.procedures = procedures
