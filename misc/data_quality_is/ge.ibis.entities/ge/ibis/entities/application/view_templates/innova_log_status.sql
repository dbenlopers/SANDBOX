CREATE OR REPLACE VIEW v_innova_log_status AS
    SELECT
        innova_log_pull.serial_number AS serial_number,
        custo.customer_name AS customer_name,
        ae.sdm_key AS sdm_key,
        ae.integration_mode AS integration_mode,
        innova_log_pull.aet AS aet,
        innova_log_pull.datetime_last_pull AS datetime_last_pull,
        innova_log_pull.nb_fail AS nb_fail,
        innova_log_pull.measure_date AS measure_date,
        TO_DAYS(innova_log_pull.measure_date) - TO_DAYS(innova_log_pull.datetime_last_pull) AS day_since_last_pull,
        status.status AS status,
        rationale.rationale AS rational
    FROM innova_log_pull_status
    JOIN innova_log_pull
    ON (innova_log_pull_status.innova_log_id = innova_log_pull.id)
    JOIN rationale
    ON (rationale.id = innova_log_pull_status.rationale_id)
    JOIN status
    ON (status.id = innova_log_pull_status.status_id)
    LEFT JOIN
        (SELECT
            customer.serial_number AS serial_number,
            customer.customer_name AS customer_name
        FROM customer
        WHERE customer.is_last = 1) AS custo
    ON (innova_log_pull.serial_number = custo.serial_number)
    LEFT JOIN
        (SELECT
            application_entity.serial_number AS serial_number,
                application_entity.aet AS aet,
                application_entity.sdm_key AS sdm_key,
                integration_mode.integration_mode AS integration_mode
        FROM
            application_entity
        LEFT JOIN ae_integration ON (application_entity.id = ae_integration.application_entity_id)
        LEFT JOIN integration_mode ON (ae_integration.integration_mode_id = integration_mode.id)
        WHERE application_entity.is_last = 1) AS ae
    ON (innova_log_pull.aet = ae.aet
        AND innova_log_pull.serial_number = ae.serial_number)
;