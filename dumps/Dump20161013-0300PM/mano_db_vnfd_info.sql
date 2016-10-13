-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: 116.89.184.43    Database: mano_db
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `vnfd_info`
--

DROP TABLE IF EXISTS `vnfd_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vnfd_info` (
  `uuid` varchar(36) NOT NULL COMMENT 'VNFD ID',
  `vnfdVendor` varchar(36) NOT NULL,
  `vnfdImageName` varchar(36) NOT NULL,
  `vnfdImageIId` varchar(36) NOT NULL,
  `vnfdVersion` varchar(36) NOT NULL,
  `vnfdType` enum('VNF_KVM','VNF_DOCKER') NOT NULL DEFAULT 'VNF_DOCKER' COMMENT 'Type of VNF Image',
  `vnfdFlavorId` varchar(36) NOT NULL,
  `vnfdDesc` varchar(500) NOT NULL,
  `configType` enum('CONSOLE','PLAYNET_UIUX','BOTH') NOT NULL DEFAULT 'PLAYNET_UIUX',
  `configRepository` varchar(100) NOT NULL,
  `configNumFile` int(10) NOT NULL DEFAULT '0',
  `configPathFile` varchar(2000) NOT NULL,
  `vnfConfigDesc` varchar(2000) NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='VNF Descriptor';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vnfd_info`
--

LOCK TABLES `vnfd_info` WRITE;
/*!40000 ALTER TABLE `vnfd_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `vnfd_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-13 15:10:13