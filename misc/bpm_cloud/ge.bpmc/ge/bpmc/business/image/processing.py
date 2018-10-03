# -*- coding: utf-8 -*-
import json
import os
import statistics
import time as time
from math import acos, atan, degrees, sqrt

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as ndi
from scipy import signal as sg
from scipy import stats
from scipy.optimize import curve_fit
from skimage import exposure, measure, transform
from skimage.filters import (rank, threshold_minimum, threshold_niblack,
                             threshold_otsu)
from skimage.measure import find_contours, label
from skimage.morphology import disk
from skimage.segmentation import find_boundaries
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.util import img_as_ubyte
from sklearn.cluster import DBSCAN
from sklearn.linear_model import RANSACRegressor
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

from ge.bpmc.exceptions.processing import BPMProcessingInvalidException

from . import (KDCM_ACDT, KDCM_BDPE, KDCM_BRIP, KDCM_BTSA, KDCM_COLH,
               KDCM_COLS, KDCM_COLV, KDCM_CORV, KDCM_COSH, KDCM_COUH,
               KDCM_CPFR, KDCM_IMLA, KDCM_IMPS, KDCM_IMTP, KDCM_MANU,
               KDCM_MODN, KDCM_PHIN, KDCM_PIXA, KDCM_PRIT, KDCM_ROWS,
               KDCM_SFTV, KDCM_SOPC, KDCM_VIPO, LBL_IMF_PT_UNDEF,
               LBL_NOT_RLVT_WO_MUSCLE_DTCT, ContourConfidenceLevel)
from .contour import (contour_checker_cc, contour_checker_mlo,
                      pre_extrapolation_cc, pre_extrapolation_mlo)
from .point import ImagePoint


