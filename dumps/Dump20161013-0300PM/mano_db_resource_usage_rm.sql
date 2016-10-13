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
INSERT INTO `resource_usage_rm` VALUES ('8b36d48f-903d-11e6-b184-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'port',0,0,0,'0000-00-00 00:00:00','2016-10-12 05:13:14',NULL),('8b3797e1-903d-11e6-bd2d-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'vnfs',0,0,0,'0000-00-00 00:00:00','2016-10-12 05:13:14',NULL),('8b385b30-903d-11e6-b13a-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'vcpus',0,0,0,'0000-00-00 00:00:00','2016-10-12 05:13:14',NULL),('8b39458f-903d-11e6-a2be-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'network',0,0,0,'0000-00-00 00:00:00','2016-10-12 05:13:14',NULL),('8b39bac0-903d-11e6-a4c3-0050568b49a9','25970fbcfb0a4c2fb42ccc18f1bccde3',NULL,'memory',0,0,0,'0000-00-00 00:00:00','2016-10-12 05:13:14',NULL);
/*!40000 ALTER TABLE `resource_usage_rm` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-13 15:10:12
