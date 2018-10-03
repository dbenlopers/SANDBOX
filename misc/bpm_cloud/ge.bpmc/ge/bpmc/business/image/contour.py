# -*- coding: utf-8 -*-

import enum
from math import *

import numpy as np
import pandas as pd

from . import (MAX_BRANCHES_CC, MAX_BRANCHES_MLO, MAX_INTERSECT_DIST,
               MAX_INTERSECT_DIST_LEFT, RELEVANCE_MIN_POINTS,
               ContourConfidenceLevel)
from .point import find_A, find_B, find_C, find_H, find_M, localise


def relevant_branch(branch, max_y, max_x, min_points):
    '''
    Utility to determine if a branch is relevant.

    :param branch: ndarray of 2 dimensions containing doubles.
    :param max_y: int, max y position.
    :param max_x: int, max x position.
    :param min_points: int, minimal number of points for the branch to be
    relevant.
    '''
    x, y = branch[-1, 0], branch[-1, 1]
    return ((y == max_y or x == max_x or 0 in [x, y]) and
            len(branch) > min_points)


def relevant_branches(branches, rows, columns,
                      min_points=RELEVANCE_MIN_POINTS):
    '''
    Utility to extract relevant branches in ndarrays.

    :param branch: ndarrays of 2 dimensions containing doubles.
    :param rows: int, rows in image.
    :param columns: int, columns in image.
    :param min_points: int, minimal number of points for a branch to be
    relevant.
    '''
    max_y = rows - 1
    max_x = columns - 1
    return list(filter(lambda b: relevant_branch(b, max_y, max_x, min_points),
                       branches))


def sort_branches(branches, items=[]):
    '''
    Utility to sort branches based on points y and x coordinates.

    :param branches: list of ndarray of 2 dimensions containing doubles.
    :param items: list of dicts such as below.
    '''
    for n, branch in enumerate(branches):
        items.append({
            'x': branch[0][0],
            'y': branch[0][1],
            'branch_idx': 0,
            'branches_idx': n
        })
        items.append({
            'x': branch[-1][0],
            'y': branch[-1][1],
            'branch_idx': 1,
            'branches_idx': n
        })

    return sorted(items, key=lambda pt: (pt['y'], pt['x']))


def distance_pt(ref, pt, spacing):
    '''
    Utility returning the distance between two points.

    :param ref: a dict containing points 'x' and 'y' values.
    :param pt: a dict containing points 'x' and 'y' values.
    :param spacing: float, horizontal pixel spacing.
    '''
    return (sqrt(pow((pt['x'] - ref['x']), 2) + pow((pt['y'] - ref['y']), 2)) *
            spacing)


def next_point(ref, points, spacing, ignored=[]):
    '''
    Utility returning the closest point.

    :param ref: a dict containing points 'x' and 'y' values, the branch
    index if the list containing it 'branches_idx' and the point index
    in the branch 'branch_idx'.
    :param spacing: float, horizontal pixel spacing.
    :param points: a list of  dicts containing points 'x' and 'y' values.
    :param ignored: a list of branches_idx that should be ignored.
    '''
    available_points = [
        pt for pt in points if pt['branches_idx'] not in ignored]
    diffs = [distance_pt(ref, pt, spacing) for pt in available_points]
    idx = diffs.index(min(diffs))
    return diffs[idx], available_points[idx]


def set_flags(locs, flag1, flag2, flag3):
    '''
    Sets flag based on common rules for MLO and CC.
    Flag order is important, expecting:
    - for cc: at_flag, t2imc_flag, nipple_flag
    - for mlo: pm_flag, imf_flag, nipple_flag

    :param locs: list of strings resulting from a call to localise().
    :param flag1: a variable to store the enum value.
    :param flag2: a variable to store the enum value.
    :param flag3: a variable to store the enum value.
    '''
    if 'T' in locs:
        flag1 = ContourConfidenceLevel.NOK.value
    if 'B' in locs:
        flag2 = ContourConfidenceLevel.NOK.value
    if 'R' in locs:
        flag3 = ContourConfidenceLevel.NOK.value
    return flag1, flag2, flag3


