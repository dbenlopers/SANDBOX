CREATE OR REPLACE PROCEDURE update_agg_study()
BEGIN
    START TRANSACTION;
    	DROP INDEX IF EXISTS idx_aggstudy_ds ON {DATA_SCHEMA}.agg_study_data_source;
    	DROP INDEX IF EXISTS idx_aggstudy_ds_sdmkey ON {DATA_SCHEMA}.agg_study_data_source;
    	DELETE FROM {DATA_SCHEMA}.agg_study_data_source;
    	INSERT INTO {DATA_SCHEMA}.agg_study_data_source (
			serial_number, customer_name, pole, country, sdm_key,
			integration_mode, encrypted_siuid, local_study_id, modality,
			study_date, dicom_first_received, dicom_last_received,
			ctlog_first_insert, aet, nb_dicom_aet_producer, dicom_aet_producer,
			dosimetric_success_rate, dicompattern_success_rate, ctlog_status,
			ctlog_obs, inferred_integration_mode)
		SELECT
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
    	CREATE INDEX idx_aggstudy_ds ON {DATA_SCHEMA}.agg_study_data_source (serial_number, aet, dicom_aet_producer);
    	CREATE INDEX idx_aggstudy_ds_sdmkey ON {DATA_SCHEMA}.agg_study_data_source (sdm_key);
    COMMIT;
END ;