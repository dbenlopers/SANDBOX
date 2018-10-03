CREATE OR REPLACE DATABASE `ibis` 
	CHARACTER SET = utf8
	COLLATE = utf8_general_ci;
USE `ibis`;

-- Table definition

CREATE OR REPLACE TABLE `customer`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`is_active` BOOL,
   `last_update` DATETIME,
   `revision_number` INT(10),
   `serial_number` VARCHAR(50) NOT NULL,
   `dosewatch_version` VARCHAR(50),
   `serphylink_version` VARCHAR(50),
   `customer_name` VARCHAR(255),
   `project_type` VARCHAR(40),
   `is_identified_agreement` BOOL,
   `is_important` BOOL,
   `project_manager` VARCHAR(50),
   `application_specialist` VARCHAR(50),
   `dictionary_version` VARCHAR(40),
   `country` VARCHAR(40),
   `pole` VARCHAR(10),
   `worklist_enabled` BOOL,
   `decommissioning` BOOL,
   `iguana_channels` BOOL,
   `installation_date` DATETIME,
   `state` VARCHAR(50),
   `system_id` VARCHAR(150),
   `town` VARCHAR(50),
   `location` POINT,
   `deal_type` VARCHAR(50),
   `product_type` VARCHAR(20),
   `is_last` BOOL NOT NULL,
   `is_monitored` BOOL NOT NULL DEFAULT 0
);

CREATE OR REPLACE TABLE `custom_dictionary`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   `local_id` INT,
   `code` VARCHAR(100),
   `description` VARCHAR(255)
);

