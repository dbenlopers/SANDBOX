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
		(
            SELECT application_entity.serial_number as sn, application_entity.aet as ae_aet, integration_mode.integration_mode
            FROM application_entity
            LEFT JOIN ae_integration ON application_entity.id = ae_integration.application_entity_id
            LEFT JOIN integration_mode ON ae_integration.integration_mode_id = integration_mode.id
            WHERE
                application_entity.is_last = 1
        ) AS ae ON (study.aet = ae.ae_aet AND study.serial_number = ae.sn)
	WHERE
		study.start_date >= (CURDATE() - INTERVAL 21 DAY))
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