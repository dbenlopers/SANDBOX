-- This procedure store into a table data that make match between all device, dw version, integration mode
-- & expected message type
CREATE OR REPLACE PROCEDURE update_im_mt()
BEGIN
	START TRANSACTION;
	    DROP INDEX IF EXISTS idx_integration_mode_message_type ON integration_mode_message_type;
	    DELETE FROM integration_mode_message_type;
		INSERT INTO integration_mode_message_type (sdm_key, dw_v, im_id, im, message_type, modality)
			SELECT
				sub.supported_device_id as sdm_key,
				sub.dosewatch_version as dw_v,
				sub.integration_mode_id as im_id,
				integration_mode.integration_mode as im,
				sub.message_type,
				integration_mode.modality
			FROM
				integration_mode
				JOIN
					(SELECT
						cl.integration_mode_id, mp.message_type, mp.id, cl.supported_device_id, cl.dosewatch_version
					FROM
						connectivity_list cl, connectivity_pattern cp, message_pattern mp
					WHERE
					 	cp.connectivity_list_id=cl.id AND cp.message_pattern_id=mp.id
					GROUP BY
						cl.integration_mode_id, mp.message_type, cl.supported_device_id, cl.dosewatch_version) AS sub
				ON integration_mode.id = sub.integration_mode_id;
		CREATE INDEX idx_integration_mode_message_type ON integration_mode_message_type (sdm_key, dw_v, im_id, im, message_type, modality);
	COMMIT;
END ;