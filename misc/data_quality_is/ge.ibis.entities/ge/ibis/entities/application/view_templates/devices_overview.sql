CREATE OR REPLACE VIEW v_devices_overview AS
With last_monitoring as (
SELECT
    {DATA_SCHEMA}.agg_study_data_source.serial_number AS serial_number,
    {DATA_SCHEMA}.agg_study_data_source.aet as aet,
    COALESCE({DATA_SCHEMA}.agg_study_data_source.aet,
            {DATA_SCHEMA}.agg_study_data_source.dicom_aet_producer) AS agg_aet,
    COUNT(DISTINCT {DATA_SCHEMA}.agg_study_data_source.local_study_id) AS number_of_examinations,
    MAX(study_date) AS last_study_date,
    MAX(dicom_last_received) AS last_received_dicom,
    MAX(ctlog_first_insert) AS last_received_ctlog,
    ROUND(AVG(dosimetric_success_rate), 3) AS avg_dosimetric_success_rate,
    ROUND(AVG(dicompattern_success_rate), 3) AS avg_dicom_success_rate,
    AVG(IF({DATA_SCHEMA}.agg_study_data_source.ctlog_status = 'OK',
        1,
        0)) AS ctlog_success_rate,
    CASE
        WHEN
            AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dosimetric_success_rate,
                    0)) >= 0.85
        THEN
            'No issue'
        WHEN
            (AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dosimetric_success_rate,
                    0)) < 0.85
                AND AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dosimetric_success_rate,
                    0)) >= 0.35)
        THEN
            'Unusual issue'
        WHEN
            AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dosimetric_success_rate,
                    0)) < 0.35
        THEN
            'Recurrent issue'
    END AS dosi_test,
    CASE
        WHEN
            GREATEST(AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF({DATA_SCHEMA}.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) >= 0.85
        THEN
            'No issue'
        WHEN
            (GREATEST(AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF({DATA_SCHEMA}.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) < 0.85
                AND GREATEST(AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF({DATA_SCHEMA}.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) >= 0.35)
        THEN
            'Unusual issue'
        WHEN
            GREATEST(AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF({DATA_SCHEMA}.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) < 0.35
        THEN
            'Recurrent issue'
    END AS dicom_test,
    CASE
        WHEN
            AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dosimetric_success_rate,
                    0)) >= 0.85
        THEN
            'No dosimetric issue'
        WHEN
            (AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dosimetric_success_rate,
                    0)) < 0.85
                AND AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dosimetric_success_rate,
                    0)) >= 0.35)
        THEN
            'Unusual dosimetric issue'
        WHEN
            AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dosimetric_success_rate,
                    0)) < 0.35
        THEN
            'Recurrent dosimetric issue'
    END AS dosi_test_verbose,
    CASE
        WHEN
            GREATEST(AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF({DATA_SCHEMA}.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) >= 0.85
        THEN
            'No connectivity issue'
        WHEN
            (GREATEST(AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF({DATA_SCHEMA}.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) < 0.85
                AND GREATEST(AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF({DATA_SCHEMA}.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) >= 0.35)
        THEN
            'Unusual connectivity issue'
        WHEN
            GREATEST(AVG(IFNULL({DATA_SCHEMA}.agg_study_data_source.dicompattern_success_rate,
                            0)),
                    AVG(IF({DATA_SCHEMA}.agg_study_data_source.ctlog_status = 'OK',
                        1,
                        0))) < 0.35
        THEN
            'Recurrent connectivity issue'
    END AS dicom_test_verbose,
    CONCAT(COALESCE({DATA_SCHEMA}.agg_study_data_source.aet,
                    {DATA_SCHEMA}.agg_study_data_source.dicom_aet_producer),
            ' (',
            COUNT(DISTINCT {DATA_SCHEMA}.agg_study_data_source.local_study_id),
            ')') AS aet_plus_exams
FROM
    {DATA_SCHEMA}.agg_study_data_source
GROUP BY serial_number , COALESCE({DATA_SCHEMA}.agg_study_data_source.aet,
        {DATA_SCHEMA}.agg_study_data_source.dicom_aet_producer))

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