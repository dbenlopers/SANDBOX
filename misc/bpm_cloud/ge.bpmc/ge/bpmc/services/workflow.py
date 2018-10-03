# -*- coding: utf-8 -*-

from copy import copy

from sqlalchemy import and_, case, delete, func, or_, text, update

from ge.bpmc import SOP_CLASS_FORMAT, business
from ge.bpmc.exceptions.base import BPMFlaskException
from ge.bpmc.exceptions.matching import BPMMatchingException
from ge.bpmc.exceptions.processing import (BPMProcessingException,
                                           BPMProcessingInvalidException)
from ge.bpmc.exceptions.storage import BPMNoAvailableStorage
from ge.bpmc.persistence.orm import (ExamORM, ExamStatusEnum, ImageMatchORM,
                                     ImageMetadataORM, ImageMetricsDisplayORM,
                                     ImageMetricsORM, ImageORM,
                                     ImageStatusEnum, ImageStatusORM,
                                     IssuerORM, LateralityEnum,
                                     PresentationIntentTypeEnum, ProcedureORM,
                                     ProcedureStatusEnum, ProcedureStatusORM)
from ge.bpmc.persistence.viewmodels import (ExamProceduresImageResultsVM,
                                            ImageMatchingDataVM, ImageResultVM,
                                            ProcedureImageResultsVM)
from ge.bpmc.utilities.sqlalchemy import sqlalchemy_get_unique_item_or_none


