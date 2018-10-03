# -*- coding: utf-8 -*-

from logging import DEBUG, INFO, WARN, Formatter, StreamHandler

from celery.bin import worker
from flask import Flask
from flask_restful_swagger_2 import get_swagger_blueprint
from flask_swagger_ui import get_swaggerui_blueprint

from ge.bpmc import API_JSON_ENTRYPOINT, API_UI, BPM_VERSION

BPM_LOG_FORMATTER = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class ApiApplication:

    docs = []

    def __init__(self, title, identifier,
                 api, host, port):
        self.title = title
        self.flask_app = Flask(identifier)
        self.api = api
        self.host = host
        self.port = port

        self.flask_app.register_blueprint(api.blueprint)
        self.add_documentation()

    def add_documentation(self):
        self.docs.append(self.api.get_swagger_doc())
        self.flask_app.register_blueprint(
            get_swagger_blueprint(
                self.docs,
                API_JSON_ENTRYPOINT,
                title=self.title,
                api_version=BPM_VERSION
            ))

        self.flask_app.register_blueprint(
            get_swaggerui_blueprint(
                API_UI,
                API_JSON_ENTRYPOINT + '.json',
                config={
                    'supportedSubmitMethods': ['get']
                }
            ), url_prefix=API_UI)

    def run(self):
        self.flask_app.run(self.host, self.port, threaded=True)


class WorkerApplication:

    argv = None
    app = None

    def __init__(self, application, queues, name='worker', level='WARN'):
        self.app = application
        self.argv = ['celery', 'worker', '-n', name, '-P', 'eventlet',
                     '-l', level]
        if queues:
            self.argv += ['-Q', ','.join(queues)]

    def run(self):
        self.app.start(argv=self.argv)


class BeatApplication:

    argv = None
    app = None

    def __init__(self, application, level='WARN'):
        self.app = application
        self.argv = ['celery', 'beat', '-l', level]

    def run(self):
        self.app.start(argv=self.argv)
