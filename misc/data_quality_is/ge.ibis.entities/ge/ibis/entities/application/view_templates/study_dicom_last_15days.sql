CREATE OR REPLACE VIEW v_study_dicom_last15days AS
    SELECT
        CAST(GROUP_CONCAT(DISTINCT dicom_input.id) AS CHAR (255)) AS dicom_id,
        dicom_input.serial_number,
        COUNT(DISTINCT dicom_input.aet) AS nb_aet_producer,
        CAST(GROUP_CONCAT(DISTINCT dicom_input.aet) AS CHAR (255)) AS aet_producer,
        dicom_input.encrypted_siuid,
        MIN(dicom_input.datetime_first_received) AS datetime_first_received,
        MAX(dicom_input.datetime_last_received) AS datetime_last_received,
        AVG(IF(dicom_input_status.status_id = 1,
            1,
            0)) AS dicompattern_success_rate
    FROM
        dicom_input
            LEFT JOIN
        dicom_input_status ON dicom_input.id = dicom_input_status.dicom_input_id
    WHERE
        dicom_input.datetime_first_received >= (CURDATE() - INTERVAL 15 DAY)
    GROUP BY dicom_input.serial_number , dicom_input.encrypted_siuid;