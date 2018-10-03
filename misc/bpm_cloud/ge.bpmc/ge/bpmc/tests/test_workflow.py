# -*- coding: utf-8 -*-
import operator
from copy import deepcopy
from datetime import timedelta

from mockito import mock, unstub, when

from ge.bpmc import business as BPMBusiness
from ge.bpmc.app.injection import Contexts, Core, Services
from ge.bpmc.business.image.processing import IDIProcessor
from ge.bpmc.exceptions.base import BPMFlaskException
from ge.bpmc.exceptions.matching import BPMMatchingException
from ge.bpmc.exceptions.processing import (BPMProcessingException,
                                           BPMProcessingInvalidException)
from ge.bpmc.exceptions.storage import BPMNoAvailableStorage
from ge.bpmc.persistence.orm import ImageStatusEnum, ProcedureStatusEnum
from ge.bpmc.tests.base import ISSUER_KEY, BaseDataModelTestCase
from ge.bpmc.utilities.sqlalchemy import transaction

COMPUTATION_REQUEST = {
    'image': [
        [12948, 12971, 12945, 12874, 12860],
        [12948, 12971, 12945, 12874, 12860],
        [12948, 12971, 12945, 12874, 12860]
    ],
    'exam_uid': 0,
    'procedure_uid': 0,
    'modality': {
        'model_name': 'Senographe Pristina',
        'software_version': '1.13',
        'manufacturer_name': 'GE HEALTHCARE'
    },
    'sop_class': '1.2.840.10008.5.1.4.1.1.1.2.1',
    'breast_implant_present': 'NO',
    'image_laterality': 'R',
    'acquisition_time': '2016-09-01T15:05:22',
    'view_position': 'CC',
    'processing_data': {
        'imager_pixel_spacing': {
            'horizontal': 0.1,
            'vertical': 0.1
        },
        'rows': 2850,
        'columns': 2394,
        'photometric_interpretation': 'MONOCHROME1',
        'presentation_intent_type': 'FOR PROCESSING',
        'bits_allocated': 16,
        'image_type': ['ORIGINAL', 'PRIMARY', ''],
        'body_part_examined': 'BREAST',
        'collimator_shape': 'RECTANGULAR',
        'collimator_left_vertical_edge': 0,
        'collimator_right_vertical_edge': 2395,
        'collimator_lower_horizontal_edge': 2851,
        'collimator_upper_horizontal_edge': 0
    },
    'compression_force': 103,
    'size_of_return': {
        'rows': 1000,
        'columns': 1000
    },
    'extra': {'my_key': 'my_value'}
}

METRICS = {
    'criteria': {
        'symmetry': 0,
        'length_of_posterior_nipple_line': 0,
        'centricity': 0,
        'bottom_overlapping': 0,
        'opposite_overlapping': 0,
        'top_overlapping': 0,
        'pectoral_muscle_angle': 0,
        'pectoral_muscle_visible_up_to_nipple_line': 0,
        'pectoral_muscle_width': 0,
        'nipple_visible_in_profile': True,
        'nipple_angle': 0,
        'absence_of_breast_sagging': 0,
        'compression': 0
    },
    'overlay': {
        'symmetry': {
            'x': 0,
            'y': 0
        },
        'length_of_posterior_nipple_line': {
            'start': {
                'x': 0,
                'y': 0
            },
            'end': {
                'x': 0,
                'y': 0
            }
        },
        'centricity': {
            'x': 0,
            'y': 0
        },
        'bottom_overlapping': 0,
        'opposite_overlapping': 0,
        'top_overlapping': 0,
        'pectoral_muscle_angle': {
            'start': {
                'start': {
                    'x': 0,
                    'y': 0
                },
                'end': {
                    'x': 0,
                    'y': 0
                }
            },
            'end': {
                'start': {
                    'x': 0,
                    'y': 0
                },
                'end': {
                    'x': 0,
                    'y': 0
                }
            }
        },
        'pectoral_muscle_visible_up_to_nipple_line': {
            'x': 0,
            'y': 0
        },
        'pectoral_muscle_width': {
            'start': {
                'x': 0,
                'y': 0
            },
            'end': {
                'x': 0,
                'y': 0
            }
        },
        'inframmary_fold_visible': {
            'x': 0,
            'y': 0
        },
        'axillary_tail_visible': {
            'x': 0,
            'y': 0
        },
        'transition_to_intermammary_cleft_visible': {
            'x': 0,
            'y': 0
        },
        'nipple_visible_in_profile': {
            'x': 0,
            'y': 0
        },
        'nipple_angle': {
            'start': {
                'x': 0,
                'y': 0
            },
            'end': {
                'x': 0,
                'y': 0
            }
        },
        'absence_of_breast_sagging': {
            'x': 0,
            'y': 0
        },
        'compression': {
            'x': 0,
            'y': 0
        }
    }
}

