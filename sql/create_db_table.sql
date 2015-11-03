CREATE DATABASE `appdemo`;
USE `appdemo`;
CREATE TABLE `demodata` (
`id` INTEGER NOT NULL AUTO_INCREMENT,
`name` VARCHAR(100),
`notes` TEXT,
`timestamp` TIMESTAMP,
PRIMARY KEY (`id`),
KEY (`name`)
);

CREATE TABLE `demodata_erase_log` (
`id` INTEGER NOT NULL AUTO_INCREMENT,
`timestamp` TIMESTAMP,
PRIMARY KEY (`id`),
KEY (`timestamp`)
);

-- put some initial data into the table
--INSERT INTO demodata VALUES ('','Brantley', 'This a test!','2015-01-01 12:00:00');
-- test table
--select * from demodata;
