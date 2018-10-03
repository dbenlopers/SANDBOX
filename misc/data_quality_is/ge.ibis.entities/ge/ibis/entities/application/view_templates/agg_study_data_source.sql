CREATE OR REPLACE VIEW `v_agg_study_data_source` AS
with study_dosi as (
SELECT
    COALESCE(v_study_dicom_last15days.serial_number,
            v_study_dosimetric_last15days.serial_number) AS serial_number,
    COALESCE(v_study_dicom_last15days.encrypted_siuid,
            v_study_dosimetric_last15days.encrypted_siuid) AS encrypted_siuid,
    v_study_dosimetric_last15days.local_study_id,
	v_study_dosimetric_last15days.study_id as dosi_id,
	v_study_dicom_last15days.dicom_id,
    v_study_dosimetric_last15days.study_date AS study_date,
    v_study_dicom_last15days.datetime_first_received as dicom_first_received,
    v_study_dicom_last15days.datetime_last_received as dicom_last_received,
    v_study_dosimetric_last15days.modality,
    COALESCE(v_study_dosimetric_last15days.aet, IF(v_study_dicom_last15days.nb_aet_producer = 1,v_study_dicom_last15days.aet_producer,NULL)) AS aet,
    v_study_dicom_last15days.nb_aet_producer as nb_dicom_aet_producer,
    v_study_dicom_last15days.aet_producer as dicom_aet_producer,
    v_study_dicom_last15days.dicompattern_success_rate,
    v_study_dosimetric_last15days.dosimetric_success_rate
FROM
    v_study_dicom_last15days
        LEFT OUTER JOIN
    v_study_dosimetric_last15days ON (v_study_dicom_last15days.serial_number = v_study_dosimetric_last15days.serial_number
        AND v_study_dicom_last15days.encrypted_siuid = v_study_dosimetric_last15days.encrypted_siuid)
UNION ALL
SELECT
    COALESCE(v_study_dicom_last15days.serial_number,
    v_study_dosimetric_last15days.serial_number) AS serial_number,
    COALESCE(v_study_dicom_last15days.encrypted_siuid,
    v_study_dosimetric_last15days.encrypted_siuid) AS encrypted_siuid,
    v_study_dosimetric_last15days.local_study_id,
	v_study_dosimetric_last15days.study_id as dosi_id,
	v_study_dicom_last15days.dicom_id,
    v_study_dosimetric_last15days.study_date AS study_date,
    v_study_dicom_last15days.datetime_first_received as dicom_first_received,
    v_study_dicom_last15days.datetime_last_received as dicom_last_received,
    v_study_dosimetric_last15days.modality,
    COALESCE(v_study_dosimetric_last15days.aet, IF(v_study_dicom_last15days.nb_aet_producer = 1,v_study_dicom_last15days.aet_producer,NULL)) AS aet,
    v_study_dicom_last15days.nb_aet_producer as nb_dicom_aet_producer,
    v_study_dicom_last15days.aet_producer as dicom_aet_producer,
    v_study_dicom_last15days.dicompattern_success_rate,
    v_study_dosimetric_last15days.dosimetric_success_rate
FROM
    v_study_dicom_last15days
        RIGHT JOIN
    v_study_dosimetric_last15days ON (v_study_dicom_last15days.serial_number = v_study_dosimetric_last15days.serial_number
        AND v_study_dicom_last15days.encrypted_siuid = v_study_dosimetric_last15days.encrypted_siuid)
WHERE
    v_study_dicom_last15days.encrypted_siuid IS NULL
        AND v_study_dicom_last15days.serial_number IS NULL)
