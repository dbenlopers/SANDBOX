# coding=utf-8
from celery.schedules import crontab
from kombu import Queue
import configparser
import os

cfg_parser = configparser.ConfigParser()
cfg_parser.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "..{}config.cfg".format(os.sep)))
"""
# List of modules to import when celery starts.
imports = ('data_quality.tasks.persistence',
           'data_quality.tasks.logic',
           'data_quality.tasks.periodic',
           'data_quality.tasks.etl')

# Result store settings.
result_backend = None
event_queue_expires = 10
task_ignore_result = True
result_expires = 1
        
# Broker settings.
broker_url = "{}".format(cfg_parser['broker']['dsn'])

# Worker settings

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Paris'
enable_utc = True

task_queue = (
    Queue('Periodic', routing_key='periodic'),
    Queue('Logic', routing_key='logic'),
    Queue('Persistence', routing_key='persistence'),
    Queue('ETL', routing_key='etl')
)

# Celery routes/queue for all processing function declared

task_routes = {
    'data_quality.tasks.etl.*': {'queue': 'ETL', 'routing_key': 'etl'},
    'data_quality.tasks.periodic.*': {'queue': 'Periodic', 'routing_key': 'periodic'},
    'data_quality.tasks.logic.*': {'queue': 'Logic', 'routing_key': 'logic'},
    'data_quality.tasks.persistence.*': {'queue': 'Persistence', 'routing_key': 'persistence'}
}

# Periodic processing rules
beat_schedule = {
    'Check_new dosimetrics': {
        'task': 'data_quality.tasks.periodic.search_new_dosimetric',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['dosimetric']['_PERIODIC_SEARCH_PROCESSING_HRS_BEAT']))
        ,
    },
    'Check_new innovalog': {
        'task': 'data_quality.tasks.periodic.search_new_innovalogpull',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['innovalog']['_PERIODIC_SEARCH_PROCESSING_HRS_BEAT']))
        ,
    },
    'Check_new ctlogpattern': {
        'task': 'data_quality.tasks.periodic.search_new_ctlogpattern',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['ctlog']['_PERIODIC_SEARCH_PROCESSING_HRS_BEAT']))
        ,
    },
    'Check_new dicominput': {
        'task': 'data_quality.tasks.periodic.search_new_dicominput',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['dicompattern']['_PERIODIC_SEARCH_PROCESSING_HRS_BEAT']))
        ,
    },
    'ETL business': {
        'task': 'data_quality.tasks.periodic.etl_update_business_data',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['periodic_tasks']['_UPDATE_DATA_HRS_BEAT']))
        ,
    },
    'ETL probe': {
        'task': 'data_quality.tasks.periodic.etl_update_probes_data',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['periodic_tasks']['_UPDATE_PROBES_HRS_BEAT']))
        ,
    },
    'ETL update connectivity list': {
        'task': 'data_quality.tasks.periodic.reconstruct_connectivity_list',
        'schedule': crontab(minute=0, hour='1', day_of_week=[cfg_parser.getint('periodic_tasks', '_UPDATE_CL_DAYS_BEAT')])
        ,
    },
    'ETL update translator config': {
        'task': 'data_quality.tasks.periodic.reconstruct_translatorconfig',
        'schedule': crontab(minute=0, hour='2', day_of_week=[cfg_parser.getint('periodic_tasks', '_UPDATE_TC_DAYS_BEAT')])
        ,
    },
    'Check new ae': {
        'task': 'data_quality.tasks.periodic.search_new_ae',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['periodic_tasks']['_PERIODIC_SEARCH_PROCESSING_AE_HRS_BEAT']))
    },
    'Refreshing materialized view': {
        'task': 'data_quality.tasks.periodic.refresh_materialized_view',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['periodic_tasks']['_REFRESH_VIEW_HOURS_BEAT']))
        ,
    }
}
"""

CELERY_IMPORTS = ('data_quality.tasks.persistence',
                  'data_quality.tasks.logic',
                  'data_quality.tasks.periodic',
                  'data_quality.tasks.etl')

CELERY_RESULT_BACKEND = None
CELERY_EVENT_QUEUE_EXPIRES = 10
CELERY_IGNORE_RESULT = True
CELERY_TAKS_RESULT_EXPIRES = 1

# Broker settings.
BROKER_URL = "{}".format(cfg_parser['broker']['url'])

# Worker settings

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Europe/Paris'
CELERY_ENABLE_UTC = True

CELERY_QUEUES = (
    Queue('Periodic', routing_key='periodic'),
    Queue('Logic', routing_key='logic'),
    Queue('Persistence', routing_key='persistence'),
    Queue('ETL', routing_key='etl')
)