CREATE OR REPLACE TABLE `customer_dictionary`(
	`customer_id` INT NOT NULL,
   `customdictionary_id` INT NOT NULL,
   PRIMARY KEY (`customer_id`, `customdictionary_id`),
   CONSTRAINT `FK_customerdictionary_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
	CONSTRAINT `FK_customerdictionary_custom_dictionary_id` FOREIGN KEY (`customdictionary_id`) REFERENCES `custom_dictionary` (`id`)
);

CREATE OR REPLACE TABLE `workaround` (
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`name` VARCHAR(255)
);

CREATE OR REPLACE TABLE `customer_workaround` (
	`workaround_id` INT NOT NULL,
	`customer_id` INT NOT NULL,
	PRIMARY KEY (`workaround_id`, `customer_id`),
	CONSTRAINT `FK_customerworkaround_workaround_id` FOREIGN KEY (`workaround_id`) REFERENCES `workaround` (`ID`),
	CONSTRAINT `FK_customerworkaround_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`)
);

CREATE OR REPLACE TABLE `ftp_connection`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   `enabled` BOOL,
   `active_mode_enabled` BOOL,
   `ftp_secured` BOOL,
   `ip_adress` VARCHAR(45),
   `pass_phrase` VARCHAR(100),
   `port` INT(11),
   `private_key` VARCHAR(100),
   `data` MEDIUMBLOB,
   CHECK (`data` IS NULL OR JSON_VALID(`data`)),
   `hash` VARCHAR(50)
);

CREATE OR REPLACE TABLE `supported_device`(
	`id` INT PRIMARY KEY NOT NULL,
   `is_deleted` BOOL,
   `manufacturer` VARCHAR(100),
   `name` VARCHAR(100),
   `type` VARCHAR(100),
   `characteristics` VARCHAR(255),
   `alternate_name` VARCHAR(255),
   `last_update` DATETIME
);

CREATE OR REPLACE TABLE `application_entity`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   `local_ae_id` INT,
   `aet` VARCHAR(100),
   `common_name` VARCHAR(100),
   `contrast` BOOL,
   `ftp_connection_type` VARCHAR(50),
   `data_type` VARCHAR(50),
   `deleted` BOOL,
   `device` VARCHAR(100),
   `device_type` VARCHAR(10),
   `has_integration_request` BOOL,
   `ignored_sr_numbers` VARCHAR(255),
   `image_translator` VARCHAR(70),
   `ip` VARCHAR(45),
   `last_updated` DATETIME,
   `licensed` BOOL,
   `manufacturer` VARCHAR(100),
   `message_type` VARCHAR(50),
   `modality_worklist_enabled` BOOL,
   `mpps_series_duplicate_removal` BOOL,
   `port` INT(11),
   `ris_ae_name` VARCHAR(50),
   `screenshot_translator` VARCHAR(70),
   `sdm_key` INT NOT NULL,
   `secondary_data_type` VARCHAR(50),
   `secondary_image_translator` VARCHAR(70),
   `secondary_translator` VARCHAR(70),
   `serial_number` VARCHAR(50) NOT NULL,
   `software_version` VARCHAR(255),
   `station_name` VARCHAR(100),
   `system_id` VARCHAR(50),
   `tertiary_data_type` VARCHAR(50),
   `tertiary_image_translator` VARCHAR(70),
   `tertiary_translator` VARCHAR(70),
   `translator` VARCHAR(70),
   `update_type` VARCHAR(50),
   `is_last` BOOL NOT NULL,
   `status` VARCHAR(1) NOT NULL DEFAULT 'N'
);

CREATE OR REPLACE TABLE `ae_ftp`(
	`applicationentity_id` INT NOT NULL,
   `ftpconnection_id` INT NOT NULL,
   PRIMARY KEY (`applicationentity_id`, `ftpconnection_id`),
   CONSTRAINT `FK_aeftp_applicationentity_id` FOREIGN KEY (`applicationentity_id`) REFERENCES `application_entity` (`id`),
   CONSTRAINT `FK_aeftp_ftpconection_id` FOREIGN KEY (`ftpconnection_id`) REFERENCES `ftp_connection` (`id`)
);

CREATE OR REPLACE TABLE `integration_mode` (
 	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
 	`integration_mode` VARCHAR(100),
 	`modality` VARCHAR(20)
);

CREATE OR REPLACE TABLE `ae_integration` (
	`applicationentity_id` INT NOT NULL,
	`integrationmode_id` INT NOT NULL,
	PRIMARY KEY (`applicationentity_id`, `integrationmode_id`),
	CONSTRAINT `FK_aeintegration_applicationentity_id` FOREIGN KEY (`applicationentity_id`) REFERENCES `application_entity` (`id`),
	CONSTRAINT `FK_aeintegration_integrationmode_id` FOREIGN KEY (`integrationmode_id`) REFERENCES `integration_mode` (`id`)
);

CREATE OR REPLACE TABLE `translator_config`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`allow_mpps_series_duplicate_removal` bool,
   `contrast` BOOL,
   `data_type` VARCHAR(20),
   `translator_id` INT,
   `translator_default` BOOL,
   `translator_code` VARCHAR(70),
   `deleted` BOOL,
   `device_name` VARCHAR(255),
   `device_version` VARCHAR(50),
   `dosewatch_lower_version_bound` VARCHAR(10),
   `dosewatch_upper_version_bound` VARCHAR(10),
   `integration_mode` VARCHAR(70),
   `manufacturer` VARCHAR(100),
   `modality` VARCHAR(20),
   `image_translator_id` INT,
   `image_translator_default` BOOL,
   `image_translator_code` VARCHAR(70),
   `sdm_key` INT(11),
   `secondary_data_type` VARCHAR(30),
   `secondary_translator_id` INT,
   `secondary_translator_default` BOOL,
   `secondary_translator_code` VARCHAR(70),
   `tertiary_data_type` VARCHAR(30),
   `tertiary_translator_id` INT,
   `tertiary_translator_default` BOOL,
   `tertiary_translator_code` VARCHAR(70),
   `secondary_image_translator_id` INT,
   `secondary_image_translator_default` BOOL,
   `secondary_image_translator_code` VARCHAR(70),
   `tertiary_image_translator_id` INT,
   `tertiary_image_translator_default` BOOL,
   `tertiary_image_translator_code` VARCHAR(70),
   `update_date` DATETIME,
   CONSTRAINT `FK_translator_sdmkey` FOREIGN KEY (`sdm_key`) REFERENCES `supported_device` (`id`)
);

CREATE OR REPLACE TABLE `device_version_requirement`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`value` VARCHAR(255),
	`rule` VARCHAR(20),
	`relation` VARCHAR(20)
);

CREATE OR REPLACE TABLE `translator_config_device_version_requirement`(
	`translatorconfig_id` INT NOT NULL,
	`deviceversionrequirements_id` INT NOT NULL,
	PRIMARY KEY (`translatorconfig_id`, `deviceversionrequirements_id`),
	CONSTRAINT `FK_TransConfdevReqt_translatorconfig_id` FOREIGN KEY (`translatorconfig_id`) REFERENCES `translator_config` (`id`) ON DELETE CASCADE,
	CONSTRAINT `FK_TransConfdevReq_deviceVersReq_ID` FOREIGN KEY (`deviceversionrequirements_id`) REFERENCES `device_version_requirement` (`id`)
);

CREATE OR REPLACE TABLE `study`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   `type` VARCHAR(30),
   `measure_date` DATETIME,
   `serial_number` VARCHAR(50),
   `aet` VARCHAR(100),
   `encrypted_siuid` VARCHAR(255),
   `local_study_id` INT,
   `software_version` VARCHAR(255),
   `start_date` DATETIME,
   `sdm_key` INT,
   `translator_code` VARCHAR(70),
   `data` MEDIUMBLOB,
   CHECK (`data` IS NULL OR JSON_VALID(`data`)),
   `image_translator_code` VARCHAR(70),
   `status` VARCHAR(1) NOT NULL DEFAULT 'N',
   `reception_date` DATETIME(3)
);

CREATE OR REPLACE TABLE `dicom_pattern`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`software_version` VARCHAR(255),
	`message_command` VARCHAR(20),
	`sop_class` VARCHAR(100),
	`message_type` VARCHAR(25),
	`series_number` VARCHAR(20),
	`study_status` VARCHAR(20),
	`message_status` VARCHAR(1),
	`hash` VARCHAR(50)
);

CREATE OR REPLACE TABLE `dicom_input`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`measure_date` DATETIME,
	`serial_number` VARCHAR(50),
	`aet` VARCHAR(100),
	`station_name` VARCHAR(50),
	`manufacturers_model_name` VARCHAR(50),
	`encrypted_siuid` VARCHAR(255),
	`datetime_first_received` DATETIME,
	`datetime_last_received` DATETIME,
	`status` VARCHAR(1) NOT NULL DEFAULT 'N',
	`reception_date` DATETIME(3)
);

CREATE OR REPLACE TABLE `dicom_input_pattern`(
	`dicominput_id` INT NOT NULL,
    `dicompattern_id` INT NOT NULL,
    PRIMARY KEY (`dicominput_id`, `dicompattern_id`),
    CONSTRAINT `FK_dicomInPat_dicominput_id` FOREIGN KEY (`dicominput_id`) REFERENCES `dicom_input` (`id`) ON DELETE CASCADE,
    CONSTRAINT `FK_dicomInPat_dicompattern_id` FOREIGN KEY (`dicompattern_id`) REFERENCES `dicom_pattern` (`id`),
	`total_number_messages` INT
);

CREATE OR REPLACE TABLE `innova_log_pull`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`measure_date` DATETIME,
	`serial_number` VARCHAR(50),
	`aet` VARCHAR(100),
	`local_ae_id` INT,
	`nb_fail` SMALLINT UNSIGNED,
	`datetime_last_pull` DATETIME,
	`datetime_first_fail` DATETIME,
	`datetime_last_fail` DATETIME,
	`status` VARCHAR(1) NOT NULL DEFAULT 'N',
	`reception_date` DATETIME(3),
	CONSTRAINT `Uni_innova_sn_aet` UNIQUE (`serial_number`, `aet`)
);

CREATE OR REPLACE TABLE `ct_log_pattern`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`measure_date` DATETIME,
	`serial_number` VARCHAR(50),
	`local_ae_id` INT,
	`aet` VARCHAR(100),
	`parent_message_key` INT,
	`exam_number` INT,
	`local_study_id` INT,
	`patient_key` INT,
	`datetime_first_insert` DATETIME,
	`number_of_files` SMALLINT UNSIGNED,
	`message_status` SMALLINT UNSIGNED,
	`number_of_message_type` SMALLINT UNSIGNED,
	`sum_exam_proto` SMALLINT UNSIGNED,
	`sum_protocol_xml` SMALLINT UNSIGNED,
	`sum_scan_request` SMALLINT UNSIGNED,
	`sum_localizer` SMALLINT UNSIGNED,
	`sum_image` SMALLINT UNSIGNED,
	`sum_rdsr` SMALLINT UNSIGNED,
	`sum_screenshot` SMALLINT UNSIGNED,
	`sum_sr` SMALLINT UNSIGNED,
	`sum_unknow` SMALLINT UNSIGNED,
	`sum_screenshot_contrast` SMALLINT UNSIGNED,
	`sum_prodiag_exam` SMALLINT UNSIGNED,
	`sum_prodiag` SMALLINT UNSIGNED,
	`sum_auto_ma` SMALLINT UNSIGNED,
	`sum_wrong_file` SMALLINT UNSIGNED,
	`status` VARCHAR(1) NOT NULL DEFAULT 'N',
	`reception_date` DATETIME(3)
);

CREATE OR REPLACE TABLE `rational`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`rational` VARCHAR(15) NOT NULL
);

CREATE OR REPLACE TABLE `status`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`status` VARCHAR(4) NOT NULL
);

CREATE OR REPLACE TABLE `dosimetric`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`study_id` INT NOT NULL,
	`type` VARCHAR(25) NOT NULL,
	`status_id` INT NOT NULL,
	`rational_id` INT NOT NULL,
	`value` DOUBLE,
	CONSTRAINT `FK_dosimetric_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
	CONSTRAINT `FK_dosimetric_rational` FOREIGN KEY (`rational_id`) REFERENCES `rational` (`id`),
	CONSTRAINT `FK_dosimetruc_study_id` FOREIGN KEY (`study_id`) REFERENCES `study` (`id`) ON DELETE CASCADE
);

