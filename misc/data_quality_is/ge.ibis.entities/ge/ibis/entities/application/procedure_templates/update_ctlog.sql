-- This stored procedure update materialized view for ctlog_last_15days
CREATE OR REPLACE PROCEDURE update_ctlog()
BEGIN
    START TRANSACTION;
        DROP INDEX IF EXISTS idx_ctlog ON {DATA_SCHEMA}.ctlog_last_15days;
        DELETE FROM {DATA_SCHEMA}.ctlog_last_15days;
        INSERT INTO {DATA_SCHEMA}.ctlog_last_15days (
            serial_number, aet, local_study_id, datetime_first_insert,
            `status`, rational, inferred_integration_mode)
        SELECT
                                                    serial_number,
                                                    aet,
                                                    local_study_id,
                                                    datetime_first_insert,
                                                    status,
                                                    rational,
                                                    inferred_integration_mode
                                              FROM
                                                    v_ctlog_last15days;
        CREATE INDEX idx_ctlog ON {DATA_SCHEMA}.ctlog_last_15days (
            serial_number, aet);
    COMMIT;
END ;