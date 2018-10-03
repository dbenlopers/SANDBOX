# -*- coding: utf-8 -*-

import os

# TODO: Change SQL scripts to SQLAlchemy generated statements
# see https://stackoverflow.com/questions/9766940/ +
#     how-to-create-an-sql-view-with-sqlalchemy

TEMPLATES_FOLDER = 'view_templates'

MAPPING = [
    {'view_name': 'v_dosimetric_data_last21days',
     'file_name': 'dosimetric_data_last_21days.sql'},
    {'view_name': 'v_dosimetric_last15days',
     'file_name': 'dosimetric_last_15days.sql'},
    {'view_name': 'v_pattern_last15days',
     'file_name': 'pattern_last_15days.sql'},
    {'view_name': 'v_study_dicom_last15days',
     'file_name': 'study_dicom_last_15days.sql'},
    {'view_name': 'v_study_dosimetric_last15days',
     'file_name': 'study_dosimetric_last_15days.sql'},
    {'view_name': 'v_ctlog_last15days',
     'file_name': 'ctlog_last_15days.sql'},
    {'view_name': 'v_agg_study_data_source',
     'file_name': 'agg_study_data_source.sql'},
    {'view_name': 'v_aet',
     'file_name': 'aet.sql'},
    {'view_name': 'v_devices_overview',
     'file_name': 'devices_overview.sql'},
    {'view_name': 'v_innova_log_status',
     'file_name': 'innova_log_status.sql'}
]


def load_templates(replace_kwargs):
    templates = []
    for mapping in MAPPING:
        view_name = mapping['view_name']
        file_name = mapping['file_name']
        path = os.sep.join([os.path.dirname(os.path.realpath(__file__)),
                            TEMPLATES_FOLDER, file_name])
        with open(path, newline=None) as _file:
            templates.append(
                (view_name, _file.read().format(**replace_kwargs)))

    return templates


def deploy_views(session, data_schema):
    # Views deployment
    statements = load_templates({'DATA_SCHEMA': data_schema})
    for view_name, stmt in statements:
        session.execute(stmt)
