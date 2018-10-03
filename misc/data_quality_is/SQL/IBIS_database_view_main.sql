USE ibis;

-- View creation

-- This view expose raw dosimetric data since 21 days
CREATE OR REPLACE  VIEW v_dosimetric_data_last21days AS
WITH dosi_data as (
SELECT
		study.serial_number,
		study.id as study_id,
		study.aet,
		ae.integration_mode,
		study.local_study_id,
		study.type as modality,
		DATE(study.start_date) as date,
		study.sdm_key,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.total_dap"), DOUBLE),3) as study_total_dap,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.total_dap_test"), DOUBLE),3) as serie_total_dap,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.entrance_dose"), DOUBLE),3) as study_entrance_dose,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.entrance_dose_test"), DOUBLE),3) as serie_entance_dose,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.organ_dose"), DOUBLE),3) as study_organ_dose,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.organ_dose_test"), DOUBLE),3) as serie_organ_dose,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.tne"), DOUBLE),3) as study_tne,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.tne_test"), DOUBLE),3) as serie_tne,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.total_ak"), DOUBLE),3) as study_total_ak,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.total_ak_test"), DOUBLE),3) as serie_total_ak,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.fluoro_ak"), DOUBLE),3) as study_fluoro_ak,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.fluoro_ak_test"), DOUBLE),3) as serie_fluoro_ak,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.fluoro_dap"), DOUBLE),3) as study_fluoro_dap,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.fluoro_dap_test"), DOUBLE),3) as serie_fluoro_dap,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.record_ak"), DOUBLE),3) as study_record_ak,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.record_ak_test"), DOUBLE),3) as serie_record_ak,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.record_time"), DOUBLE),3) as study_record_time,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.record_time_test"), DOUBLE),3) as serie_record_time,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.tnrf"), DOUBLE),3) as study_tnrf,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.tnrf_test"), DOUBLE),3) as serie_tnrf,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.ttf"), DOUBLE),3) as study_ttf,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.ttf_test"), DOUBLE),3) as serie_ttf,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.total_dlp"), DOUBLE),3) as study_total_dlp,
		ROUND(CONVERT(JSON_VALUE(DATA, "$.total_dlp_test"), DOUBLE),3) as serie_total_dlp,
		CONVERT(JSON_VALUE(DATA, "$.num_localizers_value"), INT) as num_localizers
	FROM
		study
		LEFT JOIN
		(SELECT
        application_entity.serial_number as sn,
            application_entity.aet as ae_aet,
            integration_mode.integration_mode
    FROM
        application_entity
    LEFT JOIN ae_integration ON application_entity.id = ae_integration.applicationentity_id
    LEFT JOIN integration_mode ON ae_integration.integrationmode_id = integration_mode.id
    WHERE
        application_entity.is_last = 1) AS ae ON (study.aet = ae.ae_aet
        AND study.serial_number = ae.sn)
	WHERE
		study.start_date >= CURDATE() - INTERVAL 21 DAY)
