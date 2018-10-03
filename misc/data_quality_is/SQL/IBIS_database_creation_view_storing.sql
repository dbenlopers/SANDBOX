CREATE OR REPLACE DATABASE `data`
	CHARACTER SET = utf8
	COLLATE = utf8_general_ci;
USE `data`;

-- table for materialized view

CREATE OR REPLACE TABLE `agg_study_data_source` (
    `serial_number` VARCHAR(50),
    `customer_name` VARCHAR(255),
    `pole` VARCHAR(50),
    `country` VARCHAR(50),
    `sdm_key` INT,
    `integration_mode` VARCHAR(100),
    `encrypted_siuid` VARCHAR(255),
    `local_study_id` INT,
    `modality` VARCHAR(10),
    `study_date` DATETIME,
    `dicom_first_received` DATETIME,
    `dicom_last_received` DATETIME,
    `ctlog_first_insert` DATETIME,
    `aet` VARCHAR(100),
    `nb_dicom_aet_producer` INT,
    `dicom_aet_producer` VARCHAR(150),
    `dosimetric_success_rate` FLOAT,
    `dicompattern_success_rate` FLOAT,
    `ctlog_status` VARCHAR(4),
    `ctlog_obs` VARCHAR(15),
    `inferred_integration_mode` VARCHAR(100)
);
-- CREATE OR REPLACE INDEX `idx_aggstudy_ds` ON `agg_study_data_source` (`serial_number`, `aet`, `dicom_aet_producer`);
-- CREATE OR REPLACE INDEX `idx_aggstudy_ds_sdmkey` ON `agg_study_data_source` (`sdm_key`);


CREATE OR REPLACE TABLE `pattern_last_15days` (
    `serial_number` VARCHAR(50),
    `encrypted_siuid` VARCHAR(255),
    `customer_name` VARCHAR(255),
    `aet` VARCHAR(100),
    `sdm_key` INT,
    `modality` VARCHAR(10),
    `integration_mode` VARCHAR(100),
    `study_date` DATETIME,
    `datetime_first_received` DATETIME,
    `prod_command` VARCHAR(20),
    `prod_sop_class` VARCHAR(100),
    `prod_message_type` VARCHAR(25),
    `prod_series_number` VARCHAR(20),
    `prod_study_status` VARCHAR(20),
    `prod_message_status` VARCHAR(1),
    `message_type` VARCHAR(50),
    `status` VARCHAR(4),
    `rational` VARCHAR(15)
);
--
 CREATE OR REPLACE INDEX `idx_pattern` ON `pattern_last_15days` (`serial_number`, `aet`);

CREATE OR REPLACE TABLE `dosimetric_last_15days` (
    `serial_number` VARCHAR(50),
    `pole` VARCHAR(10),
    `customer_name` VARCHAR(255),
    `aet` VARCHAR(100),
    `sdm_key` INT,
    `modality` VARCHAR(30),
    `integration_mode` VARCHAR(100),
    `study_date` DATETIME,
    `study_id` INT,
    `dosimetric_type` VARCHAR(25),
    `dosimetric_diff` DOUBLE,
    `status` VARCHAR(4),
    `rational` VARCHAR(15)
);
-- CREATE OR REPLACE INDEX `idx_dosimetric` ON `dosimetric_last_15days` (`serial_number`, `aet`);


CREATE OR REPLACE TABLE `ctlog_last_15days` (
    `serial_number` VARCHAR(50),
    `aet` VARCHAR(100),
    `local_study_id` INT,
    `datetime_first_insert` DATETIME,
    `status` VARCHAR(4),
    `rational` VARCHAR(15),
    `inferred_integration_mode` VARCHAR(100)
);
-- CREATE OR REPLACE INDEX `idx_ctlog` ON `ctlog_last_15days` (`serial_number`, `aet`);


CREATE OR REPLACE TABLE `devices_overview` (
    `serial_number` VARCHAR(50),
    `customer_name` VARCHAR(255),
    `aet` VARCHAR(100),
    `common_name` VARCHAR(100),
    `local_ae_id` INT(11),
    `contrast` TINYINT(4),
    `ftp_connection_type` VARCHAR(50),
    `deleted` TINYINT(4),
    `device` VARCHAR(100),
    `modality` VARCHAR(10),
    `sdm_key` INT(11),
    `manufacturer` VARCHAR(100),
    `software_version` VARCHAR(255),
    `aet_system_id` VARCHAR(50),
    `station_name` VARCHAR(100),
    `mpps_series_duplicate_removal` TINYINT(4),
    `modality_worklist_enabled` TINYINT(4),
    `data_type` VARCHAR(50),
    `translator` VARCHAR(70),
    `image_translator` VARCHAR(70),
    `secondary_data_type` VARCHAR(50),
    `secondary_translator` VARCHAR(70),
    `secondary_image_translator` VARCHAR(70),
    `tertiary_data_type` VARCHAR(50),
    `tertiary_translator` VARCHAR(70),
    `tertiary_image_translator` VARCHAR(70),
    `ae_last_update` DATETIME,
    `integration_mode` VARCHAR(100),
    `ftp_enabled` INT(11),
    `ftp_secured` TINYINT(4),
    `project_type` VARCHAR(40),
    `project_manager` VARCHAR(50),
    `application_specialist` VARCHAR(50),
    `country` VARCHAR(40),
    `pole` VARCHAR(10),
    `dosewatch_version` VARCHAR(50),
    `dictionary_version` VARCHAR(40),
    `state` VARCHAR(50),
    `town` VARCHAR(50),
    `latitude` FLOAT,
    `longitude` FLOAT,
    `product_type` VARCHAR(20),
    `customer_system_id` VARCHAR(150),
    `customer_installation_date` DATETIME,
    `customer_last_update` DATETIME,
    `is_active` TINYINT(4),
    `worklist_enabled` TINYINT(4),
    `decommissioning` TINYINT(4),
    `iguana_channels` TINYINT(4),
    `has_active_monitoring` BIGINT(20),
    `agg_aet` VARCHAR(250),
    `number_of_examinations` BIGINT(21),
    `last_study_date` DATETIME,
    `last_received_dicom` DATETIME,
    `last_received_ctlog` DATETIME,
    `avg_dosimetric_success_rate` DOUBLE(20 , 3 ),
    `avg_dicom_success_rate` DOUBLE(20 , 3 ),
    `ctlog_success_rate` DECIMAL(54),
    `dosi_test` VARCHAR(15),
    `dicom_test` VARCHAR(15),
    `dosi_test_verbose` VARCHAR(26),
    `dicom_test_verbose` VARCHAR(28),
    `aet_plus_exams` VARCHAR(274)
);
-- CREATE OR REPLACE INDEX `idx_devices_overview` ON `devices_overview` (`serial_number`);