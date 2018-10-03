# -*- coding: utf-8 -*-

from ge.bpmc.business.image.matching import ProcedureProcessor
from ge.bpmc.business.translator import (to_matching_data,
                                         to_science_image_matches)
from ge.bpmc.exceptions.matching import BPMMatchingException
import traceback


def match_procedure_images(logger, images_metadata):
    """
    Runs the matching algorithm

    :logger: a logging.Logger instance
    :images_metadata: is a list of dicts based on the view model
    ge.bpmc.persistence.viewmodels.ImageMatchingDataVM.to_dict() method

    returns a list of dicts such as
    [{ pair: [uid1, uid2], criteria: {'symmetry':0} },
     { pair: [uid1, uid3], criteria: {'length_of_posterior_nipple_line':0}}]
    Pairs are unique
    """
    try:
        matches = to_science_image_matches(images_metadata)
        processor = ProcedureProcessor(matches)
        processor.compute()
        return to_matching_data(processor)
    except Exception as err:
        raise BPMMatchingException(traceback.format_exc())
