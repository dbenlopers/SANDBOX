CREATE OR REPLACE VIEW v_aet AS
    SELECT
        customer.serial_number AS serial_number,
        application_entity.aet AS aet,
        application_entity.common_name AS common_name,
        application_entity.local_ae_id AS local_ae_id,
        application_entity.contrast AS contrast,
        application_entity.ftp_connection_type AS ftp_connection_type,
        application_entity.deleted AS deleted,
        application_entity.device AS device,
        application_entity.device_type AS modality,
        application_entity.sdm_key AS sdm_key,
        application_entity.manufacturer AS manufacturer,
        application_entity.software_version AS software_version,
        application_entity.system_id AS aet_system_id,
        application_entity.station_name AS station_name,
        application_entity.mpps_series_duplicate_removal AS mpps_series_duplicate_removal,
        application_entity.modality_worklist_enabled AS modality_worklist_enabled,
        application_entity.data_type AS data_type,
        application_entity.translator AS translator,
        application_entity.image_translator AS image_translator,
        application_entity.secondary_data_type AS secondary_data_type,
        application_entity.secondary_translator AS secondary_translator,
        application_entity.secondary_image_translator AS secondary_image_translator,
        application_entity.tertiary_data_type AS tertiary_data_type,
        application_entity.tertiary_translator AS tertiary_translator,
        application_entity.tertiary_image_translator AS tertiary_image_translator,
        application_entity.last_updated AS ae_last_update,
        integration_mode.integration_mode AS integration_mode,
        IFNULL(ftp_connection.enabled, 0) AS ftp_enabled,
        ftp_connection.ip_address AS ip_adress,
        ftp_connection.ftp_secured AS ftp_secured,
        customer.customer_name AS customer_name,
        customer.project_type AS project_type,
        customer.project_manager AS project_manager,
        customer.application_specialist AS application_specialist,
        customer.country AS country,
        customer.pole AS pole,
        customer.dosewatch_version AS dosewatch_version,
        customer.serphylink_version AS serphylink_version,
        customer.dictionary_version AS dictionary_version,
        customer.state AS state,
        customer.town AS town,
        customer.latitude AS latitude,
        customer.longitude AS longitude,
        customer.product_type AS product_type,
        customer.system_id AS customer_system_id,
        customer.installation_date AS customer_installation_date,
        customer.last_update AS customer_last_update,
        customer.is_active AS is_active,
        customer.worklist_enabled AS worklist_enabled,
        customer.decommissioning AS decommissioning,
        customer.iguana_channels AS iguana_channels
    FROM customer
    LEFT JOIN application_entity
    ON (customer.serial_number = application_entity.serial_number)
    LEFT JOIN ae_integration
    ON (application_entity.id = ae_integration.application_entity_id)
    LEFT JOIN integration_mode
    ON (ae_integration.integration_mode_id = integration_mode.id)
    LEFT JOIN ae_ftp
    ON (application_entity.id = ae_ftp.application_entity_id)
    LEFT JOIN ftp_connection
    ON (ae_ftp.ftp_connection_id = ftp_connection.id)
    WHERE customer.project_type = 'PRODUCTION'
    AND customer.is_last = 1
    AND (application_entity.is_last = 1 OR application_entity.is_last is NULL)
;