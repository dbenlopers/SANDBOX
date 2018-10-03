# -*- coding: utf-8 -*-

from . import FLAG_PRES, FLAG_PROC


class ProcedureProcessor:

    def __init__(self, images):
        """
        :images: list of image dicts containing keys necessary to instanciate
        an ImageMatcher (see bellow)
        """
        self.reset_flags()
        proc = sorted(
            filter(lambda x: x['presentation_intent_type'] == FLAG_PROC,
                   images), key=lambda x: x['acquisition_date'])
        pres = sorted(
            filter(lambda x: x['presentation_intent_type'] == FLAG_PRES,
                   images), key=lambda x: x['acquisition_date'])
        self.image_list_for_processing = [ImageMatch(**x) for x in proc]
        self.image_list_for_presentation = [ImageMatch(**x) for x in pres]

    def reset_flags(self):
        self.flag_RMLO = self.flag_LMLO = self.flag_RCC = self.flag_LCC = None

    def compute(self):
        """
        Utility method preventing to manually run each step of the computation
        for each list.
        """
        for list_ in [self.image_list_for_processing,
                      self.image_list_for_presentation]:
            self.compute_matching(list_)
            self.compute_symmetry(list_)
            self.compute_length_of_posterior_line(list_)
            self.reset_flags()

    def compute_matching(self, list_):
        for elem in reversed(list_):
            # if for processing #flag_clinicalview_pit

            if None in [self.flag_RMLO, self.flag_LMLO, self.flag_RCC,
                        self.flag_LCC]:
                flag_name = 'flag_%s' % elem.clinical_view
                flag = getattr(self, flag_name)
                if flag is None:
                    setattr(self, flag_name, elem.image_uid)

    def compute_kpi(self, flag_1, flag_2, kpi_attr, kpi_name, result_attr,
                    list_):
        if None not in [flag_1, flag_2]:
            ptr_1 = list(
                filter(lambda x: x.image_uid == flag_1, list_))[0]
            ptr_2 = list(
                filter(lambda x: x.image_uid == flag_2, list_))[0]
            attr_1 = getattr(ptr_1, kpi_attr)
            attr_2 = getattr(ptr_2, kpi_attr)
            kpi_value = abs(attr_1 - attr_2) if (attr_1 and attr_2) else None

            setattr(ptr_1, result_attr, flag_2)
            setattr(ptr_2, result_attr, flag_1)
            setattr(ptr_1, kpi_name, kpi_value)
            setattr(ptr_2, kpi_name, kpi_value)

    def compute_length_of_posterior_line(self, list_):
        self.compute_kpi(self.flag_RMLO,  self.flag_RCC,
                         'attribute_length_of_posterior_nipple_line',
                         'kpi_length_of_posterior_line',
                         'laterality_match_uid', list_)
        self.compute_kpi(self.flag_LMLO,  self.flag_LCC,
                         'attribute_length_of_posterior_nipple_line',
                         'kpi_length_of_posterior_line',
                         'laterality_match_uid', list_)

    def compute_symmetry(self, list_):
        self.compute_kpi(self.flag_RMLO,  self.flag_LMLO,
                         'attribute_symmetry', 'kpi_symmetry',
                         'view_position_match_uid', list_)
        self.compute_kpi(self.flag_RCC,  self.flag_LCC,
                         'attribute_symmetry', 'kpi_symmetry',
                         'view_position_match_uid', list_)


class ImageMatch:

    def __init__(self, image_uid=None, acquisition_date=None,
                 image_laterality='L', view_position='CC',
                 presentation_intent_type='FOR PROCESSING',
                 attribute_symmetry=None,
                 attribute_length_of_posterior_nipple_line=None):
        self.image_uid = image_uid
        self.acquisition_date = acquisition_date
        self.image_laterality = image_laterality
        self.view_position = view_position
        self.presentation_intent_type = presentation_intent_type
        self.attribute_symmetry = attribute_symmetry
        self.attribute_length_of_posterior_nipple_line = (
            attribute_length_of_posterior_nipple_line)
        self.clinical_view = self.image_laterality + self.view_position
        self.kpi_length_of_posterior_line = self.kpi_symmetry = None
        self.laterality_match_uid = None
        self.view_position_match_uid = None

    def to_dict(self):
        return self.__dict__
