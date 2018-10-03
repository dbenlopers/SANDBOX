CREATE INDEX measures_date datetime ON measures(date);

ALTER TABLE measures
    ADD COLUMN IF NOT EXISTS `min_available` VARCHAR(20) AFTER `value`,
    ADD COLUMN IF NOT EXISTS `max_available` VARCHAR(20) AFTER `min_available`,
    ADD COLUMN IF NOT EXISTS `max_available_unit` VARCHAR(20) AFTER `max_available`;