SELECT
	dosi_data.serial_number,
	dosi_data.study_id,
	dosi_data.aet,
	dosi_data.integration_mode,
	dosi_data.local_study_id,
	dosi_data.modality,
	dosi_data.date,
	dosi_data.sdm_key,
	dosi_data.study_total_dap,
	dosi_data.serie_total_dap,
	ROUND(Abs((dosi_data.study_total_dap-dosi_data.serie_total_dap)/dosi_data.study_total_dap) * 100, 3) as diff_total_dap_rate,
	dosi_data.study_total_dap - dosi_data.serie_total_dap as diff_total_dap_rel,
	dosi_data.study_entrance_dose,
	dosi_data.serie_entance_dose,
	ROUND(Abs((dosi_data.study_entrance_dose-dosi_data.serie_entance_dose)/dosi_data.study_entrance_dose) * 100, 3) as diff_entrance_dose_rate,
	dosi_data.study_entrance_dose - dosi_data.serie_entance_dose as diff_entrance_dose_rel,
	dosi_data.study_organ_dose,
	dosi_data.serie_organ_dose,
	ROUND(Abs((dosi_data.study_organ_dose-dosi_data.serie_organ_dose)/dosi_data.study_organ_dose) * 100, 3) as diff_organ_dose_rate,
	dosi_data.study_organ_dose - dosi_data.serie_organ_dose as diff_organ_dose_rel,
	dosi_data.study_tne,
	dosi_data.serie_tne,
	ROUND(Abs((dosi_data.study_tne-dosi_data.serie_tne)/dosi_data.study_tne) * 100, 3) as diff_tne_rate,
	dosi_data.study_tne - dosi_data.serie_tne as diff_tne_rel,
	dosi_data.study_total_ak,
	dosi_data.serie_total_ak,
	ROUND(Abs((dosi_data.study_total_ak-dosi_data.serie_total_ak)/dosi_data.study_total_ak) * 100, 3) as diff_total_ak_rate,
	dosi_data.study_total_ak - dosi_data.serie_total_ak as diff_total_ak_rel,
	dosi_data.study_fluoro_ak,
	dosi_data.serie_fluoro_ak,
	ROUND(Abs((dosi_data.study_fluoro_ak-dosi_data.serie_fluoro_ak)/dosi_data.study_fluoro_ak) * 100, 3) as diff_fluoro_ak_rate,
	dosi_data.study_fluoro_ak - dosi_data.serie_fluoro_ak as diff_fluoro_ak_rel,
	dosi_data.study_fluoro_dap,
	dosi_data.serie_fluoro_dap,
	ROUND(Abs((dosi_data.study_fluoro_dap-dosi_data.serie_fluoro_dap)/dosi_data.study_fluoro_dap) * 100, 3) as diff_fluoro_dap_rate,
	dosi_data.study_fluoro_dap - dosi_data.serie_fluoro_dap as diff_fluoro_dap_rel,
	dosi_data.study_record_ak,
	dosi_data.serie_record_ak,
	ROUND(Abs((dosi_data.study_record_ak-dosi_data.serie_record_ak)/dosi_data.study_record_ak) * 100, 3) as diff_record_ak_rate,
	dosi_data.study_record_ak - dosi_data.serie_record_ak as diff_record_ak_rel,
	dosi_data.study_record_time,
	dosi_data.serie_record_time,
	ROUND(Abs((dosi_data.study_record_time-dosi_data.serie_record_time)/dosi_data.study_record_time) * 100, 3) as diff_record_time_rate,
	dosi_data.study_record_time - dosi_data.serie_record_time as diff_record_time_rel,
	dosi_data.study_tnrf,
	dosi_data.serie_tnrf,
	ROUND(Abs((dosi_data.study_tnrf-dosi_data.serie_tnrf)/dosi_data.study_tnrf) * 100, 3) as diff_tnrf_rate,
	dosi_data.study_tnrf - dosi_data.serie_tnrf as diff_tnrf_rel,
	dosi_data.study_ttf,
	dosi_data.serie_ttf,
	ROUND(Abs((dosi_data.study_ttf-dosi_data.serie_ttf)/dosi_data.study_ttf) * 100, 3) as diff_ttf_rate,
	dosi_data.study_ttf - dosi_data.serie_ttf as diff_ttf_rel,
	dosi_data.study_total_dlp,
	dosi_data.serie_total_dlp,
	ROUND(Abs((dosi_data.study_total_dlp-dosi_data.serie_total_dlp)/dosi_data.study_total_dlp) * 100, 3) as diff_total_dlp_rate,
	dosi_data.study_total_dlp - dosi_data.serie_total_dlp as diff_total_dlp_rel,
	dosi_data.num_localizers
FROM
	dosi_data;

