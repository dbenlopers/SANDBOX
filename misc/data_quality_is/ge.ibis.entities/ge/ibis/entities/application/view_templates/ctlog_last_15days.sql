CREATE OR REPLACE VIEW v_ctlog_last15days AS
    SELECT
        ct_log_pattern.id AS ctlog_id,
        ct_log_pattern.serial_number,
        ct_log_pattern.aet,
        ct_log_pattern.local_study_id,
        ct_log_pattern.datetime_first_insert,
        `status`.`status`,
        rationale.rationale as rational,
        integration_mode.integration_mode AS inferred_integration_mode
    FROM
        ct_log_pattern_status
    JOIN ct_log_pattern
    ON (ct_log_pattern.id = ct_log_pattern_status.ct_log_pattern_id)
    LEFT JOIN integration_mode
    ON (integration_mode.id = ct_log_pattern_status.infered_integration_mode_id)
    JOIN `status`
    ON (ct_log_pattern_status.status_id = `status`.id)
    JOIN rationale
    ON (rationale.id = ct_log_pattern_status.rationale_id)
    WHERE
        ct_log_pattern.datetime_first_insert >= (CURDATE() - INTERVAL 15 DAY);