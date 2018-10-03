# -*- coding: utf-8 -*-

import os
import json

rules_path = os.path.join(os.path.dirname(__file__), 'rules.json')
with open(rules_path, 'r') as rules_file:
    rules = json.load(rules_file)
    rules_file.close()


rationale_mapping = {'NFF': 1, 'ENHANCEMENT': 2,
                     'LIMITED': 3, 'WARNING': 4,
                     'ERROR': 5, 'CRITICAL': 6,
                     'MISSING': 7, 'EXTRA': 8,
                     'NOIM': 9, 'CL_UNKNOWN': 10,
                     'NONSENSE': 11, 'AE_UNKNOWN': 12}
status_mapping = {'OK': 1, 'NOK': 2, 'NA': 3}
ctlog_key_to_file_type_mapping = {
    'sum_exam_proto': 'EXAM_PROTO',
    'sum_image': 'IMAGE',
    'sum_localizer': 'LOCALIZER',
    'sum_rdsr': 'RDSR',
    'sum_scan_request': 'SCAN_REQUEST',
    'sum_screenshot': 'SCREENSHOT',
    'sum_screenshot_contrast': '± DICOM-SR (996)'
}