# Celery routes/queue for all processing function declared
CELERY_ROUTES = {
    'data_quality.tasks.logic.batch_innovalog_test': {
        'queue': 'Logic',
        'routing_key': 'logic',
    },
    'data_quality.tasks.logic.batch_dosimetric_test': {
        'queue': 'Logic',
        'routing_key': 'logic',
    },
    'data_quality.tasks.logic.batch_ctlog_test': {
        'queue': 'Logic',
        'routing_key': 'logic',
    },
    'data_quality.tasks.logic.batch_dicominput_test': {
        'queue': 'Logic',
        'routing_key': 'logic',
    },
    'data_quality.tasks.logic.batch_translator_test': {
        'queue': 'Logic',
        'routing_key': 'logic'
    },
    'data_quality.tasks.persistence.batch_store_dosimetrics_update_study_status': {
        'queue': 'Persistence',
        'routing_key': 'persistence',
    },
    'data_quality.tasks.persistence.batch_store_innovalog_state_update_innova_status': {
        'queue': 'Persistence',
        'routing_key': 'persistence',
    },
    'data_quality.tasks.persistence.batch_store_ctlogpattern_status_update_ctlogpattern_status': {
        'queue': 'Persistence',
        'routing_key': 'persistence',
    },
    'data_quality.tasks.persistence.batch_store_dicominput_status_update_dicominput_status': {
        'queue': 'Persistence',
        'routing_key': 'persistence',
    },
    'data_quality.tasks.persistence.batch_store_translatorconf_status_update_ae_status': {
        'queue': 'Persistence',
        'routing_key': 'persistence',
    },
    'data_quality.tasks.periodic.search_new_dosimetric': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.search_new_innovalogpull': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.search_new_ctlogpattern': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.search_new_dicominput': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.search_new_ae': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.search_all_new_input': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.reconstruct_connectivity_list': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.reconstruct_translatorconfig': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.refresh_materialized_view': {
        'queue': 'Periodic',
        'routing_key': 'periodic'
    },
    'data_quality.tasks.periodic.etl_update_business_data': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.etl_update_device': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.etl_update_customer': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.etl_update_ae': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.etl_update_probes_data': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.etl_import_probes_data_dicompattern': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.etl_import_probes_data_innovalog': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.etl_import_probes_data_consolidation': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.periodic.etl_import_probes_data_ctlog': {
        'queue': 'Periodic',
        'routing_key': 'periodic',
    },
    'data_quality.tasks.etl.import_translatorconfig': {
        'queue': 'ETL',
        'routing_key': 'etl',
    },
    'data_quality.tasks.etl.import_customer': {
        'queue': 'ETL',
        'routing_key': 'etl',
    },
    'data_quality.tasks.etl.import_ae': {
        'queue': 'ETL',
        'routing_key': 'etl',
    },
    'data_quality.tasks.etl.import_device': {
        'queue': 'ETL',
        'routing_key': 'etl',
    },
    'data_quality.tasks.etl.import_connectivitylist': {
        'queue': 'ETL',
        'routing_key': 'etl',
    },
    'data_quality.tasks.etl.import_dicompatterns': {
        'queue': 'ETL',
        'routing_key': 'etl',
    },
    'data_quality.tasks.etl.import_ctlog': {
        'queue': 'ETL',
        'routing_key': 'etl',
    },
    'data_quality.tasks.etl.import_innovalog': {
        'queue': 'ETL',
        'routing_key': 'etl',
    },
    'data_quality.tasks.etl.import_consolidation': {
        'queue': 'ETL',
        'routing_key': 'etl',
    }
}

# Periodic processing rules
CELERYBEAT_SCHEDULE = {
    'Check_new dosimetrics': {
        'task': 'data_quality.tasks.periodic.search_new_dosimetric',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['dosimetric']['_PERIODIC_SEARCH_PROCESSING_HRS_BEAT']))
        ,
    },
    'Check_new innovalog': {
        'task': 'data_quality.tasks.periodic.search_new_innovalogpull',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['innovalog']['_PERIODIC_SEARCH_PROCESSING_HRS_BEAT']))
        ,
    },
    'Check_new ctlogpattern': {
        'task': 'data_quality.tasks.periodic.search_new_ctlogpattern',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['ctlog']['_PERIODIC_SEARCH_PROCESSING_HRS_BEAT']))
        ,
    },
    'Check_new dicominput': {
        'task': 'data_quality.tasks.periodic.search_new_dicominput',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['dicompattern']['_PERIODIC_SEARCH_PROCESSING_HRS_BEAT']))
        ,
    },
    'ETL business': {
        'task': 'data_quality.tasks.periodic.etl_update_business_data',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['periodic_tasks']['_UPDATE_DATA_HRS_BEAT']))
        ,
    },
    'ETL probe': {
        'task': 'data_quality.tasks.periodic.etl_update_probes_data',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['periodic_tasks']['_UPDATE_PROBES_HRS_BEAT']))
        ,
    },
    'ETL update connectivity list': {
        'task': 'data_quality.tasks.periodic.reconstruct_connectivity_list',
        'schedule': crontab(minute=0, hour='1', day_of_week=[cfg_parser.getint('periodic_tasks', '_UPDATE_CL_DAYS_BEAT')])
        ,
    },
    'ETL update translator config': {
        'task': 'data_quality.tasks.periodic.reconstruct_translatorconfig',
        'schedule': crontab(minute=0, hour='2', day_of_week=[cfg_parser.getint('periodic_tasks', '_UPDATE_TC_DAYS_BEAT')])
        ,
    },
    'Check new ae': {
        'task': 'data_quality.tasks.periodic.search_new_ae',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['periodic_tasks']['_PERIODIC_SEARCH_PROCESSING_AE_HRS_BEAT']))
    },
    'Refreshing materialized view': {
        'task': 'data_quality.tasks.periodic.refresh_materialized_view',
        'schedule': crontab(minute=0, hour='{}'.format(cfg_parser['periodic_tasks']['_REFRESH_VIEW_HOURS_BEAT']))
        ,
    }
}