-- This view dosimetric test since 15 days
CREATE OR REPLACE VIEW v_dosimetric_last15days AS
    SELECT
        ibis.study.serial_number AS serial_number,
        custo.pole AS pole,
        custo.customer_name AS customer_name,
        ibis.study.aet AS aet,
        ae.sdm_key AS sdm_key,
        ibis.study.type AS modality,
        ae.integration_mode AS integration_mode,
        ibis.study.start_date AS study_date,
        ibis.study.id AS study_id,
        ibis.dosimetric.type AS dosimetric_type,
        ibis.dosimetric.value AS dosimetric_diff,
        ibis.status.status AS status,
        ibis.rational.rational AS rational
    FROM
        ibis.study
            JOIN
        ibis.dosimetric ON (ibis.dosimetric.study_id = ibis.study.id)
            JOIN
        ibis.status ON (ibis.status.id = ibis.dosimetric.status_id)
            JOIN
        ibis.rational ON (ibis.rational.id = ibis.dosimetric.rational_id)
            LEFT JOIN
        (SELECT
            ibis.customer.serial_number AS serial_number,
                ibis.customer.customer_name AS customer_name,
                ibis.customer.pole AS pole
        FROM
            ibis.customer
        WHERE
            ibis.customer.is_last = 1) custo ON (ibis.study.serial_number = custo.serial_number)
            LEFT JOIN
        (SELECT
            ibis.application_entity.serial_number AS serial_number,
                ibis.application_entity.aet AS aet,
                ibis.application_entity.sdm_key AS sdm_key,
                ibis.integration_mode.integration_mode AS integration_mode
        FROM
            ((ibis.application_entity
        LEFT JOIN ibis.ae_integration ON (ibis.application_entity.id = ibis.ae_integration.applicationentity_id))
        LEFT JOIN ibis.integration_mode ON (ibis.ae_integration.integrationmode_id = ibis.integration_mode.id))
        WHERE
            ibis.application_entity.is_last = 1) ae ON (ibis.study.aet = ae.aet
            AND ibis.study.serial_number = ae.serial_number)
    WHERE
        ibis.study.start_date >= CURDATE() - INTERVAL 15 DAY
;

-- This view expose incoming pattern test since 15 days
CREATE OR REPLACE VIEW v_pattern_last15days AS
    SELECT
        ibis.dicom_input.serial_number AS serial_number,
        ibis.dicom_input.encrypted_siuid AS encrypted_siuid,
        ibis.dicom_input.id AS dicom_input_id,
        ibis.study.id AS study_id,
        ibis.study.local_study_id AS local_study_id,
        custo.customer_name AS customer_name,
        ibis.dicom_input.aet AS aet,
        ae.sdm_key AS sdm_key,
        ae.device_type AS modality,
        ae.integration_mode AS integration_mode,
        ibis.study.start_date AS study_date,
        ibis.dicom_input.datetime_first_received AS datetime_first_received,
        ibis.dicom_pattern.message_command AS prod_command,
        ibis.dicom_pattern.sop_class AS prod_sop_class,
        ibis.dicom_pattern.message_type AS prod_message_type,
        ibis.dicom_pattern.series_number AS prod_series_number,
        ibis.dicom_pattern.study_status AS prod_study_status,
        ibis.dicom_pattern.message_status AS prod_message_status,
        ibis.message_pattern.message_type AS message_type,
        IFNULL(ibis.status.status, 'NA') AS status,
        IFNULL(ibis.rational.rational, 'AE_UNKNOW') AS rational
    FROM
        ibis.dicom_input
            LEFT JOIN
        ibis.dicominput_status ON (ibis.dicominput_status.dicominput_id = ibis.dicom_input.id)
            LEFT JOIN
        ibis.status ON (ibis.status.id = ibis.dicominput_status.status_id)
            LEFT JOIN
        ibis.rational ON (ibis.rational.id = ibis.dicominput_status.rational_id)
            LEFT JOIN
        ibis.dicom_pattern ON (ibis.dicom_pattern.id = ibis.dicominput_status.dicompattern_id)
            LEFT JOIN
        ibis.message_pattern ON (ibis.dicominput_status.messagepattern_id = ibis.message_pattern.id)
            LEFT JOIN
        ibis.study ON (ibis.study.serial_number = ibis.dicom_input.serial_number
            AND ibis.study.encrypted_siuid = ibis.dicom_input.encrypted_siuid)
            LEFT JOIN
        (SELECT
            ibis.customer.serial_number AS serial_number,
                ibis.customer.customer_name AS customer_name
        FROM
            ibis.customer
        WHERE
            ibis.customer.is_last = 1) custo ON (ibis.dicom_input.serial_number = custo.serial_number)
            LEFT JOIN
        (SELECT
            ibis.application_entity.serial_number AS serial_number,
                ibis.application_entity.aet AS aet,
                ibis.application_entity.sdm_key AS sdm_key,
                ibis.application_entity.device_type AS device_type,
                ibis.integration_mode.integration_mode AS integration_mode
        FROM
            ibis.application_entity
        LEFT JOIN ibis.ae_integration ON (ibis.application_entity.id = ibis.ae_integration.applicationentity_id)
        LEFT JOIN ibis.integration_mode ON (ibis.ae_integration.integrationmode_id = ibis.integration_mode.id)
        WHERE
            ibis.application_entity.is_last = 1) ae ON (ibis.dicom_input.aet = ae.aet
            AND ibis.dicom_input.serial_number = ae.serial_number)
    WHERE
        ibis.dicom_input.datetime_first_received >= CURDATE() - INTERVAL 15 DAY
