BEGIN;
--
-- Create model Activity
--
CREATE TABLE `personalized_options_activity` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `purpose` varchar(2) NOT NULL, `from_id` integer NOT NULL, `to_id` integer NOT NULL, `from_lat` double precision NOT NULL, `from_lon` double precision NOT NULL, `to_lat` double precision NOT NULL, `to_lon` double precision NOT NULL, `walk_time` smallint UNSIGNED NULL, `bike_time` smallint UNSIGNED NULL);
--
-- Create model TravelOption
--
CREATE TABLE `personalized_options_traveloption` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `day_of_week` varchar(2) NOT NULL, `slot_id` smallint UNSIGNED NOT NULL, `tz` varchar(2) NOT NULL, `drive` varchar(100) NOT NULL, `transit` varchar(200) NOT NULL, `uber` varchar(200) NOT NULL, `activity_id` integer NOT NULL);
--
-- Alter unique_together for activity (1 constraint(s))
--
ALTER TABLE `personalized_options_activity` ADD CONSTRAINT personalized_options_activity_from_id_to_id_56861f33_uniq UNIQUE (`from_id`, `to_id`);
--
-- Create index day_of_week_slot_tz_idx on field(s) day_of_week, slot_id, tz of model traveloption
--
CREATE INDEX `day_of_week_slot_tz_idx` ON `personalized_options_traveloption` (`day_of_week`, `slot_id`, `tz`);
--
-- Alter unique_together for traveloption (1 constraint(s))
--
ALTER TABLE `personalized_options_traveloption` ADD CONSTRAINT personalized_options_tra_activity_id_day_of_week__c579fe87_uniq UNIQUE (`activity_id`, `day_of_week`, `slot_id`);
ALTER TABLE `personalized_options_traveloption` ADD CONSTRAINT `personalized_options_activity_id_7e95b00e_fk_personali` FOREIGN KEY (`activity_id`) REFERENCES `personalized_options_activity` (`id`);
COMMIT;
