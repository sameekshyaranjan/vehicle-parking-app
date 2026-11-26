CREATE UNIQUE INDEX `reservation_one_active_per_spot` ON `reservation`
    ((CASE WHEN `leaving_timestamp` IS NULL THEN `spot_id` ELSE NULL END));

CREATE UNIQUE INDEX `reservation_one_active_per_user` ON `reservation`
    ((CASE WHEN `leaving_timestamp` IS NULL THEN `user_id` ELSE NULL END));

CREATE TRIGGER `reservation_release_audit`
AFTER UPDATE ON `reservation` FOR EACH ROW
    INSERT INTO `reservation_audit` (`reservation_id`, `event_type`, `recorded_at`, `final_cost`)
    SELECT NEW.id, 'RELEASED', UTC_TIMESTAMP(6), NEW.parking_cost
    FROM DUAL
    WHERE OLD.leaving_timestamp IS NULL AND NEW.leaving_timestamp IS NOT NULL;