;

-- This view expose @ study level incoming pattern test
CREATE OR REPLACE VIEW v_study_dicom_last15days AS
    SELECT
        CAST(GROUP_CONCAT(DISTINCT dicom_input.id) AS CHAR (255)) AS dicom_id,
        dicom_input.serial_number,
        COUNT(DISTINCT dicom_input.aet) AS nb_aet_producer,
        CAST(GROUP_CONCAT(DISTINCT dicom_input.aet) AS CHAR (255)) AS aet_producer,
        dicom_input.encrypted_siuid,
        MIN(dicom_input.datetime_first_received) AS datetime_first_received,
        MAX(dicom_input.datetime_last_received) AS datetime_last_received,
        AVG(IF(dicominput_status.status_id = 1,
            1,
            0)) AS dicompattern_success_rate
    FROM
        dicom_input
            LEFT JOIN
        dicominput_status ON dicom_input.id = dicominput_status.dicominput_id
    WHERE
        dicom_input.datetime_first_received >= CURDATE() - INTERVAL + 15 DAY
    GROUP BY dicom_input.serial_number , dicom_input.encrypted_siuid;


-- This view expose @ study level dosimetric test
CREATE OR REPLACE VIEW v_study_dosimetric_last15days AS
    SELECT
        CAST(GROUP_CONCAT(DISTINCT study.id) AS CHAR (255)) AS study_id,
        study.serial_number,
        CAST(GROUP_CONCAT(DISTINCT study.aet) AS CHAR (255)) AS aet,
        MIN(study.start_date) AS study_date,
        CAST(GROUP_CONCAT(DISTINCT study.type) AS CHAR (255)) AS modality,
        study.local_study_id AS local_study_id,
        study.encrypted_siuid,
        AVG(IF(dosimetric.status_id = 1, 1, 0)) AS dosimetric_success_rate
    FROM
        study
            JOIN
        dosimetric ON dosimetric.study_id = study.id
    WHERE
        study.start_date >= CURDATE() - INTERVAL + 15 DAY
    GROUP BY study.encrypted_siuid , study.local_study_id;


-- This view expose @ study level ctlog connectivity test
CREATE OR REPLACE VIEW v_ctlog_last15days AS
    SELECT
        ct_log_pattern.id AS ctlog_id,
        ct_log_pattern.serial_number,
        ct_log_pattern.aet,
        ct_log_pattern.local_study_id,
        ct_log_pattern.datetime_first_insert,
        status.status,
        rational.rational,
        integration_mode.integration_mode AS inferred_integration_mode
    FROM
        ctlogpattern_status
            JOIN
        ct_log_pattern ON (ct_log_pattern.id = ctlogpattern_status.ctlogpattern_id)
            LEFT JOIN
        integration_mode ON (integration_mode.id = ctlogpattern_status.infered_integrationmode_id)
            JOIN
        status ON (ctlogpattern_status.status_id = status.id)
            JOIN
        rational ON (rational.id = ctlogpattern_status.rational_id)
    WHERE
        ct_log_pattern.datetime_first_insert >= CURDATE() - INTERVAL + 15 DAY;


-- This view expose an aggregate view @ study level, an aggregate data source with ctlog, dosimetric and pattern
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
    LEFT JOIN ae_integration ON application_entity.id = ae_integration.applicationentity_id
    LEFT JOIN integration_mode ON ae_integration.integrationmode_id = integration_mode.id
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
    LEFT JOIN ae_integration ON application_entity.id = ae_integration.applicationentity_id
    LEFT JOIN integration_mode ON ae_integration.integrationmode_id = integration_mode.id
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

