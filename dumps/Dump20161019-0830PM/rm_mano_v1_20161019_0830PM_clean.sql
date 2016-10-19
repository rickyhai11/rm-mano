-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: 116.89.184.43    Database: rm_mano_v1
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
-- Table structure for table `flavour_info_rm`
--

DROP TABLE IF EXISTS `flavour_info_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flavour_info_rm` (
  `uuid` varchar(36) NOT NULL COMMENT 'Flavour ID',
  `vMemory` int(10) NOT NULL DEFAULT '0' COMMENT 'MB',
  `numVirCpu` int(10) NOT NULL DEFAULT '0',
  `storageSize` int(10) NOT NULL DEFAULT '0' COMMENT 'GB',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flavour_info_rm`
--

LOCK TABLES `flavour_info_rm` WRITE;
/*!40000 ALTER TABLE `flavour_info_rm` DISABLE KEYS */;
/*!40000 ALTER TABLE `flavour_info_rm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images_rm`
--

DROP TABLE IF EXISTS `images_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `images_rm` (
  `image_id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `image_status` enum('ACTIVE','DOWN','BUILD','ERROR') DEFAULT 'BUILD',
  PRIMARY KEY (`image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images_rm`
--

LOCK TABLES `images_rm` WRITE;
/*!40000 ALTER TABLE `images_rm` DISABLE KEYS */;
/*!40000 ALTER TABLE `images_rm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `networks_details_rm`
--

DROP TABLE IF EXISTS `networks_details_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `networks_details_rm` (
  `uuid` int(36) NOT NULL AUTO_INCREMENT,
  `network_name` varchar(200) NOT NULL,
  `network_id` varchar(200) NOT NULL,
  `network_status` enum('ACTIVE','DOWN','BUILD','ERROR') NOT NULL DEFAULT 'BUILD',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `networks_details_rm`
--

LOCK TABLES `networks_details_rm` WRITE;
/*!40000 ALTER TABLE `networks_details_rm` DISABLE KEYS */;
/*!40000 ALTER TABLE `networks_details_rm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quota_rm`
--

DROP TABLE IF EXISTS `quota_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quota_rm` (
  `uuid` varchar(36) NOT NULL,
  `project_id` varchar(36) NOT NULL,
  `resource` varchar(36) NOT NULL,
  `hard_limit` int(20) NOT NULL DEFAULT '0',
  `allocated` int(20) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='quotas for all resources';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quota_rm`
--

LOCK TABLES `quota_rm` WRITE;
/*!40000 ALTER TABLE `quota_rm` DISABLE KEYS */;
INSERT INTO `quota_rm` VALUES ('27db278f-9513-11e6-9085-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3','vmemory',5000,0,'0000-00-00 00:00:00','2016-10-18 11:58:23','0000-00-00 00:00:00'),('27dc600f-9513-11e6-b4c3-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3','vnfs',15,0,'0000-00-00 00:00:00','2016-10-18 11:58:23','0000-00-00 00:00:00'),('27dcfc51-9513-11e6-acef-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3','vcpus',15,0,'0000-00-00 00:00:00','2016-10-18 11:58:23','0000-00-00 00:00:00'),('27dd988f-9513-11e6-a39a-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3','network',15,0,'0000-00-00 00:00:00','2016-10-18 11:58:23','0000-00-00 00:00:00'),('27de0dc0-9513-11e6-8f75-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3','port',15,0,'0000-00-00 00:00:00','2016-10-18 11:58:23','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `quota_rm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservation` (
  `reservation_id` int(36) NOT NULL AUTO_INCREMENT,
  `usage_id` varchar(36) NOT NULL,
  `label` varchar(100) DEFAULT 'Default',
  `region_id` varchar(100) NOT NULL,
  `user_id` varchar(100) DEFAULT 'admin',
  `project_id` varchar(100) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `flavor_id` varchar(36) NOT NULL,
  `image_id` varchar(100) NOT NULL,
  `network_id` varchar(200) NOT NULL,
  `number_vnfs` int(20) NOT NULL,
  `status` enum('ACTIVE','INACTIVE','BUILD','ERROR') NOT NULL DEFAULT 'INACTIVE',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `summary` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`reservation_id`),
  UNIQUE KEY `usage_id_UNIQUE` (`usage_id`),
  KEY `flavor_id_idx` (`flavor_id`),
  KEY `project_id_idx` (`project_id`),
  CONSTRAINT `usage_id` FOREIGN KEY (`usage_id`) REFERENCES `resource_usage_rm` (`uuid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5556 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation`
--

LOCK TABLES `reservation` WRITE;
/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;
/*!40000 ALTER TABLE `reservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource_usage_rm`
--

DROP TABLE IF EXISTS `resource_usage_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resource_usage_rm` (
  `uuid` varchar(36) NOT NULL,
  `project_id` varchar(45) NOT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  `resource` varchar(45) NOT NULL,
  `in_use` int(45) NOT NULL DEFAULT '0',
  `reserved` int(45) NOT NULL DEFAULT '0',
  `until_refresh` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='Resource Usage table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource_usage_rm`
--

LOCK TABLES `resource_usage_rm` WRITE;
/*!40000 ALTER TABLE `resource_usage_rm` DISABLE KEYS */;
INSERT INTO `resource_usage_rm` VALUES ('27dc11f0-9513-11e6-aa2b-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'vmemory',0,0,0,'0000-00-00 00:00:00','2016-10-18 08:51:55',NULL),('27dcae30-9513-11e6-a28e-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'vnfs',0,0,0,'0000-00-00 00:00:00','2016-10-18 08:51:55',NULL),('27dd4a70-9513-11e6-8160-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'vcpus',0,0,0,'0000-00-00 00:00:00','2016-10-18 08:51:55',NULL),('27dde6ae-9513-11e6-b770-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'network',0,0,0,'0000-00-00 00:00:00','2016-10-18 08:51:55',NULL),('27de82f0-9513-11e6-815a-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'port',0,0,0,'0000-00-00 00:00:00','2016-10-18 08:51:55',NULL);
/*!40000 ALTER TABLE `resource_usage_rm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rsv_vnf_rm`
--

DROP TABLE IF EXISTS `rsv_vnf_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rsv_vnf_rm` (
  `reservation_id` varchar(100) NOT NULL,
  `vnf_id` varchar(36) NOT NULL,
  PRIMARY KEY (`reservation_id`,`vnf_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rsv_vnf_rm`
--

LOCK TABLES `rsv_vnf_rm` WRITE;
/*!40000 ALTER TABLE `rsv_vnf_rm` DISABLE KEYS */;
/*!40000 ALTER TABLE `rsv_vnf_rm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vnfdid_rsv_rm`
--

DROP TABLE IF EXISTS `vnfdid_rsv_rm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vnfdid_rsv_rm` (
  `vnfdId` varchar(36) NOT NULL,
  `reservation_id` int(36) NOT NULL,
  PRIMARY KEY (`vnfdId`,`reservation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='VNF Descriptor and reservation info';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vnfdid_rsv_rm`
--

LOCK TABLES `vnfdid_rsv_rm` WRITE;
/*!40000 ALTER TABLE `vnfdid_rsv_rm` DISABLE KEYS */;
/*!40000 ALTER TABLE `vnfdid_rsv_rm` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-19 20:30:19
