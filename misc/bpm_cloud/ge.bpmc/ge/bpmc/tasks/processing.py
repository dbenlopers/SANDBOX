# -*- coding: utf-8 -*-

import json

from ge.bpmc import MAX_BUSINESS_TASK_RETRIES, business
from ge.bpmc.app.injection import Contexts, Core, Factories, Services
from ge.bpmc.services.storageclient import StorageClient
from ge.bpmc.utilities.sqlalchemy import transaction

app = Factories.celery_factory()


@transaction(Core.logger, Contexts.em)
def wrapped_process_image(uid, metadata):
    """
    Handles processing from bytes retrieval to result persistence.

    Keywords:
    uid -- Image uid
    metadata -- Computation request payload sent w/o pixelmap
    """
    req = StorageClient.get_image({'Content-Type': 'application/json'}, uid)
    image = req.json().get('bytes')
    metadata['image'] = image
    wf = Services.workflow()
    metrics, processed_image = wf.process_image(uid, metadata)
    return metrics, processed_image


@app.task(bind=True, max_retries=MAX_BUSINESS_TASK_RETRIES)
def process_image(self, uid, metadata):
    """
    Image processing that generates kpis, overlay & image.

    Keywords:
    uid -- Image uid
    image_metadata -- Computation request payload sent w/o pixelmap
    """
    logger = Core.logger()
    logger.info('Running image processing for image uid %(uid)s' % (
        {'uid': uid}
    ))
    try:
        metrics, processed_image = wrapped_process_image(uid, metadata)
        if processed_image:
            req = StorageClient.post_metrics_image(
                {'Content-Type': 'application/json'},
                json.dumps({'metrics_uid': metrics.uid,
                            'image': list(processed_image)})
            )
            if req.status_code != 200:
                raise ValueError('Could not persist processed image')
        logger.info('Image %(uid)s has been processed' % ({'uid': uid}))
    except Exception as e:
        logger.exception(e)
        self.retry(exc=e)
