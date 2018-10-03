# -*- coding: utf-8 -*-
"""
Definition of celery app
"""
from __future__ import absolute_import
from celery import Celery


app = Celery('data_quality')
app.config_from_object('data_quality.celeryconfig')


if __name__ == '__main__':
    app.start()