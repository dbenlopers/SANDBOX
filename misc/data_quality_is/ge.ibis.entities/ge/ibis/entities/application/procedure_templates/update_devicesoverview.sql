-- This stored procedure update materialized view for device_overview
CREATE OR REPLACE PROCEDURE update_devicesoverview()
BEGIN
    START TRANSACTION;
        DROP INDEX IF EXISTS idx_devices_overview ON {DATA_SCHEMA}.devices_overview;
        DELETE FROM {DATA_SCHEMA}.devices_overview;
        INSERT INTO {DATA_SCHEMA}.devices_overview (
            `serial_number`, `customer_name`, `aet`, `common_name`, 
            `local_ae_id`, `contrast`, `ftp_connection_type`, `deleted`,
            `device`, `modality`, `sdm_key`, `manufacturer`,
            `software_version`, `aet_system_id`, `station_name`,
            `mpps_series_duplicate_removal`, `modality_worklist_enabled`,
            `data_type`, `translator`, `image_translator`,
            `secondary_data_type`, `secondary_translator`,
            `secondary_image_translator`, `tertiary_data_type`,
            `tertiary_translator`, `tertiary_image_translator`,
            `ae_last_update`, `integration_mode`, `ftp_enabled`,
            `ftp_secured`, `project_type`, `project_manager`,
            `application_specialist`, `country`, `pole`, `dosewatch_version`,
            `dictionary_version`, `state`, `town`, `latitude`, `longitude`,
            `product_type`, `customer_system_id`,
            `customer_installation_date`, `customer_last_update`,
            `is_active`, `worklist_enabled`, `decommissioning`,
            `iguana_channels`, `has_active_monitoring`, `agg_aet`,
            `number_of_examinations`, `last_study_date`,
            `last_received_dicom`, `last_received_ctlog`,
            `avg_dosimetric_success_rate`, `avg_dicom_success_rate`,
            `ctlog_success_rate`, `dosi_test`, `dicom_test`,
            `dosi_test_verbose`, `dicom_test_verbose`, `aet_plus_exams`)
        SELECT * FROM v_devices_overview;
        CREATE INDEX idx_devices_overview ON {DATA_SCHEMA}.devices_overview (serial_number, agg_aet);
    COMMIT;
END ;