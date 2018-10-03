CREATE OR REPLACE VIEW v_dosimetric_last15days AS
    SELECT
        study.serial_number AS serial_number,
        custo.pole AS pole,
        custo.customer_name AS customer_name,
        study.aet AS aet,
        ae.sdm_key AS sdm_key,
        study.type AS modality,
        ae.integration_mode AS integration_mode,
        study.start_date AS study_date,
        study.id AS study_id,
        dosimetric.type AS dosimetric_type,
        dosimetric.value AS dosimetric_diff,
        `status`.`status` AS `status`,
        rationale.rationale AS rational
    FROM study
    JOIN dosimetric ON (dosimetric.study_id = study.id)
    JOIN `status` ON (`status`.id = dosimetric.status_id)
    JOIN rationale ON (rationale.id = dosimetric.rationale_id)
    LEFT JOIN
        (SELECT
            customer.serial_number AS serial_number,
            customer.customer_name AS customer_name,
            customer.pole AS pole
        FROM
            customer
        WHERE
            customer.is_last = 1) AS custo
    ON (study.serial_number = custo.serial_number)
    LEFT JOIN
        (SELECT
            application_entity.serial_number AS serial_number,
            application_entity.aet AS aet,
            application_entity.sdm_key AS sdm_key,
            integration_mode.integration_mode AS integration_mode
        FROM
            (
                (application_entity
                 LEFT JOIN ae_integration
                 ON  (application_entity.id = ae_integration.application_entity_id)
                )
                LEFT JOIN integration_mode
                ON (ae_integration.integration_mode_id = integration_mode.id)
            )
        WHERE
            application_entity.is_last = 1) ae ON (study.aet = ae.aet
            AND study.serial_number = ae.serial_number)
    WHERE
        study.start_date >= (CURDATE() - INTERVAL 15 DAY)
;