SELECT
    COALESCE(study_dosi.serial_number,
            v_ctlog_last15days.serial_number) AS serial_number,
    custo.customer_name,
    custo.pole,
    custo.country,
    ae.sdm_key,
    ae.integration_mode,
    study_dosi.encrypted_siuid,
    COALESCE(study_dosi.local_study_id,
            v_ctlog_last15days.local_study_id) AS local_study_id,
	study_dosi.dosi_id,
	study_dosi.dicom_id,
	v_ctlog_last15days.ctlog_id,
    study_dosi.modality,
    study_dosi.study_date,
    study_dosi.dicom_first_received,
    study_dosi.dicom_last_received,
    v_ctlog_last15days.datetime_first_insert as ctlog_first_insert,
    study_dosi.aet AS aet,
    study_dosi.nb_dicom_aet_producer,
    study_dosi.dicom_aet_producer,
    study_dosi.dosimetric_success_rate,
    study_dosi.dicompattern_success_rate,
    v_ctlog_last15days.status AS ctlog_status,
    v_ctlog_last15days.rational AS ctlog_obs,
    v_ctlog_last15days.inferred_integration_mode AS inferred_integration_mode
FROM
    study_dosi
        RIGHT outer JOIN
    v_ctlog_last15days ON (study_dosi.serial_number = v_ctlog_last15days.serial_number
        AND study_dosi.local_study_id = v_ctlog_last15days.local_study_id)
        LEFT JOIN
    (SELECT
        serial_number, customer_name, pole, country
    FROM
        customer
    WHERE
        is_last = 1) AS custo ON (COALESCE(study_dosi.serial_number,
            v_ctlog_last15days.serial_number) = custo.serial_number)
        LEFT outer JOIN
    (SELECT
        application_entity.serial_number,
            application_entity.aet,
            application_entity.sdm_key,
            integration_mode.integration_mode
    FROM
        application_entity
    LEFT JOIN ae_integration ON application_entity.id = ae_integration.application_entity_id
    LEFT JOIN integration_mode ON ae_integration.integration_mode_id = integration_mode.id
    WHERE
        application_entity.is_last = 1) AS ae ON (study_dosi.aet = ae.aet
        AND study_dosi.serial_number = ae.serial_number)
WHERE
    study_dosi.study_date >= CURDATE() - INTERVAL + 14 DAY OR study_dosi.study_date is NULL
UNION ALL
SELECT
    study_dosi.serial_number AS serial_number,
    custo.customer_name,
    custo.pole,
    custo.country,
    ae.sdm_key,
    ae.integration_mode,
    study_dosi.encrypted_siuid,
    study_dosi.local_study_id,
	study_dosi.dosi_id,
	study_dosi.dicom_id,
	NULL as ctlog_id,
    study_dosi.modality,
    study_dosi.study_date,
    study_dosi.dicom_first_received,
    study_dosi.dicom_last_received,
    NULL as ctlog_first_insert,
    study_dosi.aet AS aet,
    study_dosi.nb_dicom_aet_producer,
    study_dosi.dicom_aet_producer,
    study_dosi.dosimetric_success_rate,
    study_dosi.dicompattern_success_rate,
    NULL AS ctlog_status,
    NULL AS ctlog_obs,
    NULL AS inferred_integration_mode
FROM
    study_dosi
        LEFT JOIN
    (SELECT
        serial_number, customer_name, pole, country
    FROM
        customer
    WHERE
        is_last = 1) AS custo ON (study_dosi.serial_number = custo.serial_number)
        LEFT outer JOIN
    (SELECT
        application_entity.serial_number,
            application_entity.aet,
            application_entity.sdm_key,
            integration_mode.integration_mode
    FROM
        application_entity
    LEFT JOIN ae_integration ON application_entity.id = ae_integration.application_entity_id
    LEFT JOIN integration_mode ON ae_integration.integration_mode_id = integration_mode.id
    WHERE
        application_entity.is_last = 1) AS ae ON (study_dosi.aet = ae.aet
        AND study_dosi.serial_number = ae.serial_number)
WHERE
    (study_dosi.serial_number , study_dosi.local_study_id) NOT IN (SELECT
            serial_number, local_study_id
        FROM
            v_ctlog_last15days
        WHERE
            local_study_id IS NOT NULL)
        AND study_dosi.study_date >= CURDATE() - INTERVAL + 14 DAY OR study_dosi.study_date is NULL
;