# -*- coding: utf-8 -*-

import logging
import os
import unittest
import uuid

from dependency_injector import providers

from ge.bpmc.app.injection import Contexts, Core, Gateways
from ge.bpmc.persistence.orm import (ExamStatusEnum, ImageStatusEnum,
                                     ProcedureStatusEnum, metadata)
from ge.bpmc.utilities.injector import set_configuration

ISSUER_ID = 'test_issuer'
ISSUER_KEY = str(uuid.uuid4())
MODALITY_MODEL_NAME = 'Senographe Pristina'
MODALITY_SOFTW_VERS = '3.2.3'
MODALITY_MANUF_NAME = 'General Eletric'
SOP_CLASS_IDENTIFIER = '1.2.840.10008.5.1.4.1.1.2'


class ResultWrapper:
    """
    Use an instance of ResultWrapper in a thenAnswer call from mockito to check
    that a mocked method is called when it is not returning any result.
    """
    EXPECTED_RESPONSE = None
    RESPONSE = None

    def exec(self, *args, **kwargs):
        self.RESPONSE = self.EXPECTED_RESPONSE


class BaseDataModelTestCase(unittest.TestCase):

    def setUp(self):
        dsn = os.environ.get(
            'BPM_UT_DB', 'mysql+pymysql://root:root@127.0.0.1:3306/test')
        data = {
            # 'sqlite:///:memory:'},
            'database': {
                'dsn': dsn
            }
        }
        set_configuration(data)
        Core.logger.override(providers.Singleton(
            logging.Logger, name='bpm-default'))
        self.em = Contexts.em()
        metadata.create_all(Gateways.session().bind)

    def tearDown(self):
        metadata.drop_all(Gateways.session().bind)

    def create_issuer(self):
        return self.em.add_issuer({
            'identifier': ISSUER_ID,
            'key': ISSUER_KEY
        })

    def create_exam(self, issuer_uid):
        return self.em.add_exam({
            'issuer_uid': issuer_uid
        })

    def create_exam_status(self, exam_uid):
        return self.em.add_exam_status({
            'exam_uid': exam_uid,
            'status': ExamStatusEnum.Waiting.value
        })

    def create_procedure(self, exam_uid):
        return self.em.add_procedure({
            'exam_uid': exam_uid
        })

    def create_procedure_status(self, procedure_uid):
        return self.em.add_procedure_status({
            'procedure_uid': procedure_uid,
            'ready': False,
            'status': ProcedureStatusEnum.Waiting.value
        })

    def create_repository(self, name='test_repo', host='127.0.0.1',
                          use_ssl=True):
        return self.em.add_repository({
            'name': name,
            'host': host,
            'use_ssl': use_ssl,
        })

    def create_modality_type(self):
        return self.em.add_modality_type({
            'model_name': MODALITY_MODEL_NAME,
            'software_version': MODALITY_SOFTW_VERS,
            'manufacturer_name': MODALITY_MANUF_NAME
        })

    def create_sop_class(self):
        return self.em.add_sop_class({
            'sop_class_identifier': SOP_CLASS_IDENTIFIER})

    def create_image(self, procedure_uid, repository_uid, modality_type_uid,
                     sop_class_uid, metadata_uid):
        return self.em.add_image({
            'procedure_uid': procedure_uid,
            'repository_uid': repository_uid,
            'modality_type_uid': modality_type_uid,
            'sop_class_uid': sop_class_uid,
            'metadata_uid': metadata_uid,
            'inserted_on': None,
        })

    def create_image_metadata(self, processing_data, extra=None):
        return self.em.add_image_metadata({
            'breast_implant_present': True,
            'image_laterality': 'L',
            'acquisition_time': '2017-11-12 12:01:03',
            'processing_data': processing_data,
            'view_position': 'CC',
            'compression_force': 100,
            'size_of_return_rows': 1000,
            'size_of_return_columns': 1000,
            'extra': extra,
        })

    def create_image_status(self, image_uid):
        return self.em.add_image_status({
            'image_uid': image_uid,
            'ready': False,
            'status': ImageStatusEnum.Waiting.value
        })

    def create_image_metrics(self, image_uid):
        return self.em.add_image_metrics({
            'image_uid': image_uid,
            'criteria': {},
            'overlay': {}
        })

    def create_image_metrics_display(self, metrics_uid, repository_uid):
        return self.em.add_image_metrics_display({
            'image_metrics_uid': metrics_uid,
            'repository_uid': repository_uid
        })

    def create_application_stack(self):
        issuer = self.create_issuer()
        repository = self.create_repository()
        return (issuer, repository)

    def create_exam_stack(self):
        issuer, repository = self.create_application_stack()
        exam = self.create_exam(issuer.uid)
        exam_status = self.create_exam_status(exam.uid)
        return (issuer, repository, exam, exam_status)

    def create_procedure_base(self, exam):
        procedure = self.create_procedure(exam.uid)
        procedure_status = self.create_procedure_status(procedure.uid)
        return (procedure, procedure_status)

    def create_procedure_stack(self):
        (issuer, repository, exam, exam_status) = self.create_exam_stack()
        procedure, procedure_status = self.create_procedure_base(exam)
        return (issuer, repository, exam, exam_status, procedure,
                procedure_status)

    def create_image_base(self, procedure, repository, modality_type=None,
                          sop_class=None):
        if modality_type is None:
            modality_type = self.create_modality_type()
        if sop_class is None:
            sop_class = self.create_sop_class()
        image_metadata = self.create_image_metadata({})
        image = self.create_image(procedure.uid, repository.uid,
                                  modality_type.uid, sop_class.uid,
                                  image_metadata.uid)
        image_status = self.create_image_status(image.uid)
        return (modality_type, sop_class, image_metadata, image, image_status)

    def create_image_stack(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status) = self.create_procedure_stack()
        (modality_type, sop_class, image_metadata, image,
         image_status) = self.create_image_base(procedure, repository)
        return (issuer, repository, exam, exam_status, procedure,
                procedure_status, modality_type, sop_class, image_metadata,
                image, image_status)

    def create_image_metrics_base(self, image, repository):
        image_metrics = self.create_image_metrics(image.uid)
        image_metrics_display = self.create_image_metrics_display(
            image_metrics.uid, repository.uid)
        return (image_metrics, image_metrics_display)

    def create_image_with_image_metrics_base(
            self, procedure, repository, modality_type=None, sop_class=None):
        (modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_base(
             procedure, repository, modality_type=modality_type,
             sop_class=sop_class)
        (image_metrics,
         image_metrics_display) = self.create_image_metrics_base(
             image, repository)
        return (modality_type, sop_class, image_metadata,
                image, image_status, image_metrics, image_metrics_display)

    def create_processed_image_stack(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()
        (image_metrics,
         image_metrics_display) = self.create_image_metrics_base(
             image, repository)
        return (issuer, repository, exam, exam_status, procedure,
                procedure_status, modality_type, sop_class, image_metadata,
                image, image_status, image_metrics, image_metrics_display)
