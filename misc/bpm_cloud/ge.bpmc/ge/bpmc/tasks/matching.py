# -*- coding: utf-8 -*-

from ge.bpmc import MAX_BUSINESS_TASK_RETRIES, business
from ge.bpmc.app.injection import Contexts, Core, Factories, Services
from ge.bpmc.utilities.sqlalchemy import transaction

app = Factories.celery_factory()


@transaction(Core.logger, Contexts.em)
def wrapped_match_procedure_images(procedure_uid):
    wf = Services.workflow()
    wf.match_procedure(procedure_uid)


@app.task(bind=True, max_retries=MAX_BUSINESS_TASK_RETRIES)
def match_procedure_images(self, procedure_uid):
    """
    Matches up to two sets of two images for a procedure.

    Keyword arguments:
    procedure_uid -- Int, Procedure  UID
    images_metadata -- List of tuple which contains for each image uid the
    image_laterality, view_position, acquisition_time and overlay_data
    """
    logger = Core.logger()
    logger.info('Running matching for procedure %(uid)s' % (
        {'uid': procedure_uid}))
    try:
        wrapped_match_procedure_images(procedure_uid)
        logger.info('Procedure %(uid)s has been matched' % (
            {'uid': procedure_uid}))
    except Exception as e:
        logger.exception(e)
        self.retry(exc=e)