def cc_flags(first_point_loc, last_point_loc, first_point, last_point,
             rows, columns, at_flag, nipple_flag, t2imc_flag):
    '''
    Specific flags management for CC based on contour first point and last
    point once sorted.

    :param first_point_loc: a string resulting from a call to localise().
    :param last_point_loc: a string resulting from a call to localise().
    :param first_point: a tuple containing point values 'x' and 'y'.
    :param last_point: a tuple containing point values 'x' and 'y'.
    :param rows: int, rows in image.
    :param columns: int, columns in image.
    :param at_flag: a variable to store the enum value.
    :param nipple_flag: a variable to store the enum value.
    :param t2imc_flag: a variable to store the enum value.
    '''
    if first_point_loc == 'T':
        at_flag = (ContourConfidenceLevel.NOK.value if first_point[0] >
                   columns / 3 else ContourConfidenceLevel.OK.value)

    if (first_point_loc in ['R', 'B']) or (last_point_loc == 'T'):
        nipple_flag = at_flag = t2imc_flag = ContourConfidenceLevel.NOK.value

    elif last_point_loc == 'R':
        nipple_flag = t2imc_flag = ContourConfidenceLevel.NOK.value
    elif last_point_loc == 'B':
        t2imc_flag = (ContourConfidenceLevel.NOK.value if last_point[0] >
                      columns / 3 else ContourConfidenceLevel.OK.value)

    return at_flag, nipple_flag, t2imc_flag


def mlo_flags(first_point_loc, last_point_loc, first_point, last_point,
              rows, columns, pm_flag, nipple_flag, imf_flag):
    '''
    Specific flags management for CC based on contour first point and last
    point once sorted.

    :param first_point_loc: a string resulting from a call to localise()
    :param last_point_loc: a string resulting from a call to localise()
    :param first_point: a tuple containing point values 'x' and 'y'.
    :param last_point: a tuple containing point values 'x' and 'y'.
    :param rows: int, rows in image.
    :param columns: int, columns in image.
    :param pm_flag: a variable to store the enum value
    :param nipple_flag: a variable to store the enum value
    :param imf_flag: a variable to store the enum value
    '''
    if first_point_loc == 'L':
        pm_flag = ContourConfidenceLevel.NOK.value

    if (first_point_loc == 'T' and first_point[0] > columns / 2 and
            first_point[0] < columns / 10):
        pm_flag = ContourConfidenceLevel.NOK.value

    if (first_point_loc in ['R', 'B']) or (last_point_loc == 'T'):
        nipple_flag = pm_flag = imf_flag = ContourConfidenceLevel.NOK.value

    if last_point_loc == 'R':
        nipple_flag = imf_flag = ContourConfidenceLevel.NOK.value

    if last_point_loc == 'B' and last_point[0] > columns / 3:
        imf_flag = ContourConfidenceLevel.NOK.value

    return pm_flag, nipple_flag, imf_flag


def reverse_axes(branch):
    return np.array([x[::-1] for x in branch])


def contour_checker(
        branches, rows, columns, pixel_spacing,
        max_branches, flag_method,
        max_intersection_dist=MAX_INTERSECT_DIST,
        max_intersection_dist_left=MAX_INTERSECT_DIST_LEFT):
    '''
    Utility that maps the segments in the contour so that each segment follows
    the previous one. Orders points inside each segment so that the contour
    contains also the segment points ordered from top to bottom.

    :param branches: ndarrays with 2 dimensions of double, segments
    of the contour
    :param rows: int, number of rows in the image
    :param columns: int, number of columns in the image
    :param pixel_spacing: array of floats, pixel spacing x and y
    :param max_intersection_dist: maximal distance between two points for them
    to be considered as linked
    :param max_intersection_dist_left: maximal distance between first and last
    point if one on them is on the left of the image.
    :returns: contour and flags. Flags depend of the image type (CC or MLO).
    '''
    # find_contours doc is wrong, it returns y, x coords instead of x, y...
    branches = list(map(reverse_axes, branches))
    branches_relevant = relevant_branches(branches, rows, columns)

    nb_branches = len(branches_relevant)
    if (nb_branches == 0) or (nb_branches >= max_branches):
        val = ContourConfidenceLevel.NOK.value
        return 0, val, val, val

    flag1 = flag2 = flag3 = ContourConfidenceLevel.OK.value

    extremities = sort_branches(branches_relevant)
    first_branch_idx = extremities[0]['branches_idx']
    first_branch_pos = extremities[0]['branch_idx']
    first_branch = branches_relevant[first_branch_idx]
    contour = first_branch[::-1] if first_branch_pos != 0 else first_branch
    extracted_branches = [first_branch_idx]
    horizontal_spacing = pixel_spacing[0]

    if nb_branches > 1:
        while len(extracted_branches) < nb_branches:
            last_pt = contour[-1]
            last_pt_dict = {'x': last_pt[0], 'y': last_pt[1]}
            dist, next_pt = next_point(
                last_pt_dict, extremities, horizontal_spacing,
                ignored=extracted_branches)
            next_branch_idx = next_pt['branches_idx']
            next_branch_pos = next_pt['branch_idx']
            next_branch = branches_relevant[next_branch_idx]
            contour = np.concatenate([
                contour,
                (next_branch[::-1] if next_branch_pos != 0 else next_branch)])
            extracted_branches.append(next_branch_idx)

            locs = [
                localise(last_pt_dict['x'], last_pt_dict['y'], rows, columns),
                localise(next_pt['x'], next_pt['y'], rows, columns)]

            if dist > max_intersection_dist:
                flag2, flag3, flag1 = set_flags(
                    locs, flag2, flag3, flag1)

            if (dist > max_intersection_dist_left) and ('L' in locs):
                val = ContourConfidenceLevel.NOK.value
                return ([], val, val, val)

    first_point = contour[0]
    last_point = contour[-1]
    first_point_loc = localise(first_point[0], first_point[1], rows,
                               columns)
    last_point_loc = localise(last_point[0], last_point[1], rows,
                              columns)

    flag2, flag1, flag3 = flag_method(
        first_point_loc, last_point_loc, first_point, last_point,
        rows, columns, flag2, flag1, flag3)
    return contour.tolist(), flag1, flag2, flag3


