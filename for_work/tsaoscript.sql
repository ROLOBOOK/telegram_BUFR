-- MySQL Script generated by MySQL Workbench
-- Сб 07 сен 2019 21:38:40
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema cao
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema cao
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cao` DEFAULT CHARACTER SET utf8 ;
USE `cao` ;

-- -----------------------------------------------------
-- Table `cao`.`UGMS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cao`.`UGMS` (
  `idUGMS` INT NOT NULL AUTO_INCREMENT,
  `UGMS` VARCHAR(45) NULL,
  PRIMARY KEY (`idUGMS`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cao`.`Stations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cao`.`Stations` (
  `numberStation` INT NOT NULL,
  `name_stations` VARCHAR(45) NULL,
  `UGMS_idUGMS` INT NOT NULL,
  PRIMARY KEY (`numberStation`),
  INDEX `fk_Stations_UGMS_idx` (`UGMS_idUGMS` ASC),
  CONSTRAINT `fk_Stations_UGMS`
    FOREIGN KEY (`UGMS_idUGMS`)
    REFERENCES `cao`.`UGMS` (`idUGMS`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cao`.`releaseZonde`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cao`.`releaseZonde` (
  `idRelease` INT NOT NULL auto_increment,
  `Stations_numberStation` INT NOT NULL,
  `date` DATETIME NULL,
  `coordinateStation` VARCHAR(45) NULL,
  `oborudovanie_zond` VARCHAR(45) NULL,
  `height` INT NULL,
  `number_look` INT NULL,
  `lengthOfTheSuspension` INT NULL,
  `amountOfGas` INT NULL,
  `gasForFillingTheShell` INT NULL,
  `filling` INT NULL,
  `weightOfTheShell` INT NULL,
  `typeShell` INT NULL,
  `radiosondeShellManufacturer` INT NULL,
  `configurationOfRadiosondeSuspension` INT NULL,
  `configurationOfTheRadiosonde` INT NULL,
  `typeOfHumiditySensor` INT NULL,
  `temperatureSensorType` INT NULL,
  `pressureSensorType` INT NULL,
  `carrierFrequency` INT NULL,
  `text_info` VARCHAR(45) NULL,
  `s_n_zonda` VARCHAR(45) NULL,
  `PO_versia` VARCHAR(45) NULL,
  `MethodGeopotentialHeight` INT NULL,
  `ugol` INT NULL,
  `azimut` INT NULL,
  `h_opor` INT NULL,
  `groundBasedRradiosondeSignalReceptionSystem` INT NULL,
  `identificator` VARCHAR(45) NULL,
  `sensingNnumber` INT NULL,
  `date_start` DATETIME NULL,
  PRIMARY KEY (`idRelease`),
  INDEX `fk_releaseZonde_Stations1_idx` (`Stations_numberStation` ASC),
  CONSTRAINT `fk_releaseZonde_Stations1`
    FOREIGN KEY (`Stations_numberStation`)
    REFERENCES `cao`.`Stations` (`numberStation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

ALTER TABLE `cao`.`releaseZonde`
ADD UNIQUE INDEX `Stations_numberStation_UNIQUE` (`Stations_numberStation` ASC),
ADD UNIQUE INDEX `date_start_UNIQUE` (`date_start` ASC);


-- -----------------------------------------------------
-- Table `cao`.`content_telegram`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cao`.`content_telegram` (
  `id` INT NOT NULL auto_increment,
  `Stations_numberStation` INT NOT NULL,
  `date` DATETIME NULL,
  `time` FLOAT NULL,
  `P` FLOAT NULL,
  `T` FLOAT NULL,
  `Td` FLOAT NULL,
  `H` FLOAT NULL,
  `D` FLOAT NULL,
  `V` FLOAT NULL,
  `dLat` FLOAT NULL,
  `dLon` FLOAT NULL,
  `Flags` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_table1_Stations1_idx` (`Stations_numberStation` ASC),
  CONSTRAINT `fk_table1_Stations1`
    FOREIGN KEY (`Stations_numberStation`)
    REFERENCES `cao`.`Stations` (`numberStation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- create user 'fol` for work to base
-- -----------------------------------------------------

create user 'fol'@'%' identified by 'Qq123456';
grant all privileges on *.* to 'fol'@'%';
flush privileges;