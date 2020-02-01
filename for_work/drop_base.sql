drop database cao2;


-- MySQL Script generated by MySQL Workbench
-- Сб 07 сен 2019 21:38:40
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema cao2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema cao2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cao2` DEFAULT CHARACTER SET utf8 ;
USE `cao2` ;


-- -----------------------------------------------------
-- Table `cao2`.`info_pusk`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cao2`.`info_pusk` (
`idRelease` INT NOT NULL auto_increment,
`index_station` INT NULL,
`time_pusk` DATETIME NULL,
`time_srok` DATETIME NULL,
`koordinat` VARCHAR(45) NULL,
`oborudovanie` VARCHAR(45) NULL,
`oblachnost` VARCHAR(45) NULL,
`sdvig_vetra` INT NULL,
`metod_opredeleniy_visoti` INT NULL,
`po_versia` VARCHAR(45) NULL,
`s_n_zonda` VARCHAR(45) NULL,
`algoritm_popravok_izmereniy_vlagnosti` INT NULL,
`nesyshay_chastota` INT NULL,
`datchik_davleniy` INT NULL,
`datchik_temperatur` INT NULL,
`datchik_vlagnosti` INT NULL,
`text_info` VARCHAR(45) NULL,
`nomer_nabludenia` INT NULL,
`nomer_zondirovania` INT NULL,
`fio_nabludateliy` VARCHAR(45) NULL,
`nazemnaiy_sistema_priema_signalov` INT NULL,
`visota` INT NULL,
`visota_anteni` INT NULL,
`popravka_azimut` INT NULL,
`popravka_ygl` INT NULL,
`radio_ykritie` INT NULL,
`configur_zonda` INT NULL,
`configur_podveski_zonda` INT NULL,
`proizvoditel_obolochki` INT NULL,
`tip_obolochki` INT NULL,
`massa_obolochki` FLOAT NULL,
`gaz_dly_napolnenia` INT NULL,
`kolichestbo_gaza` FLOAT NULL,
`dlina_podvesa` INT NULL,
`prichina_prikrashenia`  INT NULL,
  PRIMARY KEY (`idRelease`))
ENGINE = InnoDB;

ALTER TABLE `cao2`.`info_pusk`
ADD CONSTRAINT `12` UNIQUE KEY(`index_station`, `time_pusk`);

