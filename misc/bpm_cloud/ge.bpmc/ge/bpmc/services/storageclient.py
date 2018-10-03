# -*- coding: utf-8 -*-

import requests

from ge.bpmc import (HEADER_CMPT_KEY, HEADER_ISSUER_KEY,
                     STORE_IMAGE_ENTRYPOINT, STORE_METRICS_IMAGE_ENTRYPOINT)
from ge.bpmc.app.injection import Core


class ClassProperty(property):
    """Subclass property to make classmethod properties possible"""
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class StorageClient:

    @ClassProperty
    @classmethod
    def _default_headers(cls):
        return {HEADER_CMPT_KEY: Core.config.tokens.component()}

    @ClassProperty
    @classmethod
    def _storage_uri(cls):
        return Core.config.app.storage_uri()

    @classmethod
    def _build_uri(cls, *args):
        return cls._storage_uri + '/'.join(list(args))

    @classmethod
    def _update_headers(cls, headers):
        headers.update(cls._default_headers)

    @classmethod
    def _post(cls, headers, data, uri):
        return requests.post(uri, data=data, headers=headers)

    @classmethod
    def _get(cls, headers, uri):
        return requests.get(uri, headers=headers)

    @classmethod
    def post(cls, headers, data, uri):
        cls._update_headers(headers)
        return cls._post(headers, data, uri)

    @classmethod
    def get(cls, headers, uri):
        cls._update_headers(headers)
        return cls._get(headers, uri)

    @classmethod
    def post_computation_request(cls, headers, data):
        uri = cls._build_uri(STORE_IMAGE_ENTRYPOINT)
        return cls.post(headers, data, uri)

    @classmethod
    def get_image(cls, headers, uid):
        uri = cls._build_uri(STORE_IMAGE_ENTRYPOINT, str(uid))
        return cls.get(headers, uri)

    @classmethod
    def post_metrics_image(cls, headers, data):
        uri = cls._build_uri(STORE_METRICS_IMAGE_ENTRYPOINT)
        return cls.post(headers, data, uri)

    @classmethod
    def get_metrics_image(cls, headers, uid):
        uri = cls._build_uri(STORE_METRICS_IMAGE_ENTRYPOINT, str(uid))
        return cls.get(headers, uri)
