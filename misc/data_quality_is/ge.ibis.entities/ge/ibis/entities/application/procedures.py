# -*- coding: utf-8 -*-

import os

TEMPLATES_FOLDER = 'procedure_templates'

MAPPING = [
    {'procedure_name': 'update_agg_study',
     'file_name': 'update_agg_study.sql'},
    {'procedure_name': 'update_pattern',
     'file_name': 'update_pattern.sql'},
    {'procedure_name': 'update_dosimetric',
     'file_name': 'update_dosimetric.sql'},
    {'procedure_name': 'update_ctlog',
     'file_name': 'update_ctlog.sql'},
    {'procedure_name': 'update_devicesoverview',
     'file_name': 'update_devicesoverview.sql'},
    {'procedure_name': 'update_all_stored_views',
     'file_name': 'update_all_stored_views.sql'},
    {'procedure_name': 'update_im_mt',
     'file_name': 'update_im_mt.sql'},
]


def load_templates(replace_kwargs):
    templates = []
    for mapping in MAPPING:
        proc_name = mapping['procedure_name']
        file_name = mapping['file_name']
        path = os.sep.join([os.path.dirname(os.path.realpath(__file__)),
                            TEMPLATES_FOLDER, file_name])
        with open(path, newline=None) as _file:
            templates.append(
                (proc_name, _file.read().format(**replace_kwargs)))

    return templates


def deploy_procedures(session, data_schema):
    # Procedures deployment
    statements = load_templates({'DATA_SCHEMA': data_schema})
    for proc_name, stmt in statements:
        session.execute(stmt)
