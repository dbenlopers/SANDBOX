CREATE OR REPLACE VIEW v_study_dosimetric_last15days AS
    SELECT
        CAST(GROUP_CONCAT(DISTINCT study.id) AS CHAR (255)) AS study_id,
        study.serial_number,
        CAST(GROUP_CONCAT(DISTINCT study.aet) AS CHAR (255)) AS aet,
        MIN(study.start_date) AS study_date,
        CAST(GROUP_CONCAT(DISTINCT study.type) AS CHAR (255)) AS modality,
        study.local_study_id AS local_study_id,
        study.encrypted_siuid,
        AVG(IF(dosimetric.status_id = 1, 1, 0)) AS dosimetric_success_rate
    FROM
        study
    JOIN 
        dosimetric ON dosimetric.study_id = study.id
    WHERE
        study.start_date >= (CURDATE() - INTERVAL 15 DAY)
    GROUP BY study.encrypted_siuid , study.local_study_id;