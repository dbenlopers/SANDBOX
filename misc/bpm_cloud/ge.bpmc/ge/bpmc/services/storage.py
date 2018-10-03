# -*- coding: utf-8 -*-

import configparser
import json
import os
from contextlib import contextmanager
from io import BytesIO, StringIO

from webdav3.exceptions import (NoConnection, NotEnoughSpace,
                                RemoteResourceNotFound)

from ge.bpmc import (SOP_CLASS_FORMAT, STORAGE_DEFAULT_FORMAT,
                     STORAGE_METRICS_SUFFIX)
from ge.bpmc.dav.client import BPMDavClient
from ge.bpmc.exceptions.base import BPMFlaskException
from ge.bpmc.exceptions.storage import BPMMissingImage, BPMNoAvailableStorage
from ge.bpmc.utilities.conf import check_configuration_keys
from ge.bpmc.utilities.image import (bpm_representation_to_buffer,
                                     file_content_to_bpm_representation)


class StorageService:

    em = None
    _logger_ = None
    _webdav_opts_ = {}
    _webdav_client_opts_ = {}

    def __init__(self, logger, em, wf,
                 webdav_opts={}, webdav_client_opts={}):
        self.em = em
        self.wf = wf
        self._logger_ = logger
        self._webdav_opts_ = webdav_opts
        self._webdav_client_opts_ = webdav_client_opts

    def get_webdav_client(self, webdav_opts={}):
        """
        Returns a BPMDavClient instance.

        Keyword arguments:
        webdav_opts -- A dictionary with extra options to pass
        to the client. Optional.
        """
        webdav_opts.update(self._webdav_opts_)
        client = BPMDavClient(webdav_opts)
        client.request_options.update(self._webdav_client_opts_)
        return client

    def download_to_buffer(self, image_uid, repo,
                           ext=STORAGE_DEFAULT_FORMAT, suffix=''):
        """
        Downloads image binary data to buffer

        Keyword arguments:
        image -- Int, image UID
        repo -- A repository instance
        ext -- String, expected file format. Optional.
        suffix -- Str, pasted after the image_uid when querying file name
        """
        proto = 'https' if repo.use_ssl else 'http'
        webdav_opts = {
            'webdav_hostname': "%(proto)s://%(uri)s" % (
                {'proto': proto, 'uri': repo.host})
        }
        dav_client = self.get_webdav_client(webdav_opts)
        image_path = '%s%s.%s' % (image_uid, suffix, ext)
        buffer = BytesIO()
        dav_client.download_from(buffer, image_path)
        return buffer

    def transfer_to_host(self, uid, buffer, repo,
                         ext=STORAGE_DEFAULT_FORMAT, suffix=''):
        """
        Pushes file to a webdav server.

        Keyword arguments:
        uid -- Int, Image UID
        buffer -- Buffer containing file content
        repo -- a Repository instance
        ext -- String, expected file format. Optional.
        suffix -- Str, pasted after the image_uid when generating file name
        """
        proto = 'https' if repo.use_ssl else 'http'
        webdav_opts = {
            'webdav_hostname': "%(proto)s://%(uri)s" % (
                {'proto': proto, 'uri': repo.host})
        }
        dav_client = self.get_webdav_client(webdav_opts)
        upload_opts = {
            'buff': buffer,
            'remote_path': '/%s%s.%s' % (uid, suffix, ext)
        }
        dav_client.upload_to(**upload_opts)

    def persist_image(self, uid, repo, bytes_array,
                      ext=STORAGE_DEFAULT_FORMAT, blacklist=[], suffix=''):
        """
        Manage image persistance using known available repositories.
        Returns Repository uid on success.

        Keyword arguments:
        uid -- Int, Image UID
        repo -- Repository instance
        bytes_array -- List of bytes containing image data
        ext -- String, extension used upon persistence
        blacklist -- List of repository uids to avoid
        suffix -- Str, pasted after the image_uid when generating file name
        """
        buffer = bpm_representation_to_buffer(bytes_array)
        try:
            self.transfer_to_host(uid, buffer, repo, suffix=suffix)
            return repo.uid
        except (NotEnoughSpace, NoConnection) as e:
            # Disabled while no keepalive process is implemented
            # self.em.upd_repository('uid', repo.uid, {'available': False})
            blacklist.append(repo.uid)
            new_repo = self.em.get_available_repository(blacklist)
            if new_repo:
                message = 'Repository "{name}" went down while pushing image.'
                if isinstance(e, NotEnoughSpace):
                    message += ' Disk is full.'
                self._logger_.warning(message.format(**{'name': repo.name}))
                self.persist_image(
                    uid, new_repo, bytes_array, ext, blacklist, suffix)
                self.logger.info(
                    'Image %(uid)s has been stored with prefix %(suffix)s' % ({
                        'uid': uid,
                        'suffix': suffix
                    }))
            else:
                raise BPMNoAvailableStorage()

    def get_image_bytes(self, image_uid, repository, ext, suffix=''):
        try:
            buffer = self.download_to_buffer(
                image_uid, repository, ext=ext, suffix=suffix)
            return file_content_to_bpm_representation(buffer)
        except (RemoteResourceNotFound, NoConnection) as e:
            message = 'Could not query image with uid {uid}'
            self._logger_.warning(message.format(**{'uid': image_uid}))
        return None

    def query_image(self, image_uid, ext=STORAGE_DEFAULT_FORMAT, suffix=''):
        """
        Gets image data from its repository and
        returns the binary data as a list.

        Keyword arguments:
        image_uid -- Int, an Image uid
        ext -- Str, extension for the file
        suffix -- Str, pasted after the image_uid when generating file name
        """
        repository = self.em.get_image_repository(image_uid)
        if not repository:
            raise BPMMissingImage('Image does not exist')
        return self.get_image_bytes(image_uid, repository,
                                    ext=ext, suffix=suffix)

    def query_metrics_image(self, image_uid, ext=STORAGE_DEFAULT_FORMAT,
                            suffix=STORAGE_METRICS_SUFFIX):
        """
        Gets image data from its repository and
        returns the binary data as a list.

        Keyword arguments:
        image_uid -- Int, an Image uid
        ext -- Str, extension for the file
        suffix -- Str, pasted after the image_uid when generating file name
        """
        repository = self.em.get_metrics_image_repository(image_uid)
        if not repository:
            raise BPMMissingImage('Image does not exist')
        return self.get_image_bytes(image_uid, repository,
                                    ext=ext, suffix=suffix)

    def store_image(self, issuer_key, payload):
        """
        Extracts image data and persists data on a repository.
        At this point, the code calling this method is responsible of testing
        the existence of the issuer_key in the database.

        Keyword arguments:
        issuer_key -- String, an Issuer key
        payload -- a Dict containing image data,
        see api._bpm_schemas.ComputationRequestPayload
        """
        issuer = self.em.get_issuer('key', issuer_key)
        exam, procedure, image, repository = \
            self.wf.compute_request(issuer, payload)
        final_repo_uid = self.persist_image(
            image.uid, repository, payload.get('image'))
        if repository.uid != final_repo_uid:
            self.em.upd_image('uid', image.uid,
                              {'repository_uid': final_repo_uid})
        return {'exam': exam.uid, 'procedure': procedure.uid,
                'image': image.uid}

    def store_metrics_image(self, metrics_uid, bytes_):
        """
        Stores the image generated by the image processing.

        Keyword arguments:
        metrics_uid -- The image_metrics uid
        bytes_ -- List of bytes lists
        """
        repository = self.em.get_available_repository()
        if not repository:
            raise BPMNoAvailableStorage()
        metrics_image = self.em.add_image_metrics_display({
            'image_metrics_uid': metrics_uid,
            'repository_uid': repository.uid
        })
        final_repo_uid = self.persist_image(
            metrics_image.uid, repository, bytes_,
            suffix=STORAGE_METRICS_SUFFIX)
        if repository.uid != final_repo_uid:
            self.em.upd_image_metrics('uid', metrics_image.uid,
                                      {'repository_uid': final_repo_uid})
        return {'image': metrics_image.uid}