-- This view expose all know aet with info
CREATE OR REPLACE VIEW v_aet AS
    SELECT
        customer.serial_number AS serial_number,
        application_entity.aet AS aet,
        application_entity.common_name AS common_name,
        application_entity.local_ae_id AS local_ae_id,
        application_entity.contrast AS contrast,
        application_entity.ftp_connection_type AS ftp_connection_type,
        application_entity.deleted AS deleted,
        application_entity.device AS device,
        application_entity.device_type AS modality,
        application_entity.sdm_key AS sdm_key,
        application_entity.manufacturer AS manufacturer,
        application_entity.software_version AS software_version,
        application_entity.system_id AS aet_system_id,
        application_entity.station_name AS station_name,
        application_entity.mpps_series_duplicate_removal AS mpps_series_duplicate_removal,
        application_entity.modality_worklist_enabled AS modality_worklist_enabled,
        application_entity.data_type AS data_type,
        application_entity.translator AS translator,
        application_entity.image_translator AS image_translator,
        application_entity.secondary_data_type AS secondary_data_type,
        application_entity.secondary_translator AS secondary_translator,
        application_entity.secondary_image_translator AS secondary_image_translator,
        application_entity.tertiary_data_type AS tertiary_data_type,
        application_entity.tertiary_translator AS tertiary_translator,
        application_entity.tertiary_image_translator AS tertiary_image_translator,
        application_entity.last_updated AS ae_last_update,
        integration_mode.integration_mode AS integration_mode,
        IFNULL(ftp_connection.enabled, 0) AS ftp_enabled,
        ftp_connection.ip_adress AS ip_adress,
        ftp_connection.ftp_secured AS ftp_secured,
        customer.customer_name AS customer_name,
        customer.project_type AS project_type,
        customer.project_manager AS project_manager,
        customer.application_specialist AS application_specialist,
        customer.country AS country,
        customer.pole AS pole,
        customer.dosewatch_version AS dosewatch_version,
        customer.serphylink_version AS serphylink_version,
        customer.dictionary_version AS dictionary_version,
        customer.state AS state,
        customer.town AS town,
        customer.latitude AS latitude,
        customer.longitude AS longitude,
        customer.product_type AS product_type,
        customer.system_id AS customer_system_id,
        customer.installation_date AS customer_installation_date,
        customer.last_update AS customer_last_update,
        customer.is_active AS is_active,
        customer.worklist_enabled AS worklist_enabled,
        customer.decommissioning AS decommissioning,
        customer.iguana_channels AS iguana_channels
    FROM
        customer
            LEFT JOIN
        application_entity ON (customer.serial_number = application_entity.serial_number)
            LEFT JOIN
        ae_integration ON (application_entity.id = ae_integration.applicationentity_id)
            LEFT JOIN
        integration_mode ON (ae_integration.integrationmode_id = integration_mode.id)
            LEFT JOIN
        ae_ftp ON (application_entity.id = ae_ftp.applicationentity_id)
            LEFT JOIN
        ftp_connection ON (ae_ftp.ftpconnection_id = ftp_connection.id)
    WHERE
        customer.project_type = 'PRODUCTION'
            AND customer.is_last = 1
            AND (application_entity.is_last = 1 OR application_entity.is_last is NULL)
;

