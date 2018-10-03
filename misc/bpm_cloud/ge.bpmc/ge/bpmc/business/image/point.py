# -*- coding: utf-8 -*-

from math import pi, sqrt


class ImagePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def invert_laterality(self, column):
        return [column - self.x, self.y]


def localise(x, y, rows, columns):
    """
    Identify the image corner associated with this point (x,y)
    """
    return (
        ((x == columns - 1) and 'R') or  # RIGHT
        ((x == 0) and 'L') or  # LEFT
        ((y == rows - 1) and 'B') or  # BOTTOM
        ((y == 0) and 'T')  # TOP
    )

##########################################
#
# POINT EXTRAPOLATION IN CONTOUR
#
##########################################


def distance(A, B):
    return sqrt((pow((A.x - B.x), 2) + pow((A.y - B.y), 2)))


def find_A(contour, M, B, H, reverse=False):
    diffs = []
    M_idx = contour.index([M.x, M.y])
    B_idx = contour.index([B.x, B.y])
    ct_slice = contour[B_idx:M_idx] if reverse else contour[M_idx:B_idx]
    a = distance(M, H)
    for pt in ct_slice:
        current = ImagePoint(pt[0], pt[1])
        b = distance(M, current)
        c = distance(current, H)
        theta = abs(
            180 * ((pow(a, 2) + pow(c, 2) - pow(b, 2)) / (2 * a * c)) / pi)
        diffs.append(abs(theta - 45))
    idx = diffs.index(min(diffs))
    A = ImagePoint(ct_slice[idx][0], ct_slice[idx][1])
    return A, idx


def find_B(contour, H):
    diffs = list(map(lambda pt: abs(pt[0] - H.x), contour))
    idx = diffs.index(min(diffs))
    B = ImagePoint(contour[idx][0], contour[idx][1])
    return B, idx


def find_C(A, M):
    C = ImagePoint(A.x, M.y)
    return C


def find_M(contour):
    M = ImagePoint(contour[0][0], contour[0][1])
    return M


def find_H(M):
    H = ImagePoint(round(M.x / 3), M.y)
    return H
