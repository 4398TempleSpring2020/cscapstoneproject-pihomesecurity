CREATE DATABASE  IF NOT EXISTS `mypidb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `mypidb`;
-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com    Database: mypidb
-- ------------------------------------------------------
-- Server version	5.7.22-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Employee`
--

DROP TABLE IF EXISTS `Employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Employee` (
  `EmployeeID` int(11) NOT NULL AUTO_INCREMENT,
  `EmployeeName` varchar(255) NOT NULL,
  `EmployeeUsername` varchar(65) NOT NULL,
  `EmployeePassword` varchar(45) NOT NULL,
  `LastLogin` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`EmployeeID`),
  UNIQUE KEY `idEmployee_UNIQUE` (`EmployeeID`),
  UNIQUE KEY `EmployeeUsername` (`EmployeeUsername`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `EmployeeHomeRelationship`
--

DROP TABLE IF EXISTS `EmployeeHomeRelationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EmployeeHomeRelationship` (
  `EmployeeID` int(11) NOT NULL,
  `AccountID` int(11) NOT NULL,
  `AccessDate` datetime NOT NULL,
  KEY `AccountID_idx` (`AccountID`),
  KEY `EmployeeID_idx` (`EmployeeID`),
  CONSTRAINT `AccountID` FOREIGN KEY (`AccountID`) REFERENCES `HomeAccount` (`AccountID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `EmployeeID` FOREIGN KEY (`EmployeeID`) REFERENCES `Employee` (`EmployeeID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `HomeAccount`
--

DROP TABLE IF EXISTS `HomeAccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HomeAccount` (
  `AccountID` int(11) NOT NULL AUTO_INCREMENT,
  `AccountUsername` varchar(45) NOT NULL,
  `AccountPassword` varchar(45) NOT NULL,
  `AccountPin` int(11) NOT NULL,
  `FirstName` varchar(65) NOT NULL,
  `LastName` varchar(65) NOT NULL,
  `EmailAddress` varchar(255) NOT NULL,
  `HomeAccountAddress` varchar(255) NOT NULL,
  `PhoneNumber` bigint(11) NOT NULL,
  `NumOfUsers` int(11) DEFAULT '1',
  `AccountActiveFlag` tinyint(4) NOT NULL DEFAULT '1',
  `IncidentPhoneNumber` bigint(11) NOT NULL DEFAULT '911',
  PRIMARY KEY (`AccountID`),
  UNIQUE KEY `idCustomer_UNIQUE` (`AccountID`),
  UNIQUE KEY `AccountUsername_UNIQUE` (`AccountUsername`),
  UNIQUE KEY `HomeAccountAddress_UNIQUE` (`HomeAccountAddress`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `IncidentData`
--

DROP TABLE IF EXISTS `IncidentData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `IncidentData` (
  `IncidentID` varchar(32) NOT NULL,
  `AccountID` int(11) NOT NULL,
  `DateRecorded` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `BadIncidentFlag` tinyint(4) DEFAULT '0',
  `LastAccessed` datetime DEFAULT CURRENT_TIMESTAMP,
  `UserAccessed` varchar(65) DEFAULT NULL,
  `AdminComments` varchar(255) DEFAULT NULL,
  `DeletionBlockFlag` tinyint(4) NOT NULL DEFAULT '1',
  `EmergencyContactedFlag` tinyint(4) NOT NULL DEFAULT '0',
  `MicrophonePath` varchar(255) NOT NULL,
  `ImagePaths` varchar(1054) NOT NULL,
  `FriendlyMatchFlag` tinyint(4) NOT NULL DEFAULT '0',
  `UltrasonicPath` varchar(255) NOT NULL,
  PRIMARY KEY (`IncidentID`),
  UNIQUE KEY `idIncident_UNIQUE` (`IncidentID`),
  KEY `idCustomer_idx` (`AccountID`),
  CONSTRAINT `idCustomer` FOREIGN KEY (`AccountID`) REFERENCES `HomeAccount` (`AccountID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `UserAccounts`
--

DROP TABLE IF EXISTS `UserAccounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `UserAccounts` (
  `UserID` int(11) NOT NULL AUTO_INCREMENT,
  `AccountID` int(11) NOT NULL,
  `Username` varchar(65) NOT NULL,
  `UserPassword` varchar(45) NOT NULL,
  `UserPhoneNumber` bigint(11) NOT NULL,
  `MasterUserFlag` tinyint(4) NOT NULL,
  `DateCreated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `LastLogin` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `PhoneId` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `idAccountPermission_UNIQUE` (`UserID`),
  UNIQUE KEY `Usermame_UNIQUE` (`Username`),
  KEY `idCustomer_idx` (`AccountID`),
  CONSTRAINT `idCustomer2` FOREIGN KEY (`AccountID`) REFERENCES `HomeAccount` (`AccountID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-15 17:06:32