METRICS2 = deepcopy(METRICS)
METRICS2['overlay']['symmetry'] = {'x': 1, 'y': 1}
METRICS2['overlay']['length_of_posterior_nipple_line'] = {
    'start': {
        'x': 1,
        'y': 1
    },
    'end': {
        'x': 1,
        'y': 1
    }
}


class WorkflowTestCase(BaseDataModelTestCase):

    def setUp(self):
        when(Core.logger()).warning(...).thenReturn(None)
        super(WorkflowTestCase, self).setUp()
        self.wf = Services.workflow()

    def tearDown(self):
        super(WorkflowTestCase, self).tearDown()
        unstub(when(Core.logger()).warning(...))

    @transaction(Core.logger, Contexts.em)
    def test_compute_request(self):
        issuer, repository = self.create_application_stack()
        exam, procedure, image, repository = (
            self.wf.compute_request(issuer, COMPUTATION_REQUEST))
        self.assertNotEqual(exam, None)
        self.assertNotEqual(procedure, None)
        self.assertNotEqual(image, None)
        self.assertNotEqual(repository, None)

    @transaction(Core.logger, Contexts.em)
    def test_compute_request_invalid_sop_class(self):
        issuer, repository = self.create_application_stack()
        cr = deepcopy(COMPUTATION_REQUEST)
        cr['sop_class'] = '1_1_2_3_4'
        with self.assertRaises(BPMFlaskException):
            self.wf.compute_request(issuer, cr)

    @transaction(Core.logger, Contexts.em)
    def test_compute_request_invalid_laterality(self):
        issuer, repository = self.create_application_stack()
        cr = deepcopy(COMPUTATION_REQUEST)
        cr['image_laterality'] = 'D'
        with self.assertRaises(BPMFlaskException):
            self.wf.compute_request(issuer, cr)

    @transaction(Core.logger, Contexts.em)
    def test_compute_request_close_procedure(self):
        issuer, repository = self.create_application_stack()
        exam, procedure, image, repository = (
            self.wf.compute_request(issuer, COMPUTATION_REQUEST))
        cr = deepcopy(COMPUTATION_REQUEST)
        cr['exam'] = exam.uid
        exam, procedure2, image2, repository = (
            self.wf.compute_request(issuer, cr))
        procedure_status = self.em.get_procedure_status(
            'procedure_uid', procedure.uid)
        self.assertNotEqual(procedure_status, ProcedureStatusEnum.Closed.value)

    @transaction(Core.logger, Contexts.em)
    def test_compute_request_invalid_presentation_intent_type(self):
        issuer, repository = self.create_application_stack()
        cr = deepcopy(COMPUTATION_REQUEST)
        cr['processing_data']['presentation_intent_type'] = 'for testing'
        with self.assertRaises(BPMFlaskException):
            self.wf.compute_request(issuer, cr)

    @transaction(Core.logger, Contexts.em)
    def test_compute_request_invalid_breast_implant_present(self):
        issuer, repository = self.create_application_stack()
        cr = deepcopy(COMPUTATION_REQUEST)
        cr['breast_implant_present'] = 'maybe'
        with self.assertRaises(BPMFlaskException):
            self.wf.compute_request(issuer, cr)

    @transaction(Core.logger, Contexts.em)
    def test_compute_request_no_storage(self):
        issuer = self.create_issuer()
        with self.assertRaises(BPMNoAvailableStorage):
            self.wf.compute_request(issuer, COMPUTATION_REQUEST)

    @transaction(Core.logger, Contexts.em)
    def test_compute_request_reopen(self):
        issuer, repository = self.create_application_stack()
        exam, procedure, image, repository = (
            self.wf.compute_request(issuer, COMPUTATION_REQUEST))
        self.em.upd_procedure_status('procedure_uid', procedure.uid, {
            'status': ProcedureStatusEnum.Done.value
        })
        cr = deepcopy(COMPUTATION_REQUEST)
        cr['exam_uid'] = exam.uid
        cr['procedure_uid'] = procedure.uid
        self.wf.compute_request(issuer, cr)
        pc_status = self.em.get_procedure_status('procedure_uid',
                                                 procedure.uid)
        self.assertEqual(pc_status.status, ProcedureStatusEnum.Waiting.value)

    @transaction(Core.logger, Contexts.em)
    def test_compute_request_reopen_clean_match(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()
        (x, y, image_metadata2, image2, image_status2, image_metrics2,
         image_metrics_display2) = self.create_image_with_image_metrics_base(
             procedure, repository, modality_type=modality_type,
             sop_class=sop_class)
        (x, y, image_metadata3, image3, image_status3, image_metrics3,
         image_metrics_display3) = self.create_image_with_image_metrics_base(
             procedure, repository, modality_type=modality_type,
             sop_class=sop_class)
        self.wf.associate_matched_images(image2.uid, image3.uid)
        image2_matches = self.em.get_image_matches(image2.uid)
        image3_matches = self.em.get_image_matches(image3.uid)
        self.assertListEqual(image2_matches, [image3.uid])
        self.assertListEqual(image3_matches, [image2.uid])
        self.em.upd_procedure_status('procedure_uid', procedure.uid, {
            'status': ProcedureStatusEnum.Done.value
        })
        cr = deepcopy(COMPUTATION_REQUEST)
        cr['exam_uid'] = exam.uid
        cr['procedure_uid'] = procedure.uid
        self.wf.compute_request(issuer, cr)
        pc_status = self.em.get_procedure_status('procedure_uid',
                                                 procedure.uid)
        self.assertEqual(pc_status.status, ProcedureStatusEnum.Waiting.value)
        image2_matches = self.em.get_image_matches(image2.uid)
        image3_matches = self.em.get_image_matches(image3.uid)
        self.assertTrue(image3.uid not in image2_matches)
        self.assertTrue(image2.uid not in image3_matches)

    @transaction(Core.logger, Contexts.em)
    def test_match_procedure(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status, image_metrics,
         image_metrics_display) = self.create_processed_image_stack()
        (x, y, image_metadata2, image2, image_status2, image_metrics2,
         image_metrics_display2) = self.create_image_with_image_metrics_base(
             procedure, repository, modality_type=modality_type,
             sop_class=sop_class)
        (x, y, image_metadata3, image3, image_status3, image_metrics3,
         image_metrics_display3) = self.create_image_with_image_metrics_base(
             procedure, repository, modality_type=modality_type,
             sop_class=sop_class)
        match = {
            'pair': [image.uid, image2.uid],
            'criteria': {'symmetry': 0, 'length_of_posterior_nipple_line': 0},
            'overlays': {}
            #     {
            #         image.uid: {
            #             'symmetry': {'x': 0, 'y': 0},
            #             'length_of_posterior_nipple_line': {
            #                 'start': {'x': 0, 'y': 0},
            #                 'end': {'x': 0, 'y': 0},
            #             }
            #         },
            #         image2.uid: {
            #             'symmetry': {'x': 1, 'y': 1},
            #             'length_of_posterior_nipple_line': {
            #                 'start': {'x': 1, 'y': 1},
            #                 'end': {'x': 1, 'y': 1},
            #             }
            #         }
            # }
        }
        when(BPMBusiness).match_procedure_images(...).thenReturn([match])
        self.wf.match_procedure(procedure.uid)
        unstub()
        procedure_status = self.em.get_procedure_status(
            'procedure_uid', procedure.uid)
        self.assertEqual(procedure_status.status,
                         ProcedureStatusEnum.Done.value)
        image = self.em.get_image('uid', image.uid)
        image_matches = self.em.get_image_matches(image.uid)
        image2 = self.em.get_image('uid', image2.uid)
        image2_matches = self.em.get_image_matches(image2.uid)
        image_metrics = self.em.get_image_metrics('uid', image_metrics.uid)
        image_metrics2 = self.em.get_image_metrics('uid', image_metrics2.uid)
        self.assertTrue(image2.uid, image_matches)
        self.assertTrue(image.uid, image2_matches)
        self.assertTrue(
            match['criteria'].items() <= image_metrics.criteria.items())
        self.assertTrue(
            match['criteria'].items() <= image_metrics2.criteria.items())
        # self.assertTrue(
        #     match['overlays'][image.uid].items() <=
        #     image_metrics.overlay.items())
        # self.assertTrue(
        #     match['overlays'][image2.uid].items() <=
        #     image_metrics2.overlay.items())

        (when(BPMBusiness).match_procedure_images(...)
         .thenRaise(BPMMatchingException))
        self.wf.match_procedure(procedure.uid)
        unstub()
        procedure_status = self.em.get_procedure_status(
            'procedure_uid', procedure.uid)
        self.assertEqual(procedure_status.status,
                         ProcedureStatusEnum.Error.value)

    @transaction(Core.logger, Contexts.em)
    def test_process_image(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()
        (when(BPMBusiness).process_image(...)
         .thenReturn(({}, {}, None)))
        res = self.wf.process_image(image.uid, COMPUTATION_REQUEST)
        image_status = self.em.get_image_status('image_uid', image.uid)
        self.assertEqual(image_status.status, ImageStatusEnum.Processed.value)

        (when(BPMBusiness).process_image(...)
         .thenRaise(BPMProcessingInvalidException))
        res = self.wf.process_image(image.uid, COMPUTATION_REQUEST)
        unstub()
        image_status = self.em.get_image_status('image_uid', image.uid)
        self.assertEqual(image_status.status, ImageStatusEnum.Invalid.value)

        when(BPMBusiness).process_image(...).thenRaise(BPMProcessingException)
        res = self.wf.process_image(image.uid, COMPUTATION_REQUEST)
        unstub()
        image_status = self.em.get_image_status('image_uid', image.uid)
        self.assertEqual(image_status.status, ImageStatusEnum.Error.value)

    @transaction(Core.logger, Contexts.em)
    def test_consume_issuer_available_procedures(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status) = self.create_procedure_stack()
        res = self.wf.consume_issuer_available_procedures(ISSUER_KEY)
        self.assertEqual(res, [])
        self.em.upd_procedure_status('procedure_uid', procedure.uid,
                                     {'ready': True})
        res = self.wf.consume_issuer_available_procedures(ISSUER_KEY)
        self.assertNotEqual(res, [])
        res = self.wf.consume_issuer_available_procedures(ISSUER_KEY)
        self.assertEqual(res, [])

    @transaction(Core.logger, Contexts.em)
    def test_consume_issuer_available_images(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()
        res = self.wf.consume_issuer_available_images(ISSUER_KEY)
        self.assertEqual(res, [])
        self.em.upd_image_status('image_uid', image.uid,
                                 {'ready': True})
        res = self.wf.consume_issuer_available_images(ISSUER_KEY)
        self.assertNotEqual(res, [])
        res = self.wf.consume_issuer_available_images(ISSUER_KEY)
        self.assertEqual(res, [])

    @transaction(Core.logger, Contexts.em)
    def test_update_processed_procedures(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()
        procedure2, procedure2_status = self.create_procedure_base(exam)
        (x, y, image_metadata2, image2, image2_status) = (
            self.create_image_base(procedure2, repository,
                                   modality_type, sop_class))
        procedure3, procedure3_status = self.create_procedure_base(exam)
        (x, y, image_metadata3, image3, image3_status) = (
            self.create_image_base(procedure3, repository,
                                   modality_type, sop_class))
        procedure_uids = self.wf.update_processed_procedures()
        self.assertEqual(len(procedure_uids), 0)
        self.em.upd_image_status('uid', image2_status.uid, {
            'status': ImageStatusEnum.Processed.value
        })
        self.em.upd_image('uid', image2.uid, {
            'inserted_on': image2.inserted_on + timedelta(minutes=-11)
        })
        procedure_uids = self.wf.update_processed_procedures()
        self.assertEqual(len(procedure_uids), 1)
        self.assertEqual(procedure_uids[0], procedure2.uid)

        # Check that image must be processed before changing procedure status
        self.em.upd_image('uid', image.uid, {
            'inserted_on': image.inserted_on + timedelta(minutes=-11)
        })
        procedure_uids = self.wf.update_processed_procedures()
        self.assertEqual(len(procedure_uids), 0)
        self.em.upd_image_status('uid', image_status.uid, {
            'status': ImageStatusEnum.Processed.value
        })
        procedure_uids = self.wf.update_processed_procedures()
        self.assertEqual(len(procedure_uids), 1)
        self.assertEqual(procedure_uids[0], procedure.uid)

        # Checks that a closed procedure bypasses the 10min threshold
        self.em.upd_procedure_status('uid', procedure3_status.uid, {
            'status': ProcedureStatusEnum.Closed.value
        })
        self.em.upd_image_status('uid', image3_status.uid, {
            'status': ImageStatusEnum.Processed.value
        })
        procedure_uids = self.wf.update_processed_procedures()
        self.assertEqual(len(procedure_uids), 1)
        self.assertEqual(procedure_uids[0], procedure3.uid)

    @transaction(Core.logger, Contexts.em)
    def test_get_procedure_matching_data(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status, image_metrics,
         image_metrics_display) = self.create_processed_image_stack()
        (x, y, image_metadata2, image2, image_status2, image_metrics2,
         image_metrics_display2) = self.create_image_with_image_metrics_base(
             procedure, repository, modality_type=modality_type,
             sop_class=sop_class)
        (x, y, image_metadata3, image3, image_status3, image_metrics3,
         image_metrics_display3) = self.create_image_with_image_metrics_base(
             procedure, repository, modality_type=modality_type,
             sop_class=sop_class)
        self.em.upd_image_status('uid', image_status.uid, {
            'status': ImageStatusEnum.Processed.value
        })
        self.em.upd_image_status('uid', image_status2.uid, {
            'status': ImageStatusEnum.Processed.value
        })
        images_metadata = self.wf.get_procedure_matching_data(procedure.uid)
        uids = [x.get('uid') for x in images_metadata]
        self.assertEqual(len(uids), 2)
        self.assertEqual(uids, [image.uid, image2.uid])
        images_metadata.sort(key=operator.itemgetter('uid'))
        (uid, laterality, view_position, acquisition_time, criteria,
         processing_data) = [images_metadata[0].get(x) for x in [
             'uid', 'image_laterality', 'view_position', 'acquisition_time',
             'criteria', 'processing_data']]
        self.assertEqual(uid, image.uid)
        self.assertEqual(laterality, image_metadata.image_laterality)
        self.assertEqual(view_position, image_metadata.view_position)
        self.assertEqual(acquisition_time, image_metadata.acquisition_time)
        self.assertEqual(criteria, image_metrics.criteria)
        self.assertEqual(processing_data, image_metadata.processing_data)

    @transaction(Core.logger, Contexts.em)
    def test_associate_matched_images(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()
        (procedure2, procedure2_status) = self.create_procedure_base(exam)
        (x, y, image_metadata2, image2, image_status2) = (
            self.create_image_base(
                procedure, repository, modality_type=modality_type,
                sop_class=sop_class))
        (x, y, image_metadata3, image3, image_status3) = (
            self.create_image_base(
                procedure2, repository, modality_type=modality_type,
                sop_class=sop_class))
        self.wf.associate_matched_images(image.uid, image2.uid)
        image = self.em.get_image('uid', image.uid)
        image2 = self.em.get_image('uid', image2.uid)
        image3 = self.em.get_image('uid', image3.uid)
        image_matches = self.em.get_image_matches(image.uid)
        image2_matches = self.em.get_image_matches(image2.uid)
        image3_matches = self.em.get_image_matches(image3.uid)
        self.assertTrue(image2.uid in image_matches)
        self.assertTrue(image.uid in image2_matches)
        self.assertEqual([], image3_matches)

    @transaction(Core.logger, Contexts.em)
    def test_get_image_result(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status, image_metrics,
         image_metrics_display) = self.create_processed_image_stack()
        extra_content = {'test': 'test'}
        self.em.upd_image_metadata('uid', image_metadata.uid, {
            'extra': extra_content
        })
        image_result = self.wf.get_image_result(issuer.key, image.uid)
        self.assertNotEqual(image_result, None)
        self.assertEqual(image_result.uid, image.uid)
        self.assertEqual(image_result.extra, extra_content)

    @transaction(Core.logger, Contexts.em)
    def test_get_procedure_result(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status, image_metrics,
         image_metrics_display) = self.create_processed_image_stack()
        (x, y, image_metadata2, image2, image_status2, image_metrics2,
         image_metrics_display2) = self.create_image_with_image_metrics_base(
             procedure, repository, modality_type=modality_type,
             sop_class=sop_class)
        (x, y, image_metadata3, image3, image_status3, image_metrics3,
         image_metrics_display3) = self.create_image_with_image_metrics_base(
             procedure, repository, modality_type=modality_type,
             sop_class=sop_class)
        (x, y, image_metadata4, image4, image_status4, image_metrics4,
         image_metrics_display4) = self.create_image_with_image_metrics_base(
             procedure, repository, modality_type=modality_type,
             sop_class=sop_class)

        self.wf.associate_matched_images(image.uid, image2.uid)
        self.wf.associate_matched_images(image.uid, image4.uid)
        self.em.upd_image_metrics('uid', image_metrics.uid, METRICS)
        self.em.upd_image_metrics('uid', image_metrics2.uid, METRICS2)
        proc_result = self.wf.get_procedure_result(issuer.key, procedure.uid)
        self.assertNotEqual(proc_result, None)
        self.assertEqual(proc_result.uid, procedure.uid)
        self.assertEqual(len(proc_result.images), 4)
        self.assertEqual(proc_result.images[0].uid, image.uid)
        self.assertEqual(proc_result.images[0].uid, image.uid)
        matched = proc_result.matching_data
        self.assertEqual(len(matched), 2)
        kpis = matched[0]['kpis']
        # overlays = matched[0]['overlays']
        # overlays.sort(
        #     key=operator.itemgetter('image_uid'))
        self.assertEqual(
            kpis['symmetry'], METRICS['criteria']['symmetry'])
        self.assertEqual(
            kpis['length_of_posterior_nipple_line'],
            METRICS['criteria']['length_of_posterior_nipple_line'])
        # self.assertEqual(len(overlays), 2)
        # self.assertEqual(overlays[0]['image_uid'], image.uid)
        # self.assertEqual(overlays[0]['overlay']['symmetry'],
        #                  METRICS['overlay']['symmetry'])
        # self.assertEqual(overlays[1]['image_uid'], image2.uid)
        # self.assertEqual(overlays[1]['overlay']['symmetry'],
        #                  METRICS2['overlay']['symmetry'])

    @transaction(Core.logger, Contexts.em)
    def test_get_exam_result(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status, image_metrics,
         image_metrics_display) = self.create_processed_image_stack()
        exam_result = self.wf.get_exam_result(issuer.key, exam.uid)
        self.assertNotEqual(exam_result, None)
        self.assertEqual(exam_result.uid, exam.uid)
        self.assertEqual(len(exam_result.procedures), 1)
        proc_result = exam_result.procedures[0]
        self.assertEqual(proc_result.uid, procedure.uid)
        self.assertEqual(len(proc_result.images), 1)
        self.assertEqual(proc_result.images[0].uid, image.uid)

    @transaction(Core.logger, Contexts.em)
    def test_close_previous_procedures(self):
        (issuer, repository, exam, exam_status, procedure,
         procedure_status, modality_type, sop_class, image_metadata,
         image, image_status) = self.create_image_stack()
        procedure2, procedure_status2 = self.create_procedure_base(exam)
        self.wf.close_previous_procedures(exam.uid, procedure2.uid)
        procedure_status = self.em.get_procedure_status(
            'procedure_uid', procedure.uid)
        self.assertEqual(procedure_status.status,
                         ProcedureStatusEnum.Closed.value)
