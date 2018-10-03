# -*- coding:utf-8 -*-

import enum

#######################
#
# Contour detection
#
#######################

# Minimum number of points in a branch for it to be relevant
RELEVANCE_MIN_POINTS = 150

MAX_INTERSECT_DIST = 10
MAX_INTERSECT_DIST_LEFT = 50
MAX_BRANCHES_CC = MAX_BRANCHES_MLO = 5

#######################
#
# Enums
#
#######################


class ContourConfidenceLevel(enum.Enum):
    OK = 1
    PARTIAL = 2
    NOK = 3

#######################
#
# Labels
#
#######################


LBL_IMF_PT_UNDEF = 'imf point not detected'
LBL_NOT_RLVT_WO_MUSCLE_DTCT = 'not relevant without pectoral muscle detection'

#######################
#
# Flags
#
#######################

FLAG_PROC = 'FOR PROCESSING'
FLAG_PRES = 'FOR PRESENTATION'

#######################
#
# Dicom keys
#
#######################

KDCM_BDPE = 'BodyPartExamined'
KDCM_COLS = 'Columns'
KDCM_ROWS = 'Rows'
KDCM_CPFR = 'CompressionForce'
KDCM_IMLA = 'ImageLaterality'
KDCM_IMTP = 'ImageType'
KDCM_IMPS = 'ImagerPixelSpacing'
KDCM_MANU = 'Manufacturer'
KDCM_MODN = 'ManufacturerModelName'
KDCM_PHIN = 'PhotometricInterpretation'
KDCM_PIXA = 'PixelArray'
KDCM_PRIT = 'PresentationIntentType'
KDCM_VIPO = 'ViewPosition'
KDCM_SOPC = 'SOPClassUID'
KDCM_SFTV = 'SoftwareVersions'
KDCM_BTSA = 'BitsAllocated'
KDCM_COSH = 'CollimatorShape'
KDCM_COLV = 'CollimatorLeftVerticalEdge'
KDCM_CORV = 'CollimatorRightVerticalEdge'
KDCM_COLH = 'CollimatorLowerHorizontalEdge'
KDCM_COUH = 'CollimatorUpperHorizontalEdge'
KDCM_BRIP = 'BreastImplantPresent'
KDCM_ACDT = 'AcquisitionDatetime'
