# -*- coding: utf-8 -*-

import math

from . import (ctlog_key_to_file_type_mapping, rationale_mapping, rules,
               status_mapping)


def relative(a, b, rel_tol):
    return math.isclose(a, b, rel_tol=rel_tol)


def decimal(a, b, dec_tol):
    return abs(a - b) < dec_tol


def get_rule(category, variant='default', fail_over='default'):
    rule = rules.get(category, {})
    return rule.get(variant) or rule.get(fail_over)


def get_status_couple(status_key, rationale_key):
    return (status_mapping[status_key], rationale_mapping[rationale_key])


def get_ctlog_supported_filetypes(ctlog_entry):
    return [
        v for k, v in ctlog_key_to_file_type_mapping.items() if ctlog_entry[k]]
