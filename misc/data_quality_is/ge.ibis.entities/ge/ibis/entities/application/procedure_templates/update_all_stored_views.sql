-- This procedure call all proc that store view into table
CREATE OR REPLACE PROCEDURE update_all_stored_views()
BEGIN
    CALL update_ctlog();
    CALL update_pattern();
    CALL update_dosimetric();
    CALL update_agg_study();
    CALL update_devicesoverview();
END ; 