class WorkflowService:
    """
    Handles business rules for BPM
    """

    def __init__(self, logger, science_logger, em):
        self.logger = logger
        self.science_logger = science_logger
        self.em = em

    def _get_image_results_base_query(self):
        return (self.em._session_.query(
            ImageORM.uid,
            ImageStatusORM.status,
            case([(ImageMatchORM.destination.isnot(None),
                   ImageMatchORM.destination)], else_=0),
            ImageMetricsORM.overlay,
            ImageMetricsORM.criteria,
            ImageMetricsDisplayORM.uid,
            ImageMetadataORM.extra).
            join(ImageMatchORM, ImageMatchORM.origin == ImageORM.uid,
                 isouter=True).
            join(ImageMetadataORM).
            join(ImageStatusORM).
            join(ImageMetricsORM).
            join(ImageMetricsDisplayORM))

    def extract_matching_data(self, image_result):
        '''
        Removes kpis and overlay related to the procedure from the image
        and returns them.
        The reason we do this is because this information is generated at the
        image level when matching is done. This is only necessary if the image
        has been matched to another one.

        Keyword arguments:
        image_result -- An ImageResultVM instance
        '''
        if not image_result.matched_with:
            return
        data = {'uid': image_result.uid}
        data['match'] = image_result.matched_with
        if image_result.overlay != {}:
            data['ov_sym'] = (image_result.overlay.pop('symmetry')
                              if 'symmetry' in image_result.overlay else None)
            data['ov_lg_pnl'] = (image_result.overlay.pop(
                'length_of_posterior_nipple_line')
                if 'length_of_posterior_nipple_line' in image_result.overlay
                else None)
        if image_result.criteria != {}:
            data['kpi_sym'] = (image_result.criteria.pop('symmetry')
                               if 'symmetry'
                               in image_result.criteria else None)
            data['kpi_lg_pnl'] = (image_result.criteria.pop(
                'length_of_posterior_nipple_line')
                if 'length_of_posterior_nipple_line' in image_result.criteria
                else None)
        return data

    def concat_procedure_matching_data(self, proc_data):
        '''
        Use extracted image matching data to build up a dict
        containing formated procedure matching data.

        Keyword arguments:
        proc_data -- A list of dictionnaries generated using
        extract_matching_data on a ImageResultVM.
        '''
        proc_data = [x for x in filter(lambda x: x is not None, proc_data)]
        if (len(proc_data) % 2) != 0:
            # This should NEVER happen unless
            # matching or persistence went wrong
            raise ValueError('Matching data is expected to contains pairs')
        matched = []

        while(proc_data):
            item = proc_data.pop(0)
            filtered = [x for x in
                        filter(lambda x: x['match'] == item['uid'], proc_data)]
            if not filtered:
                # Likewise, this should never happen
                raise ValueError('Associated pair not found')
            paired = proc_data.pop(proc_data.index(filtered[0]))

            matched.append({
                'pair': [item['uid'], paired['uid']],
                'kpis': {
                    'symmetry': item['kpi_sym'],
                    'length_of_posterior_nipple_line':
                        item['kpi_lg_pnl']
                },
                # 'overlays': [
                #     {
                #         'image_uid': item['uid'],
                #         'overlay': {
                #             'symmetry': item['ov_sym'],
                #             'length_of_posterior_nipple_line':
                #                 item['ov_lg_pnl']
                #         }
                #     },
                #     {
                #         'image_uid': paired['uid'],
                #         'overlay': {
                #             'symmetry': paired['ov_sym'],
                #             'length_of_posterior_nipple_line':
                #                 paired['ov_lg_pnl']
                #         }
                #     }
                # ]
            })
        return matched

    @sqlalchemy_get_unique_item_or_none
    def get_image_result(self, issuer_key, image_uid):
        '''
        Returns an image result if exist. See ImageResultVM class for more
        details. The image content is still missing since bytes need to be
        queried using the storage service.

        Keyword arguments:
        issuer_key -- Str, an Issuer key
        image_uid -- Int, an Image uid
        '''
        base_query = self._get_image_results_base_query()
        img_res_query = (base_query
                         .join(ProcedureORM)
                         .join(ExamORM)
                         .join(IssuerORM)
                         .filter(ImageORM.uid == image_uid)
                         .filter(IssuerORM.key == issuer_key))
        item = img_res_query.first()
        if not item:
            return ImageResultVM(*([None] * 7))
        ct = ImageResultVM(*item)
        # At the image level, we just want to filter this data
        self.extract_matching_data(ct)
        return ct

    @sqlalchemy_get_unique_item_or_none
    def get_procedure_result(self, issuer_key, proc_uid):
        '''
        Returns procedure image results if exist. See ProcedureImageResultsVM
        class for more details. This contains the procedure uid, its status and
        associated image results.

        Keyword arguments:
        issuer_key -- Str, an Issuer key
        proc_uid -- Int, a procedure uid
        '''
        proc = (self.em._session_
                .query(ProcedureORM.uid, ProcedureStatusORM.status)
                .join(ProcedureStatusORM)
                .join(ExamORM)
                .join(IssuerORM)
                .filter(IssuerORM.key == issuer_key)
                .filter(ProcedureORM.uid == proc_uid).one())
        base_query = self._get_image_results_base_query()
        proc_images = [ImageResultVM(*x) for x in
                       base_query.filter(ImageORM.procedure_uid == proc_uid)
                       .all()]
        self.em.upd_procedure_status('procedure_uid', proc_uid, {
            'sent': True
        })
        matching_data = self.concat_procedure_matching_data(
            list(map(self.extract_matching_data, proc_images)))
        unique_images = list({x.uid: x for x in proc_images}.values())
        return ProcedureImageResultsVM(*proc,
                                       matching_data,
                                       unique_images)

    @sqlalchemy_get_unique_item_or_none
    def get_exam_result(self, issuer_key, exam_uid):
        '''
        Returns exam procedure image results if exist. See
        ExamProceduresImageResultsVM class for more details. This contains the
        exam uid, its status and associated procedures image results.

        Keyword arguments:
        issuer_key -- Str, an Issuer key
        exam_uid -- Int, an Exam uid
        '''
        exam = (self.em._session_
                .query(ExamORM.uid)
                .join(IssuerORM)
                .filter(IssuerORM.key == issuer_key)
                .filter(ExamORM.uid == exam_uid).one())
        procs = (self.em._session_
                 .query(ProcedureORM.uid, ProcedureStatusORM.status)
                 .join(ProcedureStatusORM)
                 .filter(ProcedureORM.exam_uid == exam_uid).all())
        procedures = []
        base_query = self._get_image_results_base_query()
        for proc_uid, proc_status in procs:
            proc_images = [ImageResultVM(*x) for x in
                           base_query.filter(
                               ImageORM.procedure_uid == proc_uid)
                           .all()]
            matching_data = self.concat_procedure_matching_data(
                list(map(self.extract_matching_data, proc_images)))
            unique_images = list({x.uid: x for x in proc_images}.values())
            procedures.append(ProcedureImageResultsVM(
                proc_uid, proc_status, matching_data, unique_images))

        ps = ProcedureStatusORM._sa_class_manager.mapper.mapped_table
        if procs:
            self.em._session_.execute(
                update(ps)
                .where(ps.c.procedure_uid.in_([x[0] for x in procs]))
                .values({'sent': True})
            )
        self.em.upd_exam_status('exam_uid', exam_uid, {
            'sent': True
        })
        return ExamProceduresImageResultsVM(exam_uid, procedures)

    def consume_issuer_available_procedures(self, issuer_key):
        """
        Returns all procedures set as ready for the issuer and then
        removes the ready flag.

        Keyword arguments:
        issuer_key -- Str, an Issuer key
        """
        items = self.em._session_ \
            .query(ProcedureORM) \
            .join(ProcedureStatusORM) \
            .join(ExamORM) \
            .join(IssuerORM) \
            .filter(IssuerORM.key == issuer_key) \
            .filter(ProcedureStatusORM.ready.is_(True)).all()
        # Emptying ready items
        if items:
            st_table = ProcedureStatusORM._sa_class_manager.mapper.mapped_table
            stmt = update(st_table) \
                .where(st_table.c.procedure_uid.in_([x.uid for x in items])) \
                .values(ready=False)
            self.em._session_.execute(stmt)
        self.logger.debug('Consumed procedures for issuer %(key)s' % ({
            'key': issuer_key}))
        return [copy(x) for x in items]

    def consume_issuer_available_images(self, issuer_key):
        """
        Returns all images set as ready for the issuer and then
        removes the ready flag.

        Keyword arguments:
        issuer_key -- Str, an Issuer key
        """
        items = self.em._session_ \
            .query(ImageORM) \
            .join(ImageStatusORM) \
            .join(ProcedureORM) \
            .join(ExamORM) \
            .join(IssuerORM) \
            .filter(IssuerORM.key == issuer_key) \
            .filter(ImageStatusORM.ready.is_(True)).all()
        # Emptying ready items
        if items:
            st_table = ImageStatusORM._sa_class_manager.mapper.mapped_table
            stmt = update(st_table) \
                .where(st_table.c.image_uid.in_([x.uid for x in items])) \
                .values(ready=False)
            self.em._session_.execute(stmt)
        self.logger.debug('Consumed images for issuer %(key)s' % ({
            'key': issuer_key}))
        return [copy(x) for x in items]

    def associate_matched_images(self, uid1, uid2):
        """
        Sets the 'matched_with' column of an image pair

        Keyword arguments:
        uid1 -- Int, Image UID
        uid2 -- Int, associated image UID
        """
        self.em.add_image_match({'origin': uid1, 'destination': uid2})
        self.em.add_image_match({'origin': uid2, 'destination': uid1})

    def update_matched_images_metrics(self, uid1, uid2, criteria, overlays):
        """
        Updates matched images metrics metadata.

        Keyword arguments:
        uid1 -- Int, Image UID
        uid2 -- Int, associated image UID
        criteria -- Dict, contains updated/missing keys
        overlays -- List of Dict, contains updated/missing keys for each image
                    id
        """
        metrics_table = ImageMetricsORM._sa_class_manager.mapper.mapped_table
        uid1_metrics = self.em.get_image_metrics('image_uid', uid1)
        uid2_metrics = self.em.get_image_metrics('image_uid', uid2)
        self.logger.debug('Updating image metrics %s %s %s %s' % (
            uid1, uid2, criteria, overlays))
        uid1_metrics.criteria.update(criteria)
        uid2_metrics.criteria.update(criteria)
        # TODO: Implement overlay management in image matching
        # uid1_metrics.overlay.update(overlays.get(uid1))
        # uid2_metrics.overlay.update(overlays.get(uid2))
        stmt1 = update(metrics_table).where(
            metrics_table.c.image_uid == uid1
        ).values({
            'criteria': uid1_metrics.criteria,
            # 'overlay': uid1_metrics.overlay
        })
        stmt2 = update(metrics_table).where(
            metrics_table.c.image_uid == uid2
        ).values({
            'criteria': uid2_metrics.criteria,
            # 'overlay': uid2_metrics.overlay
        })
        self.em._session_.execute(stmt1)
        self.em._session_.execute(stmt2)

    def get_procedure_matching_data(self, uid):
        """
        Returns images metadata required for matching for a specific procedure.
        image metadata: List of dict which contains for each image the
        image_laterality, view_position, acquisition_time and the overlay.

        Keyword arguments:
        uid -- Int, Procedure  UID
        """
        return [ImageMatchingDataVM(*x).to_dict() for x in self.em._session_
                .query(ImageORM.uid, ImageMetadataORM.image_laterality,
                       ImageMetadataORM.view_position,
                       ImageMetadataORM.acquisition_time,
                       ImageMetricsORM.criteria,
                       ImageMetadataORM.processing_data)
                .join(ImageMetricsORM)
                .join(ImageMetadataORM)
                .join(ImageStatusORM)
                .filter(ImageStatusORM.status ==
                        ImageStatusEnum.Processed.value)
                .filter(ImageORM.procedure_uid == uid).all()]

    def match_procedure(self, procedure_uid):
        """
        Runs the matching algorythm on a processed procedure.

        Keyword arguments:
        procedure_uid -- Int, Procedure UID
        """
        images_metadata = self.get_procedure_matching_data(procedure_uid)
        try:
            matches = business.match_procedure_images(
                self.science_logger, images_metadata)
            self.logger.debug(
                'Matched procedure %(uid)s with matches %(matches)s' % ({
                    'uid': procedure_uid,
                    'matches': [x['pair'] for x in matches]}))
            for match in matches:
                uid1, uid2 = match['pair']
                self.associate_matched_images(uid1, uid2)
                self.update_matched_images_metrics(
                    uid1, uid2, match['criteria'],
                    match.get('overlays', {}))
            status = ProcedureStatusEnum.Done.value
        except BPMMatchingException as err:
            self.logger.warning(err)
            status = ProcedureStatusEnum.Error.value
        self.em.upd_procedure_status('procedure_uid', procedure_uid, {
            'status': status
        })

    def close_previous_procedures(self, exam_uid, current_procedure_uid):
        """
        Updates an exam's previous procedures status to
        ProcedureStatusEnum.Closed if they are still in waiting status.

        Keyword arguments:
        exam_uid -- Int, Exam UID
        current_procedure_uid -- Int, the current Procedure UID
        """
        proc_uids = (self.em._session_.query(ProcedureORM.uid)
                     .join(ProcedureStatusORM)
                     .join(ExamORM)
                     .filter(ExamORM.uid == exam_uid)
                     .filter(ProcedureStatusORM.status ==
                             ProcedureStatusEnum.Waiting.value)
                     .filter(ProcedureORM.uid < current_procedure_uid).all())

        if not proc_uids:
            return

        pst = ProcedureStatusORM._sa_class_manager.mapper.mapped_table
        upd = update(pst).where(
            pst.c.procedure_uid.in_([x[0] for x in proc_uids])
        ).values({
            'status': ProcedureStatusEnum.Closed.value
        })
        self.em._session_.execute(upd)

    def update_processed_procedures(self):
        """
        Sets procedures status & readiness flag if considered as finished.
        Returns the updated procedures afterwards.
        """
        ps = self.em._session_.query(
            ProcedureORM.uid.label('uid'),
            func.sum(
                case([
                    (ImageStatusORM.status == ImageStatusEnum.Waiting.value, 1)
                ], else_=0)
            ).label('pending'),
            func.max(ImageORM.inserted_on).label('inserted'),
            ProcedureStatusORM.status.label('status')) \
            .join(ProcedureStatusORM) \
            .join(ImageORM) \
            .join(ImageStatusORM) \
            .filter(ProcedureStatusORM.status.in_([
                    ProcedureStatusEnum.Closed.value,
                    ProcedureStatusEnum.Waiting.value])) \
            .group_by(ProcedureORM.uid).subquery('ps', with_labels=True)

        query = self.em._session_ \
            .query(ps.c.uid) \
            .select_entity_from(ps) \
            .filter(ps.c.pending == 0) \
            .filter(
                or_(
                    ps.c.status == ProcedureStatusEnum.Closed.value,
                    and_(
                        func.now() > func.date_add(
                            ps.c.inserted, text('INTERVAL 10 MINUTE')),
                        ps.c.status == ProcedureStatusEnum.Waiting.value
                    )
                )
            )

        pst = ProcedureStatusORM._sa_class_manager.mapper.mapped_table
        upd = update(pst).where(
            pst.c.procedure_uid.in_(query)
        ).values({
            'ready': True,
            'status': ProcedureStatusEnum.Processed.value
        })

        processed = [
            x[0] for x in self.em._session_.query(ProcedureStatusORM.uid)
            .filter(
                ProcedureStatusORM.status ==
                ProcedureStatusEnum.Processed.value)
            .all()]
        self.em._session_.execute(upd)
        updated_query = self.em._session_ \
            .query(ProcedureStatusORM.procedure_uid) \
            .filter(
                ProcedureStatusORM.status ==
                ProcedureStatusEnum.Processed.value)
        updated_query = (updated_query.filter(
            ProcedureStatusORM.uid.notin_(processed)) if processed
            else updated_query)
        return [x[0] for x in updated_query.all()]

    def process_image(self, uid, metadata):
        processed_image = None
        metrics = None
        try:
            criteria, overlay, processed_image = business.process_image(
                self.science_logger, metadata)
            image_status = ImageStatusEnum.Processed.value
            metrics = (self.em.get_image_metrics('image_uid', uid) or
                       self.em.add_image_metrics({
                           'image_uid': uid,
                           'criteria': criteria,
                           'overlay': overlay
                       }))
        except BPMProcessingInvalidException as err:
            self.logger.warning('Invalid image with uid %s' % uid)
            image_status = ImageStatusEnum.Invalid.value
        except BPMProcessingException as err:
            self.logger.warning(err)
            image_status = ImageStatusEnum.Error.value

        self.em.upd_image_status('image_uid', uid, {
            'status': image_status,
            'ready': image_status == ImageStatusEnum.Processed.value
        })

        return (metrics, processed_image)

    def compute_request(self, issuer, payload):
        image_sop_class = payload.get('sop_class')
        if not SOP_CLASS_FORMAT.match(image_sop_class):
            raise BPMFlaskException('Invalid SOP Class')
        sop_class = self.em \
            .get_or_create_sop_class(image_sop_class)

        modality_metadata = payload.get('modality', {})
        model_name = modality_metadata.get('model_name')
        software_version = modality_metadata.get('software_version')
        manufacturer_name = modality_metadata.get('manufacturer_name')
        modality_type = self.em.get_or_create_modality_type(
            model_name, software_version, manufacturer_name)

        exam_args = {
            'exam_uid': payload.get('exam_uid', None),
            'issuer_uid': issuer.uid
        }
        exam = self.em.get_or_create_exam(**exam_args)
        exam_status = self.em.get_or_create_exam_status(
            exam.uid,
            ProcedureStatusEnum.Waiting.value)
        procedure_args = {
            'procedure_uid': payload.get('procedure_uid', None),
            'exam_uid': exam.uid
        }
        procedure = self.em.get_or_create_procedure(**procedure_args)
        procedure_status = self.em.get_or_create_procedure_status(
            procedure.uid,
            ProcedureStatusEnum.Waiting.value)
        self.close_previous_procedures(exam.uid, procedure.uid)
        repository = self.em.get_available_repository()
        if not repository:
            raise BPMNoAvailableStorage()

        # Reopen procedure if necessary

        if procedure_status.status != ProcedureStatusEnum.Waiting.value:
            self.em.upd_procedure_status('uid', procedure_status.uid, {
                'status': ProcedureStatusEnum.Waiting.value
            })
            query = (self.em._session_
                     .query(ImageORM.uid)
                     .filter(ImageORM.procedure_uid == procedure.uid))

            it = ImageMatchORM._sa_class_manager.mapper.mapped_table
            match_delete_stmt = (
                delete(it)
                .where(or_(
                    it.c.origin.in_(query),
                    it.c.destination.in_(query))
                ))
            self.em._session_.execute(match_delete_stmt)

        # Metadata validation

        processing_data = payload.get('processing_data')
        sor = payload.get('size_of_return')
        acquisition_time = payload.get('acquisition_time')
        image_laterality = payload.get('image_laterality')
        breast_implant_present = payload.get('breast_implant_present').lower()
        presentation_intent_type = processing_data \
            .get('presentation_intent_type').upper()
        image_pixel_spacing = processing_data \
            .get('imager_pixel_spacing', {})

        if not self.em.in_laterality(image_laterality):
            raise BPMFlaskException(
                'Invalid laterality, possible values are %s' % (
                    ','.join(["'%s'" % x.value
                              for x in LateralityEnum.__members__.values()])
                ))

        if not self.em.in_presentation_intent_type(presentation_intent_type):
            raise BPMFlaskException(
                'Invalid presentation intent type, possible values are %s' % (
                    ','.join(["'%s'" % x.value
                              for x in
                              PresentationIntentTypeEnum.__members__.values()])
                ))

        if breast_implant_present == 'yes':
            breast_implant_present = True
        elif breast_implant_present == 'no':
            breast_implant_present = False
        else:
            raise BPMFlaskException('Invalid breast_implant_present,' +
                                    'should be "yes" or "no"')

        image_metadata_kwargs = {
            'breast_implant_present': breast_implant_present,
            'image_laterality': image_laterality,
            'acquisition_time': acquisition_time,
            'processing_data': processing_data,
            'view_position': payload.get('view_position'),
            'compression_force': payload.get('compression_force'),
            'size_of_return_rows': sor.get('rows'),
            'size_of_return_columns': sor.get('columns'),
            'extra': payload.get('requester_extra', None)
        }

        img_metadata = self.em.add_image_metadata(image_metadata_kwargs)

        image_kwargs = {
            'procedure_uid': procedure.uid,
            'repository_uid': repository.uid,
            'modality_type_uid': modality_type.uid,
            'sop_class_uid': sop_class.uid,
            'metadata_uid': img_metadata.uid,
            'inserted_on': None,
            'matched_with': None
        }

        image = self.em.add_image(image_kwargs)
        image_status = self.em.add_image_status({
            'image_uid': image.uid,
            'ready': False,
            'status': ImageStatusEnum.Waiting.value
        })
        self.logger.debug('Request computed with metadata %(metadata)s' % ({
            'metadata': {'exam': exam.uid, 'procedure': procedure.uid,
                         'image': image.uid, 'repository': repository.uid}
        }))
        return (exam, procedure, image, repository)
