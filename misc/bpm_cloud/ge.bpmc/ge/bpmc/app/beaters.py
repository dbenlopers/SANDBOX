# -*- coding: utf-8 -*-


from ge.bpmc.app.injection import Application, Factories
from ge.bpmc.app.workers import BPMWorker
from ge.bpmc.tasks import periodic


class PeriodicBeater(BPMWorker):

    def __init__(self, configfile):
        app = Factories.celery_factory()
        app.on_after_configure.connect(periodic.setup_periodic_tasks)
        super(PeriodicBeater, self).__init__(configfile)
        beater = Application.beat(level=self.loglevel)
        beater.run()