class IDIProcessor:

    def __init__(self, logger, data_dcm):
        # TODO FUTURE : explicit dependency on foreign object ?!
        # TODO FUTURE : reorder attributes
        # TODO FUTURE: collimator shape robustness

        self.logger = logger
        self.display = {}
        self.kpi = {}
        self.body_part_examinated = data_dcm.get(KDCM_BDPE)
        self.columns = data_dcm.get(KDCM_COLS)
        self.rows = data_dcm.get(KDCM_ROWS)

        self.compression_force = data_dcm.get(KDCM_CPFR)
        self.coefficient_directeur = None
        self.ordonne_a_lorigine = None

        self.image_laterality = data_dcm.get(KDCM_IMLA)
        self.image_type = data_dcm.get(KDCM_IMTP)

        self.imager_pixel_spacing = list(
            map(float, data_dcm.get(KDCM_IMPS, '').split('/')))
        self.manufacturer = data_dcm.get(KDCM_MANU)
        self.manufacturer_model_name = data_dcm.get(KDCM_MODN)
        self.photometric_interpretation = data_dcm.get(KDCM_PHIN)
        self.pixel_array_original = data_dcm.get(KDCM_PIXA)
        self.presentation_intent_type = data_dcm.get(KDCM_PRIT)
        self.view_position = data_dcm.get(KDCM_VIPO)
        self.sop_class = data_dcm.get(KDCM_SOPC)
        self.software_version = data_dcm.get(KDCM_SFTV)
        self.bits_allocated = data_dcm.get(KDCM_BTSA)

        # Python3's dict.get method is equivalent to .get(key, None)
        self.collimator_shape = data_dcm.get(KDCM_COSH)
        self.collimator_left_vertical_edge = data_dcm.get(KDCM_COLV)
        self.collimator_right_vertical_edge = data_dcm.get(KDCM_CORV)
        self.collimator_lower_horizontal_edge = data_dcm.get(KDCM_COLH)
        self.collimator_upper_horizontal_edge = data_dcm.get(KDCM_COUH)

        self.breast_implant_present = data_dcm.get(KDCM_BRIP, 'NO')
        self.acquisition_time = data_dcm.get(KDCM_ACDT)

    # Eligibility

    def image_eligibility(self):
        """The eligibility of image is tested.
            If return status is I, we considered that the processing
            is not relevant
            the modality of eligibility is based on a conf file in json format
            the conf file is located in 'configuration\\eligibility.json'

            Output:
                Status:
                    W: Wait,
                    I: invalid
        """

        # TODO : Status normalization
        # TODO FUTURE : eligibility hierarchy
        # TODO FUTURE : hard call to json keys to remove

        self.logger.debug('image_processing_eligibility_check ...')
        self.status = 'W'
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'configuration', 'eligibility.json')

        if filename:
            with open(filename, 'r') as f:
                datastore = json.load(f)
        for key in datastore.keys():
            if self.__getattribute__(key) in datastore[key]['eligible']:
                pass
            else:
                self.logger.debug(
                    '%s %s' %
                    (self.__getattribute__(key), datastore[key]['eligible']))
                raise BPMProcessingInvalidException()

        self.logger.debug('image status = %s' % self.status)

    # Laterality

    def image_collimator_resizing(self):
        """The image is reshape in correlatioin with the collimator (shape/size)
        """

        # TODO : handle other than rectangular collimators exlicitly
        # TODO : Booleans are usefull

        if self.collimator_shape == 'RECTANGULAR':

            self.pixel_array_collimated = (
                np.asarray(self.pixel_array_original)[
                    self.collimator_upper_horizontal_edge:
                    self.collimator_lower_horizontal_edge,
                    self.collimator_left_vertical_edge:
                    self.collimator_right_vertical_edge-1]
            )
            self.rows_old = self.columns
            self.columns_old = self.rows
            self.rows = (self.collimator_lower_horizontal_edge -
                         self.collimator_upper_horizontal_edge - 1)
            self.columns = (self.collimator_right_vertical_edge -
                            self.collimator_left_vertical_edge - 1)
            self.flag_collimated = 'Y'

        else:
            self.pixel_array_collimated = np.asarray(self.pixel_array_original)
            self.flag_collimated = 'N'

    def laterality_transformation(self):
        """ Revert the image if laterality is'R' """
        self.logger.debug('Laterality: %s ...' % self.image_laterality)
        if self.image_laterality == 'R':
            self.pixel_array = np.fliplr(self.pixel_array_collimated)
            self.flag_lateralisation = 'Y'
        elif self.image_laterality == 'L':
            self.flag_lateralisation = 'N'
            self.pixel_array = np.asarray(self.pixel_array_collimated)
        self.pixel_array_original_for_pm = self.pixel_array
        self.logger.debug('Laterality_flag: %s' % self.flag_lateralisation)

    # Laterality
    # at the end of processing result need to be retransform

    def result_laterality_transformation(self):

        if self.image_laterality == 'R' and self.flag_lateralisation == 'Y':

            for i in range(0, len(self.contour_extrapolated), 1):
                self.contour_extrapolated[i] = [
                    self.columns-self.contour_extrapolated[i][0],
                    self.contour_extrapolated[i][1]]
            for i in range(0, len(self.contour), 1):
                self.contour[i] = [self.columns -
                                   self.contour[i][0], self.contour[i][1]]

            self.display['no_opposite_overlapping'] = (
                self.columns - self.display['no_opposite_overlapping'])
            self.display['breast_center_point'] = ImagePoint(

                self.columns - self.display['breast_center_point'].x,
                self.display['breast_center_point'].y)
            if self.flag_nipple == ContourConfidenceLevel.OK.value:
                if self.display['nipple_expected_point'] is None:
                    self.display['nipple_detected_point'] = ImagePoint(

                        self.columns - self.display['nipple_detected_point'].x,
                        self.display['nipple_detected_point'].y)
                elif self.display['nipple_detected_point'] is None:
                    self.display['nipple_expected_point'] = ImagePoint(

                        self.columns - self.display['nipple_expected_point'].x,
                        self.display['nipple_expected_point'].y)

            if self.view_position == 'MLO':
                if self.flag_imf == ContourConfidenceLevel.OK.value:
                    self.display['imf_point'] = ImagePoint(

                        self.columns - self.display['imf_point'].x,
                        self.display['imf_point'].y)
                if self.flag_pm == ContourConfidenceLevel.OK.value:
                    self.display['pectoral_muscle_start_point'] = ImagePoint(
                        self.columns -
                        self.display['pectoral_muscle_start_point'].x,
                        self.display['pectoral_muscle_start_point'].y)
                    self.display['pectoral_muscle_end_point'] = ImagePoint(
                        self.columns -
                        self.display['pectoral_muscle_end_point'].x,
                        self.display['pectoral_muscle_end_point'].y)
                    self.display['intersection_point_pm_pnl'] = ImagePoint(
                        self.columns -
                        self.display['intersection_point_pm_pnl'].x,
                        self.display['intersection_point_pm_pnl'].y)
            elif self.view_position == 'CC':
                if self.flag_at in [ContourConfidenceLevel.OK.value,
                                    ContourConfidenceLevel.PARTIAL.value]:
                    self.display['axillary_tail_point'] = ImagePoint(

                        self.columns -
                        self.display['axillary_tail_point'].x,
                        self.display['axillary_tail_point'].y)
                tkey = 'transition_to_intermammary_cleft_point'
                if self.flag_t2imc in [ContourConfidenceLevel.OK.value,
                                       ContourConfidenceLevel.PARTIAL.value]:
                    self.display[tkey] = (
                        ImagePoint(

                            self.columns -
                            self.display[tkey].x,
                            self.display[tkey].y))

                self.display['nipple_ideal_point'] = ImagePoint(

                    self.columns -
                    self.display['nipple_ideal_point'].x,
                    self.display['nipple_ideal_point'].y)

    # Contrast

    def contrast_verification(self):
        """ revert contrast if the contrast if right part of the image
        is darker than the left part """

        self.logger.debug(
            'Contrast verification %s ...' % self.photometric_interpretation)
        # Comparison of contrast mean value between first and last third
        pixel_array_1_3 = self.pixel_array[:round(self.rows),
                                           :round(self.columns / 3)]
        pixel_array_3_3 = self.pixel_array[:round(
            self.rows), round(self.columns / 3):]
        mean_value_1_3 = np.mean(pixel_array_1_3)
        mean_value_3_3 = np.mean(pixel_array_3_3)

        if mean_value_1_3 <= mean_value_3_3:
            self.pixel_array = self.pixel_array
            self.flag_contrast = 'N'
            image_contrast_inverted = np.zeros((self.rows, self.columns))

            mx = max(max(self.pixel_array_original))
            mn = min(min(self.pixel_array_original))
            med = mx - mn

            for i in range(self.rows):
                for j in range(self.columns):
                    image_contrast_inverted[i][j] = (
                        ((self.pixel_array[i][j] - med) * -1) + med)
            self.pixel_array_original_for_pm = image_contrast_inverted

        else:

            image_contrast_inverted = np.zeros((self.rows, self.columns))

            mx = max(max(self.pixel_array_original))
            mn = min(min(self.pixel_array_original))
            med = mx - mn

            for i in range(self.rows):
                for j in range(self.columns):
                    image_contrast_inverted[i][j] = (
                        ((self.pixel_array[i][j] - med) * -1) + med)
            self.pixel_array = image_contrast_inverted
            self.flag_contrast = 'Y'

        self.logger.debug('Contrast flag: %s' % self.flag_contrast)

    # Segmentation

    def segmentation(self):
        """ segmentation of the image with a threshold calculated
        on a gaussian mixture from histogram """

        self.logger.debug('Segmentation ...')
        # Read image

        pixel_array_ravel = self.pixel_array.ravel()

        # Fit GMM
        gmm = GaussianMixture(n_components=2, random_state=42)
        gmm = gmm.fit(X=np.expand_dims(pixel_array_ravel, 1))

        # Evaluate GMM
        gmm_x = np.linspace(0, pixel_array_ravel.max(), 50)
        gmm_y = np.exp(gmm.score_samples(gmm_x.reshape(-1, 1)))

        if gmm.means_[0] >= gmm.means_[1]:
            means1 = gmm.means_[0]
            means0 = gmm.means_[1]
        elif gmm.means_[0] < gmm.means_[1]:
            means1 = gmm.means_[1]
            means0 = gmm.means_[0]

        threshold = (10 * means1 + 1 * means0) / 11

        self.pixel_array = self.pixel_array > threshold

        # median filter to remove artefact on image
        self.pixel_array = sg.medfilt(self.pixel_array)

    # Branches detection

    def branches_detection(self):
        """ detection of branch, based on marching square method
        branch is a piece of contour, from a border to a border, """

        self.branches = measure.find_contours(
            self.pixel_array, 0.9, fully_connected='high',
            positive_orientation='high')

    # Contour checker

    def contour_checker(self):
        """ The contour is ckeked to estimate the relevancy of the computaiton
        for each view flag are define for each step of breast positioning

        Output is a sorted contour(x,y)"""
        self.logger.debug("contour checker ...")
        if self.view_position == 'MLO':
            self.contour, self.flag_nipple, self.flag_pm, self.flag_imf = \
                contour_checker_mlo(self.branches, self.rows,
                                    self.columns, self.imager_pixel_spacing)
            self.logger.debug('nipple %s pm %s imf %s' %
                              (self.flag_nipple, self.flag_pm, self.flag_imf))
        if self.view_position == 'CC':
            self.contour, self.flag_nipple, self.flag_at, self.flag_t2imc = \
                contour_checker_cc(self.branches, self.rows,
                                   self.columns, self.imager_pixel_spacing)
            self.logger.debug(
                'nipple %s at %s t2imc %s' %
                (self.flag_nipple, self.flag_at, self.flag_t2imc))

    # extrapolation "normal"

    def extrapolation_down(self):
        """Contour is extrapolated after point B and another contour
        is generated call 'contour_extrapoalted"""

        # Extrapolation after point B ##
        self.logger.debug('extrapolation ... ')

        contour_a_to_b = []
        contour_a_to_b = [
            [point[0], point[1]] for point in self.contour_down
            if point[0] >= self.B.x and point[0] <= self.A.x and
            point != [self.M.x, self.M.y]
        ]
        theta = [atan((point[0] - self.C.x) / (float(point[1]) - self.C.y))
                 for point in contour_a_to_b]
        rho = [np.sqrt((point[0] - self.C.x) ** 2 + (point[1] - self.C.y) ** 2)
               for point in contour_a_to_b]

        theta_min = min(theta)

        def curve(theta, a, b):
            return a * (theta - (90)) ** 2 + b

        popt, pcov = curve_fit(curve, theta, rho)

        theta_fit = np.arange(theta_min, theta_min * 2, -0.001)
        rho_fit = curve(theta_fit, popt[0], popt[1])

        extrapolation_x = rho_fit * (np.sin(theta_fit)) + self.C.x
        extrapolation_y = rho_fit * (np.cos(theta_fit)) + self.C.y

        contour_extrapolated_part = []
        contour_extrapolated_part = [
            [extrapolation_x[i], extrapolation_y[i]]
            for i in range(len(extrapolation_x))
            if extrapolation_x[i] >= 0]

        # Consitency between original contour: contour and extrapolated contour
        # "contour extrapolated part" based on distance from point C

        contour_origin_to_b = self.contour[:self.B_idx]
        contour_after_b = self.contour[self.B_idx:]
        contour_b_to_end_before_split = []
        contour_b_to_end_after_split = []
        self.index_split_point = self.B_idx
        split_point = None

        for i, point in enumerate(contour_extrapolated_part):
            diffs = [abs(pt[0] - point[0]) for pt in contour_after_b]
            idx = diffs.index(min(diffs)) + self.B_idx

            distextra = sqrt(
                pow((point[0] - self.C.x), 2) +
                pow((point[1] - self.C.y), 2))
            distorig = sqrt(
                pow((self.contour[idx][0] - self.C.x), 2) +
                pow((self.contour[idx][1] - self.C.y), 2))
            if distextra < distorig:
                if split_point:
                    self.split_point_down = ImagePoint(
                        point[0], point[1])
                else:
                    split_point = ImagePoint(
                        point[0], point[1])
                    self.index_split_point = i + self.B_idx

                contour_b_to_end_after_split.append(
                    [round(point[0]), round(point[1])])

            elif distextra >= distorig:
                contour_b_to_end_before_split.append(
                    [round(self.contour[idx][0]), round(self.contour[idx][1])])

        if split_point:
            pointa = getattr(self, 'split_point_down', ImagePoint(0, 0))
            threshold_len_b_to_end = len(contour_b_to_end_before_split) - 1
            try:
                pointb = ImagePoint(
                    contour_b_to_end_before_split[threshold_len_b_to_end][0],
                    contour_b_to_end_before_split[threshold_len_b_to_end][1])
            except:
                pointb = ImagePoint(
                    contour_origin_to_b[len(contour_origin_to_b) - 1][0],
                    contour_origin_to_b[len(contour_origin_to_b) - 1][1])
            contour_b_to_end_before_split.append(
                [(pointa.x + 2 * pointb.x) / 3, (pointa.y + 2 * pointb.y) / 3])
            contour_b_to_end_before_split.append(
                [(pointa.x + pointb.x) / 2, (pointa.y + pointb.y) / 2])
            contour_b_to_end_before_split.append(
                [(2 * pointa.x + pointb.x) / 3, (2 * pointa.y + pointb.y) / 3])
        else:

            pass
        self.contour_extrapolated = contour_origin_to_b + \
            contour_b_to_end_before_split + contour_b_to_end_after_split

        # extrapolation "inversé"

    def extrapolation_down_inv(self):
        """Contour is extrapolated after point Bp and another
        contour is generated; called contour_extrapolated"""

        # Extrapolation after point B ##
        self.logger.debug('extrapolation ... ')
        contour_down_inv = []
        contour_down_inv = [[point[0], (self.rows - point[1])]
                            for point in self.contour_up]
        contour_inv = []
        contour_inv = [[point[0], self.rows - point[1]]
                       for point in self.contour]

        Cp_inv = ImagePoint(self.Cp.x, self.rows - self.Cp.y)
        Bp_inv = ImagePoint(self.Bp.x, self.rows - self.Bp.y)
        Ap_inv = ImagePoint(self.Ap.x, self.rows - self.Ap.y)

        contour_a_to_b = []
        contour_a_to_b = [[point[0], point[1]] for point in contour_down_inv if
                          point[0] >= Bp_inv.x and point[0] <= Ap_inv.x and
                          point != [self.M.x, self.M.y]]
        theta = [atan((point[0] - Cp_inv.x) / (float(point[1]) - Cp_inv.y))
                 for point in contour_a_to_b]
        rho = [np.sqrt((point[0] - Cp_inv.x) ** 2 + (point[1] - Cp_inv.y) ** 2)
               for point in contour_a_to_b]

        theta_min = min(theta)

        def curve(theta, a, b):
            return a * (theta - (90)) ** 2 + b

        popt, pcov = curve_fit(curve, theta, rho)

        theta_fit = np.arange(theta_min, theta_min * 2, -0.001)
        rho_fit = curve(theta_fit, popt[0], popt[1])

        extrapolation_x = rho_fit * (np.sin(theta_fit)) + Cp_inv.x
        extrapolation_y = rho_fit * (np.cos(theta_fit)) + Cp_inv.y

        contour_extrapolated_part = []
        contour_extrapolated_part = [
            [extrapolation_x[i], extrapolation_y[i]]
            for i in range(len(extrapolation_x))
            if extrapolation_x[i] >= 0]

        # Consitency between original contour: contour and extrapolated contour
        # "contour extrapolated part" based on distance from point C

        contour_b_to_end_before_split = []
        contour_b_to_end_after_split = []
        self.index_split_point = self.Bp_idx
        split_point = None

        for i, point in enumerate(contour_extrapolated_part):
            diffs = [abs(pt[0] - point[0]) for pt in contour_inv]
            idx = diffs.index(min(diffs))

            distextra = sqrt(
                pow((point[0] - Cp_inv.x), 2) +
                pow((point[1] - Bp_inv.y), 2))
            distorig = sqrt(
                pow((contour_inv[idx][0] - Cp_inv.x), 2) +
                pow((contour_inv[idx][1] - Cp_inv.y), 2))

            if distextra < distorig:
                if not split_point:
                    split_point = ImagePoint(point[0], point[1])
                    self.index_split_point = i + self.Bp_idx

                contour_b_to_end_after_split.append(
                    [round(point[0]), round(point[1])])

            elif distextra >= distorig:
                contour_b_to_end_before_split.append(
                    [round(self.contour[idx][0]), round(self.contour[idx][1])])

        diffs = [abs(pt[0] - self.Bp.x) for pt in self.contour_extrapolated]
        idx = diffs.index(min(diffs))

        contour_origin_to_b = self.contour_extrapolated[idx:]

        if split_point:
            self.split_point_down_inv = ImagePoint(
                contour_b_to_end_after_split[0][0],
                contour_b_to_end_after_split[0][1])
            pointa = self.split_point_down_inv
            threshold_len_b_to_end = len(contour_b_to_end_before_split) - 1
            try:
                pointb = ImagePoint(
                    contour_b_to_end_before_split[threshold_len_b_to_end][0],
                    contour_b_to_end_before_split[threshold_len_b_to_end][1])
            except:
                pointb = ImagePoint(
                    contour_origin_to_b[0][0],
                    self.rows - contour_origin_to_b[0][1])

            contour_b_to_end_before_split.append(
                [(pointa.x + 2 * pointb.x) / 3, (pointa.y + 2 * pointb.y) / 3])
            contour_b_to_end_before_split.append(
                [(pointa.x + pointb.x) / 2, (pointa.y + pointb.y) / 2])
            contour_b_to_end_before_split.append(
                [(2 * pointa.x + pointb.x) / 3, (2 * pointa.y + pointb.y) / 3])

        contour_b_to_end = (contour_b_to_end_before_split +
                            contour_b_to_end_after_split)
        contour_b_to_end = [[point[0], self.rows - point[1]]
                            for point in contour_b_to_end]

        contour_b_to_end.reverse()

        self.contour_extrapolated = contour_b_to_end + contour_origin_to_b

    def mask(self):
        """ a mask is genrated from contour extrapolated"""

        self.logger.debug('mask generation...')

        shape = (self.rows, self.columns)
        image_built = np.zeros(shape)

        for point in self.contour_extrapolated:
            for idxi in [0]:
                for idxj in [0]:
                    image_built[int(point[1] + idxi), int(point[0] + idxj)] = 1

        image_built = img_as_ubyte(image_built)
        markers = rank.gradient(image_built, disk(15)) > 0

        self.label_image = label(markers, background=1)

        self.label_image = label(markers, background=1)
        tmp1 = self.label_image[750, 0]
        tmp2 = self.label_image[1250, 0]
        tmp3 = self.label_image[1750, 0]

        if tmp1 == tmp2 == tmp3:

            self.image_mask = self.label_image == tmp1

        else:
            self.image_mask = self.label_image == round(
                (tmp1 + (2 * tmp2) + tmp3) / 4)

    def breast_center(self):
        """ from mask define the breast center """

        self.logger.debug('breast center ...')
        cnt = 0
        sumx = 0
        sumy = 0

        mask_threshold = int((self.contour_extrapolated[0][1] +
                              self.contour_extrapolated[
                              len(self.contour_extrapolated) - 1][1]) / 2)
        tmp = self.image_mask[mask_threshold, 0]

        for y in range(self.rows):
            for x in range(self.columns):
                if self.image_mask[y, x]:
                    cnt = cnt + 1
                    sumx = sumx + x
                    sumy = sumy + y

        self.breast_center_point = ImagePoint(sumx / cnt, sumy / cnt)
        self.display['breast_center_point'] = self.breast_center_point

    def extrapolation(self):
        """ manage extrapolation """

        if self.view_position == 'MLO':
            if self.flag_imf == ContourConfidenceLevel.OK.value:
                (self.contour_down, self.M, self.H, self.B, self.A, self.C,
                 self.A_idx, self.B_idx) = pre_extrapolation_mlo(self.contour)
                self.extrapolation_down()
            else:
                self.contour_extrapolated = self.contour

        if self.view_position == 'CC':
            (self.contour_down, self.contour_up, self.M, self.H, self.B,
             self.Bp, self.A, self.Ap, self.C, self.Cp, self.A_idx, self.B_idx,
             self.Ap_idx, self.Bp_idx) = pre_extrapolation_cc(self.contour)

            if self.flag_t2imc in [ContourConfidenceLevel.OK.value,
                                   ContourConfidenceLevel.PARTIAL.value]:
                self.extrapolation_down()
            else:
                self.contour_extrapolated = self.contour

            if self.flag_at in [ContourConfidenceLevel.OK.value,
                                ContourConfidenceLevel.PARTIAL.value]:
                self.extrapolation_down_inv()
            else:

                self.contour_extrapolated = self.contour

        self.mask()
        self.breast_center()

    def kpi_overlapping(self):
        """ from mask define kpi
            KPI :
            no_bottom_overlapping
            no_opposite_overlapping
            no_top_overlapping (only CC)"""
        self.logger.debug('kpi overlap...')
        self.display['no_bottom_overlapping'] = int(
            max([point[1] for point in self.contour_extrapolated]))
        self.kpi['kpi_no_bottom_overlapping'] = (
            self.rows - self.display['no_bottom_overlapping']) * float(
            self.imager_pixel_spacing[1])

        self.display['no_opposite_overlapping'] = int(
            max([point[0] for point in self.contour_extrapolated]))
        self.kpi['kpi_no_opposite_overlapping'] = (
            self.columns - self.display['no_opposite_overlapping']) * float(
            self.imager_pixel_spacing[1])

        if self.view_position == 'CC':
            top_ov = int(
                min([point[1] for point in self.contour_extrapolated]))
            self.display['no_top_overlapping'] = top_ov if top_ov > 0 else 0
            self.kpi['kpi_no_top_overlapping'] = (
                self.display['no_top_overlapping'] *
                float(self.imager_pixel_spacing[1]))

    def centricity(self):
        """The system shall determine in CC views whether the breast
        is vertically centered within the image
        (only for CC views"""
        self.logger.debug('centricity')
        self.kpi['kpi_centricity'] = (
            (self.breast_center_point.y - (self.rows / 2)) / self.rows)

    def symmetry(self):
        """atrribute to determine the symmetry with a image with the same
        view_postion, and a opposite laterality """
        self.logger.debug('symmetry...')
        self.kpi['attribute_symmetry'] = self.breast_center_point.y / self.rows

    # kpi overlapping

    def imf_detection(self, distance_between_points_in_mm=30,
                      distance_for_straight_line_in_mm=25,
                      curvature_min=179):
        """define the inframmary fold point which is the point
        with the biggest curvature in the contour """

        self.logger.debug('imf detection  ... ')
        self.curvature_in_deg = 360
        dist = []
        imf_detection_contour = self.contour[self.index_split_point:]
        for i, point in enumerate(imf_detection_contour):
            if i < len(imf_detection_contour) - 1:
                distance = sqrt(
                    (point[0] - imf_detection_contour[i + 1][0]) ** 2 +
                    (point[1] - imf_detection_contour[i + 1][1]) ** 2)
                distanceinmm = distance * float(self.imager_pixel_spacing[0])
                dist.append(distanceinmm)

        # TODO: @VINCENT remove usage of statistics module
        referenced_distance = int(round(
            self.M.x * (1 / 16) * self.imager_pixel_spacing[0] /
            statistics.mean(dist)))

        for i, point in enumerate(self.contour):
            if ((i > self.index_split_point) and
                    (i < len(self.contour) - referenced_distance)):

                distance_b = sqrt(
                    (point[0] - self.contour[i - referenced_distance][0])**2 +
                    (point[1] - self.contour[i - referenced_distance][1])**2)
                distance_c = sqrt(
                    (point[0] - self.contour[i + referenced_distance][0])**2 +
                    (point[1] - self.contour[i + referenced_distance][1])**2)
                distance_a = sqrt(
                    (self.contour[i - referenced_distance][0] -
                     self.contour[i + referenced_distance][0]) ** 2 +
                    (self.contour[i - referenced_distance][1] -
                     self.contour[i + referenced_distance][1]) ** 2)
                cosa = (distance_b ** 2 + distance_c ** 2 -
                        distance_a ** 2) / (2 * distance_b * distance_c)
                curvature_in_rad = acos(round(cosa, 2))

                angle_deg = degrees(curvature_in_rad)
                if angle_deg < self.curvature_in_deg:
                    self.curvature_in_deg = angle_deg
                    self.imf_idx = i
                self.display['imf_point'] = ImagePoint(
                    self.contour[self.imf_idx][0],
                    self.contour[self.imf_idx][1])

        if self.curvature_in_deg <= curvature_min:
            im_pt = self.display['imf_point']
            self.kpi['kpi_imf_horizontal_position_in_mm'] = im_pt.x * float(
                self.imager_pixel_spacing[0])
            self.kpi['kpi_imf_vertical_position_in_mm'] = im_pt.y * float(
                self.imager_pixel_spacing[1])

            x_limit = self.display['imf_point'].x
            y_limit = self.display['imf_point'].y

            a = []
            for i in self.pixel_array:
                a.append(i[int(x_limit):])

            b = a[int(y_limit):]
            total_max = self.rows * self.columns
            total_b = (self.columns - x_limit) * (self.rows - y_limit)

            area = total_max - sum(sum(a))
            area_below_imf_line = total_b - sum(sum(b))
            self.kpi['kpi_absence_of_breast_sagging'] = (
                area_below_imf_line / area)

            imf_point = self.contour[self.imf_idx]

            contour_before_imf_point = []
            contour_after_imf_point = []

            tmp = 0
            for point in self.contour:
                if point == imf_point:
                    tmp = 1
                distance = sqrt(
                    (point[0] - imf_point[0]) ** 2 +
                    (point[1] - imf_point[1]) ** 2) * (
                        self.imager_pixel_spacing[0])
                if distance < distance_for_straight_line_in_mm:
                    if tmp == 0:
                        contour_before_imf_point.append(point)
                    elif tmp == 1:
                        contour_after_imf_point.append(point)
            contour_before_imf_point.append(imf_point)

            x_contour_before_imf_point = []
            x_contour_before_imf_point = [
                int(point[0]) for point in contour_before_imf_point]

            y_contour_before_imf_point = []
            y_contour_before_imf_point = [
                int(point[1]) for point in contour_before_imf_point]

            y_contour_after_imf_point = []
            y_contour_after_imf_point = [
                int(point[0]) for point in contour_after_imf_point]

            x_contour_after_imf_point = []
            x_contour_after_imf_point = [
                int(point[1]) for point in contour_after_imf_point]

            self.after_imf_x = x_contour_after_imf_point
            self.after_imf_y = y_contour_after_imf_point
            self.before_imf_x = x_contour_before_imf_point
            self.before_imf_y = y_contour_before_imf_point

            x_contour_after_imf_point = np.array(x_contour_after_imf_point)
            y_contour_before_imf_point = np.array(y_contour_before_imf_point)
            (slope_contour_before_imf_point,
             intercept_contour_before_imf_point,
             r_value_contour_before_imf_point,
             p_value_contour_before_imf_point,
             std_err_contour_before_imf_point) = stats.linregress(
                x_contour_before_imf_point, y_contour_before_imf_point)

            x_contour_after_imf_point = np.array(x_contour_after_imf_point)
            y_contour_after_imf_point = np.array(y_contour_after_imf_point)
            (slope_contour_after_imf_point, intercept_contour_after_imf_point,
             r_value_contour_after_imf_point, p_value_contour_after_imf_point,
             std_err_contour_after_imf_point) = stats.linregress(
                x_contour_after_imf_point, y_contour_after_imf_point)

            x_straight_line_before_imf_point = range(
                min(x_contour_before_imf_point),
                max(x_contour_before_imf_point), 1)

            x_straight_line_after_imf_point = range(
                min(x_contour_after_imf_point),
                max(x_contour_after_imf_point), 1)

            Cy = max(x_contour_after_imf_point) + (
                round(len(x_contour_after_imf_point) / 4))
            Cx = (intercept_contour_after_imf_point +
                  slope_contour_after_imf_point * (
                      max(x_contour_after_imf_point) +
                      (round(len(x_contour_after_imf_point) / 4))))

            Ax = max(x_contour_before_imf_point) + round(
                len(x_contour_before_imf_point) / 4)
            Ay = (intercept_contour_before_imf_point +
                  slope_contour_before_imf_point * (
                      max(x_contour_before_imf_point) +
                      round(len(x_contour_before_imf_point) / 4)))

            a = sqrt((imf_point[0] - Cx) ** 2 + (imf_point[1] - Cy) ** 2)
            b = sqrt((Cx - Ax) ** 2 + (Cy - Ay) ** 2)
            c = sqrt((imf_point[0] - Ax) ** 2 + (imf_point[1] - Ay) ** 2)

            self.kpi['kpi_inframmary_fold_without_skin_folds_angle'] = degrees(
                acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)))
            self.logger.debug(
                'inframmary_fold_without_skin_folds_angle %s' %
                self.kpi['kpi_inframmary_fold_without_skin_folds_angle'])

            self.contour_to_circle_fit = []
            for i in range(len(x_straight_line_before_imf_point)):
                lim_before_pt = (intercept_contour_before_imf_point +
                                 slope_contour_before_imf_point *
                                 x_straight_line_before_imf_point[i])
                imf_point_idx = len(y_contour_before_imf_point) - 1 - i
                if y_contour_before_imf_point[imf_point_idx] >= lim_before_pt:
                    self.contour_to_circle_fit.append(
                        [x_contour_before_imf_point[imf_point_idx],
                         y_contour_before_imf_point[imf_point_idx]])
                else:
                    break

            for i in range(len(x_straight_line_after_imf_point)):
                diffs = [abs(item - x_straight_line_after_imf_point[i])
                         for item in x_contour_after_imf_point]
                idx = diffs.index(min(diffs))
                lim_after_pt = (intercept_contour_after_imf_point +
                                slope_contour_after_imf_point *
                                x_straight_line_after_imf_point[i])
                if y_contour_after_imf_point[idx] >= lim_after_pt:
                    self.contour_to_circle_fit.append(
                        [y_contour_after_imf_point[i],
                         x_contour_after_imf_point[i]])

                else:

                    break

            image_for_imf_circle_fit = np.zeros([self.rows, self.columns])

            for point in self.contour_to_circle_fit:
                image_for_imf_circle_fit[point[1], point[0]] = 1
            imagee = img_as_ubyte(image_for_imf_circle_fit)
            # Detect two radii

            hough_radii = np.arange(20, 35, 2)
            hough_res = hough_circle(imagee, hough_radii)

            # Select the most prominent 5 circles
            accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                                       total_num_peaks=1)
            try:
                self.kpi['kpi_inframmary_fold_without_skin_folds_radius'] = (
                    float(radii * self.imager_pixel_spacing[0]))
            except:
                self.kpi['kpi_inframmary_fold_without_skin_folds_radius'] = 0
        else:
            self.display['imf_point'] = ImagePoint(0, 0)
            self.logger.debug(LBL_IMF_PT_UNDEF)
            # self.kpi.update({k: LBL_IMF_PT_UNDEF for k in [
            #     'kpi_imf_horizontal_position_in_mm',
            #     'kpi_imf_vertical_position_in_mm',
            #     'kpi_inframmary_fold_without_skin_folds_radius',
            #     'kpi_inframmary_fold_without_skin_folds_angle',
            #     'kpi_absence_of_breast_sagging']})

    # at/t2imc detection

    def at_t2imc_detection(self):

        self.logger.debug('at_t2imc_detection')

        self.image_mask = np.invert(self.image_mask)

        difference = (self.pixel_array <= 0) - (self.image_mask == 0)
        difference_erosion = ndi.binary_erosion(
            difference, structure=np.ones((20, 20))).astype('bool')
        difference_median_filter = rank.median(difference_erosion, disk(5))
        difference_dilation = (
            ndi
            .binary_dilation(difference_median_filter,
                             structure=np.ones((20, 20)))
            .astype('bool'))

        self.image_difference = difference_dilation

        image_diff_at = self.image_difference[:round(self.rows / 2)]
        image_diff_t2imc = self.image_difference[round(self.rows / 2):]
        self.kpi['kpi_axillary_tail_area'] = sum(
            sum(image_diff_at)) * self.imager_pixel_spacing[0] ** 2
        self.kpi['kpi_transition_to_intermammary_cleft_area'] = sum(
            sum(image_diff_t2imc)) * self.imager_pixel_spacing[0] ** 2

        x_at = 0
        y_at = 0
        if self.kpi['kpi_axillary_tail_area'] == 0:
            pass
        else:
            for j, column in enumerate(image_diff_at):
                for i, point in enumerate(column):
                    if point:
                        if i > x_at and i < 3 * self.rows / 4:
                            x_at = i
                            y_at = j

        self.display['axillary_tail_point'] = ImagePoint(x_at, y_at)

        x_t2imc = 0
        y_t2imc = 0
        if self.kpi['kpi_transition_to_intermammary_cleft_area'] == 0:
            pass
        else:
            for j, column in enumerate(image_diff_t2imc):
                for i, point in enumerate(column):
                    if point:
                        if i > x_t2imc and i < 3 * self.rows / 4:
                            x_t2imc = i
                            y_t2imc = j + round(self.rows / 2)

        self.display['axillary_tail_point'] = ImagePoint(x_at, y_at)
        self.display['transition_to_intermammary_cleft_point'] = ImagePoint(
            x_t2imc, y_t2imc)
        self.kpi['kpi_axillary_taildistance'] = self.display.get(
            'axillary_tail_point').x * self.imager_pixel_spacing[0]
        self.kpi['kpi_transition_to_intermammary_cleft_distance'] = (
            self.display['transition_to_intermammary_cleft_point'].x *
            self.imager_pixel_spacing[0])

    # nipple_detection

    def nipple_detection(self, number_of_point_to_smooth=320,
                         threshold_of_nipple_selection=4.5):
        """The goal is to extract from the contour the nipple.

        The smoothed contour is calculated, for a bunch of 161 points.
        The average position in X and in Y of these points is selected.

        From the central part of the contour, there are a comparison between
        original contour and a smooth contour, the most distant point in the
        original contour from smooth contour is the nipple.

        For this point the computation is based on a dedicated part of the
        contour this parts is define:

            In MLO is the skin line between 1/3 upper
            and 1/5 lower of the contour

            In CC is the skin line between 1/4 of the contour for each side"""

        self.logger.debug('nipple_detection')
        if self.view_position == 'CC':
            contour_nipple_detection = self.contour[
                round(len(self.contour) / 4): round(
                    len(self.contour) - len(self.contour) / 4)]
        elif self.view_position == 'MLO':
            contour_nipple_detection = self.contour[
                round(len(self.contour) / 3): round(
                    len(self.contour) - len(self.contour) / 5)]

        smooth_contour = []

        for point in range(round(number_of_point_to_smooth / 2),
                           round(len(contour_nipple_detection) -
                                 number_of_point_to_smooth / 2), 1):
            tmp_contour_x = []
            tmp_contour_y = []

            for i in range(round(-number_of_point_to_smooth / 2), round(
                    number_of_point_to_smooth / 2), 1):
                tmp_contour_x.append(contour_nipple_detection[point + i][0])
                tmp_contour_y.append(contour_nipple_detection[point + i][1])

            if len(tmp_contour_y) > 0:

                tmp = [np.mean(tmp_contour_x), np.mean(tmp_contour_y)]
                smooth_contour.append(tmp)

            else:
                break

        compare_contour = contour_nipple_detection[
            round(number_of_point_to_smooth / 2): round(
                -number_of_point_to_smooth / 2)]

        difference = []

        for i in range(len(smooth_contour)):
            difference.append(sqrt(
                (smooth_contour[i][0] - compare_contour[i][0]) ** 2 + (
                    smooth_contour[i][1] - compare_contour[i][1]) ** 2))

        idx = difference.index(max(difference))
        self.display['nipple_detected_point'] = ImagePoint(
            compare_contour[idx][0], compare_contour[idx][1])

        if self.view_position == 'CC':
            difference_min = 1000000
            for point in range(len(self.contour)):
                difference_tmp = np.abs(
                    self.contour[point][1] - round(self.breast_center_point.y))
                if difference_min > difference_tmp:
                    difference_min = difference_tmp
                    idx_ideal_point = point

            self.display['nipple_ideal_point'] = ImagePoint(
                self.contour[idx_ideal_point][0],
                self.contour[idx_ideal_point][1])

        else:
            pass

        if max(difference) < 4.5:
            if self.view_position == 'CC':
                self.display['nipple_expected_point'] = self.M
                self.display['nipple_detected_point'] = None

            else:  # in MLO
                # to adapt with PM
                self.display['nipple_expected_point'] = self.M
                self.display['nipple_detected_point'] = None
        else:
            self.display['nipple_expected_point'] = None

        if self.display['nipple_detected_point'] is None:
            self.kpi['kpi_nipple_visible_in_profile'] = False
        else:
            self.kpi['kpi_nipple_visible_in_profile'] = True

        if self.view_position == 'CC':
            nip_key = ('nipple_detected_point'
                       if self.display['nipple_detected_point']
                       else 'nipple_expected_point')
            self.nipple_point_to_evaluate = self.display[nip_key]
            a = sqrt(
                (self.display['nipple_ideal_point'].x -
                 self.nipple_point_to_evaluate.x) ** 2 +
                (self.display['nipple_ideal_point'].y -
                 self.nipple_point_to_evaluate.y) ** 2)
            b = sqrt((self.display['nipple_ideal_point'].x - 0) ** 2 + (
                self.display['nipple_ideal_point'].y -
                self.nipple_point_to_evaluate.y) ** 2)
            c = sqrt(
                (0 - self.nipple_point_to_evaluate.x) ** 2 + (
                    self.nipple_point_to_evaluate.y -
                    self.nipple_point_to_evaluate.y) ** 2)

            self.kpi['kpi_nipple_angle'] = degrees(
                acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))

        if self.view_position == 'CC':
            self.kpi['attribute_length_of_posterior_nipple_line'] = (
                self.nipple_point_to_evaluate.x * self.imager_pixel_spacing[0])
        else:
            self.logger.debug(LBL_NOT_RLVT_WO_MUSCLE_DTCT)

    def pectoral_muscle_detection_dbscan(self):
        self.logger.debug('pectoral_muscle_detection_dbscan...')

        half_c_len = round(len(self.contour_extrapolated)/2)
        min_contour_x_pm = int(
            min(self.contour_extrapolated[:half_c_len])[0])

        image_corner_left = self.pixel_array_original_for_pm[0:round(
            self.display['no_bottom_overlapping']/3),
            0:round(min_contour_x_pm-10)]

        image_corner_left_ravel = image_corner_left.ravel()
        # Fit GMM
        gmm = GaussianMixture(n_components=2, random_state=42)
        try:
            gmm = gmm.fit(X=np.expand_dims(image_corner_left_ravel, 1))
        except:
            self.kpi['pectoral_muscle_width'] = 0
            self.kpi['pectoral_muscle_angle'] = 0
            self.kpi['attribute_length_of_posterior_nipple_line'] = 0
            self.display['pectoral_muscle_end_point'] = ImagePoint(0, 0)
            self.display['pectoral_muscle_start_point'] = ImagePoint(0, 0)
            self.display['intersection_point_pm_pnl'] = ImagePoint(0, 0)
            return

        # Evaluate GMM
        gmm_x = np.linspace(0, image_corner_left_ravel.max(), 50)
        gmm_y = np.exp(gmm.score_samples(gmm_x.reshape(-1, 1)))

        limit_min = gmm.means_.min()
        img_first_gmm = np.zeros((self.pixel_array_original_for_pm.shape))
        for i in range(img_first_gmm.shape[0]):
            for j in range(img_first_gmm.shape[1]):
                if self.pixel_array_original_for_pm[i, j] < limit_min:
                    img_first_gmm[i, j] = limit_min
                else:
                    img_first_gmm[i,
                                  j] = self.pixel_array_original_for_pm[i, j]

        hist, bins_center = exposure.histogram(image_corner_left)

        img_first_gmm_ravel = img_first_gmm.ravel()

        # Fit GMM
        gmm = GaussianMixture(n_components=3, random_state=42)
        gmm = gmm.fit(X=np.expand_dims(img_first_gmm_ravel, 1))

        # Evaluate GMM
        gmm_x = np.linspace(0, img_first_gmm_ravel.max(), 50)
        gmm_y = np.exp(gmm.score_samples(gmm_x.reshape(-1, 1)))

        limit_min = gmm.means_.max()-50

        img_second_gmm = np.zeros((self.pixel_array_original_for_pm.shape))
        for i in range(img_second_gmm.shape[0]):
            for j in range(img_second_gmm.shape[1]):
                if img_first_gmm[i, j] < limit_min:
                    img_second_gmm[i, j] = round(limit_min)
                else:
                    img_second_gmm[i, j] = round(img_first_gmm[i, j])

        hist, bins_center = exposure.histogram(img_first_gmm)

        selem = np.ones((5, 20))
        img_median = rank.median(img_second_gmm/img_second_gmm.max(), selem)
        self.logger.debug(img_median.shape)
        img_resize = transform.resize(
            img_median, (round(img_median.shape[0]/10),
                         round(img_median.shape[1]/10)))
        self.logger.debug(img_resize.shape)

        img_gradient = np.zeros(img_resize.shape)
        img_gradient_follower = np.zeros(img_resize.shape)

        a = ((img_resize.max()-img_resize.min()) / img_resize.shape[1])
        x = []
        y = []

        for i in range(img_resize.shape[0]):
            for j in range(img_resize.shape[1]):
                if j == 0:
                    alpha = round(img_resize[i, j], 3)
                    alpha2 = round(img_resize[i, j], 3)
                else:
                    if round(img_resize[i, j], 3) <= alpha:
                        alpha = round(img_resize[i, j], 3)
                    else:
                        alpha = alpha
                if round(img_resize[i, j], 3) <= alpha2:
                    alpha2 = round(img_resize[i, j], 3)
                else:
                    alpha2 = alpha2+a

                img_gradient[i, j] = alpha
                img_gradient_follower[i, j] = alpha2

        min_contour_x_10 = round(min_contour_x_pm/10)

        x = []
        y = []

        diff_gradient = img_gradient_follower > img_gradient_follower.min()
        for i in range(round(img_gradient_follower.shape[0]/2)):
            for j in range(1, min_contour_x_10, 1):
                if (not diff_gradient[i, j]) and diff_gradient[i, j-1]:
                    x.append(j*10)
                    y.append(i*10)

        Y = [[x[i], y[i]] for i in range(len(x))]

        scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
        X = scaler.fit_transform(Y)

        self.logger.debug('Img gradient follower %s' %
                          round(img_gradient_follower.shape[0]/2))
        self.logger.debug('Min contour %s' % min_contour_x_10)
        self.logger.debug('y length %s' % len(y))
        self.logger.debug('x length %s' % len(x))
        self.logger.debug('Y length %s' % len(Y))
        self.logger.debug('X length %s' % len(X))

        # #############################################################################
        # Compute DBSCAN
        db = DBSCAN(eps=0.3, min_samples=10).fit(X)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_

        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        self.logger.debug('Estimated number of clusters: %d' % n_clusters_)

        X = scaler.inverse_transform(X)
        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = [plt.cm.Spectral(each)
                  for each in np.linspace(0, 1, len(unique_labels))]
        pm_candidates = []

        # Preset values to avoid errors later

        self.kpi['pectoral_muscle_width'] = 0
        self.kpi['pectoral_muscle_angle'] = 0
        self.kpi['attribute_length_of_posterior_nipple_line'] = 0
        self.display['pectoral_muscle_end_point'] = ImagePoint(0, 0)
        self.display['pectoral_muscle_start_point'] = ImagePoint(0, 0)
        self.display['intersection_point_pm_pnl'] = ImagePoint(0, 0)

        for k, col in zip(unique_labels, colors):
            try:
                if k == -1:
                    # Black used for noise.
                    col = [0, 0, 0, 1]
                    break

                class_member_mask = (labels == k)

                xy = X[class_member_mask & core_samples_mask]
                xy_2 = []
                for i in xy:
                    if i[0] < 1:
                        break
                    else:
                        xy_2.append(i)
                xy_2 = np.asarray(xy_2)

                xx = []
                yy = []
                for i in range(len(xy_2)):
                    xx.append(xy_2[i][0])
                    yy.append(xy_2[i][1])
                xx = np.asarray(xx)
                yy = np.asarray(yy)

                model = RANSACRegressor(min_samples=2)

                model.fit(xx[:, np.newaxis], yy)
                self.logger.debug(model.estimator_)

                xfit = np.linspace(0, 600, 100)
                yfit = model.predict(xfit[:, np.newaxis])

                p0 = [xfit[0], yfit[0]]
                p1 = [xfit[len(xfit)-1], yfit[len(xfit)-1]]

                coefficient_directeur = (p0[1] - p1[1])/(p0[0] - p1[0])
                ordonne_a_lorigine = p1[1]-(coefficient_directeur*p1[0])

                if (coefficient_directeur < 0 and
                        ordonne_a_lorigine < (4*self.rows/4)):
                    pm_candidates.append(
                        (coefficient_directeur, ordonne_a_lorigine,
                         len(xy_2[:, 0])))

                if len(pm_candidates) == 0:
                    self.coefficient_directeur = 0
                    self.ordonne_a_lorigine = 0
                elif len(pm_candidates) == 1:
                    self.coefficient_directeur = pm_candidates[0][0]
                    self.ordonne_a_lorigine = pm_candidates[0][1]
                else:
                    lenght = [pm[2] for pm in pm_candidates]
                    idx = lenght.index(max(lenght))

                    self.coefficient_directeur = pm_candidates[idx][0]
                    self.ordonne_a_lorigine = pm_candidates[idx][1]

                if (self.coefficient_directeur != 0 and
                        self.ordonne_a_lorigine != 0):

                    self.display['pectoral_muscle_end_point'] = ImagePoint(
                        int((0-self.ordonne_a_lorigine) /
                            self.coefficient_directeur), 0)
                    self.display['pectoral_muscle_start_point'] = ImagePoint(
                        0, int(self.coefficient_directeur * 0 +
                               self.ordonne_a_lorigine))

                    self.kpi['pectoral_muscle_width'] = (
                        self.display['pectoral_muscle_end_point'].x *
                        self.imager_pixel_spacing[0])
                    self.kpi['pectoral_muscle_angle'] = degrees(atan(
                        self.display['pectoral_muscle_end_point'].x /
                        self.display['pectoral_muscle_start_point'].y))

                    self.intersection_pnl_line_edge = 0

                    try:
                        a = self.display['nipple_detected_point']
                    except:
                        a = self.display['nipple_expected_point']
                    c = ImagePoint(
                        self.display['pectoral_muscle_end_point'].x,
                        self.display['pectoral_muscle_end_point'].y)
                    distance_b = sqrt((c.x-a.x)**2 + (c.y-a.y)**2)

                    for i in range(
                            self.display['pectoral_muscle_end_point'].x-1,
                            -500, -1):
                        y = (self.coefficient_directeur * i +
                             self.ordonne_a_lorigine)
                        b = ImagePoint(i, y)
                        distance_c = sqrt((b.x-a.x)**2 + (b.y-a.y)**2)
                        distance_a = sqrt((c.x-b.x)**2 + (c.y-b.y)**2)
                        angle = round(degrees(
                            acos((distance_a**2 + distance_c**2 -
                                  distance_b**2) /
                                 (2*distance_a*distance_c))))
                        if i == 0:
                            self.intersection_pm_line_edge = b

                        if angle == 90:
                            self.intersection_pnl_line_pm_line = b
                            break
                        elif angle < 90:
                            self.intersection_pnl_line_pm_line = b
                            break

                    self.coefficient_directeur_pnl = ((
                        a.y - self.intersection_pnl_line_pm_line.y) /
                        (a.x - self.intersection_pnl_line_pm_line.x))
                    self.ordonne_a_lorigine_pnl = (
                        self.intersection_pnl_line_pm_line.y -
                        (self.coefficient_directeur_pnl *
                         self.intersection_pnl_line_pm_line.x))
                    self.intersection_pnl_line_edge = ImagePoint(
                        0, self.ordonne_a_lorigine_pnl)

                    if self.intersection_pnl_line_edge == 0:
                        self.kpi[
                            'pectoral_muscle_visible_up_to_nipple_line'] = 0
                    else:
                        self.kpi[
                            'pectoral_muscle_visible_up_to_nipple_line'] = (
                                (self.intersection_pnl_line_edge.y -
                                 self.display['pectoral_muscle_start_point'].y
                                 ) / self.intersection_pnl_line_edge.y)

                    self.kpi[
                        'attribute_length_of_posterior_nipple_line'] = (sqrt(
                            (self.intersection_pnl_line_pm_line.x-a.x)**2 +
                            (self.intersection_pnl_line_pm_line.y-a.y)**2) *
                        self.imager_pixel_spacing[0])

                    self.display['intersection_point_pm_pnl'] = (
                        self.intersection_pnl_line_pm_line)
                else:
                    pt_0 = ImagePoint(0, 0)
                    self.kpi['pectoral_muscle_width'] = 0
                    self.kpi['pectoral_muscle_angle'] = 0
                    self.kpi['attribute_length_of_posterior_nipple_line'] = 0
                    self.display['pectoral_muscle_end_point'] = pt_0
                    self.display['pectoral_muscle_start_point'] = pt_0
                    self.display['intersection_point_pm_pnl'] = pt_0
            except Exception as e:
                self.logger.debug(e)

        self.logger.debug('coef %s' % self.coefficient_directeur)
        self.logger.debug('ord %s' % self.ordonne_a_lorigine)

    def image_processing(self):
        st = time.time()

        self.image_eligibility()
        self.image_collimator_resizing()
        self.laterality_transformation()
        self.contrast_verification()
        self.segmentation()
        self.branches_detection()
        self.contour_checker()
        if self.view_position == 'MLO':
            if self.flag_imf == ContourConfidenceLevel.OK.value:
                self.extrapolation()
                self.imf_detection()
            else:
                self.contour_extrapolated = self.contour
                self.mask()
                self.breast_center()
            self.kpi_overlapping()
            self.symmetry()

            if self.flag_nipple == ContourConfidenceLevel.OK.value:
                self.nipple_detection()
            if self.flag_pm == ContourConfidenceLevel.OK.value:
                self.pectoral_muscle_detection_dbscan()

        if self.view_position == 'CC':
            if (self.flag_at in [ContourConfidenceLevel.OK.value,
                                 ContourConfidenceLevel.PARTIAL.value] or
                self.flag_t2imc in [ContourConfidenceLevel.OK.value,
                                    ContourConfidenceLevel.PARTIAL.value]):
                self.extrapolation()
                self.at_t2imc_detection()
            else:
                self.contour_extrapolated = self.contour
                self.mask()
                self.breast_center()

            self.kpi_overlapping()
            self.symmetry()
            self.centricity()

            if self.flag_nipple == ContourConfidenceLevel.OK.value:
                self.nipple_detection()

        if (self.image_laterality == 'R' and
                self.flag_lateralisation == 'Y'):
            self.result_laterality_transformation()

        self.kpi['kpi_compression'] = self.compression_force

        self.processing_time = time.time() - st

        self.logger.debug('Processing done %0.2fs' % self.processing_time)

    def image_processing_printer(self, px_array, save_fig='n'):
        try:
            self.logger.debug('imf %s pm %s nipple %s' %
                              (self.flag_imf, self.flag_pm, self.flag_nipple))
            self.logger.debug('Curvature = ', self.curvature_in_deg)
        except:
            self.logger.debug(
                'nipple %s at %s t2imc %s' %
                (self.flag_nipple, self.flag_at, self.flag_t2imc))

        plt.figure(figsize=(15, 15))
        plt.imshow(px_array, cmap=plt.cm.binary)

        for i in range(0, len(self.contour), 1):
            plt.plot(self.contour[i][0], self.contour[i][1], 'b,')

        if self.view_position == 'MLO':
            if self.flag_imf == ContourConfidenceLevel.OK.value:
                plt.plot(self.display['imf_point'].x,
                         self.display['imf_point'].y, 'bo')

                x_coord = self.display['imf_point'].x
                y_coord = self.display['imf_point'].y
                plt.annotate('IMF', fontsize=20,
                             xy=(x_coord, y_coord),
                             xycoords='data',
                             color='orange',
                             ha='center')

            if self.flag_pm == ContourConfidenceLevel.OK.value:
                try:
                    self.nipple_point_to_evaluate = self.display[
                        'nipple_detected_point']
                except:
                    self.nipple_point_to_evaluate = self.display[
                        'nipple_expected_point']
                try:
                    plt.plot((self.display['pectoral_muscle_start_point'].x,
                              self.display['pectoral_muscle_end_point'].x),
                             (self.display['pectoral_muscle_start_point'].y,
                              self.display['pectoral_muscle_end_point'].y),
                             'r--')

                    x_coord = float(
                        (self.display['pectoral_muscle_start_point'].x +
                         self.display['pectoral_muscle_end_point'].x) / 2)
                    y_coord = float(
                        (self.display['pectoral_muscle_start_point'].y +
                         self.display['pectoral_muscle_end_point'].y) / 2)
                    plt.annotate('PECT', fontsize=20,
                                 xy=(x_coord, y_coord),
                                 xycoords='data',
                                 color='orange',
                                 ha='center')

                    plt.plot((self.display['intersection_point_pm_pnl'].x,
                              self.nipple_point_to_evaluate.x), (
                        self.display['intersection_point_pm_pnl'].y,
                        self.nipple_point_to_evaluate.y))

                    x_coord = float(
                        (self.display['intersection_point_pm_pnl'].x +
                         self.nipple_point_to_evaluate.x) / 2)
                    y_coord = float(
                        (self.display['intersection_point_pm_pnl'].y +
                         self.nipple_point_to_evaluate.y) / 2)
                    plt.annotate('PECT INTERSECT', fontsize=20,
                                 xy=(x_coord, y_coord),
                                 xycoords='data',
                                 color='orange',
                                 ha='center')

                except:
                    pass

        elif self.view_position == 'CC':
            if self.flag_at in [ContourConfidenceLevel.OK.value,
                                ContourConfidenceLevel.PARTIAL.value]:
                plt.plot(self.display['axillary_tail_point'].x,
                         self.display['axillary_tail_point'].y, 'y*')

                x_coord = self.display['axillary_tail_point'].x
                y_coord = self.display['axillary_tail_point'].y
                plt.annotate('AXILLARY POINT', fontsize=20,
                             xy=(x_coord, y_coord),
                             xycoords='data',
                             color='orange',
                             ha='center')

            if self.flag_t2imc in [ContourConfidenceLevel.OK.value,
                                   ContourConfidenceLevel.PARTIAL.value]:
                plt.plot(
                    self.display['transition_to_intermammary_cleft_point'].x,
                    self.display['transition_to_intermammary_cleft_point'].y,
                    'y*')

                x_coord = (
                    self.display['transition_to_intermammary_cleft_point'].x)
                y_coord = (
                    self.display['transition_to_intermammary_cleft_point'].y)
                plt.annotate('TRANSITION TO IMC', fontsize=20,
                             xy=(x_coord, y_coord),
                             xycoords='data',
                             color='orange',
                             ha='center')

        if self.flag_nipple == ContourConfidenceLevel.OK.value:
            try:
                plt.plot(self.display['nipple_detected_point'].x,
                         self.display['nipple_detected_point'].y, 'r*')
                plt.annotate('NIPPLE DETECTED', fontsize=20,
                             xy=(self.display['nipple_detected_point'].x,
                                 self.display['nipple_detected_point'].y),
                             xycoords='data',
                             color='orange',
                             ha='center')
            except:
                plt.plot(self.display['nipple_expected_point'].x,
                         self.display['nipple_expected_point'].y, 'y*')
                x_coord = self.display['nipple_expected_point'].x
                y_coord = self.display['nipple_expected_point'].y
                plt.annotate('NIPPLE EXPECTED', fontsize=20,
                             xy=(x_coord, y_coord),
                             xycoords='data',
                             color='orange',
                             ha='center')

        plt.plot((0, self.columns - 1),
                 (self.display['no_bottom_overlapping'],
                  self.display['no_bottom_overlapping']),
                 'r')
        x_coord = float(self.display['no_bottom_overlapping'] / 2)
        y_coord = float(
            (self.columns - 1 + self.display['no_bottom_overlapping']) / 2)
        plt.annotate('BTM OVERLAP', fontsize=20,
                     xy=(x_coord, y_coord),
                     xycoords='data',
                     color='orange',
                     ha='center')
        plt.plot((self.display['no_opposite_overlapping'],
                  self.display['no_opposite_overlapping']), (0, self.rows - 1),
                 'r')
        x_coord = float(self.display['no_opposite_overlapping'] / 2)
        y_coord = float((self.rows - 1 +
                         self.display['no_opposite_overlapping']) / 2)
        plt.annotate('OPPOSITE OVERLAP', fontsize=20,
                     xy=(x_coord, y_coord),
                     xycoords='data',
                     color='orange',
                     ha='center')
        if self.view_position == 'CC':
            plt.plot((0, self.columns - 1),
                     (self.display['no_top_overlapping'],
                      self.display['no_top_overlapping']),
                     'r')
            x_coord = float(self.display['no_top_overlapping'] / 2)
            y_coord = float((self.columns - 1 +
                             self.display['no_top_overlapping']) / 2)
            plt.annotate('TOP OVERLAP', fontsize=20,
                         xy=(x_coord, y_coord),
                         xycoords='data',
                         color='orange',
                         ha='center')
        # plt.show()
        if save_fig == 'n':
            pass
        else:
            try:
                plt.savefig(save_fig)
            except Exception as e:
                self.logger.debug(e)
