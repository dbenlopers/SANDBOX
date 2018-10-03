-- This stored procedure update materialized view for pattern_last_15days
CREATE OR REPLACE PROCEDURE update_pattern()
BEGIN
    START TRANSACTION;
        DROP INDEX IF EXISTS idx_pattern ON {DATA_SCHEMA}.pattern_last_15days;
        DELETE FROM {DATA_SCHEMA}.pattern_last_15days;
        INSERT INTO {DATA_SCHEMA}.pattern_last_15days (
            serial_number, encrypted_siuid, customer_name, aet, sdm_key,
            modality, integration_mode, study_date, datetime_first_received,
            prod_command, prod_sop_class, prod_message_type,
            prod_series_number, prod_study_status, prod_message_status,
            message_type, `status`, rational)
        
        SELECT
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
        CREATE INDEX idx_pattern ON {DATA_SCHEMA}.pattern_last_15days (serial_number, aet);
    COMMIT;
END ;