-- This view expose aet monitored with high level status
CREATE OR REPLACE VIEW v_devices_overview AS
With last_monitoring as (
SELECT
    data.agg_study_data_source.serial_number AS serial_number,
    data.agg_study_data_source.aet as aet,
    COALESCE(data.agg_study_data_source.aet,
            data.agg_study_data_source.dicom_aet_producer) AS agg_aet,
    COUNT(DISTINCT data.agg_study_data_source.local_study_id) AS number_of_examinations,
    MAX(study_date) AS last_study_date,
    MAX(dicom_last_received) AS last_received_dicom,
    MAX(ctlog_first_insert) AS last_received_ctlog,
    ROUND(AVG(dosimetric_success_rate), 3) AS avg_dosimetric_success_rate,
    ROUND(AVG(dicompattern_success_rate), 3) AS avg_dicom_success_rate,
    AVG(IF(data.agg_study_data_source.ctlog_status = 'OK',
        1,
        0)) AS ctlog_success_rate,
    CASE
        WHEN
            AVG(IFNULL(data.agg_study_data_source.dosimetric_success_rate,
                    0)) >= 0.85
        THEN
            'No issue'
        WHEN
            (AVG(IFNULL(data.agg_study_data_source.dosimetric_success_rate,
                    0)) < 0.85
                AND AVG(IFNULL(data.agg_study_data_source.dosimetric_success_rate,
                    0)) >= 0.35)
        THEN
            'Unusual issue'
        WHEN
            AVG(IFNULL(data.agg_study_data_source.dosimetric_success_rate,
                    0)) < 0.35
        THEN
            'Recurrent issue'
    END AS dosi_test,
    CASE
        WHEN
            GREATEST(AVG(IFNULL(data.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF(data.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) >= 0.85
        THEN
            'No issue'
        WHEN
            (GREATEST(AVG(IFNULL(data.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF(data.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) < 0.85
                AND GREATEST(AVG(IFNULL(data.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF(data.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) >= 0.35)
        THEN
            'Unusual issue'
        WHEN
            GREATEST(AVG(IFNULL(data.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF(data.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) < 0.35
        THEN
            'Recurrent issue'
    END AS dicom_test,
    CASE
        WHEN
            AVG(IFNULL(data.agg_study_data_source.dosimetric_success_rate,
                    0)) >= 0.85
        THEN
            'No dosimetric issue'
        WHEN
            (AVG(IFNULL(data.agg_study_data_source.dosimetric_success_rate,
                    0)) < 0.85
                AND AVG(IFNULL(data.agg_study_data_source.dosimetric_success_rate,
                    0)) >= 0.35)
        THEN
            'Unusual dosimetric issue'
        WHEN
            AVG(IFNULL(data.agg_study_data_source.dosimetric_success_rate,
                    0)) < 0.35
        THEN
            'Recurrent dosimetric issue'
    END AS dosi_test_verbose,
    CASE
        WHEN
            GREATEST(AVG(IFNULL(data.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF(data.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) >= 0.85
        THEN
            'No connectivity issue'
        WHEN
            (GREATEST(AVG(IFNULL(data.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF(data.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) < 0.85
                AND GREATEST(AVG(IFNULL(data.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF(data.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) >= 0.35)
        THEN
            'Unusual connectivity issue'
        WHEN
            GREATEST(AVG(IFNULL(data.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF(data.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) < 0.35
        THEN
            'Recurrent connectivity issue'
    END AS dicom_test_verbose,
    CONCAT(COALESCE(data.agg_study_data_source.aet,
                    data.agg_study_data_source.dicom_aet_producer),
            ' (',
            COUNT(DISTINCT data.agg_study_data_source.local_study_id),
            ')') AS aet_plus_exams
FROM
    data.agg_study_data_source
GROUP BY serial_number , COALESCE(data.agg_study_data_source.aet,
        data.agg_study_data_source.dicom_aet_producer))

SELECT
	COALESCE(v_aet.serial_number, last_monitoring.serial_number) as serial_number,
    v_aet.customer_name as customer_name,
    COALESCE(v_aet.aet, last_monitoring.aet) as aet,
    v_aet.common_name,
    v_aet.local_ae_id as local_ae_id,
    v_aet.contrast as contrast,
    v_aet.ftp_connection_type as ftp_connection_type,
    v_aet.deleted as deleted,
    v_aet.device as device,
    v_aet.modality as modality,
    v_aet.sdm_key as sdm_key,
    v_aet.manufacturer as manufacturer,
    v_aet.software_version as software_version,
    v_aet.aet_system_id as aet_system_id,
    v_aet.station_name as station_name,
    v_aet.mpps_series_duplicate_removal as mpps_series_duplicate_removal,
    v_aet.modality_worklist_enabled as modality_worklist_enabled,
    v_aet.data_type as data_type,
    v_aet.translator as translator,
    v_aet.image_translator as image_translator,
    v_aet.secondary_data_type as secondary_data_type,
    v_aet.secondary_translator as secondary_translator,
    v_aet.secondary_image_translator as secondary_image_translator,
    v_aet.tertiary_data_type as tertiary_data_type,
    v_aet.tertiary_translator as tertiary_translator,
    v_aet.tertiary_image_translator as tertiary_image_translator,
    v_aet.ae_last_update as ae_last_update,
    v_aet.integration_mode as integration_mode,
    v_aet.ftp_enabled as ftp_enabled,
    v_aet.ftp_secured as ftp_secured,
    v_aet.project_type as project_type,
    v_aet.project_manager as project_manager,
    v_aet.application_specialist as application_specialist,
    v_aet.country as country,
    v_aet.pole as pole,
    v_aet.dosewatch_version as dosewatch_version,
    v_aet.dictionary_version as dictionary_version,
    v_aet.state as state,
    v_aet.town as town,
    v_aet.latitude as latitude,
    v_aet.longitude as longitude,
    v_aet.product_type as product_type,
    v_aet.customer_system_id as customer_system_id,
    v_aet.customer_installation_date as customer_installation_date,
    v_aet.customer_last_update as customer_last_update,
    v_aet.is_active as is_active,
    v_aet.worklist_enabled as worklist_enabled,
    v_aet.decommissioning as decommissioning,
    v_aet.iguana_channels as iguana_channels,
    IF(last_monitoring.aet IS NULL, 0, 1) as has_active_monitoring,
    last_monitoring.agg_aet as agg_aet,
    last_monitoring.number_of_examinations as number_of_examinations,
    last_monitoring.last_study_date as last_study_date,
    last_monitoring.last_received_dicom as last_received_dicom,
    last_monitoring.last_received_ctlog as last_received_ctlog,
    last_monitoring.avg_dosimetric_success_rate as avg_dosimetric_success_rate,
    last_monitoring.avg_dicom_success_rate as avg_dicom_success_rate,
    last_monitoring.ctlog_success_rate as ctlog_success_rate,
    last_monitoring.dosi_test as dosi_test,
    last_monitoring.dicom_test as dicom_test,
    last_monitoring.dosi_test_verbose as dosi_test_verbose,
    last_monitoring.dicom_test_verbose as dicom_test_verbose,
    last_monitoring.aet_plus_exams as aet_plus_exams
FROM
    v_aet
        LEFT OUTER JOIN
    last_monitoring ON (v_aet.serial_number = last_monitoring.serial_number
        AND v_aet.aet = last_monitoring.aet)
WHERE
	v_aet.aet IS NOT NULL
UNION ALL
SELECT
--     COALESCE(v_aet.serial_number, last_monitoring.serial_number) as serial_number,
    last_monitoring.serial_number as serial_number,
    v_aet.customer_name as customer_name,
--     COALESCE(v_aet.aet, last_monitoring.aet) as aet,
    last_monitoring.aet as aet,
    v_aet.common_name,
    v_aet.local_ae_id as local_ae_id,
    v_aet.contrast as contrast,
    v_aet.ftp_connection_type as ftp_connection_type,
    v_aet.deleted as deleted,
    v_aet.device as device,
    v_aet.modality as modality,
    v_aet.sdm_key as sdm_key,
    v_aet.manufacturer as manufacturer,
    v_aet.software_version as software_version,
    v_aet.aet_system_id as aet_system_id,
    v_aet.station_name as station_name,
    v_aet.mpps_series_duplicate_removal as mpps_series_duplicate_removal,
    v_aet.modality_worklist_enabled as modality_worklist_enabled,
    v_aet.data_type as data_type,
    v_aet.translator as translator,
    v_aet.image_translator as image_translator,
    v_aet.secondary_data_type as secondary_data_type,
    v_aet.secondary_translator as secondary_translator,
    v_aet.secondary_image_translator as secondary_image_translator,
    v_aet.tertiary_data_type as tertiary_data_type,
    v_aet.tertiary_translator as tertiary_translator,
    v_aet.tertiary_image_translator as tertiary_image_translator,
    v_aet.ae_last_update as ae_last_update,
    v_aet.integration_mode as integration_mode,
    v_aet.ftp_enabled as ftp_enabled,
    v_aet.ftp_secured as ftp_secured,
    v_aet.project_type as project_type,
    v_aet.project_manager as project_manager,
    v_aet.application_specialist as application_specialist,
    v_aet.country as country,
    v_aet.pole as pole,
    v_aet.dosewatch_version as dosewatch_version,
    v_aet.dictionary_version as dictionary_version,
    v_aet.state as state,
    v_aet.town as town,
    v_aet.latitude as latitude,
    v_aet.longitude as longitude,
    v_aet.product_type as product_type,
    v_aet.customer_system_id as customer_system_id,
    v_aet.customer_installation_date as customer_installation_date,
    v_aet.customer_last_update as customer_last_update,
    v_aet.is_active as is_active,
    v_aet.worklist_enabled as worklist_enabled,
    v_aet.decommissioning as decommissioning,
    v_aet.iguana_channels as iguana_channels,
    IF(last_monitoring.aet IS NULL, 0, 1) as has_active_monitoring,
    last_monitoring.agg_aet as agg_aet,
    last_monitoring.number_of_examinations as number_of_examinations,
    last_monitoring.last_study_date as last_study_date,
    last_monitoring.last_received_dicom as last_received_dicom,
    last_monitoring.last_received_ctlog as last_received_ctlog,
    last_monitoring.avg_dosimetric_success_rate as avg_dosimetric_success_rate,
    last_monitoring.avg_dicom_success_rate as avg_dicom_success_rate,
    last_monitoring.ctlog_success_rate as ctlog_success_rate,
    last_monitoring.dosi_test as dosi_test,
    last_monitoring.dicom_test as dicom_test,
    last_monitoring.dosi_test_verbose as dosi_test_verbose,
    last_monitoring.dicom_test_verbose as dicom_test_verbose,
    last_monitoring.aet_plus_exams as aet_plus_exams
FROM
    v_aet
        RIGHT OUTER JOIN
    last_monitoring ON v_aet.serial_number = last_monitoring.serial_number
WHERE
    v_aet.aet IS NULL
;



-- This view expose innova log device status
CREATE OR REPLACE VIEW v_innova_log_status AS
    SELECT
        ibis.innova_log_pull.serial_number AS serial_number,
        custo.customer_name AS customer_name,
        ae.sdm_key AS sdm_key,
        ae.integration_mode AS integration_mode,
        ibis.innova_log_pull.aet AS aet,
        ibis.innova_log_pull.datetime_last_pull AS datetime_last_pull,
        ibis.innova_log_pull.nb_fail AS nb_fail,
        ibis.innova_log_pull.measure_date AS measure_date,
        TO_DAYS(ibis.innova_log_pull.measure_date) - TO_DAYS(ibis.innova_log_pull.datetime_last_pull) AS day_since_last_pull,
        ibis.status.status AS status,
        ibis.rational.rational AS rational
    FROM
        ibis.innovalogpull_status
            JOIN
        ibis.innova_log_pull ON (ibis.innovalogpull_status.innovalog_id = ibis.innova_log_pull.id)
            JOIN
        ibis.rational ON (ibis.rational.id = ibis.innovalogpull_status.rational_id)
            JOIN
        ibis.status ON (ibis.status.id = ibis.innovalogpull_status.status_id)
            LEFT JOIN
        (SELECT
            ibis.customer.serial_number AS serial_number,
                ibis.customer.customer_name AS customer_name
        FROM
            ibis.customer
        WHERE
            ibis.customer.is_last = 1) custo ON (ibis.innova_log_pull.serial_number = custo.serial_number)
            LEFT JOIN
        (SELECT
            ibis.application_entity.serial_number AS serial_number,
                ibis.application_entity.aet AS aet,
                ibis.application_entity.sdm_key AS sdm_key,
                ibis.integration_mode.integration_mode AS integration_mode
        FROM
            ibis.application_entity
        LEFT JOIN ibis.ae_integration ON (ibis.application_entity.id = ibis.ae_integration.applicationentity_id)
        LEFT JOIN ibis.integration_mode ON (ibis.ae_integration.integrationmode_id = ibis.integration_mode.id)
        WHERE
            ibis.application_entity.is_last = 1) ae ON (ibis.innova_log_pull.aet = ae.aet
            AND ibis.innova_log_pull.serial_number = ae.serial_number)
;
