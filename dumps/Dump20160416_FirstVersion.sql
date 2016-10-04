CREATE DATABASE  IF NOT EXISTS `rm_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `rm_db`;
-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: localhost    Database: rm_db
-- ------------------------------------------------------
-- Server version	5.7.11-log

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
-- Table structure for table `flavor_id`
--

DROP TABLE IF EXISTS `flavor_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flavor_id` (
  `flavor_id` int(12) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `ram` int(30) DEFAULT NULL,
  `disk` int(30) DEFAULT NULL,
  `vcpu` int(30) DEFAULT NULL,
  PRIMARY KEY (`flavor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flavor_id`
--

LOCK TABLES `flavor_id` WRITE;
/*!40000 ALTER TABLE `flavor_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `flavor_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_id`
--

DROP TABLE IF EXISTS `image_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image_id` (
  `image_id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_id`
--

LOCK TABLES `image_id` WRITE;
/*!40000 ALTER TABLE `image_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `image_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservation` (
  `reservation_id` varchar(100) NOT NULL DEFAULT 'AUTO_INCREMENT',
  `label` varchar(100) NOT NULL,
  `host` varchar(100) NOT NULL,
  `user` varchar(100) NOT NULL,
  `project` varchar(100) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `flavor_id` int(50) DEFAULT NULL,
  `image_id` varchar(100) NOT NULL,
  `instance_id` varchar(100) NOT NULL,
  `status` varchar(50) NOT NULL,
  `summary` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`reservation_id`),
  KEY `parenthesis _idx` (`flavor_id`),
  KEY `image_id_idx` (`image_id`),
  CONSTRAINT `flavor_id` FOREIGN KEY (`flavor_id`) REFERENCES `flavor_id` (`flavor_id`) ON DELETE CASCADE,
  CONSTRAINT `image_id` FOREIGN KEY (`image_id`) REFERENCES `image_id` (`image_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation`
--

LOCK TABLES `reservation` WRITE;
/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;
/*!40000 ALTER TABLE `reservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vcpu_capacity`
--

DROP TABLE IF EXISTS `vcpu_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcpu_capacity` (
  `uuid` int(20) NOT NULL,
  `cpu_total` int(12) NOT NULL,
  `vcpu_total` int(12) NOT NULL,
  `vcpu_used` int(12) NOT NULL,
  `cpu_available` int(12) NOT NULL,
  `vcpu_available` int(12) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `vcpu_available_UNIQUE` (`vcpu_available`),
  UNIQUE KEY `uuid_UNIQUE` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vcpu_capacity`
--

LOCK TABLES `vcpu_capacity` WRITE;
/*!40000 ALTER TABLE `vcpu_capacity` DISABLE KEYS */;
INSERT INTO `vcpu_capacity` VALUES (11,15,20,10,8,55,'2016-04-13 03:30:20','2016-04-13 03:30:59'),(12,15,20,10,8,5,'2016-04-13 03:30:20','2016-04-13 03:30:59'),(13,15,20,10,8,65,'2016-04-16 11:07:52','2016-04-16 11:07:52');
/*!40000 ALTER TABLE `vcpu_capacity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vdisk_capacity`
--

DROP TABLE IF EXISTS `vdisk_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vdisk_capacity` (
  `uuid` int(20) NOT NULL,
  `disk_total` int(100) NOT NULL,
  `disk_used` int(100) NOT NULL,
  `disk_available` int(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `disk_available_UNIQUE` (`disk_available`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vdisk_capacity`
--

LOCK TABLES `vdisk_capacity` WRITE;
/*!40000 ALTER TABLE `vdisk_capacity` DISABLE KEYS */;
/*!40000 ALTER TABLE `vdisk_capacity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vmem_capacity`
--

DROP TABLE IF EXISTS `vmem_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vmem_capacity` (
  `uuid` int(20) NOT NULL,
  `mem_total` int(100) NOT NULL,
  `vmem_total` int(100) NOT NULL,
  `vmem_used` int(100) NOT NULL,
  `mem_available` int(100) NOT NULL,
  `vmem_available` int(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `vmem_available_UNIQUE` (`vmem_available`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vmem_capacity`
--

LOCK TABLES `vmem_capacity` WRITE;
/*!40000 ALTER TABLE `vmem_capacity` DISABLE KEYS */;
INSERT INTO `vmem_capacity` VALUES (3,12,12,5,5,6,'2016-04-16 11:04:17','2016-04-16 11:04:17');
/*!40000 ALTER TABLE `vmem_capacity` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-16 20:12:51
