# -*- coding: utf-8 -*-

from ge.bpmc.app.injection import Core


class CeleryConfig:
    BROKER_URL = ''


def celery_config():
    obj = CeleryConfig()
    setattr(obj, 'BROKER_URL', Core.config.broker.dsn())
    return obj
