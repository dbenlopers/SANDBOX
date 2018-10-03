-- This stored procedure update materialized view for dosimetric_last_15days
CREATE OR REPLACE PROCEDURE update_dosimetric()
BEGIN
    START TRANSACTION;
        DROP INDEX IF EXISTS idx_dosimetric ON {DATA_SCHEMA}.dosimetric_last_15days;
        DELETE FROM {DATA_SCHEMA}.dosimetric_last_15days;
        INSERT INTO {DATA_SCHEMA}.dosimetric_last_15days (
            serial_number, pole, customer_name, aet, sdm_key, modality,
            integration_mode, study_date, study_id, dosimetric_type,
            dosimetric_diff, `status`, rational)
        SELECT
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
        CREATE INDEX idx_dosimetric ON {DATA_SCHEMA}.dosimetric_last_15days (serial_number, aet);
    COMMIT;
END ;