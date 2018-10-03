# -*- coding: utf-8 -*-

import logging

from .application import init_database as init_main
from .application.procedures import deploy_procedures as deploy_main_procs
from .application.views import deploy_views as deploy_main_views
from .archive import init_database as init_archive
from .datamarts import init_database as init_marts

logger = logging.getLogger('ge.ibis.entities')


def deploy_stack(main_session, data_session, archive_session,
                 data_schema='data'):
    logger.warn('Deploying `main` database model...')
    init_main(main_session)
    logger.warn('Deploying `data` database model...')
    init_marts(data_session)
    logger.warn('Deploying `archive` database model...')
    init_archive(archive_session)
    logger.warn('Deploying `main` views...')
    deploy_main_views(main_session, data_schema)
    logger.warn('Deploying `main` procedures...')
    deploy_main_procs(main_session, data_schema)
