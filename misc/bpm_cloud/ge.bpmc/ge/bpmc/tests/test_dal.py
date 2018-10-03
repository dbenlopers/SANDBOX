# -*- coding: utf-8 -*-


from ge.bpmc.app.injection import Contexts, Core
from ge.bpmc.persistence.orm import (ExamStatusEnum, ImageMetricsTable,
                                     ImageStatusEnum, ImageTable, IssuerORM,
                                     ProcedureStatusEnum, metadata)
from ge.bpmc.tests.base import (ISSUER_ID, ISSUER_KEY, MODALITY_MANUF_NAME,
                                MODALITY_MODEL_NAME, MODALITY_SOFTW_VERS,
                                SOP_CLASS_IDENTIFIER, BaseDataModelTestCase)
from ge.bpmc.utilities.sqlalchemy import transaction


class DALTestCase(BaseDataModelTestCase):

    @transaction(Core.logger, Contexts.em)
    def test_em_crud_methods(self):
        issuer = None
        issuer = self.em.add_obj(
            IssuerORM,
            {'identifier': ISSUER_ID,
             'key': ISSUER_KEY})
        self.assertEqual(issuer.key,
                         ISSUER_KEY, 'Invalid issuer key')
        self.assertEqual(issuer.identifier,
                         ISSUER_ID, 'Invalid issuer identifier')
        issuers = self.em.all_obj(IssuerORM)
        res = issuers[0] if issuers else None
        self.assertEqual(len(issuers), 1, 'Got more issuers than expected')
        self.assertEqual(res.to_dict(), issuer.to_dict(),
                         'Issuer not equals to previously inserted item')
        res = self.em.get_obj(IssuerORM, 'uid', issuer.uid)
        self.assertEqual(getattr(res, 'uid', None),
                         issuer.uid, 'Invalid issuer id')
        issuer = self.em.upd_obj(IssuerORM,
                                 'uid', issuer.uid,
                                 {'identifier': 'test_upd_id'})
        self.assertEqual(getattr(issuer, 'identifier', None),
                         issuer.identifier, 'Invalid issuer id after update')
        self.em.del_obj(IssuerORM, 'uid', issuer.uid)
        res = self.em.get_obj(IssuerORM, 'uid', issuer.uid)
        self.assertEqual(res, None, 'Deletion did not work properly')
        self.em._session_.close()

    @transaction(Core.logger, Contexts.em)
    def test_generated_methods(self):
        issuer = self.create_issuer()
        self.assertEqual(issuer.key,
                         ISSUER_KEY, 'Invalid issuer key')
        self.assertEqual(issuer.identifier,
                         ISSUER_ID, 'Invalid issuer identifier')
        issuers = self.em.all_issuer()
        res = issuers[0] if issuers else None
        self.assertEqual(len(issuers), 1, 'Got more issuers than expected')
        self.assertEqual(res.to_dict(), issuer.to_dict(),
                         'Issuer not equals to previously inserted item')
        res = self.em.get_issuer('uid', issuer.uid)
        self.assertEqual(getattr(res, 'uid', None),
                         issuer.uid, 'Invalid issuer id')
        issuer = self.em.upd_issuer('uid', issuer.uid,
                                    {'identifier': 'test_upd_id'})
        self.assertEqual(getattr(issuer, 'identifier', None),
                         issuer.identifier, 'Invalid issuer id after update')
        self.em.del_issuer('uid', issuer.uid)
        res = self.em.get_issuer('uid', issuer.uid)
        self.assertEqual(res, None, 'Deletion did not work properly')
        self.em._session_.close()

    @transaction(Core.logger, Contexts.em)
    def test_get_available_repository(self):
        repository = self.create_repository()
        self.assertEqual(repository.available,
                         True, 'Repository is not available')
        res = self.em.get_available_repository()
        self.assertNotEqual(res, None)
        self.assertEqual(res.to_dict(), repository.to_dict())

    @transaction(Core.logger, Contexts.em)
    def test_get_image_repository(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()
        image_item = self.em.get_image('uid', image.uid)
        self.assertEqual(image.to_dict(), image_item.to_dict())
        repo_item = self.em.get_image_repository(image.uid)
        self.assertEqual(image.repository_uid, repo_item.uid)

    @transaction(Core.logger, Contexts.em)
    def test_get_modality_type_by_unicity(self):
        modality_type = self.create_modality_type()
        mod = self.em.get_modality_type_by_unicity(
            MODALITY_MODEL_NAME,
            MODALITY_SOFTW_VERS,
            MODALITY_MANUF_NAME
        )
        self.assertEqual(modality_type.to_dict(), mod.to_dict())

    @transaction(Core.logger, Contexts.em)
    def test_get_or_create_modality_type(self):
        mod = self.em.get_modality_type_by_unicity(
            MODALITY_MODEL_NAME,
            MODALITY_SOFTW_VERS,
            MODALITY_MANUF_NAME
        )
        self.assertEqual(mod, None)
        mod = self.em.get_or_create_modality_type(
            MODALITY_MODEL_NAME,
            MODALITY_SOFTW_VERS,
            MODALITY_MANUF_NAME
        )
        self.assertNotEqual(mod, None)

    @transaction(Core.logger, Contexts.em)
    def test_get_metrics_image_repository(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status, image_metrics,
         image_metrics_display) = self.create_processed_image_stack()
        rep = self.em.get_metrics_image_repository(image_metrics_display.uid)
        self.assertEqual(rep.uid, repository.uid)

    @transaction(Core.logger, Contexts.em)
    def test_get_or_create_sop_class(self):
        sop_class = self.em.get_sop_class(
            'sop_class_identifier',
            SOP_CLASS_IDENTIFIER)
        self.assertEqual(sop_class, None)
        self.em.get_or_create_sop_class(SOP_CLASS_IDENTIFIER)
        sop_class = self.em.get_sop_class(
            'sop_class_identifier',
            SOP_CLASS_IDENTIFIER)
        self.assertNotEqual(sop_class, None)

    @transaction(Core.logger, Contexts.em)
    def test_get_or_create_exam(self):
        issuer = self.create_issuer()
        exam = self.em.get_exam(
            'issuer_uid',
            issuer.uid)
        self.assertEqual(exam, None)
        exam = self.em.get_or_create_exam(None, issuer.uid)
        self.assertNotEqual(exam, None)

    @transaction(Core.logger, Contexts.em)
    def test_get_or_create_exam_status(self):
        issuer = self.create_issuer()
        exam = self.em.get_or_create_exam(None, issuer.uid)
        exam_status = self.em.get_or_create_exam_status(
            exam_uid=exam.uid, status=ExamStatusEnum.Waiting.value)
        self.assertNotEqual(exam_status, None)
        self.assertEqual(exam_status.exam_uid, exam.uid)
        self.assertEqual(exam_status.status, ExamStatusEnum.Waiting.value)

    @transaction(Core.logger, Contexts.em)
    def test_get_or_create_procedure(self):
        issuer = self.create_issuer()
        exam = self.create_exam(issuer.uid)
        proc = self.em.get_procedure(
            'exam_uid',
            exam.uid)
        self.assertEqual(proc, None)
        proc = self.em.get_or_create_procedure(None, exam.uid)
        self.assertNotEqual(proc, None)

    @transaction(Core.logger, Contexts.em)
    def test_get_or_create_procedure_status(self):
        issuer = self.create_issuer()
        exam = self.em.get_or_create_exam(None, issuer.uid)
        exam_status = self.em.get_or_create_exam_status(
            exam_uid=exam.uid, status=ExamStatusEnum.Waiting.value)
        proc = self.em.get_or_create_procedure(None, exam.uid)
        proc_status = self.em.get_or_create_procedure_status(
            procedure_uid=proc.uid, status=ProcedureStatusEnum.Waiting.value)
        self.assertNotEqual(proc_status, None)
        self.assertEqual(proc_status.procedure_uid, proc.uid)
        self.assertEqual(proc_status.status, ProcedureStatusEnum.Waiting.value)
