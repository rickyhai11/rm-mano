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
-- Table structure for table `tenants_utilization_storage_rm`
--

DROP TABLE IF EXISTS `tenants_utilization_storage_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tenants_utilization_storage_rm` (
  `uuid` int(36) NOT NULL,
  `tenant_name` varchar(45) DEFAULT NULL,
  `tenant_id` varchar(45) DEFAULT NULL,
  `max_total_gigabytes` varchar(45) DEFAULT NULL,
  `total_gigabytes_allocated` varchar(45) DEFAULT NULL,
  `total_gigabytes_used` varchar(45) DEFAULT NULL,
  `total_gigabytes_available` varchar(45) DEFAULT NULL,
  `total_gigabytes_reserved` varchar(45) DEFAULT NULL,
  `max_total_backup_gigabytes` varchar(45) DEFAULT NULL,
  `total_backup_gigabytes_allocated` varchar(45) DEFAULT NULL,
  `total_backup_gigabytes_used` varchar(45) DEFAULT NULL,
  `total_backup_gigabytes_available` varchar(45) DEFAULT NULL,
  `total_backup_gigabytes_reserved` varchar(45) DEFAULT NULL,
  `max_total_backup` varchar(45) DEFAULT NULL,
  `total_backup_allocated` varchar(45) DEFAULT NULL,
  `total_backup_used` varchar(45) DEFAULT NULL,
  `total_backup_available` varchar(45) DEFAULT NULL,
  `total_backup_reserved` varchar(45) DEFAULT NULL,
  `max_total_snapshots` varchar(45) DEFAULT NULL,
  `total_snapshots_allocated` varchar(45) DEFAULT NULL,
  `total_snapshots_used` varchar(45) DEFAULT NULL,
  `total_snapshots_available` varchar(45) DEFAULT NULL,
  `total_snapshots_reserved` varchar(45) DEFAULT NULL,
  `max_total_volumes` varchar(45) DEFAULT NULL,
  `total_volumes_allocated` varchar(45) DEFAULT NULL,
  `total_volumes_used` varchar(45) DEFAULT NULL,
  `total_volumes_available` varchar(45) DEFAULT NULL,
  `total_volumes_reserved` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `modified_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `refresh` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenants_utilization_storage_rm`
--

LOCK TABLES `tenants_utilization_storage_rm` WRITE;
/*!40000 ALTER TABLE `tenants_utilization_storage_rm` DISABLE KEYS */;
/*!40000 ALTER TABLE `tenants_utilization_storage_rm` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-13 15:10:10
