# -*- coding: utf-8 -*-

from ge.bpmc.app.injection import Contexts, Core, Factories, Services
from ge.bpmc.utilities.network import check_broker_state
from ge.bpmc.utilities.sqlalchemy import transaction

app = Factories.celery_factory()

# setup_periodic_tasks is to be wrapped in decorator
# @app.on_after_configure.connect by the beat process


def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        15, manage_processed_procedures.s(),
        name='Manage processed procedures')


def produce_matching_task(broker, procedure_uid):
    check_broker_state(broker)
    task_fqdn = 'ge.bpmc.tasks.matching.match_procedure_images'
    broker.send_task(task_fqdn, (procedure_uid,))


@transaction(Core.logger, Contexts.em)
def identity_and_match_processed_procedures():
    broker = Factories.celery_factory()
    wf = Services.workflow()
    logger = Core.logger()
    procedures = wf.update_processed_procedures()
    for proc in procedures:
        logger.info('Processed procedure %(uid)s has been sent to matching' % (
            {'uid': proc}
        ))
        produce_matching_task(broker, proc)


@app.task
def manage_processed_procedures():
    """
    Flags procedures which should be marked as processed
    """
    identity_and_match_processed_procedures()
