# -*- coding: utf-8 -*-
import json
from copy import deepcopy
from datetime import timedelta
from io import BytesIO, StringIO

import requests
from mockito import mock, unstub, when
from webdav3.exceptions import (NoConnection, NotEnoughSpace,
                                RemoteResourceNotFound)

from ge.bpmc import business as BPMBusiness
from ge.bpmc.api.schemas.default import SimpleImageModel, StatusModel
from ge.bpmc.app.injection import Contexts, Core, Factories, Services
from ge.bpmc.dav.client import BPMDavClient
from ge.bpmc.exceptions.storage import BPMMissingImage, BPMNoAvailableStorage
from ge.bpmc.persistence.orm import RepositoryORM
from ge.bpmc.services.storageclient import StorageClient
from ge.bpmc.tasks import matching, periodic, processing
from ge.bpmc.tests.base import BaseDataModelTestCase
from ge.bpmc.tests.test_workflow import COMPUTATION_REQUEST
from ge.bpmc.utilities.image import bpm_representation_to_buffer
from ge.bpmc.utilities.injector import set_configuration
from ge.bpmc.utilities.sqlalchemy import transaction

TEST_IMAGE = [[137, 80, 78, 71],
              [10, 0, 0, 0]]

ST_COMPUTATION_REQUEST = deepcopy(COMPUTATION_REQUEST)
ST_COMPUTATION_REQUEST['image'] = TEST_IMAGE


def update_buffer(buffer, image_path):
    buffer.write(bpm_representation_to_buffer(TEST_IMAGE).getvalue())


class StorageTestCase(BaseDataModelTestCase):

    def setUp(self):
        super(StorageTestCase, self).setUp()
        data = {
            'webdav': {'options': {}, 'client_options': {}},
        }
        set_configuration(data)
        self.storage = Services.storage(wf=Services.workflow())
        self.mockDavClientMethods()

    def mockDavClientMethods(self):
        # Mock dav client
        when(BPMDavClient).download_from(...).thenAnswer(update_buffer)
        when(BPMDavClient).upload_to(...).thenReturn(None)

    def tearDown(self):
        super(StorageTestCase, self).tearDown()
        unstub()

    @transaction(Core.logger, Contexts.em)
    def test_store_image(self):
        issuer, repository = self.create_application_stack()

        computed = (
            self.storage.store_image(issuer.key, ST_COMPUTATION_REQUEST))
        self.assertTrue('exam' in computed)
        self.assertTrue('procedure' in computed)
        self.assertTrue('image' in computed)

        self.em.upd_repository('uid', repository.uid, {
            'available': False
        })
        with self.assertRaises(BPMNoAvailableStorage):
            self.storage.store_image(issuer.key, ST_COMPUTATION_REQUEST)

        when(self.storage).transfer_to_host(...).thenRaise(NotEnoughSpace)
        with self.assertRaises(BPMNoAvailableStorage):
            self.storage.store_image(issuer.key, ST_COMPUTATION_REQUEST)

        err = NoConnection('localhost')
        unstub(when(self.storage).transfer_to_host(...))
        when(self.storage).transfer_to_host(...).thenRaise(err)
        with self.assertRaises(BPMNoAvailableStorage):
            self.storage.store_image(issuer.key, ST_COMPUTATION_REQUEST)

        unstub(when(self.storage).transfer_to_host(...))
        self.create_repository(name='test_repo2', host='127.0.0.2')
        computed = (
            self.storage.store_image(issuer.key, ST_COMPUTATION_REQUEST))
        self.assertNotEqual(computed, {})

    @transaction(Core.logger, Contexts.em)
    def test_store_metrics_image(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()
        image_metrics = self.create_image_metrics(image.uid)
        res = self.storage.store_metrics_image(image_metrics.uid, TEST_IMAGE)
        self.assertNotEqual(res, None)
        img = self.em.get_image_metrics_display('uid', res['image'])
        self.assertNotEqual(img, None)
        pixels = self.storage.query_metrics_image(res['image'])
        self.assertEqual(pixels, TEST_IMAGE)

    @transaction(Core.logger, Contexts.em)
    def test_store_metrics_no_repository(self):
        with self.assertRaises(BPMNoAvailableStorage):
            self.storage.store_metrics_image(1, [])

    @transaction(Core.logger, Contexts.em)
    def test_query_metrics_image(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status, image_metrics,
         image_metrics_display) = self.create_processed_image_stack()
        bytes_ = self.storage.query_metrics_image(image_metrics_display.uid)
        self.assertEqual(bytes_, TEST_IMAGE)

    @transaction(Core.logger, Contexts.em)
    def test_query_metrics_no_repository(self):
        with self.assertRaises(BPMMissingImage):
            self.storage.query_metrics_image(1, [])

    @transaction(Core.logger, Contexts.em)
    def test_query_image(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status, image_metrics,
         image_metrics_display) = self.create_processed_image_stack()
        bytes_ = self.storage.query_image(image.uid)
        self.assertEqual(bytes_, TEST_IMAGE)

    @transaction(Core.logger, Contexts.em)
    def test_query_image_no_repository(self):
        with self.assertRaises(BPMMissingImage):
            self.storage.query_image(1)

    def test_get_image_bytes(self):
        repo = RepositoryORM(1, 'test', '127.0.0.1')
        bytes_ = self.storage.get_image_bytes(1, repo, ext='')
        self.assertEqual(bytes_, TEST_IMAGE)

    def test_get_image_bytes_no_connection(self):
        repo = RepositoryORM(1, 'test', '127.0.0.1')
        err = NoConnection('localhost')
        when(self.storage).download_to_buffer(...).thenRaise(err)
        when(self.storage._logger_).warning(...).thenReturn(None)
        bytes_ = self.storage.get_image_bytes(1, repo, ext='')
        self.assertEqual(bytes_, None)
        unstub(when(self.storage).download_to_buffer(...))
        unstub(when(self.storage._logger_).warning(...))