CREATE OR REPLACE TABLE `connectivity_list`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`supported_device_id` INT,
	`dosewatch_version` VARCHAR(50),
	`integration_mode_id` INT NOT NULL,
	`device_version` VARCHAR(255),
	`revision_number` INT,
	`priority` INT,
	`difficulty` VARCHAR(20),
	`last_update` DATETIME,
	CONSTRAINT `FK_connectlist_sdm` FOREIGN KEY (`supported_device_id`) REFERENCES `supported_device` (`id`),
	CONSTRAINT `FK_connectlist_intmode` FOREIGN KEY (`integration_mode_id`) REFERENCES `integration_mode` (`id`)
);

CREATE OR REPLACE TABLE `message_pattern`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`message_type` VARCHAR(50) UNIQUE
);

CREATE OR REPLACE TABLE `dwfunctionality`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`functionality` VARCHAR(100) UNIQUE
);

CREATE OR REPLACE TABLE `connectivity_pattern`(
	`connectivity_list_id` INT NOT NULL,
	`message_pattern_id` INT NOT NULL,
	CONSTRAINT `FK_conectpatter_cnlistid` FOREIGN KEY (`connectivity_list_id`) REFERENCES `connectivity_list` (`id`) ON DELETE CASCADE,
	CONSTRAINT `FK_conectpatter_mespatid` FOREIGN KEY (`message_pattern_id`) REFERENCES `message_pattern` (`id`)
);

