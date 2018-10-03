USE ibis;


-- Procedure to store view into table
-- This stored procedure update materialized view for agg_study_data_source

DELIMITER //
CREATE OR REPLACE PROCEDURE update_agg_study()
BEGIN
    START TRANSACTION;
    	DROP INDEX IF EXISTS idx_aggstudy_ds ON data.agg_study_data_source;
    	DROP INDEX IF EXISTS idx_aggstudy_ds_sdmkey ON data.agg_study_data_source;
    	DELETE FROM data.agg_study_data_source;
    	INSERT INTO data.agg_study_data_source SELECT
    	                                            serial_number,
    	                                            customer_name,
    	                                            pole,
    	                                            country,
    	                                            sdm_key,
    	                                            integration_mode,
    	                                            encrypted_siuid,
    	                                            local_study_id,
    	                                            modality,
    	                                            study_date,
    	                                            dicom_first_received,
    	                                            dicom_last_received,
    	                                            ctlog_first_insert,
    	                                            aet,
    	                                            nb_dicom_aet_producer,
    	                                            dicom_aet_producer,
    	                                            dosimetric_success_rate,
    	                                            dicompattern_success_rate,
    	                                            ctlog_status,
    	                                            ctlog_obs,
    	                                            inferred_integration_mode
    	                                         FROM v_agg_study_data_source;
    	CREATE INDEX idx_aggstudy_ds ON data.agg_study_data_source (serial_number, aet, dicom_aet_producer);
    	CREATE INDEX idx_aggstudy_ds_sdmkey ON data.agg_study_data_source (sdm_key);
    COMMIT;
END ;
//

DELIMITER ;


-- This stored procedure update materialized view for pattern_last_15days
DELIMITER //
CREATE OR REPLACE PROCEDURE update_pattern()
BEGIN
    START TRANSACTION;
        DROP INDEX IF EXISTS idx_pattern ON data.pattern_last_15days;
        DELETE FROM data.pattern_last_15days;
        INSERT INTO data.pattern_last_15days SELECT
                                                    serial_number,
                                                    encrypted_siuid,
                                                    customer_name,
                                                    aet,
                                                    sdm_key,
                                                    modality,
                                                    integration_mode,
                                                    study_date,
                                                    datetime_first_received,
                                                    prod_command,
                                                    prod_sop_class,
                                                    prod_message_type,
                                                    prod_series_number,
                                                    prod_study_status,
                                                    prod_message_status,
                                                    message_type,
                                                    status,
                                                    rational
                                                FROM
                                                    v_pattern_last15days;
        CREATE INDEX idx_pattern ON data.pattern_last_15days (serial_number, aet);
    COMMIT;
END ; //

DELIMITER ;


-- This stored procedure update materialized view for dosimetric_last_15days
DELIMITER //
CREATE OR REPLACE PROCEDURE update_dosimetric()
BEGIN
    START TRANSACTION;
        DROP INDEX IF EXISTS idx_dosimetric ON data.dosimetric_last_15days;
        DELETE FROM data.dosimetric_last_15days;
        INSERT INTO data.dosimetric_last_15days SELECT
                                                    serial_number,
                                                    pole,
                                                    customer_name,
                                                    aet,
                                                    sdm_key,
                                                    modality,
                                                    integration_mode,
                                                    study_date,
                                                    study_id,
                                                    dosimetric_type,
                                                    dosimetric_diff,
                                                    status,
                                                    rational
                                                FROM
                                                    v_dosimetric_last15days;
        CREATE INDEX idx_dosimetric ON data.dosimetric_last_15days (serial_number, aet);
    COMMIT;
END ; //

DELIMITER ;


-- This stored procedure update materialized view for ctlog_last_15days
DELIMITER //
CREATE OR REPLACE PROCEDURE update_ctlog()
BEGIN
    START TRANSACTION;
        DROP INDEX IF EXISTS idx_ctlog ON data.ctlog_last_15days;
        DELETE FROM data.ctlog_last_15days;
        INSERT INTO data.ctlog_last_15days SELECT
                                                    serial_number,
                                                    aet,
                                                    local_study_id,
                                                    datetime_first_insert,
                                                    status,
                                                    rational,
                                                    inferred_integration_mode
                                              FROM
                                                    v_ctlog_last15days;
        CREATE INDEX idx_ctlog ON data.ctlog_last_15days (serial_number, aet);
    COMMIT;
END ; //

DELIMITER ;



-- This stored procedure update materialized view for device_overview
DELIMITER //
CREATE OR REPLACE PROCEDURE update_devicessoverview()
BEGIN
    START TRANSACTION;
        DROP INDEX IF EXISTS idx_devices_overview ON data.devices_overview;
        DELETE FROM data.devices_overview;
        INSERT INTO data.devices_overview SELECT *
                                           FROM
                                                v_devices_overview;
        CREATE INDEX idx_devices_overview ON data.devices_overview (serial_number, agg_aet);
    COMMIT;
END ; //

DELIMITER ;

-- This procedure call all proc that store view into table
DELIMITER //
CREATE OR REPLACE PROCEDURE update_all_stored_view()
BEGIN
    CALL update_ctlog();
    CALL update_pattern();
    CALL update_dosimetric();
    CALL update_agg_study();
    CALL update_devicesoverview();
END ; //

DELIMITER ;


-- This procedure store into a table data that make match between all device, dw version, integration mode
-- & expected message type
DELIMITER //
CREATE OR REPLACE PROCEDURE update_im_mt()
BEGIN
	START TRANSACTION;
	    DROP INDEX IF EXISTS idx_integrationmode_messagetypes ON integrationmode_messagetypes;
	    DELETE FROM integrationmode_messagetypes;
		INSERT INTO integrationmode_messagetypes
			SELECT
				sub.supported_device_id as sdm_key,
				sub.dosewatch_version as dw_v,
				sub.integration_mode_id as im_id,
				integration_mode.integration_mode as im,
				sub.message_type,
				integration_mode.modality
			FROM
				integration_mode
				JOIN
					(SELECT
						cl.integration_mode_id, mp.message_type, mp.id, cl.supported_device_id, cl.dosewatch_version
					FROM
						connectivity_list cl, connectivity_pattern cp, message_pattern mp
					WHERE
					 	cp.connectivity_list_id=cl.id AND cp.message_pattern_id=mp.id
					GROUP BY
						cl.integration_mode_id, mp.message_type, cl.supported_device_id, cl.dosewatch_version) AS sub
				ON integration_mode.id = sub.integration_mode_id;
		CREATE INDEX idx_integrationmode_messagetypes ON integrationmode_messagetypes (sdm_key, dw_v, im_id, im, message_type, modality);
	COMMIT;
END ; //

DELIMITER ;
