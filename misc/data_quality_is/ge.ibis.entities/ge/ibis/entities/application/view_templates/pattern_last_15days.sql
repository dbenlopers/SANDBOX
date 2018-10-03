CREATE OR REPLACE VIEW v_pattern_last15days AS
    SELECT
        dicom_input.serial_number AS serial_number,
        dicom_input.encrypted_siuid AS encrypted_siuid,
        dicom_input.id AS dicom_input_id,
        study.id AS study_id,
        study.local_study_id AS local_study_id,
        custo.customer_name AS customer_name,
        dicom_input.aet AS aet,
        ae.sdm_key AS sdm_key,
        ae.device_type AS modality,
        ae.integration_mode AS integration_mode,
        study.start_date AS study_date,
        dicom_input.datetime_first_received AS datetime_first_received,
        dicom_pattern.message_command AS prod_command,
        dicom_pattern.sop_class AS prod_sop_class,
        dicom_pattern.message_type AS prod_message_type,
        dicom_pattern.series_number AS prod_series_number,
        dicom_pattern.study_status AS prod_study_status,
        dicom_pattern.message_status AS prod_message_status,
        message_pattern.message_type AS message_type,
        IFNULL(status.status, 'NA') AS status,
        IFNULL(rationale.rationale, 'AE_UNKNOWN') AS rational
    FROM
        dicom_input
        LEFT JOIN dicom_input_status ON (dicom_input_status.dicom_input_id = dicom_input.id)
        LEFT JOIN `status` ON (status.id = dicom_input_status.status_id)
        LEFT JOIN rationale ON (rationale.id = dicom_input_status.rationale_id)
        LEFT JOIN dicom_pattern ON (dicom_pattern.id = dicom_input_status.dicom_pattern_id)
        LEFT JOIN message_pattern ON (dicom_input_status.message_pattern_id = message_pattern.id)
        LEFT JOIN study 
        ON (study.serial_number = dicom_input.serial_number
            AND study.encrypted_siuid = dicom_input.encrypted_siuid)
        LEFT JOIN (
            SELECT customer.serial_number AS serial_number, customer.customer_name AS customer_name
            FROM customer
            WHERE customer.is_last = 1) AS custo
        ON (dicom_input.serial_number = custo.serial_number)
        LEFT JOIN (
            SELECT application_entity.serial_number AS serial_number,
                application_entity.aet AS aet,
                application_entity.sdm_key AS sdm_key,
                application_entity.device_type AS device_type,
                integration_mode.integration_mode AS integration_mode
            FROM
                application_entity
            LEFT JOIN ae_integration ON (application_entity.id = ae_integration.application_entity_id)
            LEFT JOIN integration_mode ON (ae_integration.integration_mode_id = integration_mode.id)
            WHERE
                application_entity.is_last = 1) AS ae 
        ON (dicom_input.aet = ae.aet
            AND dicom_input.serial_number = ae.serial_number)
    WHERE
        dicom_input.datetime_first_received >= (CURDATE() - INTERVAL 15 DAY)
;