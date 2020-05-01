drop database cao_bufr_v2;

-- MySQL Script generated by MySQL Workbench

-- Сб 07 сен 2019 21:38:40

-- Model: New Model    Version: 1.0

-- MySQL Workbench Forward Engineering



SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;

SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';



-- -----------------------------------------------------

-- Schema cao_bufr_v2

-- -----------------------------------------------------



-- -----------------------------------------------------

-- Schema cao_bufr_v2

-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS `cao_bufr_v2` DEFAULT CHARACTER SET utf8 ;

USE `cao_bufr_v2` ;


-- -----------------------------------------------------

-- Table `cao_bufr_v2`.`releaseZonde`

-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `cao_bufr_v2`.`releaseZonde` (

  `idRelease` INT NOT NULL auto_increment,

  `Stations_numberStation` VARCHAR(45) NOT NULL,

  `time_srok` DATETIME NULL,

  `time_pusk` DATETIME NULL,

  `koordinat` VARCHAR(45) NULL,

  `oborudovanie` VARCHAR(45) NULL,

  `oblachnost` VARCHAR(45) NULL,

  `GEOPOTENTIAL_HEIGHT_CALCULATION_002191` VARCHAR(45) NULL,

  `SOFTWARE_IDENTIFICATION_AND_VERSION_NUMBER_025061` VARCHAR(45) NULL,

  `RADIOSONDE_SERIAL_NUMBER_001081` VARCHAR(45) NULL,

  `CORRECTION_ALGORITHMS_FOR_HUMIDITY_MEASUREMENTS_002017` VARCHAR(45) NULL,

  `RADIOSONDE_OPERATING_FREQUENCY_002067` VARCHAR(45) NULL,

  `TYPE_OF_PRESSURE_SENSOR_002095` VARCHAR(45) NULL,

  `TYPE_OF_TEMPERATURE_SENSOR_002096` VARCHAR(45) NULL,

  `TYPE_OF_HUMIDITY_SENSOR_002097` VARCHAR(45) NULL,

  `RADIOSONDE_ASCENSION_NUMBER_001082` VARCHAR(45) NULL,

  `descriptor_001083` VARCHAR(45) NULL,

  `descriptor_001095` VARCHAR(45) NULL,

  `descriptor_002066` VARCHAR(45) NULL,

  `descriptor_007007` VARCHAR(45) NULL,

  `descriptor_002102` VARCHAR(45) NULL,

  `descriptor_025065` VARCHAR(45) NULL,

  `descriptor_026066` VARCHAR(45) NULL,

  `descriptor_002103` VARCHAR(45) NULL,

  `descriptor_002015` VARCHAR(45) NULL,

  `descriptor_002016` VARCHAR(45) NULL,

  `descriptor_002080` VARCHAR(45) NULL,

  `descriptor_002081` VARCHAR(45) NULL,
  
  `descriptor_002082` VARCHAR(45) NULL,

  `descriptor_002084` VARCHAR(45) NULL,

  `descriptor_002085` VARCHAR(45) NULL,

  `descriptor_002086` VARCHAR(45) NULL,

  `descriptor_035035` VARCHAR(45) NULL,

  `text_info_ValueData_205060` VARCHAR(45) NULL,

  PRIMARY KEY (`idRelease`))

ENGINE = InnoDB;







-- -----------------------------------------------------

-- Table `cao_bufr_v2`.`content_telegram`

-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `cao_bufr_v2`.`content_telegram` (

  `id` INT NOT NULL auto_increment,

  `Stations_numberStation` VARCHAR(45) NOT NULL,

  `date` DATETIME NULL,

  `time` VARCHAR(45) NULL,

  `P` VARCHAR(45) NULL,

  `T` VARCHAR(45) NULL,

  `Td` VARCHAR(45) NULL,

  `H` VARCHAR(45) NULL,

  `D` VARCHAR(45) NULL,

  `V` VARCHAR(45) NULL,

  `dLat` VARCHAR(45) NULL,

  `dLon` VARCHAR(45) NULL,

  `Flags` VARCHAR(45) NULL,

  PRIMARY KEY (`id`))

ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;

SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;

SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;



-- -----------------------------------------------------

-- create user 'fol` for work to base

-- -----------------------------------------------------