CREATE OR REPLACE TABLE `connectivity_functionality`(
	`connectivity_list_id` INT NOT NULL,
	`dwfunctionality_id` INT NOT NULL,
	CONSTRAINT `FK_conectfunc_cnlistid` FOREIGN KEY (`connectivity_list_id`) REFERENCES `connectivity_list` (`id`) ON DELETE CASCADE,
	CONSTRAINT `FK_conectfunc_dwfuncid` FOREIGN KEY (`dwfunctionality_id`) REFERENCES `dwfunctionality` (`id`)
);

CREATE OR REPLACE TABLE `innovalogpull_status`(
	`innovalog_id` INT PRIMARY KEY NOT NULL,
	`status_id` INT NOT NULL,
	`rational_id` INT NOT NULL,
	CONSTRAINT `FK_innovalogstat_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
	CONSTRAINT `FK_innovalogstat_rational` FOREIGN KEY (`rational_id`) REFERENCES `rational` (`id`),
	CONSTRAINT `FK_innovalogstat_innova_id` FOREIGN KEY (`innovalog_id`) REFERENCES `innova_log_pull` (`id`) ON DELETE CASCADE
);

CREATE OR REPLACE TABLE `ctlogpattern_status`(
    `id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`ctlogpattern_id` INT NOT NULL,
	`status_id` INT NOT NULL,
	`rational_id` INT NOT NULL,
	`infered_integrationmode_id` INT,
	CONSTRAINT `FK_ctlogstat_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
	CONSTRAINT `FK_ctlogstat_rational` FOREIGN KEY (`rational_id`) REFERENCES `rational` (`id`),
	CONSTRAINT `FK_ctlogstat_ctlog_id` FOREIGN KEY (`ctlogpattern_id`) REFERENCES `ct_log_pattern` (`id`) ON DELETE CASCADE
);

CREATE OR REPLACE TABLE `dicominput_status`(
	`id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	`dicominput_id` INT NOT NULL,
	`messagepattern_id` INT,
	`dicompattern_id` INT,
	`status_id` INT NOT NULL,
	`rational_id` INT NOT NULL,
	CONSTRAINT `FK_dicominstat_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
	CONSTRAINT `FK_dicominstat_rational` FOREIGN KEY (`rational_id`) REFERENCES `rational` (`id`),
	CONSTRAINT `FK_dicominstat_dicominput_id` FOREIGN KEY (`dicominput_id`) REFERENCES `dicom_input` (`id`) ON DELETE CASCADE
);

CREATE OR REPLACE `translatorconfig_status`(
    `ae_id` INT NOT NULL,
    `rational_id` INT NOT NULL,
	CONSTRAINT `FK_transconf_rational` FOREIGN KEY (`rational_id`) REFERENCES `rational` (`id`),
    CONSTRAINT `FK_transconf_ae_id` FOREIGN KEY (`ae_id`) REFERENCES `application_entity` (`id`) ON DELETE CASCADE
);



CREATE OR REPLACE TABLE `integrationmode_messagetypes`(
    `sdm_key` INT,
    `dw_v` VARCHAR(50),
    `im_id` INT,
    `im` VARCHAR(100),
    `message_type` VARCHAR(50),
    `modality` VARCHAR(20)
);


CREATE OR REPLACE TABLE `specific_translator`(
    `id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    `specific_translator_id` INT(11) NOT NULL,
    `code` VARCHAR(255),
    `description` VARCHAR(255),
    `datatype` VARCHAR(10),
    `is_image_translator` VARCHAR(1),
    `modality` VARCHAR(10),
    `parent_translator_key` INT(11),
    `series_number` VARCHAR(100),
    `constructor` VARCHAR(100),
    `model` VARCHAR(100),
    `software_release` VARCHAR(255),
    `calculator_name` VARCHAR(255),
    `version` VARCHAR(255),
    `is_study_updator` VARCHAR(1) DEFAULT 'N',
    `computing_in_progress` BOOL DEFAULT 0,
    `deleting_study` BOOL DEFAULT 0
);