def contour_checker_cc(branches, rows, columns, pixel_spacing):
    '''
    Proxy method for contour_checker for CC.

    :param branches: ndarrays of 2 dimensions containing contour segments.
    :param rows: int, number of rows in the image.
    :param columns: int, number of columns in the image.
    :param pixel_spacing: array of floats, pixel spacing x and y.
    '''
    contour, nipple_flag, at_flag, t2imc_flag = contour_checker(
        branches, rows, columns, pixel_spacing, MAX_BRANCHES_CC, cc_flags)
    return contour, nipple_flag, at_flag, t2imc_flag


def contour_checker_mlo(branches, rows, columns, pixel_spacing):
    '''
    Proxy method for contour_checker for MLO.

    :param branches: ndarrays of 2 dimensions containing contour segments.
    :param rows: int, number of rows in the image.
    :param columns: int, number of columns in the image.
    :param pixel_spacing: array of floats, pixel spacing x and y.
    '''
    contour, nipple_flag, pm_flag, imf_flag = contour_checker(
        branches, rows, columns, pixel_spacing, MAX_BRANCHES_MLO, mlo_flags)
    return contour, nipple_flag, pm_flag, imf_flag


def pre_extrapolation_mlo(contour):
    """
    Points detection in the image contour (MLO)
    """
    for i in range(len(contour)):
        if contour[i][0] == max(contour, key=lambda x: x[0])[0] \
                and contour[i][1] == max(contour, key=lambda x: x[0])[1]:
            break

    contour_up = contour[:i]
    contour_down = contour[i:]

    M = find_M(contour_down)
    H = find_H(M)
    B, Bidx = find_B(contour_down, H)
    A, Aidx = find_A(contour_down, M, B, H)
    C = find_C(A, H)
    Aidx = Aidx + len(contour_up)
    Bidx = Bidx + len(contour_up)

    return contour_down, M, H, B, A, C, Aidx, Bidx


def pre_extrapolation_cc(contour):
    """
    Points detection in the image contour (CC)
    """
    for i in range(len(contour)):
        if contour[i][0] == max(contour, key=lambda x: x[0])[0] \
                and contour[i][1] == max(contour, key=lambda x: x[0])[1]:
            break

    contour_up = contour[:i]
    contour_down = contour[i:]

    M = find_M(contour_down)
    H = find_H(M)
    B, Bidx = find_B(contour_down, H)
    A, Aidx = find_A(contour_down, M, B, H)
    C = find_C(A, H)
    Bp, Bpidx = find_B(contour_up, H)
    Mp = find_M(list(reversed(contour_up)))
    Ap, Apidx = find_A(contour_up, Mp, Bp, H, reverse=True)
    Cp = find_C(Ap, H)
    Aidx = Aidx + len(contour_up)
    Bidx = Bidx + len(contour_up)

    return (contour_down, contour_up, M, H, B, Bp, A, Ap, C, Cp,
            Aidx, Bidx, Apidx, Bpidx)
