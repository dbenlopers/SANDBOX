# -*- coding: utf-8 -*-
import json
from datetime import timedelta

import requests
from mockito import mock, unstub, when

from ge.bpmc import business as BPMBusiness
from ge.bpmc.api.schemas.default import SimpleImageModel, StatusModel
from ge.bpmc.app.injection import Contexts, Core, Factories, Services
from ge.bpmc.persistence.orm import ImageStatusEnum
from ge.bpmc.services.storageclient import StorageClient
from ge.bpmc.tasks import matching, periodic, processing
from ge.bpmc.tests.base import BaseDataModelTestCase, ResultWrapper
from ge.bpmc.tests.test_workflow import COMPUTATION_REQUEST
from ge.bpmc.utilities.sqlalchemy import transaction


class TasksTestCase(BaseDataModelTestCase):

    def setUp(self):
        when(Core.logger()).warning(...).thenReturn(None)
        super(TasksTestCase, self).setUp()

    def tearDown(self):
        super(TasksTestCase, self).tearDown()
        unstub(when(Core.logger()).warning(...))

    @transaction(Core.logger, Contexts.em)
    def test_process_image(self):
        when(Core.logger()).warning(...).thenReturn(None)
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()

        bytes_json = SimpleImageModel(bytes=[])
        bytes_ = mock({'status_code': 200, 'text': json.dumps(bytes_json)},
                      spec=requests.Response)
        when(bytes_).json().thenReturn(bytes_json)
        status = StatusModel(message='success')
        metrics_resp = mock({'status_code': 200, 'text': json.dumps(status)},
                            spec=requests.Response)
        when(metrics_resp).json().thenReturn(status)
        when(StorageClient).get_image(...).thenReturn(bytes_)
        when(StorageClient).post_metrics_image(...).thenReturn(metrics_resp)

        (when(BPMBusiness).process_image(...).thenReturn(({}, {}, None)))
        processing.process_image(image.uid, COMPUTATION_REQUEST)
        image_status = self.em.get_image_status('image_uid', image.uid)
        self.assertEqual(image_status.status, ImageStatusEnum.Processed.value)
        unstub(when(BPMBusiness).process_image(...))

        error = mock({'status_code': 500, 'text': 'Failed'},
                     spec=requests.Response)
        wrapper = ResultWrapper()
        wrapper.EXPECTED_RESPONSE = {'retry': 'ok'}
        # Prevents logger to log exception as expected in unittests
        when(Core.logger()).exception(...).thenReturn(None)
        when(error).json().thenReturn({'status': 'Failed'})
        when(StorageClient).post_metrics_image(...).thenReturn(error)
        when(processing.process_image).retry(...).thenAnswer(wrapper.exec)

        res = processing.process_image(image.uid, COMPUTATION_REQUEST)
        self.assertEqual(wrapper.RESPONSE, wrapper.EXPECTED_RESPONSE)
        unstub()

    @transaction(Core.logger, Contexts.em)
    def test_manage_processed_procedures(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()
        self.em.upd_image_status('uid', image_status.uid, {
            'status': ImageStatusEnum.Processed.value
        })
        self.em.upd_image('uid', image.uid, {
            'inserted_on': image.inserted_on + timedelta(minutes=-11)
        })
        wrapper = ResultWrapper()
        wrapper.EXPECTED_RESPONSE = 'Sent'
        broker = Factories.celery_factory()
        (when(periodic).produce_matching_task(...)
         .thenAnswer(wrapper.exec))
        periodic.manage_processed_procedures()
        self.assertEqual(wrapper.RESPONSE, wrapper.EXPECTED_RESPONSE)
        unstub()

    @transaction(Core.logger, Contexts.em)
    def test_match_procedure_images(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status, image_metrics,
         image_metrics_display) = self.create_processed_image_stack()
        wf = Services.workflow()
        wrapper = ResultWrapper()
        wrapper.EXPECTED_RESPONSE = 'Retry called'
        # Prevents logger to log exception as expected in unittests
        when(Core.logger()).exception(...).thenReturn(None)
        when(Core.logger()).warning(...).thenReturn(None)
        when(wf).match_procedure(...).thenRaise(Exception())
        (when(matching.match_procedure_images).retry(...)
         .thenAnswer(wrapper.exec))
        matching.match_procedure_images(procedure.uid)
        self.assertEqual(wrapper.RESPONSE, wrapper.EXPECTED_RESPONSE)
        unstub()