CREATE OR REPLACE TABLE `specific_translator_element`(
    `id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    `specific_translator_element_id` INT(11) NOT NULL,
    `translator_key` INT(11),
    `dictionary_element_key` INT(11),
    `element_name` VARCHAR(255),
    `formula` VARCHAR(255),
    `formula_separator` CHAR(1) DEFAULT ',',
    `cumulated_value` TINYINT(4) DEFAULT 0,
    `reference_element` VARCHAR(255),
    `control_element` INT(11),
    `reference_element_level` INT(11),
    `is_ref_relative_path` CHAR(1),
    `override_vr` CHAR(2)
);



-- Create index

CREATE OR REPLACE INDEX `idx_customer` ON `customer` (`last_update`, `revision_number`, `serial_number`, `customer_name`, `is_last`);
CREATE OR REPLACE INDEX `idx_connectivity_list` ON `connectivity_list` (`supported_device_id`, `dosewatch_version`, `device_version`, `integration_mode_id`);
CREATE OR REPLACE INDEX `idx_dosimetric` ON `dosimetric` (`study_id`, `type`);
CREATE OR REPLACE INDEX `idx_hash_dicompattern` ON `dicom_pattern` (`hash`);
CREATE OR REPLACE INDEX `idx_study` ON `study` (`type`, `sdm_key`, `serial_number`);
CREATE OR REPLACE INDEX `idx_start` ON `study` (`start_date`);
CREATE OR REPLACE INDEX `idx_sn_aet` ON `study` (`aet`, `serial_number`);
CREATE OR REPLACE INDEX `idx_sn` ON `study` (`serial_number`);
CREATE OR REPLACE INDEX `idx_siuid` ON `study` (`encrypted_siuid`);
CREATE OR REPLACE INDEX `idx_sn_start_date` ON `study` (`serial_number`, `start_date`);
CREATE OR REPLACE INDEX `idx_translator` ON `translator_config` (`sdm_key`, `data_type`, `translator_code`, `device_version`, `integration_mode`, `image_translator_code`, `secondary_data_type`, `secondary_translator_code`);
CREATE OR REPLACE INDEX `idx_ae_sr` on `application_entity` (`serial_number`, `local_ae_id`, `is_last`);
CREATE OR REPLACE INDEX `idx_sn_islast` ON `application_entity` (`serial_number`, `is_last`);
CREATE OR REPLACE INDEX `idx_sn_aet_islast` ON `application_entity` (`serial_number`, `aet`, `is_last`);
CREATE OR REPLACE INDEX `idx_sn_stationname_islast` ON `application_entity` (`serial_number`, `station_name`, `is_last`);
CREATE OR REPLACE INDEX `idx_sn_islast` ON `customer` (`serial_number`, `is_last`);
CREATE OR REPLACE INDEX `idx_supporteddevice` ON `supported_device` (`manufacturer`, `name`, `type`, `id`);
CREATE OR REPLACE INDEX `idx_im` on `integration_mode` (`integration_mode`, `modality`);
CREATE OR REPLACE INDEX `idx_ftpco` on `ftp_connection` (`hash`);
CREATE OR REPLACE INDEX `idx_customdict` ON `custom_dictionary` (`local_id`, `code`, `description`);
CREATE OR REPLACE INDEX `idx_integrationmode_messagetypes` ON
			`integrationmode_messagetypes` (`sdm_key`, `dw_v`, `im_id`, `im`, `message_type`, `modality`);

-- populate status & rational needed for test status

INSERT INTO `status` (`id`, `status`) VALUES
	(1, 'OK'),
	(2, 'NOK'),
	(3, "NA");
	

INSERT INTO `rational` (`id`, `rational`) VALUES
	(1, 'NFF'),
	(2, 'ENHANCEMENT'),
	(3, 'LIMITED'),
	(4, 'WARNING'),
	(5, 'ERROR'),
	(6, 'CRITICAL'),
	(7, 'MISSING'),
	(8, 'EXTRA'),
	(9, 'NOIM'),
	(10, 'CL_UNKNOW'),
	(11, 'NONSENSE'),
	(12, 'AE_UNKNOW');
