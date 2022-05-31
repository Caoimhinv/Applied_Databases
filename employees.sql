-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: employees
-- ------------------------------------------------------
-- Server version	8.0.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP DATABASE IF EXISTS `employees`;

CREATE DATABASE `employees`;

USE `employees`;

--
-- Table structure for table `dept`
--

DROP TABLE IF EXISTS `dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dept` (
  `did` varchar(5) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `lid` varchar(3) DEFAULT NULL,
  `budget` int DEFAULT NULL,
  PRIMARY KEY (`did`),
  KEY `lid` (`lid`),
  CONSTRAINT `dept_ibfk_1` FOREIGN KEY (`lid`) REFERENCES `location` (`lid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dept`
--

LOCK TABLES `dept` WRITE;
/*!40000 ALTER TABLE `dept` DISABLE KEYS */;
INSERT INTO `dept` VALUES ('HR','Human Resources','GAL',800000),('PROD1','Production Unit 1','BLA',1255000),('PROD2','Production Unit 2','SWO',1252525),('PROD3','Production Unit 3','LIM',5454545),('R&D','Research & Development','GAL',2000000),('SE','Sales - East','TUA',1100000),('SHIP1','Shipping Unit 1','ATH',45458),('SHIP2','Shipping Unit 2','SWO',4500999),('SNR','Sales - North','ROS',950555),('SST','Sales - South','GAL',1100000),('SW','Sales - West','WPT',555000);
/*!40000 ALTER TABLE `dept` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `eid` varchar(3) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `dob` DATE NOT NULL,
  `did` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`eid`),
  KEY `did` (`did`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`did`) REFERENCES `dept` (`did`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES ('E01','Sean Jones','1970-01-14','R&D'),('E02','Mary Byrne','1990-04-02','R&D'),('E03','Dan Green','1968-11-13','R&D'),('E04','Aine Flynn','2000-02-23','HR'),('E05','Kate Collins','1972-01-28','HR'),('E06','John Smith','2001-05-23','SNR'),('E07','Billy Flynn','1994-08-16','SNR'),('E08','Tom Black','1985-12-01','SST'),('E09','Claire Murphy','1988-01-13','SST'),('E10','Ruth Burke','1968-05-30','SE'),('E11','James Doherty','1974-03-13','SE'),('E12','Alice Hughes','1975-08-08','SW'),('E13','Mary Collinson','2001-02-08','PROD1'),('E14','James Taylor','1991-04-05','PROD1'),('E15','Ian Jones','1984-04-27','PROD1'),('E16','Anne Nichols','1996-07-01','SHIP1'),('E17','Billy McGuinness','1986-05-14','SHIP1'),('E18','Thomas Hughes','1975-09-08','SHIP1');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location` (
  `lid` varchar(3) NOT NULL,
  `town` varchar(50) DEFAULT NULL,
  `county` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES ('ATH','Athlone','Westmeath'),('BLA','Blanchardstown','Dublin'),('CBR','Castlebar','Mayo'),('CRE','Castlerea','Roscommon'),('LIM','Limerick','Limerick'),('LTR','Letterfrack','Galway'),('ROS','Roscommon','Roscommon'),('SWO','Swords','Dublin'),('TUA','Tuam','Galway'),('TUL','Tulsk','Roscommon'),('WPT','Westport','Mayo');
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salary`
--

DROP TABLE IF EXISTS `salary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salary` (
  `eid` varchar(3) NOT NULL,
  `from` date NOT NULL,
  `to` date NOT NULL,
  `salary` double(8,2) DEFAULT NULL,
  PRIMARY KEY (`eid`,`from`,`to`),
  KEY `did` (`eid`),
  CONSTRAINT `salary_ibfk_1` FOREIGN KEY (`eid`) REFERENCES `employee` (`eid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salary`
--

LOCK TABLES `salary` WRITE;
/*!40000 ALTER TABLE `salary` DISABLE KEYS */;
INSERT INTO `salary` VALUES ('E01','1990-01-02','1995-03-21',15000.00),('E01','1995-03-22','2010-11-12',25000.00),('E01','2010-11-13','2021-12-31',37234.23),('E01','2022-01-01','9999-12-31',41234.21),('E02','2015-04-03','2017-09-11',51330.50),('E02','2017-09-12','2019-08-11',56340.49),('E02','2019-08-12','9999-12-31',59343.49),('E03','1998-05-15','2008-05-15',47000.14),('E03','2008-05-16','2018-05-16',63340.12),('E03','2018-05-17','9999-12-31',69340.12),('E04','2018-05-15','9999-12-31',56000.00),('E05','2010-05-05','2015-05-06',52000.00),('E05','2015-05-07','9999-12-31',53135.00),('E06','2021-04-22','9999-12-31',35888.93),('E07','2018-04-22','2019-04-22',35888.93),('E07','2019-04-23','2020-04-23',36888.93),('E07','2020-04-24','2021-04-24',37888.93),('E07','2021-04-24','9999-12-21',38888.93),('E08','2005-11-04','2010-12-21',45898.93),('E08','2010-12-22','2016-12-01',49998.95),('E08','2016-12-02','2019-04-11',52000.01),('E09','2011-05-13','2012-01-05',40000.25),('E09','2012-01-06','2019-01-01',45321.22),('E09','2019-01-02','2020-04-12',46321.22),('E09','2020-04-13','2021-06-15',47005.39),('E09','2021-06-15','9999-12-31',47005.39),('E10','2022-01-15','9999-12-31',59203.39),('E11','2016-01-04','2017-01-04',49333.00),('E11','2017-01-05','2018-01-04',50333.00),('E11','2018-01-05','2019-01-05',51333.00),('E11','2019-01-06','2020-01-06',52333.00),('E11','2020-01-07','2021-01-07',53333.00),('E11','2021-01-08','9999-12-31',54333.00),('E12','2000-03-08','2005-09-14',44563.10),('E12','2005-09-15','2011-06-15',46293.10),('E12','2011-06-16','2018-04-12',49393.00),('E12','2018-04-13','2021-04-23',50000.00),('E12','2021-04-24','9999-12-31',51250.00),('E13','2021-04-24','9999-12-31',51220.00),('E14','2018-11-01','2019-12-31',51520.00),('E14','2020-01-01','2020-12-31',52900.15),('E14','2021-01-01','9999-12-31',53200.98),('E15','2016-05-01','2017-10-31',60000.00),('E15','2017-11-01','2022-01-02',64000.00),('E15','2022-01-03','9999-12-21',65000.00),('E16','2021-05-16','9999-12-21',58000.00),('E17','2014-07-02','2018-09-21',51000.00),('E17','2018-09-22','2020-02-13',56900.00),('E17','2020-02-14','2022-02-16',59277.00),('E17','2022-02-17','9999-12-31',59277.00),('E18','2010-11-17','2015-04-15',49523.00),('E18','2015-04-16','9999-12-31',53000.00);
/*!40000 ALTER TABLE `salary` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-22 13:24:54
